import aiohttp as aiohttp
from loguru import logger
from settings.config import USER_DATA_URL, GET_BOT_ADMINS_URL


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


async def get_bot_admins():
    """
    GET запрос для получения списка админов бота.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=GET_BOT_ADMINS_URL) as response:
            if response.status == 200:
                logger.success(f'Успешный GET-запрос для получения списка админов бота')
                return await response.json()
            else:
                logger.warning(f'GET-запрос для получения списка админов бота НЕ УДАЛСЯ')
                return False
