from pyrogram.types import InlineKeyboardButton

from settings.config import BASE_HOST_URL, FEEDBACK_CHAT_URL

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
    'BACK_TO_HEAD_PAGE': InlineKeyboardButton(
        text=f'🔙На главную',
        callback_data='back_to_head_page'
    ),
    'FEEDBACK_CHAT': InlineKeyboardButton(
        text=f'🌟Оставить отзыв',
        url=FEEDBACK_CHAT_URL
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

    # Выбор сервисов для сокращения ссылок
    'cutt.ly': InlineKeyboardButton(
        text=f'🔹cutt.ly',
        callback_data='short_link cutt.ly'
    ),
    'cutt.us': InlineKeyboardButton(
        text=f'🔹cutt.us',
        callback_data='short_link cutt.us'
    ),
    'clck.ru': InlineKeyboardButton(
        text=f'🔹clck.ru',
        callback_data='short_link clck.ru'
    ),
    'kortlink.dk': InlineKeyboardButton(
        text=f'🔹kortlink.dk',
        callback_data='short_link kortlink.dk'
    ),
    'gg.gg': InlineKeyboardButton(
        text=f'🔹gg.gg',
        callback_data='short_link gg.gg'
    ),
    't9y.me': InlineKeyboardButton(
        text=f'🔹t9y.me',
        callback_data='short_link t9y.me'
    ),

    # Кнопка для раздела статистики
    'CHECK_MORE': InlineKeyboardButton(
        text='🔂Проверить ещё',
        callback_data='get_statistic'
    ),

    # Раздел платежей
    'QIWI_PAY_METHD': InlineKeyboardButton(
        text='🪙QIWI',
        callback_data='pay_method qiwi',
    ),
    'CRYSTAL_PAY_METHD': InlineKeyboardButton(
        text='🪙Crystal Pay',
        callback_data='pay_method crystal',
    ),
    'TO_CARD_PAY_METHD': InlineKeyboardButton(
        text='🪙Перевод на карту',
        callback_data='pay_to_card',
    ),
    'CONFIRM_PAYMENT': InlineKeyboardButton(
        text='✅Подтвердить оплату',
        callback_data='confirm_payment',
    ),
    'CANCEL_PAYMENT': InlineKeyboardButton(
        text='❌Отменить оплату',
        callback_data='cancel_payment',
    ),
    'I_PAYD_TO_CARD': InlineKeyboardButton(
        text='✅Я перевёл',
        callback_data='i_payd_to_card',
    ),
}
