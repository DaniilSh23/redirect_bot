"""
Вспомогательные функции, которые используются в разных местах кода.
"""
from secondary_functions.req_to_bot_api import get_settings


async def make_feedback_link():
    """
    Функция, которая собирает ссылку для кнопки с отзывами.
    """
    feedback_channel_link = await get_settings(key='feedback_link')
    if not feedback_channel_link:
        return "https://t.me/durov"
    return feedback_channel_link[0].get('value')
