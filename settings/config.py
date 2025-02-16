import os
import sys
from pathlib import Path
import loguru
from dotenv import load_dotenv

load_dotenv()

# Абсолютный путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Данные Telegram
TOKEN = os.environ.get('TOKEN', 'токен бота')
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
BASE_HOST_DOMAIN = os.environ.get('BASE_HOST_DOMAIN', 'https://ya.ru/')
USER_DATA_URL = f'{BASE_HOST_URL}tlg_user/'
GET_BOT_ADMINS_URL = f'{BASE_HOST_URL}get_settings/'
LINKS_URL = f'{BASE_HOST_URL}links/'
LINK_SET_URL = f'{BASE_HOST_URL}link_set/'
START_WRAPPING_URL = f'{BASE_HOST_URL}start_wrapping/'
PAYMENTS_URL = f'{BASE_HOST_URL}payments/'
CHANGE_BALANCE_URL = f'{BASE_HOST_URL}change_balance/'
GET_LINK_OWNER = f'{BASE_HOST_URL}get_link_owner/'
TRANSACTION_URL = f'{BASE_HOST_URL}transaction/'
INTERFACE_LANG_URL = f'{BASE_HOST_URL}interface_lang/'
USER_DOMAIN_URL = f'{BASE_HOST_DOMAIN}user_domain/'

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

# Настройки логгера
MY_LOGGER = loguru.logger
MY_LOGGER.remove()  # Удаляем все предыдущие обработчики логов
MY_LOGGER.add(sink=sys.stdout, level='DEBUG')   # Все логи от DEBUG и выше в stdout
MY_LOGGER.add(  # системные логи в файл
    sink=f'{BASE_DIR}/logs/sys_log.log',
    level='DEBUG',
    rotation='10 MB',
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True
)
