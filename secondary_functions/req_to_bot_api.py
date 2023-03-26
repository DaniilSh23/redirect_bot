import json

import aiohttp as aiohttp
from loguru import logger
from settings.config import USER_DATA_URL, GET_BOT_ADMINS_URL, LINKS_URL, LINK_SET_URL, START_WRAPPING_URL


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
    GET запрос для получения списка админов бота.
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
