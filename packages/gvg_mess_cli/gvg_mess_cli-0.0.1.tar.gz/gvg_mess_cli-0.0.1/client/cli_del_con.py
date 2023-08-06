import os
import sys
import logging
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from logdat.cnf import cnf_cli_log
from client.cli_db import CliDB

LOGGER = logging.getLogger('client')


class DlgDelCon(QDialog):
    '''
    Диалоговое окно по удалению контакта.
    '''
    def __init__(self, i_db, i_cur_user):
        super().__init__()
        self.m_db = i_db
        self.m_cur_user = i_cur_user

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для удаления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.m_lbl_sel = QLabel('Выберите контакт для удаления:', self)
        self.m_lbl_sel.setFixedSize(200, 20)
        self.m_lbl_sel.move(10, 0)

        self.m_cmb_sel = QComboBox(self)
        self.m_cmb_sel.setFixedSize(200, 20)
        self.m_cmb_sel.move(10, 30)

        self.btn_ok = QPushButton('Удалить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.m_cmb_sel.addItems(self.m_db.get_contacts())

