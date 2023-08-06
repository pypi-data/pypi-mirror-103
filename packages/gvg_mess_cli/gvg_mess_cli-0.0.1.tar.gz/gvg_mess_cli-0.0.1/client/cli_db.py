import os
import sys
import logging
from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator
import datetime
from pprint import pprint
BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from logdat.cnf import cnf_cli_log

LOGGER = logging.getLogger('client')


class CliDB:
    '''
    Класс для чтения и записи в БД пользовательских данных.
    Сама БД находится на клиенте.
    '''
    class MessHist:
        def __init__(self, from_user, to_user, message):
            self.id = None
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        def __init__(self, i_new_con):
            self.con_id = None
            self.con_nm = i_new_con

    def __init__(self, i_cur_user):
        self.m_cur_user = i_cur_user
        self.m_db_engine = create_engine(f'sqlite:///cli_db_{self.m_cur_user}.db3', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
        self.m_metadata = MetaData()

        l_tbl_hist = Table('message_history', self.m_metadata,
                           Column('id', Integer, primary_key=True),
                           Column('from_user', String),
                           Column('to_user', String),
                           Column('message', Text),
                           Column('date', DateTime)
                           )

        l_tbl_contacts = Table('contacts', self.m_metadata,
                               Column('con_id', Integer, primary_key=True),
                               Column('con_nm', String, unique=True)
                               )

        self.m_metadata.create_all(self.m_db_engine)

        mapper(self.MessHist, l_tbl_hist)
        mapper(self.Contacts, l_tbl_contacts)

        Session = sessionmaker(bind=self.m_db_engine)
        self.m_sess = Session()
        self.m_sess.query(self.Contacts).delete()
        self.m_sess.commit()

    def save_message(self, i_from_user, i_to_user, i_mess):
        if not self.m_cur_user in [i_from_user, i_to_user]:
            print(f'Пришел некорректный user: {i_from_user}, {i_to_user}!')
            return
        lr_mess = self.MessHist(i_from_user, i_to_user, i_mess)
        self.m_sess.add(lr_mess)
        self.m_sess.commit()

    def get_mess_his(self, i_con=None):
        l_query = self.m_sess.query(self.MessHist)
        if i_con:
            l_query = l_query.filter((self.MessHist.from_user == i_con) |
                                     (self.MessHist.to_user == i_con))

        return sorted([(rec.from_user, rec.to_user, rec.message, rec.date)
                for rec in l_query.all()], key=lambda item: item[3])

    def is_contact_exists(self, i_con):
        if self.m_sess.query(self.Contacts).filter_by(con_nm=i_con).count():
            return True
        else:
            return False

    def add_contact(self, i_new_con):
        if not self.m_sess.query(self.Contacts).filter_by(con_nm=i_new_con).count():
            lr_new_con = self.Contacts(i_new_con)
            self.m_sess.add(lr_new_con)
            self.m_sess.commit()

    def del_contact(self, i_del_con):
        self.m_sess.query(self.Contacts).filter_by(con_nm=i_del_con).delete()
        self.m_sess.commit()

    def get_contacts(self):
        l_query = self.m_sess.query(self.Contacts)
        l_res = sorted([(rec.con_nm)
                  for rec in l_query.all()], key=lambda item: item[0])
        LOGGER.debug(f'CliDB.get_contacts: <{l_res}>.')
        return l_res

    def close(self):
        self.m_sess.close()

if __name__ == '__main__':
    #test_db = CliDB('test1')
    test_db = CliDB('user1')
    #test_db.save_message('test1', 'test2', f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
    #test_db.save_message('test1', 'sss', f'Привет! я пришел к sss, тестовое сообщение от {datetime.datetime.now()}!')
    #pprint(test_db.get_mess_his('test1'))
    pprint(test_db.get_contacts())

