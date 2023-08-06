import os
import sys
import json
import socket
import time
import logging
import argparse
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject

BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT,\
    ACTION, TIME, FROM_USER, TO_USER,\
    PRESENCE, MESSAGE, RESPONSE, ERROR, MESSAGE_TEXT,\
    ADD_CONTACT, DEL_CONTACT, EXIT, GET_USERS, USERS_LIST, \
    GET_CONTACTS, CONTACTS_LIST, DATA, PUBLIC_KEY_REQUEST
from common.delog import gvglog
from common.utils import check_message, create_message, get_message, send_message
from logdat.cnf import cnf_cli_log
from common.metas import ClientVerifier
from client.cli_db import CliDB


g_sck_lock = threading.Lock()
LOGGER = logging.getLogger('client')


class CliSck(threading.Thread, QObject):
    '''
    Класс для взимодействия с сервером через интерфейс JIM.
    Передает и принимает словарь.
    Данные передаются через сокеты.
    '''
    s_syg_new_mess = pyqtSignal(dict)
    s_syg_conn_lost = pyqtSignal()

    def __init__(self, i_cur_user, i_sock, i_db):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.m_cur_user = i_cur_user
        self.m_sock = i_sock
        self.m_db = i_db

        lls_cons = self.get_contacts_list()
        for con in lls_cons:
            self.m_db.add_contact(con)

        self.m_bl_run = True

    def run(self):
        while self.m_bl_run:
            time.sleep(1)
            try:
                with g_sck_lock:
                    self.m_sock.settimeout(0.5)
                    ldic_mess = get_message(self.m_sock)
                    LOGGER.info(f'CliSck.run.main process(proc_ans_from_srv) for: <{ldic_mess}>.')
                    self.proc_ans_from_srv(ldic_mess)
            except socket.timeout:
                continue
            except AttributeError as err:
                LOGGER.error(f'Ошибка {err.__repr__()} при получении сообщения!')
            except Exception as err:
                self.s_syg_conn_lost.emit()
                LOGGER.critical(f'CliSck.run.ERROR: <{err}>! Выход!')
                self.m_bl_run = False

    @gvglog
    def send_mess(self, i_from_user, i_to_user, i_mess):
        try:
            ldic_mess = create_message(MESSAGE,
                                       i_from_user,
                                       i_to_user,
                                       i_mess)
            with g_sck_lock:
                send_message(self.m_sock, ldic_mess)
            return True
        except Exception as exc:
            LOGGER.critical(f'CliSck.send_mess.ERROR: <{exc.__repr__()}>!')
            return False

    @gvglog
    def add_contact(self, i_con):
        try:
            ldic_mess = create_message(ADD_CONTACT,
                                       self.m_cur_user,
                                       i_con,
                                       None)
            with g_sck_lock:
                send_message(self.m_sock, ldic_mess)
                l_srv_ans = get_message(self.m_sock)
            return self.proc_ans_from_srv(l_srv_ans)
        except Exception as exc:
            LOGGER.critical(f'CliSck.add_contact.ERROR: <{exc.__repr__()}>!')
            return exc.__repr__()

    @gvglog
    def del_contact(self, i_con):
        try:
            ldic_mess = create_message(DEL_CONTACT,
                                       self.m_cur_user,
                                       i_con,
                                       None)
            with g_sck_lock:
                send_message(self.m_sock, ldic_mess)
                l_srv_ans = get_message(self.m_sock)
            return self.proc_ans_from_srv(l_srv_ans)
        except Exception as exc:
            LOGGER.critical(f'CliSck.del_contact.ERROR: <{exc.__repr__()}>!')
            return exc.__repr__()

    @gvglog
    def get_users_list(self):
        try:
            ldic_mess = create_message(GET_USERS,
                                       self.m_cur_user,
                                       None,
                                       None)
            with g_sck_lock:
                send_message(self.m_sock, ldic_mess)
                l_srv_ans = get_message(self.m_sock)
            return self.proc_ans_from_srv(l_srv_ans)
        except Exception as exc:
            LOGGER.critical(f'CliSck.get_users_list.ERROR: <{exc.__repr__()}>!')
            return exc.__repr__()

    @gvglog
    def get_contacts_list(self):
        try:
            ldic_mess = create_message(GET_CONTACTS,
                                       self.m_cur_user,
                                       None,
                                       None)
            with g_sck_lock:
                send_message(self.m_sock, ldic_mess)
                l_srv_ans = get_message(self.m_sock)
            return self.proc_ans_from_srv(l_srv_ans)
        except Exception as exc:
            LOGGER.critical(f'CliSck.get_contacts_list.ERROR: <{exc.__repr__()}>!')
            return exc.__repr__()

    @gvglog
    def proc_ans_from_srv(self, i_mess):
        if RESPONSE in i_mess:
            if i_mess[RESPONSE] == 200:
                if USERS_LIST in i_mess:
                    return i_mess[USERS_LIST]
                if CONTACTS_LIST in i_mess:
                    return i_mess[CONTACTS_LIST]
                return None
            else:
                return i_mess[ERROR]

        if i_mess[ACTION] == MESSAGE and i_mess[TO_USER] == self.m_cur_user:
            LOGGER.debug(f'\nПолучено Сообщение {i_mess.get(MESSAGE_TEXT)} от '
                         f'{i_mess.get(FROM_USER)}.\n')
            self.s_syg_new_mess.emit(i_mess)

    def run_shutdown(self):
        self.m_bl_run = False
        time.sleep(1.7)
        ldic_mess = create_message(EXIT, self.m_cur_user, None, None)

        with g_sck_lock:
            send_message(self.m_sock, ldic_mess)
        LOGGER.critical('CliSck: run_shutdown executed!')
        time.sleep(0.5)
        self.m_sock.close()

    def get_public_key(self, i_user_nm):
        LOGGER.debug(f'Запрос публичного ключа для {i_user_nm}')
        try:
            ldic_mess = create_message(PUBLIC_KEY_REQUEST,
                                       i_user_nm,
                                       None,
                                       None)
            with g_sck_lock:
                send_message(self.m_sock, ldic_mess)
                l_srv_ans = get_message(self.m_sock)
            if RESPONSE in l_srv_ans and l_srv_ans[RESPONSE] == 511:
                return l_srv_ans[DATA]
            else:
                LOGGER.error(f'Не удалось получить ключ собеседника: {i_user_nm}!')
        except Exception as exc:
            LOGGER.critical(f'CliSck.get_public_key.ERROR: <{exc.__repr__()}>!')
            return exc.__repr__()
