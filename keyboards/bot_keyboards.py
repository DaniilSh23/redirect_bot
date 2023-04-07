from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from keyboards.bot_buttons import BUTTONS_DCT

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
])

CANCEL_AND_CLEAR_STATE_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CANCEL_AND_CLEAR_STATE'],
    ],
])

CHOOSE_SHORT_LINK_KBRD = InlineKeyboardMarkup([
    [
        # BUTTONS_DCT['cutt.ly'],
        BUTTONS_DCT['cutt.us'],
        BUTTONS_DCT['clck.ru'],
    ],
    [
        BUTTONS_DCT['kortlink.dk'],
        BUTTONS_DCT['gg.gg'],
        # BUTTONS_DCT['t9y.me'],
    ],
])

BACK_TO_HEAD_PAGE_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])

BACK_TO_HEAD_PAGE_FROM_STATISTIC_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CHECK_MORE'],
    ],
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])

MY_BALANCE_PART_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['REPLENISH_BALANCE'],
    ],
    [
        BUTTONS_DCT['BACK_TO_HEAD_PAGE'],
    ],
])


PAY_METHODS_KBRD = InlineKeyboardMarkup([
    [
        # BUTTONS_DCT['QIWI_PAY_METHD'],
        BUTTONS_DCT['CRYSTAL_PAY_METHD'],
    ],
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
