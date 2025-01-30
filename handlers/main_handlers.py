import random
import time

from loguru import logger
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from filters.main_filters import filter_throttling_middleware, filter_for_cancel_and_clear_state, \
    filter_back_to_head_page
from keyboards.bot_keyboards import ADMIN_KBRD, form_head_page_keyboard
from resources.messages import MESSAGES, ALERT_MESSAGES
from secondary_functions.req_to_bot_api import post_user_data, get_settings, get_interface_language
from settings.config import BLACK_LIST, STATES_STORAGE_DCT


@Client.on_message(filter_throttling_middleware)
async def throttling_middleware_message(client, update):
    """
    Хэндлер для throttling middleware.
    Если юзера нет в чёрном списке, то добавляем и отправляем ему сообщение, когда истекает пауза.
    Если юзер уже есть в черном списке, то ничего не отвечаем.
    """
    logger.info(f'Сработал THROTTLING MIDDLEWARE на юзера {update.from_user.id}. Message')
    if update.from_user.id not in BLACK_LIST.keys():  # Если юзера нет в чёрном списке
        # Ставим ему время, когда истекает блокировка
        block_time = random.randint(3, 8)
        BLACK_LIST[update.from_user.id] = time.time() + block_time
        await client.send_message(chat_id=update.from_user.id,
                                  text=f'Слишком много запросов! Пожалуйста, подождите {block_time} сек.')


@Client.on_callback_query(filter_throttling_middleware)
async def throttling_middleware_callback(client, update):
    """
    Хэндлер для throttling middleware.
    Если юзера нет в чёрном списке, то добавляем и отправляем ему сообщение, когда истекает пауза.
    Если юзер уже есть в черном списке, то ничего не отвечаем.
    """
    logger.info(f'Сработал THROTTLING MIDDLEWARE на юзера {update.from_user.id}. Callback')
    if update.from_user.id not in BLACK_LIST.keys():  # Если юзера нет в чёрном списке
        # Ставим ему время, когда истекает блокировка
        block_time = random.randint(3, 8)
        BLACK_LIST[update.from_user.id] = time.time() + block_time
        await client.send_message(chat_id=update.from_user.id,
                                  text=f'Слишком много запросов! Пожалуйста, подождите {block_time} сек.')


@Client.on_message(filters.command(['start']))
async def start_handler(client, update: Message):
    """START. Приветственное сообщение + главное меню"""

    # Очищаем состояние, если оно было
    if STATES_STORAGE_DCT.get(update.from_user.id):
        STATES_STORAGE_DCT.pop(update.from_user.id)

    # Записываем инфу о пользователе в БД
    user_data = {
        "tlg_id": update.from_user.id,
        "is_verified": update.from_user.is_verified,
        "is_scam": update.from_user.is_scam,
        "is_fake": update.from_user.is_fake,
        "is_premium": update.from_user.is_premium,
        "first_name": update.from_user.first_name,
        "last_name": update.from_user.last_name,
        "username": update.from_user.username,
        "language_code": update.from_user.language_code,
    }
    await post_user_data(user_data=user_data)

    # Получаем список админов бота
    bot_admins = await get_settings(key='redirect_bot_admin')
    if bot_admins:
        for i_bot_admin in bot_admins:
            if i_bot_admin.get('value') == str(update.from_user.id):
                # Формируем обращение к админу
                for i_name in [update.from_user.first_name, update.from_user.username]:
                    if i_name:
                        admin_name = i_name
                        break
                else:
                    admin_name = f'пользователь с ID {update.from_user.id}'
                await update.reply_text(
                    text=f'🎉🎉🎉\n\n🙇‍♂️Рад приветствовать Вас, 👑<b>{admin_name}</b> !\n\n'
                         f'Для Вас доступна <b>админ-панель</b> по кнопке ниже🖱\n\n'
                         f'<b>Данные для входа:</b>\n'
                         f'Логин: <code>admin</code> | Пароль: <code>Red!rectB0t@dmin123</code>',
                    reply_markup=ADMIN_KBRD,
                )
                break

    # Запрашиваем тариф бота на редиректы
    tariff_response = await get_settings(key='tariff')

    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.reply_text(text="🛠 Sorry...The bot has problems with translation. Please try again later, "
                                            "we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Даём ответ пользователю
    msg_text = MESSAGES[f"START_HANDLER_MESSAGE_{language_code}"].format(
        tariff_response=tariff_response[0].get("value"))
    await update.reply_text(
        text=msg_text,
        reply_markup=await form_head_page_keyboard(language_code=language_code, tlg_id=update.from_user.id),
    )


@Client.on_callback_query(filter_for_cancel_and_clear_state)
async def cancel_and_clear_state_handler(client, update: CallbackQuery):
    """
    Хэндлер для нажатия кнопку 'Отменить' (например, при запросе ботом файла со ссылками).
    Также очищает состояние для данного юзера
    """

    # Очищаем состояние, если оно было
    if STATES_STORAGE_DCT.get(update.from_user.id):
        STATES_STORAGE_DCT.pop(update.from_user.id)

    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # TODO: нужно допилить перевод текстов
    await update.answer(
        text=ALERT_MESSAGES[f"cancel_and_return_{language_code}"],
        show_alert=True
    )
    await update.edit_message_text(
        text=MESSAGES[f"main_menu_{language_code}"],
        reply_markup=await form_head_page_keyboard(language_code=language_code, tlg_id=update.from_user.id),
    )


@Client.on_callback_query(filter_back_to_head_page)
async def back_to_head_page_handler(client, update: CallbackQuery):
    """
    Хэндлер для обработки нажатия кнопки На главную.
    """
    # Очищаем состояние, если оно было
    if STATES_STORAGE_DCT.get(update.from_user.id):
        STATES_STORAGE_DCT.pop(update.from_user.id)

    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    await update.answer(
        text=ALERT_MESSAGES[f"return_to_main_{language_code}"],
        show_alert=True
    )
    await update.edit_message_text(
        text='<b>Главное меню</b>',
        reply_markup=await form_head_page_keyboard(language_code=language_code, tlg_id=update.from_user.id),
    )


@Client.on_message(filters.command(['menu']))
async def send_menu(client, update: Message):
    """
    Хэндлер для команды /menu. Присылает меню.
    """
    # Очищаем состояние, если оно было
    if STATES_STORAGE_DCT.get(update.from_user.id):
        STATES_STORAGE_DCT.pop(update.from_user.id)

    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.reply_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                            " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    await update.reply_text(
        text='<b>Главное меню</b>',
        reply_markup=await form_head_page_keyboard(language_code=language_code, tlg_id=update.from_user.id),
    )
