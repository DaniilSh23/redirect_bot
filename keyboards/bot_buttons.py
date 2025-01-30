from pyrogram.types import InlineKeyboardButton, WebAppInfo

from settings.config import BASE_HOST_URL, FEEDBACK_CHAT_URL

BUTTONS_DCT = {
    'ADMIN_PANEL': InlineKeyboardButton(
        text=f'⌨️Админ-панель',
        url=f'{BASE_HOST_URL}admin/'
    ),

    # Главное меню
    'CREATE_LINK_rus': InlineKeyboardButton(
        text=f'🔗СОЗДАТЬ ССЫЛКУ',
        callback_data='create_link'
    ),
    'CREATE_LINK_eng': InlineKeyboardButton(
        text=f'🔗CREATE LINK',
        callback_data='create_link'
    ),
    'GET_STATISTIC_rus': InlineKeyboardButton(
        text=f'📊СТАТИСТИКА',
        callback_data='get_statistic'
    ),
    'GET_STATISTIC_eng': InlineKeyboardButton(
        text=f'📊STATISTICS',
        callback_data='get_statistic'
    ),
    'FAQ_rus': InlineKeyboardButton(
        text=f'❓ПРАВИЛА/FAQ',
        callback_data='faq_btn'
    ),
    'FAQ_eng': InlineKeyboardButton(
        text=f'❓RULES/FAQ',
        callback_data='faq_btn'
    ),
    'SUPPORT_rus': InlineKeyboardButton(
        text=f'👷‍♂️ПОДДЕРЖКА',
        callback_data='support_btn'
    ),
    'SUPPORT_eng': InlineKeyboardButton(
        text=f'👷‍♂️SUPPORT',
        callback_data='support_btn'
    ),
    'MY_BALANCE_rus': InlineKeyboardButton(
        text=f'💰МОЙ БАЛАНС',
        callback_data='my_balance'
    ),
    'MY_BALANCE_eng': InlineKeyboardButton(
        text=f'💰MY BALANCE',
        callback_data='my_balance'
    ),
    'REPLENISH_BALANCE_rus': InlineKeyboardButton(
        text=f'💸ПОПОЛНИТЬ БАЛАНС',
        callback_data='replenish_balance'
    ),
    'REPLENISH_BALANCE_eng': InlineKeyboardButton(
        text=f'💸TOP UP',
        callback_data='replenish_balance'
    ),
    'TRANSACTIONS_STORY_rus': InlineKeyboardButton(
        text=f'🧾ИСТОРИЯ ОПЕРАЦИЙ',
        callback_data='transactions_story'
    ),
    'TRANSACTIONS_STORY_eng': InlineKeyboardButton(
        text=f'🧾TRANSACTION HISTORY',
        callback_data='transactions_story'
    ),
    'CANCEL_AND_CLEAR_STATE_rus': InlineKeyboardButton(
        text=f'❌Отменить',
        callback_data='cancel_and_clear_state'
    ),
    'CANCEL_AND_CLEAR_STATE_eng': InlineKeyboardButton(
        text=f'❌Cancel',
        callback_data='cancel_and_clear_state'
    ),
    'BACK_TO_HEAD_PAGE_rus': InlineKeyboardButton(
        text=f'🔙На главную',
        callback_data='back_to_head_page'
    ),
    'BACK_TO_HEAD_PAGE_eng': InlineKeyboardButton(
        text=f'🔙HOME',
        callback_data='back_to_head_page'
    ),
    'FEEDBACK_CHAT_rus': InlineKeyboardButton(
        text=f'🌟ОТЗЫВЫ',
        url=FEEDBACK_CHAT_URL
    ),
    'FEEDBACK_CHAT_eng': InlineKeyboardButton(
        text=f'🌟REVIEWS',
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
    'TO_LINK_SHORTENING_rus': InlineKeyboardButton(
        text=f'След.шаг➡️',
        callback_data='to_link_shortening'
    ),
    'TO_LINK_SHORTENING_eng': InlineKeyboardButton(
        text=f'Next step➡️',
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
    'haa.su': InlineKeyboardButton(
        text=f'🔹haa.su',
        callback_data='short_link haa.su'
    ),
    'kurl.ru': InlineKeyboardButton(
        text=f'🔹kurl.ru',
        callback_data='short_link kurl.ru'
    ),
    'rebrandly.com': InlineKeyboardButton(
        text=f'🔹rebrandly.com',
        callback_data='short_link rebrandly.com'
    ),
    'custom_domain_rus': InlineKeyboardButton(
        text=f'🔹Наши домены ⚜️',
        callback_data='short_link custom_domain'
    ),
    'custom_domain_eng': InlineKeyboardButton(
        text=f'🔹OUR DOMAINS ⚜️',
        callback_data='short_link custom_domain'
    ),

    # Кнопка для раздела статистики
    'CHECK_MORE_rus': InlineKeyboardButton(
        text='🔂Проверить ещё',
        callback_data='get_statistic'
    ),
    'CHECK_MORE_eng': InlineKeyboardButton(
        text='🔂Check more',
        callback_data='get_statistic'
    ),

    # Раздел платежей
    'QIWI_PAY_METHD': InlineKeyboardButton(
        text='🪙QIWI',
        callback_data='pay_method qiwi',
    ),
    'CRYSTAL_PAY_METHD': InlineKeyboardButton(
        text='🌑 Crystal Pay',
        callback_data='pay_method crystal',
    ),
    'TO_CARD_PAY_METHD_rus': InlineKeyboardButton(
        text='🌕 Перевод на карту',
        callback_data='pay_to_card',
    ),
    'TO_CARD_PAY_METHD_eng': InlineKeyboardButton(
        text='🌕 Transfer to card',
        callback_data='pay_to_card',
    ),
    'CONFIRM_PAYMENT_rus': InlineKeyboardButton(
        text='✅Подтвердить оплату',
        callback_data='confirm_payment',
    ),
    'CONFIRM_PAYMENT_eng': InlineKeyboardButton(
        text='✅Confirm Payment',
        callback_data='confirm_payment',
    ),
    'CANCEL_PAYMENT_rus': InlineKeyboardButton(
        text='❌Отменить оплату',
        callback_data='cancel_payment',
    ),
    'CANCEL_PAYMENT_eng': InlineKeyboardButton(
        text='❌Cancel Payment',
        callback_data='cancel_payment',
    ),
    'I_PAYD_TO_CARD_rus': InlineKeyboardButton(
        text='✅Я перевёл',
        callback_data='i_payd_to_card',
    ),
    'I_PAYD_TO_CARD_eng': InlineKeyboardButton(
        text='✅I PAID',
        callback_data='i_payd_to_card',
    ),
    'CHANGE_LANG_rus': InlineKeyboardButton(
        text='🔤 Сменить язык',
        callback_data='change_lang',
    ),
    'CHANGE_LANG_eng': InlineKeyboardButton(
        text='🔤 Change the language',
        callback_data='change_lang',
    )
}
