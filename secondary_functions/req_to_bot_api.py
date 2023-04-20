import json

import aiohttp as aiohttp
from loguru import logger
from settings.config import USER_DATA_URL, GET_BOT_ADMINS_URL, LINKS_URL, LINK_SET_URL, START_WRAPPING_URL, \
    PAYMENTS_URL, CHANGE_BALANCE_URL, GET_LINK_OWNER, TRANSACTION_URL


async def post_user_data(user_data):
    """
    POST запрос для создания или обновления записи о пользователе в БД.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=USER_DATA_URL, data=user_data) as response:
            if response.status == 200:
                logger.success(f'Успешный POST-запрос для создания/обновления записи о пользователе бота')
                return True
            else:
                logger.warning(f'POST-запрос для создания/обновления записи о пользователе бота НЕ УДАЛСЯ')
                return False


async def get_user_data(tlg_id):
    """
    GET запрос для получения данных о пользователе телеграм из БД.
    """
    url = f'{USER_DATA_URL}?tlg_id={tlg_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            if response.status == 200:
                logger.success(f'Успешный GET запрос для получения инфы о юзере с TG ID == {tlg_id}')
                return await response.json()
            else:
                logger.warning(f'GET запрос для получения данных об юзере с TG ID == {tlg_id} НЕ УДАЛСЯ!')
                return False


async def get_settings(key):
    """
    GET запрос для получения значения какой-либо настройки бота.
    Вернет JSON, в котором в списке лежат ключи и значения настроек.
    [{"key": "value"}, ...]
    """
    url = ''.join([GET_BOT_ADMINS_URL, f'?key={key}'])
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            if response.status == 200:
                logger.success(f'Успешный GET-запрос для получения настроек')
                return await response.json()
            else:
                logger.warning(f'GET-запрос для получения списка настроек НЕ УДАЛСЯ')
                return False


async def update_or_create_link(data):
    """
    POST запрос для создания или обновления ссылки.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=LINKS_URL, json=data) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для создания/обновления ссылки.')
                return True
            else:
                logger.warning(f'Неудачный запрос для создания/обновления ссылки.')
                return False


async def post_for_create_link_set(data):
    """
    POST запрос для создания набора ссылок в БД.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=LINK_SET_URL, json=data) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для создания набора ссылок.')
                return await response.json()
            else:
                logger.warning(f'Неудачный запрос для создания набора ссылок!')
                return False


async def post_for_start_wrapping(data):
    """
    POST запрос для старта обёртки ссылок.
    Параметры:
        link_set_id - ID набора ссылок.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=START_WRAPPING_URL, json=data) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для старта обёртки ссылок.')
                return await response.json()
            else:
                logger.warning(f'Неудачный запрос для старта обёртки ссылок!')
                return False


async def post_for_create_payment(data):
    """
    POST запрос для создания в БД записи о платеже.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=PAYMENTS_URL, json=data) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос на создание в БД данных о платеже.')
                return await response.json()
            else:
                logger.warning(f'Неудачный запрос для создания в БД данных о платеже.')
                return False


async def req_for_get_payment(tlg_id=None, payment_for_dlt_id=None):
    """
    GET запрос для получения в БД записи о платеже.
    """
    if tlg_id:
        req_url = f"{PAYMENTS_URL}?tlg_id={tlg_id}"
    elif payment_for_dlt_id:
        req_url = f"{PAYMENTS_URL}?payment_for_dlt_id={payment_for_dlt_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=req_url) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для получения/удаления в БД данных о платеже.')
                return await response.json()
            elif response.status == 404:
                logger.success(f'Успешный запрос, но активных счетов не найдено.')
                return 404
            else:
                logger.warning(f'Неудачный запрос для получения/удаления в БД данных о платеже.')
                return False


async def post_for_change_balance(data):
    """
    POST запрос для изменения баланса.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=CHANGE_BALANCE_URL, json=data) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для изменения баланса.')
                return True
            else:
                logger.warning(f'Неудачный запрос для изменения баланса.')
                return False


async def get_link_owner(company_id):
    """
    GET запрос для получение TG ID владельца ссылки.
    """
    url = f'{GET_LINK_OWNER}?company_id={company_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для получения владельца ссылки.')
                return await response.json()
            elif response.status == 404:
                logger.warning(f'Владелец ссылки не найден. Статус 404.')
                return False
            else:
                logger.warning(f'Неудачный запрос для получения владельца ссылки.')
                return False


async def post_for_create_transaction(data):
    """
    POST запрос для создания транзакции
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=TRANSACTION_URL, json=data) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для создания транзакции.')
                return True
            else:
                logger.warning(f'Неудачный запрос для создания транзакции.')
                return False


async def get_transactions(tlg_id):
    """
    GET запрос для получения транзакций. Будет запущена задача по формированию файла и отправке в телегу.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{TRANSACTION_URL}?tlg_id={tlg_id}') as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для создания транзакции.')
                return True
            else:
                logger.warning(f'Неудачный запрос для создания транзакции.')
                return False
