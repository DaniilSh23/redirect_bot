import datetime
import random

from loguru import logger
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message


from filters.main_filters import filter_throttling_middleware, filter_for_cancel_and_clear_state
from keyboards.bot_keyboards import ADMIN_KBRD, HEAD_PAGE_KBRD
from secondary_functions.req_to_bot_api import post_user_data, get_settings
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
        block_time = random.randint(10, 18)
        BLACK_LIST[update.from_user.id] = datetime.datetime.now() + datetime.timedelta(seconds=block_time)
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
        block_time = random.randint(10, 18)
        BLACK_LIST[update.from_user.id] = datetime.datetime.now() + datetime.timedelta(seconds=block_time)
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
                         f'Для Вас доступна <b>админ-панель</b> по кнопке ниже🖱',
                    reply_markup=ADMIN_KBRD,
                )
                break

    # Даём ответ пользователю
    await update.reply_text(
        text='🤝Здравствуйте.\n🎁Этот бот поможет <b>обернуть Ваши ссылки</b> для редиректа.\n\n'
             'Нажимайте на кнопку <b>🔗СОЗДАТЬ ССЫЛКУ</b> и приступим.',
        reply_markup=HEAD_PAGE_KBRD
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

    await update.answer(
        text=f'Нажата кнопка ❌Отменить.\nВозврат к главному меню.',
        show_alert=True
    )
    await update.edit_message_text(
        text='<b>Главное меню</b>',
        reply_markup=HEAD_PAGE_KBRD
    )
