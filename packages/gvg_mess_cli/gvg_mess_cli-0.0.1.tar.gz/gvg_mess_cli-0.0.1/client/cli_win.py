import os
import sys
import json
import logging
import base64
from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from common.variables import MESSAGE_TEXT, FROM_USER, TO_USER
from common.delog import gvglog
from logdat.cnf import cnf_cli_log
from client.cli_db import CliDB
from client.cli_win_cnv import Ui_MainClientWindow
from client.cli_add_con import DlgAddCon
from client.cli_del_con import DlgDelCon

LOGGER = logging.getLogger('client')


class ClientMainFrame(QMainWindow):
    '''
    Класс главного окна пользователя.
    Другие окна вызываются из данного окна.
    '''
    def __init__(self, i_db, i_sck, i_from_user, i_keys):
        super().__init__()
        self.m_db = i_db
        self.m_sck = i_sck
        self.m_cur_user = i_from_user
        self.m_to_user = None

        self.m_decrypter = PKCS1_OAEP.new(i_keys)

        self.m_to_key = None
        self.m_encryptor = None

        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)
        self.ui.menu_exit.triggered.connect(qApp.exit)
        self.ui.btn_send.clicked.connect(self.send_mess)

        self.ui.btn_add_contact.clicked.connect(self.add_contact_dialog)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_dialog)
        self.ui.btn_remove_contact.clicked.connect(self.del_contact_dialog)
        self.ui.menu_del_contact.triggered.connect(self.del_contact_dialog)

        self.m_mdl_cons = None
        self.m_mdl_hist = None
        self.m_mbox = QMessageBox()
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)
        self.ui.list_contacts.doubleClicked.connect(self.sel_to_user)
        self.setWindowTitle(f'Chat for: {self.m_cur_user}')

        i_sck.s_syg_new_mess.connect(self.get_new_message)
        i_sck.s_syg_conn_lost.connect(self.connection_lost)
        self.fill_contacts_list()
        self.set_disabled_input()
        self.show()

    def upd_list_messages(self):
        ll_mess = self.m_db.get_mess_his(self.m_to_user)

        if not self.m_mdl_hist:
            self.m_mdl_hist = QStandardItemModel()
            self.ui.list_messages.setModel(self.m_mdl_hist)

        self.m_mdl_hist.clear()

        l_mes_len = len(ll_mess)
        l_start_ind = 0
        if l_mes_len > 20:
            l_start_ind = l_mes_len - 20

        for i in range(l_start_ind, l_mes_len):
            l_item = ll_mess[i]

            lr_mess = QStandardItem(f'Время: {l_item[3].replace(microsecond=0)}:\n {l_item[2]}')
            lr_mess.setEditable(False)

            if l_item[1] == self.m_cur_user:
                lr_mess.setBackground(QBrush(QColor(255, 255, 255)))
                lr_mess.setTextAlignment(Qt.AlignLeft)
            else:
                lr_mess.setTextAlignment(Qt.AlignRight)
                lr_mess.setBackground(QBrush(QColor(0, 255, 255)))

            self.m_mdl_hist.appendRow(lr_mess)

        self.ui.list_messages.scrollToBottom()

    def sel_to_user(self):
        l_to_user = self.ui.list_contacts.currentIndex().data()
        self.set_active_con(l_to_user)

    def fill_contacts_list(self):
        lls_cons = self.m_db.get_contacts()
        self.m_mdl_cons = QStandardItemModel()
        for i in lls_cons:
            lit_con = QStandardItem(i)
            lit_con.setEditable(False)
            self.m_mdl_cons.appendRow(lit_con)
        self.ui.list_contacts.setModel(self.m_mdl_cons)

    def add_contact_dialog(self):
        global g_dlg_add_con
        g_dlg_add_con = DlgAddCon(self.m_sck, self.m_db, self.m_cur_user)
        g_dlg_add_con.btn_ok.clicked.connect(lambda: self.add_contact_action(g_dlg_add_con))
        g_dlg_add_con.show()

    def del_contact_dialog(self):
        global g_dlg_del_con
        g_dlg_del_con = DlgDelCon(self.m_db, self.m_cur_user)
        g_dlg_del_con.btn_ok.clicked.connect(lambda: self.del_contact_action(g_dlg_del_con))
        g_dlg_del_con.show()

    def add_contact_action(self, i_dlg_add_con):
        l_new_con = i_dlg_add_con.m_cmb_sel.currentText()
        i_dlg_add_con.close()

        ls_res = self.m_sck.add_contact(l_new_con)
        if ls_res:
            self.m_mbox.critical(self, 'Ошибка',
                        f'Ошибка <{ls_res}> при создании контакта на сервере!')

        ls_res = self.m_db.add_contact(l_new_con)
        if ls_res:
            self.m_mbox.critical(self, 'Ошибка',
                        f'Ошибка <{ls_res}> при создании контакта на клиенте!')

        self.fill_contacts_list()
        LOGGER.info(f'cli_win.py.Успешно добавлен контакт {l_new_con}')
        self.m_mbox.information(self,
                    'Ура', f'Контакт <{l_new_con}> для пользователя <{self.m_cur_user}> успешно добавлен.')

    def del_contact_action(self, i_dlg_del_con):
        l_del_con = i_dlg_del_con.m_cmb_sel.currentText()
        i_dlg_del_con.close()

        ls_res = self.m_sck.del_contact(l_del_con)
        if ls_res:
            self.m_mbox.critical(self, 'Ошибка',
                        f'Ошибка <{ls_res}> при удалении контакта на сервере!')

        ls_res = self.m_db.del_contact(l_del_con)
        if ls_res:
            self.m_mbox.critical(self, 'Ошибка',
                        f'Ошибка <{ls_res}> при удалении контакта на клиенте!')

        self.fill_contacts_list()
        LOGGER.info(f'cli_win.py.Успешно удален контакт {l_del_con}')
        self.m_mbox.information(self,
                    'Ура', f'Контакт <{l_del_con}> для пользователя <{self.m_cur_user}> успешно удален.')

        if l_del_con == self.m_to_user:
            self.set_disabled_input()

    def send_mess(self):
        ls_mess_txt = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not ls_mess_txt:
            return

        lbts_mess_encrypted = self.m_encryptor.encrypt(ls_mess_txt.encode('utf8'))
        lbts_mess_en_base64 = base64.b64encode(lbts_mess_encrypted)
        ls_for_send_mess = lbts_mess_en_base64.decode('ascii')

        if self.m_sck:
            self.m_sck.send_mess(self.m_cur_user, self.m_to_user, ls_for_send_mess)

        self.m_db.save_message(self.m_cur_user, self.m_to_user, ls_mess_txt)
        self.upd_list_messages()

    @pyqtSlot(dict)
    def get_new_message(self, idc_mess):
        ls_encr_mess = base64.b64decode(idc_mess[MESSAGE_TEXT])
        try:
            ls_decr_mess = self.m_decrypter.decrypt(ls_encr_mess)
            ls_ready_mes = ls_decr_mess.decode('utf8')
        except (ValueError, TypeError):
            self.messages.warning(
                self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return

        ls_fr_user = idc_mess[FROM_USER]
        ls_to_user = idc_mess[TO_USER]
        self.m_db.save_message(ls_fr_user, ls_to_user, ls_ready_mes)
        self.upd_list_messages()

        if not ls_fr_user == self.m_to_user:
            if self.m_db.is_contact_exists(ls_fr_user):
                if self.m_mbox.question(self,
                                        'Сообщение',
                                        f'Получено сообщение от {ls_fr_user}, открыть чат с ним?',
                                        QMessageBox.Yes,
                                        QMessageBox.No) == QMessageBox.Yes:
                    self.set_active_con(ls_fr_user)
            else:
                ls_ques = f'Получено сообщение от {ls_fr_user}.'
                ls_ques += '\n Данного пользователя нет в вашем контакт-листе.'
                ls_ques += '\n Добавить в контакты и открыть чат с ним?'
                if self.m_mbox.question(self,
                                        'Сообщение',
                                        ls_ques,
                                        QMessageBox.Yes,
                                        QMessageBox.No) == QMessageBox.Yes:
                    self.set_active_con(ls_fr_user)
                    self.add_contact(ls_fr_user)

    @pyqtSlot()
    def connection_lost(self):
        self.m_mbox.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером. ')
        self.close()

    def set_disabled_input(self):
        self.ui.label_new_message.setText('Для выбора получателя дважды кликните на нем в окне контактов.')
        self.ui.text_message.clear()
        if self.m_mdl_hist:
            self.m_mdl_hist.clear()

        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

        self.m_to_user = None
        self.m_to_key = None
        self.m_encryptor = None

    def fill_contacts_list(self):
        lls_cons = self.m_db.get_contacts()
        self.m_mdl_cons = QStandardItemModel()
        for i in lls_cons:
            lit_con = QStandardItem(i)
            lit_con.setEditable(False)
            self.m_mdl_cons.appendRow(lit_con)
        self.ui.list_contacts.setModel(self.m_mdl_cons)

        self.m_to_key = None
        self.m_encryptor = None


    def set_active_con(self, i_to_user):
        try:
            self.m_to_key = self.m_sck.get_public_key(i_to_user)
            LOGGER.debug(f'Загружен открытый ключ для <{i_to_user}>.')

            if self.m_to_key:
                self.m_encryptor = PKCS1_OAEP.new(RSA.import_key(self.m_to_key))
        except (OSError):
            self.m_to_key = None
            self.m_encryptor = None
            logger.debug(f'Не удалось получить ключ для {self.m_to_key}')

        if not self.m_to_key:
            self.m_mbox.warning(self, 'Ошибка',
             f'Для пользователя <{i_to_user}> нет ключа шифрования.')
            return

        self.m_to_user = i_to_user
        self.ui.label_new_message.setText(f'Введите сообщение для {self.m_to_user}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)
        self.upd_list_messages()

