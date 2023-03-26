import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN', '5265303938:AAE1daGp-VJR0R15J9tHksR38hQlbCXMYdU')
API_ID = os.environ.get('API_ID', '1234567890')
API_HASH = os.environ.get('API_HASH', 'какой-то там хэш')

# Константы для API Django проекта
BASE_HOST_URL = os.environ.get('BASE_HOST_URL', 'http://127.0.0.1:8000/')
USER_DATA_URL = f'{BASE_HOST_URL}tlg_user/'
GET_BOT_ADMINS_URL = f'{BASE_HOST_URL}get_settings/'
LINKS_URL = f'{BASE_HOST_URL}links/'
LINK_SET_URL = f'{BASE_HOST_URL}link_set/'
START_WRAPPING_URL = f'{BASE_HOST_URL}start_wrapping/'

# Настройки для throttling middleware
SECNDS_BETWEEN_REQUEST = 0     # Секунды между запросами
BLACK_LIST = dict()     # юзеры, которые делают много запросов {tlg_id: datetime_when_block_expires}
USERS_REQ_DCT = dict()  # учёт запросов юзеров {tlg_id: request_datetime}

# Прочие хранилища
STATES_STORAGE_DCT = dict()     # Хранилище состояний
LINKS_OBJ_DCT = dict()  # Словарь для хранения ссылок к объектам класса RedirectLinks
