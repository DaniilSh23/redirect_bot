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
