import os
import sys
import logging
import traceback
import inspect
import socket
BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from logdat.cnf import cnf_cli_log, cnf_srv_log
from common.variables import ACTION, PRESENCE
if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def gvglog(log_fnc):
    def wrapper(*args, **kwargs):
        ret = log_fnc(*args, **kwargs)
        l_fnc1 = traceback.format_stack()[0].strip().split()[-1]
        l_fnc2 = inspect.stack()[1][3]
        l_fil2 = os.path.split(inspect.stack()[1][1])[1]
        #{log_fnc.__module__}
        LOGGER.debug(f'Вызвана функция: <{l_fil2}.'
                     f'{l_fnc2}.{log_fnc.__name__}>.')
        LOGGER.debug(f'С параметрами:   <{args}>, <{kwargs}>.')
        LOGGER.debug(f'Результат функции: <{ret}>.')
        return ret
    return wrapper


def login_required(func):
    def checker(*args, **kwargs):

        from server.srv_sck import MessSrv
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessSrv):
            l_found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    for client in args[0].m_dc_user_socks:
                        if args[0].m_dc_user_socks[client] == arg:
                            l_found = True

            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        l_found = True
            if not l_found:
                raise TypeError
        return func(*args, **kwargs)
    return checker
