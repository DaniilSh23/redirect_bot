import datetime
import random

from pyrogram import Client, filters

from filters.main_filters import filter_throttling_middleware
from keyboards.bot_keyboards import ADMIN_KBRD, HEAD_PAGE_KBRD
from secondary_functions.req_to_bot_api import post_user_data, get_bot_admins
from settings.config import BLACK_LIST


@Client.on_message(filter_throttling_middleware)
async def throttling_middleware_message(client, update):
    """
    Хэндлер для throttling middleware.
    Если юзера нет в чёрном списке, то добавляем и отправляем ему сообщение, когда истекает пауза.
    Если юзер уже есть в черном списке, то ничего не отвечаем.
    """
    print('попали в мидл message')
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
    print('попали в мидл callback')
    if update.from_user.id not in BLACK_LIST.keys():  # Если юзера нет в чёрном списке
        # Ставим ему время, когда истекает блокировка
        block_time = random.randint(10, 18)
        BLACK_LIST[update.from_user.id] = datetime.datetime.now() + datetime.timedelta(seconds=block_time)
        await client.send_message(chat_id=update.from_user.id,
                                  text=f'Слишком много запросов! Пожалуйста, подождите {block_time} сек.')


@Client.on_message(filters.command(['start']))
async def start_handler(client, message):
    """START. Приветственное сообщение + главное меню"""

    # Записываем инфу о пользователе в БД
    user_data = {
        "tlg_id": message.from_user.id,
        "is_verified": message.from_user.is_verified,
        "is_scam": message.from_user.is_scam,
        "is_fake": message.from_user.is_fake,
        "is_premium": message.from_user.is_premium,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username,
        "language_code": message.from_user.language_code,
    }
    await post_user_data(user_data=user_data)

    # Получаем список админов бота
    bot_admins = await get_bot_admins()
    if bot_admins:
        for i_bot_admin in bot_admins:
            if i_bot_admin.get('value') == str(message.from_user.id):
                # Формируем обращение к админу
                for i_name in [message.from_user.first_name, message.from_user.username]:
                    if i_name:
                        admin_name = i_name
                        break
                else:
                    admin_name = f'пользователь с ID {message.from_user.id}'
                await message.reply_text(
                    text=f'🎉🎉🎉\n\n🙇‍♂️Рад приветствовать Вас, 👑<b>{admin_name}</b> !\n\n'
                         f'Для Вас доступна <b>админ-панель</b> по кнопке ниже🖱',
                    reply_markup=ADMIN_KBRD,
                )
                break

    # Даём ответ пользователю
    await message.reply_text(
        text='🤝Здравствуйте.\n🎁Этот бот поможет <b>обернуть Ваши ссылки</b> для редиректа.\n\n'
             'Нажимайте на кнопку <b>🔗СОЗДАТЬ ССЫЛКУ</b> и приступим.',
        reply_markup=HEAD_PAGE_KBRD
    )
