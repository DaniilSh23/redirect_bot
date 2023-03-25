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
