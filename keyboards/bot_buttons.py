from pyrogram.types import InlineKeyboardButton

from settings.config import BASE_HOST_URL

BUTTONS_DCT = {
    'ADMIN_PANEL': InlineKeyboardButton(
        text=f'⌨️Админ-панель',
        url=f'{BASE_HOST_URL}admin/'
    ),

    # Главное меню
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
    'CANCEL_AND_CLEAR_STATE': InlineKeyboardButton(
        text=f'❌Отменить',
        callback_data='cancel_and_clear_state'
    ),

    # Выбор кол-ва редиректов
    'MINUS_REDIRECT': InlineKeyboardButton(
        text=f'➖',
        callback_data='minus_redirect 1'
    ),
    'PLUS_REDIRECT': InlineKeyboardButton(
        text=f'➕',
        callback_data='plus_redirect 1'
    ),
    'MINUS_10_REDIRECT': InlineKeyboardButton(
        text=f'➖10',
        callback_data='minus_redirect 10'
    ),
    'PLUS_10_REDIRECT': InlineKeyboardButton(
        text=f'➕10',
        callback_data='plus_redirect 10'
    ),
    'MINUS_100_REDIRECT': InlineKeyboardButton(
        text=f'➖100',
        callback_data='minus_redirect 100'
    ),
    'PLUS_100_REDIRECT': InlineKeyboardButton(
        text=f'➕100',
        callback_data='plus_redirect 100'
    ),
    'MINUS_1000_REDIRECT': InlineKeyboardButton(
        text=f'➖1000',
        callback_data='minus_redirect 1000'
    ),
    'PLUS_1000_REDIRECT': InlineKeyboardButton(
        text=f'➕1000',
        callback_data='plus_redirect 1000'
    ),
    'TO_LINK_SHORTENING': InlineKeyboardButton(
        text=f'След.шаг➡️',
        callback_data='to_link_shortening'
    ),

}
