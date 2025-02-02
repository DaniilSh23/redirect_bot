from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from settings.config import USER_DOMAIN_URL
from keyboards.bot_buttons import BUTTONS_DCT, my_domain_button
from resources.messages import STAT_PERIODS_RUS, STAT_PERIODS_ENG
from secondary_functions.req_to_bot_api import get_interface_language
from secondary_functions.utils import make_feedback_link

ADMIN_KBRD = InlineKeyboardMarkup(
    [
        [BUTTONS_DCT["ADMIN_PANEL"]],
    ]
)


# HEAD_PAGE_KBRD = InlineKeyboardMarkup([
#     [
#         BUTTONS_DCT['CREATE_LINK'],
#         BUTTONS_DCT['GET_STATISTIC'],
#     ],
#     [
#         BUTTONS_DCT['FAQ'],
#         BUTTONS_DCT['SUPPORT'],
#     ],
#     [
#         BUTTONS_DCT['MY_BALANCE'],
#         BUTTONS_DCT['REPLENISH_BALANCE'],
#     ],
#     [
#         BUTTONS_DCT['FEEDBACK_CHAT'],
#     ],
#     [
#         BUTTONS_DCT['CHANGE_LANG'],
#     ],
# ])


async def cancel_and_clear_state_keyboard(language_code):
    """
    Функция для создания клавиатуры с кнопкой отмены и очистки состояний.
    """
    return InlineKeyboardMarkup(
        [
            [
                BUTTONS_DCT[f"CANCEL_AND_CLEAR_STATE_{language_code}"],
            ],
        ]
    )


async def choose_short_link_keyboard(language_code):
    """
    Клавиатура для выбора сервиса сокращения ссылок.
    """
    return InlineKeyboardMarkup(
        [
            [
                BUTTONS_DCT[f"user_domain_{language_code}"],
            ],
            # [
            #     BUTTONS_DCT[f"custom_domain_{language_code}"],
            # ],
            [
                BUTTONS_DCT["clck.ru"],
                BUTTONS_DCT["haa.su"],
            ],
            [
                BUTTONS_DCT["kurl.ru"],
                # BUTTONS_DCT['rebrandly.com'],
            ],
            # [
            #     BUTTONS_DCT['gg.gg'],
            #     BUTTONS_DCT['t9y.me'],
            #     BUTTONS_DCT['cutt.ly'],
            #     BUTTONS_DCT['cutt.us'],
            #     BUTTONS_DCT['kortlink.dk'],
            # ],
        ]
    )


async def back_to_headpage_keyboard(language_code):
    """
    Клавиатура с кнопкой возврата к главному меню.
    """
    return InlineKeyboardMarkup(
        [
            [
                BUTTONS_DCT[f"BACK_TO_HEAD_PAGE_{language_code}"],
            ],
        ]
    )


async def my_balance_part_keyboard(language_code):
    """
    Клавиатура для раздела меню "Мой баланс".
    """
    return InlineKeyboardMarkup(
        [
            [
                BUTTONS_DCT[f"REPLENISH_BALANCE_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"TRANSACTIONS_STORY_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"BACK_TO_HEAD_PAGE_{language_code}"],
            ],
        ]
    )


async def after_get_transaction_keyboard(language_code):
    """
    Клавиатура для раздела, который открывается после нажатия кнопки получения списка своих транзакций.
    """
    return InlineKeyboardMarkup(
        [
            [
                BUTTONS_DCT[f"REPLENISH_BALANCE_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"BACK_TO_HEAD_PAGE_{language_code}"],
            ],
        ]
    )


async def pay_methods_keyboard(language_code):
    """
    Клавиатура для выбора метода оплаты.
    """
    return InlineKeyboardMarkup(
        [
            # [
            #     # BUTTONS_DCT['QIWI_PAY_METHD'],
            #     BUTTONS_DCT['CRYSTAL_PAY_METHD'],
            # ],
            [
                BUTTONS_DCT[f"TO_CARD_PAY_METHD_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"BACK_TO_HEAD_PAGE_{language_code}"],
            ],
        ]
    )


async def waiting_for_payment_keyboard(language_code):
    """
    Клавиатура для ожидания выполнения и подтверждения платежа. Используется при ручном переводе на карту.
    """
    return InlineKeyboardMarkup(
        [
            [
                BUTTONS_DCT[f"CONFIRM_PAYMENT_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"CANCEL_PAYMENT_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"BACK_TO_HEAD_PAGE_{language_code}"],
            ],
        ]
    )


async def pay_to_card_keyboard(language_code):
    """
    Клавиатура для оплаты переводом на карту.
    """
    return InlineKeyboardMarkup(
        [
            [
                BUTTONS_DCT[f"I_PAYD_TO_CARD_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"BACK_TO_HEAD_PAGE_{language_code}"],
            ],
        ]
    )


async def statistic_keyboard(company_id, language_code):
    """
    Клавиатура в разделе статистики.
    Записываем в колбэк кнопок по выбору периода company_id
    """
    match language_code:
        case "rus":
            stat_periods = STAT_PERIODS_RUS
        case "eng":
            stat_periods = STAT_PERIODS_ENG
        case _:
            stat_periods = STAT_PERIODS_RUS

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['today']}",
                    callback_data=f"stat_period {company_id} today",
                ),
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['yesterday']}",
                    callback_data=f"stat_period {company_id} yesterday",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['last_monday']}",
                    callback_data=f"stat_period {company_id} last_monday",
                ),
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['7_days_ago']}",
                    callback_data=f"stat_period {company_id} 7_days_ago",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['first_day_of_this_month']}",
                    callback_data=f"stat_period {company_id} first_day_of_this_month",
                ),
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['previous_month']}",
                    callback_data=f"stat_period {company_id} previous_month",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['1_month_ago']}",
                    callback_data=f"stat_period {company_id} 1_month_ago",
                ),
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['first_day_of_this_year']}",
                    callback_data=f"stat_period {company_id} first_day_of_this_year",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['1_year_ago']}",
                    callback_data=f"stat_period {company_id} 1_year_ago",
                ),
                InlineKeyboardButton(
                    text=f"🔹{stat_periods['all_time']}",
                    callback_data=f"stat_period {company_id} all_time",
                ),
            ],
            [
                BUTTONS_DCT[f"CHECK_MORE_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"BACK_TO_HEAD_PAGE_{language_code}"],
            ],
        ]
    )


async def choose_numb_of_redirect_kbrd(
    language_code, redirect_numb="1", replenish_balance=False
):
    """
    Клавиатурка для выбора кол-ва редиректов
    """
    inline_kbrd_lst = [
        [
            BUTTONS_DCT["MINUS_REDIRECT"],
            InlineKeyboardButton(  # Кол-во редиректов, как кнопка
                text=redirect_numb,
                callback_data="plug",
            ),
            BUTTONS_DCT["PLUS_REDIRECT"],
        ],
        [
            BUTTONS_DCT["MINUS_10_REDIRECT"],
            BUTTONS_DCT["PLUS_10_REDIRECT"],
        ],
        [
            BUTTONS_DCT["MINUS_100_REDIRECT"],
            BUTTONS_DCT["PLUS_100_REDIRECT"],
        ],
        [
            BUTTONS_DCT["MINUS_1000_REDIRECT"],
            BUTTONS_DCT["PLUS_1000_REDIRECT"],
        ],
        [
            BUTTONS_DCT[f"CANCEL_AND_CLEAR_STATE_{language_code}"],
            BUTTONS_DCT[f"TO_LINK_SHORTENING_{language_code}"],
        ],
    ]
    if replenish_balance:
        inline_kbrd_lst.append(
            [
                BUTTONS_DCT[f"REPLENISH_BALANCE_{language_code}"],
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_kbrd_lst)


async def form_webapp_kbrd(form_link, btn_text):
    """
    Формирование клавиатуры для перехода к форме, которая реализована через веб-приложение.
    :param form_link: ссылка на веб-форму.
    """
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=btn_text, web_app=WebAppInfo(url=form_link))],
        ]
    )


async def card_payment_processing_kbrd(tlg_id):
    """
    Клавиатура для обработки платежей на карту.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="✅Подтвердить платёж",
                    callback_data=f"confirm_card_payment {tlg_id}",
                ),
                InlineKeyboardButton(
                    text="❌Отклонить платёж",
                    callback_data=f"decline_card_payment {tlg_id}",
                ),
            ],
        ]
    )


async def form_head_page_keyboard(language_code, tlg_id):
    """
    Формируем клавиатуру для главной странице.
    (Эта функция нужна, чтобы подтягивать из БД ссылку на канал с отзывами)
    """
    # Собираем кнопку "ОТЗЫВЫ" (устанавливаем ей актуальную ссылку)
    feed_back_button = BUTTONS_DCT[f"FEEDBACK_CHAT_{language_code}"]
    feed_back_button.url = await make_feedback_link()

    return InlineKeyboardMarkup(
        [
            [await my_domain_button(lang_code=language_code, tlg_id=tlg_id)],
            [
                BUTTONS_DCT[f"CREATE_LINK_{language_code}"],
                BUTTONS_DCT[f"GET_STATISTIC_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"FAQ_{language_code}"],
                BUTTONS_DCT[f"SUPPORT_{language_code}"],
            ],
            [
                BUTTONS_DCT[f"MY_BALANCE_{language_code}"],
                BUTTONS_DCT[f"REPLENISH_BALANCE_{language_code}"],
            ],
            [
                feed_back_button,
            ],
            [
                BUTTONS_DCT[f"CHANGE_LANG_{language_code}"],
            ],
        ]
    )


async def languages_keyboard(language_code):
    """
    Клавиатура для выбора языка интерфейса.
    """
    # Получаем список доступных языков интерфейса
    languages = await get_interface_language()

    # Формируем общий список, который в последствии станет клавиатурой
    keyboard_lst = []
    for i_lang in languages:
        keyboard_lst.append(
            [
                InlineKeyboardButton(
                    text=i_lang.get("language"),
                    callback_data=f"set_lang {i_lang.get('language_code')}",
                )
            ]
        )
    keyboard_lst.append([BUTTONS_DCT[f"BACK_TO_HEAD_PAGE_{language_code}"]])

    # Скармливаем список классу, который сделает из него клавиатуру
    return InlineKeyboardMarkup(keyboard_lst)
