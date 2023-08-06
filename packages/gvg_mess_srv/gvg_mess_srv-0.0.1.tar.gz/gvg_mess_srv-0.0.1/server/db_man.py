import os
import sys
import datetime
import time
from pprint import pprint
import logging
from sqlalchemy import create_engine, Table, Column, Integer, String,\
    MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator
BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from common.delog import gvglog
from logdat.cnf import cnf_srv_log

LOGGER = logging.getLogger('server')


class DbManager:
    """
    Класс для чтения и записи в БД серверных данных.
    Сама БД находится на сервере.
    Тут лежат данные по аутентификации пользователей,
    статистики и текущему состоянию БД.
    """
    class ConnUsers:
        def __init__(self, i_user_nm, i_passwd_hash):
            self.user_id = None
            self.user_nm = i_user_nm
            self.last_log_tm = datetime.datetime.now()
            self.passwd_hash = i_passwd_hash
            self.pubkey = None

    class ActUsers:
        def __init__(self, i_user_id, i_addr, i_port):
            self.act_id = None
            self.user_id = i_user_id
            self.addr = i_addr
            self.port = i_port
            self.log_tm = datetime.datetime.now()

    class LogHist:
        def __init__(self, i_user_id, i_addr, i_port):
            self.log_id = None
            self.user_id = i_user_id
            self.addr = i_addr
            self.port = i_port
            self.log_tm = datetime.datetime.now()

    class UsersContacts:
        def __init__(self, i_user_id, i_contact_id):
            self.con_id = None
            self.user_id = i_user_id
            self.contact_id = i_contact_id

    class UsersStats:
        def __init__(self, i_user_id):
            self.sta_id = None
            self.user_id = i_user_id
            self.sent = 0
            self.accepted = 0


    def __init__(self, i_full_fn, clean_ind=True):
        self.m_db_engine = create_engine(f'sqlite:///{i_full_fn}',
                                         echo=False,
                                         pool_recycle=7200,
                                         connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        l_tbl_conn_users = Table('CONN_USERS', self.metadata,
                                 Column('user_id', Integer, primary_key=True),
                                 Column('user_nm', String, unique=True),
                                 Column('last_log_tm', DateTime),
                                 Column('passwd_hash', String),
                                 Column('pubkey', Text)
                                 )

        l_tbl_act_users = Table('ACT_USERS', self.metadata,
                                Column('act_id', Integer, primary_key=True),
                                Column('user_id', ForeignKey('CONN_USERS.user_id'), unique=True),
                                Column('addr', String),
                                Column('port', Integer),
                                Column('log_tm', DateTime)
                                )

        l_tbl_log_hist = Table('LOG_HIST', self.metadata,
                               Column('log_id', Integer, primary_key=True),
                               Column('user_id', ForeignKey('CONN_USERS.user_id')),
                               Column('addr', String),
                               Column('port', Integer),
                               Column('log_tm', DateTime)
                               )

        l_tbl_contacts = Table('CONTACTS', self.metadata,
                               Column('con_id', Integer, primary_key=True),
                               Column('user_id', ForeignKey('CONN_USERS.user_id')),
                               Column('contact_id', ForeignKey('CONN_USERS.user_id'))
                               )

        l_tbl_users_stats = Table('USERS_STATS', self.metadata,
                                  Column('sta_id', Integer, primary_key=True),
                                  Column('user_id', ForeignKey('CONN_USERS.user_id')),
                                  Column('sent', Integer),
                                  Column('accepted', Integer)
                                  )

        self.metadata.create_all(self.m_db_engine)
        mapper(self.ConnUsers, l_tbl_conn_users)
        mapper(self.ActUsers, l_tbl_act_users)
        mapper(self.LogHist, l_tbl_log_hist)
        mapper(self.UsersContacts, l_tbl_contacts)
        mapper(self.UsersStats, l_tbl_users_stats)

        Session = sessionmaker(bind=self.m_db_engine)
        self.m_sess = Session()

        if clean_ind:
            self.m_sess.query(self.ActUsers).delete()
            self.m_sess.commit()


    def log_conn_in(self, i_user_nm, i_addr, i_port, i_pubkey):
        LOGGER.info(f'Подключился пользователь: <{i_user_nm}>, <{i_addr}>, <{i_port}>, <{i_pubkey}>')

        l_us = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm)

        if l_us.count():
            l_user = l_us.first()
            l_user.last_log_tm = datetime.datetime.now()

            if l_user.pubkey != i_pubkey:
                l_user.pubkey = i_pubkey
        else:
            raise ValueError('Пользователь не зарегистрирован.')

        l_st = self.m_sess.query(self.UsersStats).filter_by(user_id=l_user.user_id)

        if not l_st.count():
            l_user_stat = self.UsersStats(l_user.user_id)
            self.m_sess.add(l_user_stat)

        l_new_act_user = self.ActUsers(l_user.user_id, i_addr, i_port)
        self.m_sess.add(l_new_act_user)

        l_hist = self.LogHist(l_user.user_id, i_addr, i_port)
        self.m_sess.add(l_hist)

        self.m_sess.commit()


    def log_conn_out(self, i_user_nm):
        l_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).first()
        self.m_sess.query(self.ActUsers).filter_by(user_id=l_user.user_id).delete()
        self.m_sess.commit()


    def reg_mess(self, i_from_user, i_to_user):
        print('Регистрация передачи:', i_from_user, i_to_user)
        lr_from_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_from_user).first()
        lr_to_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_to_user).first()

        lr_from_stats = self.m_sess.query(self.UsersStats).filter_by(user_id=lr_from_user.user_id).first()
        lr_to_stats = self.m_sess.query(self.UsersStats).filter_by(user_id=lr_to_user.user_id).first()

        if lr_from_stats:
            lr_from_stats.sent += 1

        if lr_to_stats:
            lr_to_stats.accepted += 1

        if not self.m_sess.query(self.UsersContacts).filter_by(user_id=lr_from_user.user_id,
                                                                  contact_id=lr_to_user.user_id).count():
            lr_contact = self.UsersContacts(lr_from_user.user_id, lr_to_user.user_id)
            self.m_sess.add(lr_contact)

        self.m_sess.commit()

    def add_contact(self, i_user_nm, i_con_name):
        lr_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).first()
        lr_con = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_con_name).first()

        if not lr_user:
            ls_res = f'add_contact: не найден пользователь для {i_user_nm}!'
            LOGGER.error(ls_res)
            return ls_res

        if not lr_con:
            ls_res = f'add_contact: не найден пользователь для {i_con_name}!'
            LOGGER.error(ls_res)
            return ls_res

        if self.m_sess.query(self.UsersContacts).filter_by(user_id=lr_user.user_id,
                                                           contact_id=lr_con.user_id).count():
            #print(f'add_contact: найден дубликат контактов для {i_user_nm}, {i_con_name}!')
            return

        lr_new_con = self.UsersContacts(lr_user.user_id, lr_con.user_id)
        self.m_sess.add(lr_new_con)
        self.m_sess.commit()
        LOGGER.info(f'db_man.py.add_contact: добавлен контакт {i_con_name} для {i_user_nm}.')

    def del_contact(self, i_user_nm, i_con_name):
        lr_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).first()
        lr_con = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_con_name).first()

        if not lr_user:
            ls_res = f'add_contact: не найден пользователь для {i_user_nm}!'
            LOGGER.error(ls_res)
            return ls_res

        if not lr_con:
            ls_res = f'add_contact: не найден пользователь для {i_con_name}!'
            LOGGER.error(ls_res)
            return ls_res

        self.m_sess.query(self.UsersContacts).filter(
            self.UsersContacts.user_id == lr_user.user_id,
            self.UsersContacts.contact_id == lr_con.user_id
        ).delete()
        self.m_sess.commit()
        LOGGER.info(f'db_man.py.del_contact: удален контакт {i_con_name} для {i_user_nm}.')

    def get_users_list(self):
        l_query = self.m_sess.query(
            self.ConnUsers.user_id,
            self.ConnUsers.user_nm,
            self.ConnUsers.last_log_tm
        )
        return l_query.all()

    def get_contacts_list(self, i_user_nm=None):
        lr_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).first()

        if not lr_user:
            ls_res = f'get_contacts_list: не найден пользователь для {i_user_nm}!'
            LOGGER.error(ls_res)
            return ls_res

        l_query = self.m_sess.query(self.UsersContacts).filter_by(user_id=lr_user.user_id)

        l_buf = [(rec.contact_id) for rec in l_query.all()]
        l_res = []

        for cid in l_buf:
            lr_con = self.m_sess.query(self.ConnUsers).filter_by(user_id=cid).first()
            l_res.append(lr_con.user_nm)

        return sorted(l_res)

    def get_act_users(self):
        l_query = self.m_sess.query(
            self.ConnUsers.user_nm,
            self.ActUsers.addr,
            self.ActUsers.port,
            self.ActUsers.log_tm
            ).join(self.ConnUsers)
        return l_query.all()

    def login_history(self, i_user_nm=None):
        l_query = self.m_sess.query(self.ConnUsers.user_nm,
                                     self.LogHist.log_tm,
                                     self.LogHist.addr,
                                     self.LogHist.port
                                     ).join(self.ConnUsers)
        if i_user_nm:
            l_query = l_query.filter(self.ConnUsers.user_nm == i_user_nm)
        return l_query.all()

    def get_users_stats(self):
        query = self.m_sess.query(
            self.ConnUsers.user_nm,
            self.ConnUsers.last_log_tm,
            self.UsersStats.sent,
            self.UsersStats.accepted
        ).join(self.ConnUsers)
        return query.all()

    def is_user_exists(self, i_user_nm):
        if self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).count():
            return True
        else:
            return False

    def get_hash(self, i_user_nm):
        lr_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).first()
        return lr_user.passwd_hash

    def add_user(self, i_user_nm, i_hash):
        LOGGER.info(f'db_man.py.add_user: {i_user_nm}, {i_hash}.')
        lr_new_user = self.ConnUsers(i_user_nm, i_hash)
        self.m_sess.add(lr_new_user)
        self.m_sess.commit()
        lr_stats = self.UsersStats(lr_new_user.user_id)
        self.m_sess.add(lr_stats)
        self.m_sess.commit()

    def del_user(self, i_user_nm):
        lr_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).first()
        self.m_sess.query(self.ActUsers).filter_by(user_id=lr_user.user_id).delete()
        self.m_sess.query(self.LogHist).filter_by(user_id=lr_user.user_id).delete()
        self.m_sess.query(self.UsersContacts).filter_by(user_id=lr_user.user_id).delete()
        self.m_sess.query(self.UsersContacts).filter_by(contact_id=lr_user.user_id).delete()
        self.m_sess.query(self.UsersStats).filter_by(user_id=lr_user.user_id).delete()
        self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).delete()
        self.m_sess.commit()

    def get_pubkey(self, i_user_nm):
        lr_user = self.m_sess.query(self.ConnUsers).filter_by(user_nm=i_user_nm).first()
        return lr_user.pubkey

if __name__ == '__main__':
    l_db = DbManager()
    l_db.log_conn_in('client_1', '192.168.1.4', 8888)
    l_db.log_conn_in('client_2', '192.168.1.5', 7777)
    print('Список активных пользователей 1:')
    pprint(l_db.get_act_users())
    print('---------------------------------')
    l_db.log_conn_out('client_1')
    print('Список активных пользователей 2:')
    pprint(l_db.get_act_users())
    print('---------------------------------')
    print('История входов клиента <client_1>:')
    pprint(l_db.login_history('client_1'))
    print('---------------------------------')
    print('Список пользователей:')
    pprint(l_db.get_users_list())
    print('---------------------------------')
    l_db.reg_mess('client_1', 'client_2')
    l_db.reg_mess('client_1', 'client_2')
    l_db.reg_mess('client_2', 'client_1')
    print('---------------------------------')
    pprint(l_db.get_users_stats())
    print('---------------------------------')
    #l_db.add_contact('user2', 'user1')
    #l_db.del_contact('user1', 'user2')
    pprint(l_db.get_contacts_list('user1'))

