from pyrogram import Client
from pyrogram.types import CallbackQuery

from filters.simple_filters import filter_for_faq_handler, filter_for_support_handler, filter_for_my_balance_handler
from keyboards.bot_keyboards import BACK_TO_HEAD_PAGE_KBRD, MY_BALANCE_PART_KBRD
from secondary_functions.req_to_bot_api import get_user_data


@Client.on_callback_query(filter_for_faq_handler)
async def faq_handler(client, update: CallbackQuery):
    """
    Хэндлер для раздела FAQ.
    """
    await update.edit_message_text(
        text=f'FAQ - это ведь читается как Fuck You...Или я что-то путаю? Короче тут какой-то текст',
        reply_markup=BACK_TO_HEAD_PAGE_KBRD
    )


@Client.on_callback_query(filter_for_support_handler)
async def support_handler(client, update: CallbackQuery):
    """
    Хэндлер для раздела Поддержка.
    """
    await update.edit_message_text(
        text=f'На Netflix есть такой сериал "Лучше звоните Солу". Короче, тут та же система.',
        reply_markup=BACK_TO_HEAD_PAGE_KBRD
    )


@Client.on_callback_query(filter_for_my_balance_handler)
async def my_balance_handler(client, update: CallbackQuery):
    """
    Хэндлера для раздела Мой баланс.
    """
    response = await get_user_data(tlg_id=update.from_user.id)  # Запрос к БД для получения баланса
    await update.edit_message_text(
        text=f'💰<b>Ваш баланс:</b> {response.get("balance")} руб.',
        reply_markup=MY_BALANCE_PART_KBRD
    )
