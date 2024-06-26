from pyrogram import Client
from pyrogram.types import CallbackQuery, Message

from filters.get_statistic_filters import filter_ask_user_for_comp_id, filter_get_statistic_from_keitaro, \
    get_statistic_from_period_filter
from keyboards.bot_keyboards import statistic_keyboard, cancel_and_clear_state_keyboard
from resources.messages import MESSAGES, STAT_PERIODS_RUS, STAT_PERIODS_ENG
from secondary_functions.req_to_bot_api import get_link_owner, get_interface_language
from secondary_functions.requests_to_other_services import post_req_to_keitaro_for_get_stat_by_comp_id
from settings.config import STATES_STORAGE_DCT


@Client.on_callback_query(filter_ask_user_for_comp_id)
async def ask_user_for_company_id_handler(client, update: CallbackQuery):
    """
    Запрашиваем у юзера ID компании, для получения статистики.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    await update.edit_message_text(
        text=MESSAGES[f"send_link_id_{language_code}"],
        reply_markup=await cancel_and_clear_state_keyboard(language_code=language_code)
    )
    STATES_STORAGE_DCT[update.from_user.id] = 'send_company_id_for_get_statistic'


@Client.on_message(filter_get_statistic_from_keitaro)
async def get_statistic_from_keitaro(client, update: Message):
    """
    Хэндлер для получения ID компании и сбора статистики из KEITARO.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.reply_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                            " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Проверка, что прислан верный ID компании
    if not update.text.isdigit():
        await update.reply_text(
            text=f'❗️<b>Некорректный ID</b>\n🔢ID должен состоять из цифр.\n\n'
                 f'📄Пожалуйста, <b>проверьте файл с редирект-ссылками</b>. '
                 f'В нём, <b>ниже исходной ссылки</b> указан <b>ID для сбора статистики</b>.',
            reply_markup=await cancel_and_clear_state_keyboard(language_code=language_code)
        )
        return

    # Проверяем, что статистику запрашивает владелец ссылки
    check_owner = await get_link_owner(company_id=int(update.text))
    if not check_owner or int(check_owner.get('link_owner')) != int(update.from_user.id):
        await update.reply_text(
            text=f'🤷‍♂️Не найдена статистика по ссылке с ID {update.text}.\n'
                 f'Возможно вы ввели некорректный ID или ссылка Вам не принадлежит.\n\n'
                 f'🆔<b>Пожалуйста, введите корректный ID ссылки.</b>',
            reply_markup=await cancel_and_clear_state_keyboard(language_code=language_code)
        )
        return

    # Очищаем стэйт
    STATES_STORAGE_DCT.pop(update.from_user.id)
    info_msg = await update.reply_text(
        text=MESSAGES[f"request_stats_{language_code}"]
    )

    # Выполняем запрос к кейтаро
    response = await post_req_to_keitaro_for_get_stat_by_comp_id(company_id=int(update.text))

    company_id = int(update.text)
    all_clicks = MESSAGES[f"data_not_received_or_zero_{language_code}"]
    unique_clicks = MESSAGES[f"data_not_received_or_zero_{language_code}"]
    bots = MESSAGES[f"data_not_received_or_zero_{language_code}"]

    if response:
        all_clicks = response.get("summary").get("clicks")
        unique_clicks = response.get("summary").get("stream_unique_clicks")
        bots = response.get("summary").get("bots")

    text_for_message = MESSAGES[f"statistic_info_today_{language_code}"].format(
        company_id=company_id,
        all_clicks=all_clicks,
        unique_clicks=unique_clicks if unique_clicks else "🤷‍♂️",
        bots=bots if bots else "🤷‍♂️",
    )

    # Даём ответ со статистикой
    await info_msg.edit_text(
        text=text_for_message,
        reply_markup=await statistic_keyboard(company_id=update.text, language_code=language_code)
    )


@Client.on_callback_query(get_statistic_from_period_filter)
async def get_statistic_from_period(client, update):
    """
    Получение статистики от кейтаро за конкретный период по company_id
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.reply_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                            " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    info_msg = await update.edit_message_text(
        text=MESSAGES[f"request_stats_{language_code}"]
    )

    # Выполняем запрос к кейтаро
    response = await post_req_to_keitaro_for_get_stat_by_comp_id(
        company_id=update.data.split()[1],
        period=update.data.split()[2],
    )

    company_id = int(update.data.split()[1])
    all_clicks = MESSAGES[f"data_not_received_or_zero_{language_code}"]
    unique_clicks = MESSAGES[f"data_not_received_or_zero_{language_code}"]
    bots = MESSAGES[f"data_not_received_or_zero_{language_code}"]

    if response:
        all_clicks = response.get("summary").get("clicks")
        unique_clicks = response.get("summary").get("stream_unique_clicks")
        bots = response.get("summary").get("bots")

    match language_code:
        case "rus":
            stat_periods = STAT_PERIODS_RUS
        case "eng":
            stat_periods = STAT_PERIODS_ENG
        case _:
            stat_periods = STAT_PERIODS_RUS

    text_for_message = MESSAGES[f"statistic_info_{language_code}"].format(
        stat_periods=stat_periods.get(update.data.split()[2]),
        company_id=company_id,
        all_clicks=all_clicks,
        unique_clicks=unique_clicks if unique_clicks else "🤷‍♂️",
        bots=bots if bots else "🤷‍♂️",
    )

    # Даём ответ со статистикой
    await info_msg.edit_text(
        text=text_for_message,
        reply_markup=await statistic_keyboard(update.data.split()[1], language_code)
    )
