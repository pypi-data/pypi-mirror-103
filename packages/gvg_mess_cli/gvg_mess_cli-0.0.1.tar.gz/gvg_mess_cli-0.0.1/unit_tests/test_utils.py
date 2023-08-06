"""Unit-тесты утилит"""
import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
from common.utils import get_message, send_message


class PretendSock:
    __slots__ = 'm_bts'

    def send(self, i_bytes):
        if isinstance(i_bytes, bytes):
            self.m_bts = i_bytes
            return
        raise ValueError

    def recv(self, max_len):
        if not self.m_bts:
            return None
        l_res = self.m_bts[:max_len]
        self.m_bts = None
        return l_res


class Tests(unittest.TestCase):
    dict_test_presence = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    dict_test_recv_ok = {RESPONSE: 200}
    dict_test_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_and_recv_test_presence(self):
        l_sock = PretendSock()
        send_message(l_sock, self.dict_test_presence)
        self.assertEqual(get_message(l_sock),
                         self.dict_test_presence)

    def test_send_and_recv_test_recv_ok(self):
        l_sock = PretendSock()
        send_message(l_sock, self.dict_test_recv_ok)
        self.assertEqual(get_message(l_sock),
                         self.dict_test_recv_ok)

    def test_send_and_recv_dict_test_recv_err(self):
        l_sock = PretendSock()
        send_message(l_sock, self.dict_test_recv_err)
        self.assertEqual(get_message(l_sock),
                         self.dict_test_recv_err)

    def test_send_and_recv_not_bytes(self):
        l_sock = PretendSock()
        with self.assertRaises(ValueError):
            l_sock.send(l_sock)

    def test_send_and_recv_get_all_data(self):
        l_sock = PretendSock()
        send_message(l_sock, self.dict_test_recv_err)
        get_message(l_sock)
        with self.assertRaises(ValueError):
            get_message(l_sock)


if __name__ == '__main__':
    unittest.main()
