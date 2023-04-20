import os
from dotenv import load_dotenv

load_dotenv()

# Данные Telegram
TOKEN = os.environ.get('TOKEN', '5265303938:AAE1daGp-VJR0R15J9tHksR38hQlbCXMYdU')
API_ID = os.environ.get('API_ID', '1234567890')
API_HASH = os.environ.get('API_HASH', 'какой-то там хэш')
FEEDBACK_CHAT_URL = os.environ.get('FEEDBACK_CHAT_URL', 'https://t.me/longi_gr')

# Данные платёжных систем
SECRET_QIWI_P2P = os.environ.get('SECRET_QIWI_P2P', 'секретный ключ киви')
CRYSTAL_PAY_LOGIN = os.environ.get('CRYSTAL_PAY_LOGIN', 'логин кристал пэй')
CRYSTAL_PAY_SECRET1 = os.environ.get('CRYSTAL_PAY_SECRET1', 'секретный ключ 1 кристал пэй')
CRYSTAL_PAY_SECRET2 = os.environ.get('CRYSTAL_PAY_SECRET2', 'секретный ключ 2(он же Salt) кристал пэй')

# Константы для API Django проекта
BASE_HOST_URL = os.environ.get('BASE_HOST_URL', 'http://127.0.0.1:8000/')
USER_DATA_URL = f'{BASE_HOST_URL}tlg_user/'
GET_BOT_ADMINS_URL = f'{BASE_HOST_URL}get_settings/'
LINKS_URL = f'{BASE_HOST_URL}links/'
LINK_SET_URL = f'{BASE_HOST_URL}link_set/'
START_WRAPPING_URL = f'{BASE_HOST_URL}start_wrapping/'
PAYMENTS_URL = f'{BASE_HOST_URL}payments/'
CHANGE_BALANCE_URL = f'{BASE_HOST_URL}change_balance/'
GET_LINK_OWNER = f'{BASE_HOST_URL}get_link_owner/'
TRANSACTION_URL = f'{BASE_HOST_URL}transaction/'

# Настройки для throttling middleware
SECNDS_BETWEEN_REQUEST = float(os.environ.get('SECNDS_BETWEEN_REQUEST', '0'))     # Секунды между запросами
REQ_COUNT = int(os.environ.get('REQ_COUNT', '0'))     # Количество запросов в единицу времени
BLACK_LIST = dict()     # юзеры, которые делают много запросов {tlg_id: datetime_when_block_expires}
USERS_REQ_DCT = dict()  # учёт запросов юзеров {tlg_id: [req_seconds, req_count]}

# Прочие хранилища
STATES_STORAGE_DCT = dict()     # Хранилище состояний
LINKS_OBJ_DCT = dict()  # Словарь для хранения ссылок к объектам класса RedirectLinks
PAYMENTS_OBJ_DCT = dict()   # Словарь для хранения ссылок к объектам класса UserPayments
TEMP_STORAGE_DCT = dict()   # Временное хранилище, в котором может лежать что угодно, но ключ всегда TG ID
