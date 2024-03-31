from pyrogram import Client
from pyrogram.types import CallbackQuery

from filters.simple_filters import filter_for_faq_handler, filter_for_support_handler, filter_for_my_balance_handler, \
    get_transactions_filter, change_language_filter, set_new_language_filter
from keyboards.bot_keyboards import back_to_headpage_keyboard, my_balance_part_keyboard, after_get_transaction_keyboard, \
    languages_keyboard
from resources.messages import MESSAGES, ERROR_MESSAGES
from secondary_functions.req_to_bot_api import get_user_data, get_settings, get_transactions, get_interface_language, \
    set_interface_language


@Client.on_callback_query(filter_for_faq_handler)
async def faq_handler(client, update: CallbackQuery):
    """
    Хэндлер для раздела FAQ.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    await update.edit_message_text(
        text=MESSAGES[f"faq_instruction_{language_code}"],
        reply_markup=await back_to_headpage_keyboard(language_code)
    )


@Client.on_callback_query(filter_for_support_handler)
async def support_handler(client, update: CallbackQuery):
    """
    Хэндлер для раздела Поддержка.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    support_username = await get_settings(key='support_username')
    await update.edit_message_text(
        text=MESSAGES[f"support_message_{language_code}"].format(support_username=support_username[0].get("value")),
        reply_markup=await back_to_headpage_keyboard(language_code),
    )


@Client.on_callback_query(filter_for_my_balance_handler)
async def my_balance_handler(client, update: CallbackQuery):
    """
    Хэндлер для раздела Мой баланс.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    response = await get_user_data(tlg_id=update.from_user.id)  # Запрос к БД для получения баланса
    await update.edit_message_text(
        text=MESSAGES[f"your_balance_{language_code}"].format(balance=response.get("balance")),
        reply_markup=await my_balance_part_keyboard(language_code)
    )


@Client.on_callback_query(get_transactions_filter)
async def get_transaction_handler(client, update: CallbackQuery):
    """
    Хэндлер для получения транзакций.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    trans_response = await get_transactions(tlg_id=update.from_user.id)  # Запрос для формирования файла транзакций
    balance_response = await get_user_data(tlg_id=update.from_user.id)  # Запрос к БД для получения баланса
    if trans_response and balance_response:
        await update.edit_message_text(
            text=MESSAGES[f"get_transaction_{language_code}"].format(balance={balance_response.get("balance")}),
            reply_markup=await after_get_transaction_keyboard(language_code)
        )


@Client.on_callback_query(change_language_filter)
async def change_language_handler(_, update: CallbackQuery):
    """
    Хэндлер для изменения языка.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Отправляем сообщение
    await update.edit_message_text(
        text=MESSAGES[f"choose_language_{language_code}"],
        reply_markup=await languages_keyboard(language_code)
    )


@Client.on_callback_query(set_new_language_filter)
async def set_new_language_handler(_, update: CallbackQuery):
    """
    Хэндлер для установки нового языка интерфейса.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    old_language_code = interface_lang_response["language_code"]

    # Устанавливаем новый язык
    new_lang_code = update.data.split()[1]
    set_new_lang_resp = await set_interface_language(tlg_id=update.from_user.id, language_code=new_lang_code)
    if not set_new_lang_resp:
        return await update.edit_message_text(
            text=ERROR_MESSAGES[f"base_error_{new_lang_code}"],
            reply_markup=await languages_keyboard(old_language_code)
        )

    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text=ERROR_MESSAGES["translation_error"])
    language_code = interface_lang_response["language_code"]

    # Отправляем сообщение
    await update.edit_message_text(
        text=MESSAGES[f"choose_language_{language_code}"],
        reply_markup=await languages_keyboard(language_code)
    )
