from pyrogram import Client
from pyrogram.types import CallbackQuery

from filters.simple_filters import filter_for_faq_handler, filter_for_support_handler, filter_for_my_balance_handler
from keyboards.bot_keyboards import BACK_TO_HEAD_PAGE_KBRD, MY_BALANCE_PART_KBRD
from secondary_functions.req_to_bot_api import get_user_data, get_settings


@Client.on_callback_query(filter_for_faq_handler)
async def faq_handler(client, update: CallbackQuery):
    """
    Хэндлер для раздела FAQ.
    """
    await update.edit_message_text(
        text=f'‼️ Обязательно к прочтению.\n\n'
             f'1️⃣ 1 редирект ссылка выдерживает до 3000 сообщение (исключения бывают ввиде 5000-6000 сообщений, '
             f'но это большой риск, что из-за ссылки на таком объёме Вы можете убить аккаунты '
             f'(может быть много жалоб на 1 ссылку)\n\n'
             f'2️⃣ Оптимальный объём на 1 редирект ссылку (по личному опыту) составляет 1500-2000 сообщений \n\n'
             f'3️⃣ Если на редирект ссылку начинают активно кидать жалобы во врема рассылки, она может уйти в спамблок '
             f'(как это проверить? - аккаунты сразу ловят спамблок или бан при попытке разослать эту ссылку). '
             f'Это может произойти раньше чем Вы отправите, например 2000 сообщений. '
             f'В этом случае стоит заменить ссылку (сделать новую) или использовать другую '
             f'(если Вы заказали несколько ссылок)\n\n'
             f'4️⃣На 1 источник Вы можете сделать бесконечное количество редирект '
             f'ссылок и каждая ссылку будет уникальна для Телеграм.\n\n'
             f'5️⃣ Перед тем как заказать несколько ссылок, попробуйте сначала заказать 1 '
             f'(во избежание недопониманий)\n\n'
             f'6️⃣ Сокращатели ссылок тоже важная вещь - Вы можете попробовать разные сокращатели и выбрать под себя '
             f'оптимальный. Разницы особо нет, но бывает такое что какой то сокращатель не нравится телеграму в этот '
             f'самый день и в определенном посте (например, текст + ссылка + картинка), '
             f'в этом случае стоит сменить сокращатель и попробовать другой\n\n'
             f'7️⃣ Прежде чем заказывать большой объём (уже написано в п.5, но я повторюсь) '
             f'закажите 1 ссылку и попробуйте тестово отправить её\n\n'
             f'8️⃣ Если Вы передумали делать редирект, но сумма на Вашем кабинете имеется - '
             f'возврат средств не предусмотрен в финансовом эквиваленте, '
             f'Вы можете потратить их в будущем редирект ссылки\n\n'
             f'9️⃣Если Вы сделали редирект ссылку - но она не рассылается, то в течении 5 часов (после создания) '
             f'Вы можете написать в нашу поддержку для замены той самой ссылки (при условии что вы не слали '
             f'её более чем 10+ сообщений. Мы проверим по системе и если рассылки как таковой не было с этой '
             f'ссылки - мы заменим Вам её или вернем сумму на баланс',
        reply_markup=BACK_TO_HEAD_PAGE_KBRD
    )


@Client.on_callback_query(filter_for_support_handler)
async def support_handler(client, update: CallbackQuery):
    """
    Хэндлер для раздела Поддержка.
    """
    response = await get_settings(key='support_username')
    await update.edit_message_text(
        text=f'🆘 Если у Вас имеется вопрос или Вам нужна помощь, напишите нам: {response[0].get("value")}',
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
