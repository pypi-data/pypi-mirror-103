import os
import sys
import logging
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from logdat.cnf import cnf_cli_log

LOGGER = logging.getLogger('client')


class DlgAddCon(QDialog):
    '''
    Диалоговое окно по созданию контакта.
    '''
    def __init__(self, i_sck, i_db, i_cur_user):
        super().__init__()
        self.m_sck = i_sck
        self.m_db = i_db
        self.m_cur_user = i_cur_user

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.m_lbl_sel = QLabel('Выберите контакт для добавления:', self)
        self.m_lbl_sel.setFixedSize(200, 20)
        self.m_lbl_sel.move(10, 0)

        self.m_cmb_sel = QComboBox(self)
        self.m_cmb_sel.setFixedSize(200, 20)
        self.m_cmb_sel.move(10, 30)

        self.m_btn_refresh = QPushButton('Обновить список', self)
        self.m_btn_refresh.setFixedSize(100, 30)
        self.m_btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.m_btn_cancel = QPushButton('Отмена', self)
        self.m_btn_cancel.setFixedSize(100, 30)
        self.m_btn_cancel.move(230, 60)
        self.m_btn_cancel.clicked.connect(self.close)

        self.fill_all_users()
        self.m_btn_refresh.clicked.connect(self.fill_all_users)

    def fill_all_users(self):
        self.m_cmb_sel.clear()
        lls_users_from_srv = set(self.m_sck.get_users_list())

        LOGGER.info(f'DlgAddCon.fill_all_users.lls_users_from_srv: <{lls_users_from_srv}>.')

        if self.m_cur_user in lls_users_from_srv:
            lls_users_from_srv.remove(self.m_cur_user)

        lls_existed_cons = set(self.m_db.get_contacts())
        lls_poss_cons = sorted(lls_users_from_srv - lls_existed_cons)
        self.m_cmb_sel.addItems(lls_poss_cons)

