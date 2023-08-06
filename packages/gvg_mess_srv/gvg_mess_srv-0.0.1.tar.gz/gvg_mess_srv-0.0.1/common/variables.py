"""Константы"""

import logging

# Порт по умолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
FROM_USER = 'from_user'
TO_USER = 'to_user'
PUBLIC_KEY = 'public_key'
DATA = 'data'
PUBLIC_KEY_REQUEST = 'pubkey_req'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
MESSAGE = 'message'
EXIT = 'exit'
ADD_CONTACT = 'add_contact'
DEL_CONTACT = 'del_contact'
GET_USERS = 'get_users'
USERS_LIST = 'users_list'
GET_CONTACTS = 'get_contacts'
CONTACTS_LIST = 'contacts_list'

RESPONSE = 'response'
ERROR = 'error'
MESSAGE_TEXT = 'mess_text'
DB_NAME = 'cs_db.db3'

RESPONSE_511 = {RESPONSE: 511, DATA: None}

SRV_SECTION = 'SRV-SETTINGS'
PAR_PORT = 'srv_port'
PAR_ADDR = 'srv_addr'
PAR_DB_PATH = 'db_path'
PAR_DB_FILE = 'db_file'
