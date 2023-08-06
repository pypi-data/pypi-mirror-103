import os
import sys
import json
import socket
import logging
import select
import time
import traceback
import threading
import hmac
import binascii
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT,\
    ACTION, TIME, FROM_USER, TO_USER,\
    PRESENCE, MESSAGE, RESPONSE, ERROR, MESSAGE_TEXT,\
    ADD_CONTACT, DEL_CONTACT, EXIT, MAX_CONNECTIONS,\
    GET_USERS, USERS_LIST, GET_CONTACTS, CONTACTS_LIST,\
    DB_NAME, DATA, PUBLIC_KEY, PUBLIC_KEY_REQUEST,\
    RESPONSE_511
BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from common.delog import gvglog, login_required
from logdat.cnf import cnf_srv_log
from common.utils import check_message, create_message, get_message, send_message
from common.metas import ServerVerifier
from server.descs import ListPort

LOGGER = logging.getLogger('server')


class MessSrv(threading.Thread, metaclass=ServerVerifier):
    m_port = ListPort('m_port')

    def __init__(self, i_addr, i_port, i_db):
        super().__init__()

        self.m_addr = i_addr
        self.m_port = i_port
        self.m_db = i_db

        LOGGER.info(f'Инициализация сокета...')
        self.m_sock_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        LOGGER.info(f'Создан сокет: {self.m_sock_srv}.')
        self.m_sock_srv.bind((self.m_addr, self.m_port))

        self.m_sock_srv.settimeout(0.5)
        LOGGER.info(f'Привязка к адресу, порту: address=<{self.m_addr}>, port=<{self.m_port}>.')

        self.m_ls_cli_socks = []
        self.m_messages = []
        self.m_dc_user_socks = {}
        self.m_keep_run = True

    def run(self):

        self.m_sock_srv.listen(MAX_CONNECTIONS)
        LOGGER.info(f'Прослушка началась(очередь: {MAX_CONNECTIONS})...')

        while self.m_keep_run:
            try:
                l_sock_cli, l_addr_cli = self.m_sock_srv.accept()
                LOGGER.info(f'Получен клиент(сокет): {l_sock_cli}.')
                LOGGER.info(f'Получен клиент(адрес): {l_addr_cli}.')
                self.m_ls_cli_socks.append(l_sock_cli)
                ldic_mess = get_message(l_sock_cli)
                LOGGER.info('Обработка первого запроса.')
                self.process_client_message(ldic_mess, l_sock_cli)
            except OSError:
                pass

            ll_read_cli = []
            ll_writ_cli = []
            ll_erro_cli = []

            try:
                if self.m_ls_cli_socks:
                    ll_read_cli, ll_writ_cli, ll_erro_cli = select.select(
                        self.m_ls_cli_socks, self.m_ls_cli_socks, [], 0)
            except OSError:
                pass

            #LOGGER.info(f'Получены клиенты: read: {len(ll_read_cli)}, write: {len(ll_writ_cli)}.')

            if ll_read_cli:
                for l_cli_sock in ll_read_cli:
                    try:
                        ldic_mess = get_message(l_cli_sock)
                        LOGGER.info('Обработка последующего запроса.')
                        self.process_client_message(ldic_mess, l_cli_sock)
                    except Exception as exc:

                        for l_key in self.m_dc_user_socks:
                            if self.m_dc_user_socks[l_key] == l_cli_sock:
                                self.m_db.log_conn_out(l_key)

                        LOGGER.critical(f'Клиент на чтение {l_cli_sock.getpeername()} потерян.')
                        #LOGGER.critical(f'READ.ERROR: <{exc.__repr__()}>!')
                        #traceback.print_stack()
                        self.m_ls_cli_socks.remove(l_cli_sock)
                        for k in self.m_dc_user_socks.copy():
                            if self.m_dc_user_socks[k] == l_cli_sock:
                                del self.m_dc_user_socks[k]


            if ll_writ_cli and self.m_messages:
                for lr_mess in self.m_messages:
                    try:
                        l_user_sock = self.m_dc_user_socks.get(lr_mess[TO_USER])
                        if l_user_sock:
                            send_message(l_user_sock, lr_mess)
                            LOGGER.info(f'Отправлено пользователю {lr_mess[TO_USER]} '
                                        f'от {lr_mess[FROM_USER]}.')
                    except Exception as exc:
                        LOGGER.critical(f'Клиент на запись {l_cli_sock.getpeername()} потерян.')
                        LOGGER.critical(f'WRITE.ERROR: <{exc.__repr__()}>!')
                        traceback.print_stack()
                        self.m_ls_cli_socks.remove(l_user_sock)

            self.m_messages.clear()

        self.m_sock_srv.close()
        LOGGER.info('Сервер(сокет) закрылся.')


    @login_required
    def process_client_message(self, idic_mess, i_cli_sock):

        LOGGER.error(f'server.py.process_client_message.GVG.01: <{idic_mess}>, <{i_cli_sock}>.')

        ls_chk = check_message(idic_mess)

        if ls_chk:
            ls_tot_err = f'Ошибка {ls_chk} в сообщении {idic_mess}!'
            LOGGER.error(ls_tot_err)

            send_message(i_cli_sock, {
                RESPONSE: 400,
                ERROR: ls_tot_err
            })
            return ls_tot_err

        if idic_mess[ACTION] == PRESENCE:
            self.autorize_user(idic_mess, i_cli_sock)

        elif idic_mess[ACTION] == ADD_CONTACT:
            ls_cur_user = idic_mess[FROM_USER]
            ls_contact = idic_mess[TO_USER]

            LOGGER.info(f'server.py.ADD_CONTACT.call for insert into DB: user: {ls_cur_user}, contact: {ls_contact}...')
            ls_res = self.m_db.add_contact(ls_cur_user, ls_contact)
            if ls_res:
                send_message(i_cli_sock, {RESPONSE: 400, ERROR: ls_res})
            else:
                send_message(i_cli_sock, {RESPONSE: 200})
            return f'Detected {ADD_CONTACT}'

        elif idic_mess[ACTION] == DEL_CONTACT:
            ls_cur_user = idic_mess[FROM_USER]
            ls_contact = idic_mess[TO_USER]

            LOGGER.info(f'server.py.DEL_CONTACT.call for insert into DB: user: {ls_cur_user}, contact: {ls_contact}...')
            ls_res = self.m_db.del_contact(ls_cur_user, ls_contact)
            if ls_res:
                send_message(i_cli_sock, {RESPONSE: 400, ERROR: ls_res})
            else:
                send_message(i_cli_sock, {RESPONSE: 200})
            return f'Detected {DEL_CONTACT}'

        elif idic_mess[ACTION] == MESSAGE and MESSAGE_TEXT in idic_mess:
            self.m_messages.append(idic_mess)
            self.m_db.reg_mess(idic_mess[FROM_USER], idic_mess[TO_USER])
            return 'Message added to list'

        elif idic_mess[ACTION] == GET_USERS:
            LOGGER.info(f'server.py.GET_USERS.call from DB...')
            lls_users = self.m_db.get_users_list()
            ldic_res = {RESPONSE: 200}
            ldic_res[USERS_LIST] = [rec[1] for rec in lls_users]
            send_message(i_cli_sock, ldic_res)
            return f'Detected {GET_USERS}'

        elif idic_mess[ACTION] == GET_CONTACTS:
            LOGGER.info(f'server.py.GET_CONTACTS.call from DB...')
            lls_contacts = self.m_db.get_contacts_list(idic_mess[FROM_USER])
            ldic_res = {RESPONSE: 200}
            ldic_res[CONTACTS_LIST] = lls_contacts
            send_message(i_cli_sock, ldic_res)
            return f'Detected {GET_CONTACTS}'

        elif idic_mess[ACTION] == EXIT:
            l_del_user = idic_mess[FROM_USER]
            l_del_sock = self.m_dc_user_socks[l_del_user]
            self.m_ls_cli_socks.remove(l_del_sock)
            del self.m_dc_user_socks[l_del_user]
            self.m_db.log_conn_out(l_del_user)
            return f'user {l_del_user} disconnected'

        elif idic_mess[ACTION] == PUBLIC_KEY_REQUEST:
            ls_cur_user = idic_mess[FROM_USER]
            l_resp = RESPONSE_511
            l_resp[DATA] = self.m_db.get_pubkey(ls_cur_user)
            if l_resp[DATA]:
                send_message(i_cli_sock, l_resp)
            else:
                send_message(i_cli_sock, {
                    RESPONSE: 400,
                    ERROR: f'Нет публичного ключа для <{ls_cur_user}>!'
                })

        else:
            send_message(i_cli_sock, {
                RESPONSE: 400,
                ERROR: 'Bad Request(Unknown message)'
            })
            return 'Bad Request(Unknown message)'

    def autorize_user(self, idic_mess, i_cli_sock):
        l_from_user = idic_mess[FROM_USER]

        LOGGER.debug(f'autorize_user.00: start for <{l_from_user}>.')

        if l_from_user in self.m_dc_user_socks.keys():
            send_message(i_cli_sock, {
                RESPONSE: 400,
                ERROR: f'Пользователь {l_from_user} уже занят!'
            })
            self.m_ls_cli_socks.remove(i_cli_sock)
            i_cli_sock.close()
            return

        if not self.m_db.is_user_exists(l_from_user):
            send_message(i_cli_sock, {
                RESPONSE: 400,
                ERROR: f'Пользователь {l_from_user} не зарегистрирован!'
            })
            self.m_ls_cli_socks.remove(i_cli_sock)
            i_cli_sock.close()
            return

        LOGGER.debug('autorize_user.01: correct username, starting passwd check.')

        l_mess_with_rand = RESPONSE_511
        lbts_random = binascii.hexlify(os.urandom(64))
        l_mess_with_rand[DATA] = lbts_random.decode('ascii')

        LOGGER.debug(f'autorize_user.02: auth message = {l_mess_with_rand}')
        try:
            send_message(i_cli_sock, l_mess_with_rand)
            l_ans = get_message(i_cli_sock)
        except OSError as err:
            self.m_ls_cli_socks.remove(i_cli_sock)
            i_cli_sock.close()
            LOGGER.critical('autorize_user.ERROR: in auth, data:', exc_info=err)
            return

        l_client_digest = binascii.a2b_base64(l_ans[DATA])

        l_hash = hmac.new(self.m_db.get_hash(l_from_user), lbts_random, 'MD5')
        l_digest = l_hash.digest()

        if RESPONSE in l_ans and l_ans[RESPONSE] == 511 and \
           hmac.compare_digest(l_digest, l_client_digest):

            self.m_dc_user_socks[l_from_user] = i_cli_sock

            l_cli_addr, l_cli_port = i_cli_sock.getpeername()
            LOGGER.info(f'autorize_user.insert into DB: {l_from_user}, {l_cli_addr}, {l_cli_port}...')
            self.m_db.log_conn_in(l_from_user, l_cli_addr, l_cli_port, idic_mess[PUBLIC_KEY])
            try:
                send_message(i_cli_sock, {RESPONSE: 200})
            except OSError as err:
                self.m_ls_cli_socks.remove(i_cli_sock)
                i_cli_sock.close()
                LOGGER.critical('autorize_user.ERROR: in send 200:', exc_info=err)
            return f'Detected {PRESENCE}'
        else:
            send_message(i_cli_sock, {
                RESPONSE: 400,
                ERROR: f'Неверный пароль!'
            })
            self.m_ls_cli_socks.remove(i_cli_sock)
            i_cli_sock.close()

