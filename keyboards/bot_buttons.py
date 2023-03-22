from pyrogram.types import InlineKeyboardButton

from settings.config import BASE_HOST_URL

BUTTONS_DCT = {
    'ADMIN_PANEL': InlineKeyboardButton(
        text=f'⌨️Админ-панель',
        url=f'{BASE_HOST_URL}admin/'
    ),
    'CREATE_LINK': InlineKeyboardButton(
        text=f'🔗СОЗДАТЬ ССЫЛКУ',
        callback_data='create_link'
    ),
    'GET_STATISTIC': InlineKeyboardButton(
        text=f'📊СТАТИСТИКА',
        callback_data='get_statistic'
    ),
    'FAQ': InlineKeyboardButton(
        text=f'❓FAQ',
        callback_data='faq_btn'
    ),
    'SUPPORT': InlineKeyboardButton(
        text=f'👷‍♂️ПОДДЕРЖКА',
        callback_data='support_btn'
    ),
    'MY_BALANCE': InlineKeyboardButton(
        text=f'💰МОЙ БАЛАНС',
        callback_data='my_balance'
    ),
    'REPLENISH_BALANCE': InlineKeyboardButton(
        text=f'💸ПОПОЛНИТЬ БАЛАНС',
        callback_data='replenish_balance'
    ),
}
