import json
import sys
import time
import hashlib
import binascii
from common.variables import MAX_PACKAGE_LENGTH, ENCODING,\
    ACTION, TIME, FROM_USER, TO_USER,\
    PRESENCE, EXIT, MESSAGE,\
    RESPONSE, ERROR, MESSAGE_TEXT,\
    ADD_CONTACT, DEL_CONTACT, GET_USERS, USERS_LIST,\
    GET_CONTACTS, CONTACTS_LIST,\
    PUBLIC_KEY_REQUEST
from common.delog import gvglog
from logdat.cnf import cnf_srv_log


def create_user_hash(i_user_nm, i_pass):
    lbts_pass = i_pass.encode('utf-8')
    lbts_salt = i_user_nm.lower().encode('utf-8')
    l_hash = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', lbts_pass, lbts_salt, 10000))
    return l_hash


@gvglog
def check_message(idic_mess):
    """
    Проверка JIM сообщения.
    """
    if not ACTION in idic_mess:
        return f'There is no {ACTION} in message: {idic_mess}!'

    if not TIME in idic_mess:
        return f'There is no {TIME} in message: {idic_mess}!'

    if not FROM_USER in idic_mess:
        return f'There is no {FROM_USER} in message: {idic_mess}!'

    if not(idic_mess[ACTION] == PRESENCE or
        idic_mess[ACTION] == MESSAGE or
        idic_mess[ACTION] == ADD_CONTACT or
        idic_mess[ACTION] == DEL_CONTACT or
        idic_mess[ACTION] == GET_USERS or
        idic_mess[ACTION] == GET_CONTACTS or
        idic_mess[ACTION] == PUBLIC_KEY_REQUEST or
        idic_mess[ACTION] == EXIT):
        return f'Incorrect value in {idic_mess[ACTION]} in message: {idic_mess}!'

    if idic_mess[ACTION] == MESSAGE and (not TO_USER in idic_mess):
        return f'There is no TO_USER in message: {idic_mess}!'

    if idic_mess[ACTION] == MESSAGE and (not MESSAGE_TEXT in idic_mess):
        return f'There is no MESSAGE_TEXT in message: {idic_mess}!'

    return None


@gvglog
def create_message(i_act, i_from_user, i_to_user, i_mess):
    """
    Утилита создания JIM сообщения.
    """
    if not( PRESENCE in i_act or
            MESSAGE in i_act or
            ADD_CONTACT in i_act or
            DEL_CONTACT in i_act or
            GET_USERS in i_act or
            GET_CONTACTS in i_act or
            PUBLIC_KEY_REQUEST in i_act or
            EXIT in i_act):
        raise AttributeError(f'Incorrect input ACTION: {i_act}!')

    if not i_from_user:
        raise AttributeError(f'Incorrect input FROM_USER:  {i_from_user}!')

    l_res = {ACTION: i_act,
             TIME: time.time(),
             FROM_USER: i_from_user}

    if i_to_user:
        l_res[TO_USER] = i_to_user

    if i_mess:
        l_res[MESSAGE_TEXT] = i_mess

    return l_res


@gvglog
def get_message(client):
    """
    Утилита приёма и декодирования сообщения
    принимает байты выдаёт словарь.
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@gvglog
def send_message(sock, message):
    '''
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его.
    '''
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
