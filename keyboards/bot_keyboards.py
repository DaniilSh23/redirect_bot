from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from keyboards.bot_buttons import BUTTONS_DCT
from secondary_functions.req_to_bot_api import get_settings

ADMIN_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['ADMIN_PANEL']
    ],
])

HEAD_PAGE_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CREATE_LINK'],
        BUTTONS_DCT['GET_STATISTIC'],
    ],
    [
        BUTTONS_DCT['FAQ'],
        BUTTONS_DCT['SUPPORT'],
    ],
    [
        BUTTONS_DCT['MY_BALANCE'],
        BUTTONS_DCT['REPLENISH_BALANCE'],
    ],
    [
        BUTTONS_DCT['FEEDBACK_CHAT'],
    ]
])

CANCEL_AND_CLEAR_STATE_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CANCEL_AND_CLEAR_STATE'],
    ],
])

CHOOSE_SHORT_LINK_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['custom_domain'],
    ],
    [
        # BUTTONS_DCT['cutt.ly'],
        # BUTTONS_DCT['cutt.us'],
        BUTTONS_DCT['clck.ru'],
        BUTTONS_DCT['kortlink.dk'],
    ],
    # [
    #     BUTTONS_DCT['gg.gg'],
    #     BUTTONS_DCT['t9y.me'],
    # ],
])

BACK_TO_HEAD_PAGE_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])


MY_BALANCE_PART_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['REPLENISH_BALANCE'],
    ],
    [
        BUTTONS_DCT['TRANSACTIONS_STORY'],
    ],
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])


AFTER_GET_TRANSACTIONS_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['REPLENISH_BALANCE'],
    ],
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])


PAY_METHODS_KBRD = InlineKeyboardMarkup([
    # [
    #     # BUTTONS_DCT['QIWI_PAY_METHD'],
    #     BUTTONS_DCT['CRYSTAL_PAY_METHD'],
    # ],
    [
        BUTTONS_DCT['TO_CARD_PAY_METHD'],
    ],
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])


WAITING_FOR_PAYMENT_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CONFIRM_PAYMENT'],
    ],
    [
        BUTTONS_DCT['CANCEL_PAYMENT'],
    ],
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])


PAY_TO_CARD_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['I_PAYD_TO_CARD'],
    ],
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])


async def statistic_keyboard(company_id):
    """
    Клавиатура в разделе статистики.
    Записываем в колбэк кнопок по выбору периода company_id
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text='🔹Сегодня',
                callback_data=f'stat_period {company_id} today',
            ),
            InlineKeyboardButton(
                text='🔹Вчера',
                callback_data=f'stat_period {company_id} yesterday',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🔹Тек. неделя',
                callback_data=f'stat_period {company_id} last_monday',
            ),
            InlineKeyboardButton(
                text='🔹Последн. 7 дней',
                callback_data=f'stat_period {company_id} 7_days_ago',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🔹Тек. месяц',
                callback_data=f'stat_period {company_id} first_day_of_this_month',
            ),
            InlineKeyboardButton(
                text='🔹Пред. месяц',
                callback_data=f'stat_period {company_id} previous_month',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🔹Последн. 30 дней',
                callback_data=f'stat_period {company_id} 1_month_ago',
            ),
            InlineKeyboardButton(
                text='🔹Тек. год',
                callback_data=f'stat_period {company_id} first_day_of_this_year',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🔹За год',
                callback_data=f'stat_period {company_id} 1_year_ago',
            ),
            InlineKeyboardButton(
                text='🔹За всё время',
                callback_data=f'stat_period {company_id} all_time',
            ),
        ],
        [
            BUTTONS_DCT['CHECK_MORE'],
        ],
        [
            BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
        ],
    ])


async def choose_numb_of_redirect_kbrd(redirect_numb='1', replenish_balance=False):
    """
    Клавиатурка для выбора кол-ва редиректов
    """
    inline_kbrd_lst = [
        [
            BUTTONS_DCT['MINUS_REDIRECT'],
            InlineKeyboardButton(   # Кол-во редиректов, как кнопка
                text=redirect_numb,
                callback_data='plug',
            ),
            BUTTONS_DCT['PLUS_REDIRECT'],
        ],
        [
            BUTTONS_DCT['MINUS_10_REDIRECT'],
            BUTTONS_DCT['PLUS_10_REDIRECT'],
        ],
        [
            BUTTONS_DCT['MINUS_100_REDIRECT'],
            BUTTONS_DCT['PLUS_100_REDIRECT'],
        ],
        [
            BUTTONS_DCT['MINUS_1000_REDIRECT'],
            BUTTONS_DCT['PLUS_1000_REDIRECT'],
        ],
        [
            BUTTONS_DCT['CANCEL_AND_CLEAR_STATE'],
            BUTTONS_DCT['TO_LINK_SHORTENING'],
        ]
    ]
    if replenish_balance:
        inline_kbrd_lst.append([
            BUTTONS_DCT['REPLENISH_BALANCE'],
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_kbrd_lst)


async def form_webapp_kbrd(form_link, btn_text):
    """
    Формирование клавиатуры для перехода к форме, которая реализована через веб-приложение.
    :param form_link: ссылка на веб-форму.
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=btn_text,
                web_app=WebAppInfo(url=form_link)
            )
        ],
    ])


async def card_payment_processing_kbrd(tlg_id):
    """
    Клавиатура для обработки платежей на карту.
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text='✅Подтвердить платёж',
                callback_data=f'confirm_card_payment {tlg_id}',
            ),
            InlineKeyboardButton(
                text='❌Отклонить платёж',
                callback_data=f'decline_card_payment {tlg_id}',
            )
        ],
    ])


async def form_head_page_keyboard():
    """
    Формируем клавиатуру для главной странице.
    (Эта функция нужна, чтобы подтягивать из БД ссылку на канал с отзывами)
    """
    feedback_channel_link = await get_settings(key='feedback_link')
    return InlineKeyboardMarkup([
        [
            BUTTONS_DCT['CREATE_LINK'],
            BUTTONS_DCT['GET_STATISTIC'],
        ],
        [
            BUTTONS_DCT['FAQ'],
            BUTTONS_DCT['SUPPORT'],
        ],
        [
            BUTTONS_DCT['MY_BALANCE'],
            BUTTONS_DCT['REPLENISH_BALANCE'],
        ],
        [
            InlineKeyboardButton(
                text=f'🌟ОТЗЫВЫ',
                url=feedback_channel_link[0].get('value')
            )
        ]
    ])
