from pyrogram import Client
from pyrogram.types import CallbackQuery, Message

from filters.get_statistic_filters import filter_ask_user_for_comp_id, filter_get_statistic_from_keitaro
from keyboards.bot_keyboards import CANCEL_AND_CLEAR_STATE_KBRD, \
    BACK_TO_HEAD_PAGE_FROM_STATISTIC_KBRD
from secondary_functions.requests_to_other_services import post_req_to_keitaro_for_get_stat_by_comp_id
from settings.config import STATES_STORAGE_DCT


@Client.on_callback_query(filter_ask_user_for_comp_id)
async def ask_user_for_company_id_handler(client, update: CallbackQuery):
    """
    Запрашиваем у юзера ID компании, для получения статистики.
    """
    await update.edit_message_text(
        text='📊Пришлите <b>ID ссылки</b> для проверки статистики.',
        reply_markup=CANCEL_AND_CLEAR_STATE_KBRD
    )
    STATES_STORAGE_DCT[update.from_user.id] = 'send_company_id_for_get_statistic'


@Client.on_message(filter_get_statistic_from_keitaro)
async def get_statistic_from_keitaro(client, update: Message):
    """
    Хэндлер для получения ID компании и сбора статистики из KEITARO.
    """
    if not update.text.isdigit():   # Прислан неверный ID компании
        await update.reply_text(
            text=f'❗️<b>Некорректный ID</b>\n🔢ID должен состоять из цифр.\n\n'
                 f'📄Пожалуйста, <b>проверьте файл с редирект-ссылками</b>. '
                 f'В нём, <b>ниже исходной ссылки</b> указан <b>ID для сбора статистики</b>.',
            reply_markup=CANCEL_AND_CLEAR_STATE_KBRD
        )
        return

    STATES_STORAGE_DCT.pop(update.from_user.id)     # Очищаем стэйт
    info_msg = await update.reply_text(
        text=f'📡Запрашиваю данные о статистике статистики...'
    )
    # Выполняем запрос к кейтаро
    response = await post_req_to_keitaro_for_get_stat_by_comp_id(company_id=int(update.text))

    response_comp_id = '<i>Данные не получены</i>'
    original_link = '<i>Данные не получены</i>'
    all_clicks = '<i>Данные не получены или 0</i>'
    unique_clicks = '<i>Данные не получены или 0</i>'

    if response:
        for i_elem in response:     # В ответе будет список из словарей, итерируемся по ним

            # Отлавливаем тот словарь, у которого в body лежит rows = [поток для ботов, осн. поток]
            if i_elem.get('body') and i_elem.get('body').get('rows'):
                for j_elem in i_elem.get('body').get('rows'):
                    if j_elem.get('stream') == 'Flow 2':    # Отлавливаем основной поток и забираем клики
                        all_clicks = j_elem.get('clicks')
                        unique_clicks = j_elem.get('stream_unique_clicks')

            # Отлавливаем тот словарь c body, в котором ещё лежит ID компании и её название
            if i_elem.get('body') and i_elem.get('body').get('id') and i_elem.get('body').get('name'):
                response_comp_id = i_elem.get('body').get('id')
                # В "name" лежит "REDIRECT_BOT | USER_TG_ID: {tlg_id} | {link}" - форматируем эту хрень
                original_link = i_elem.get('body').get('name').split('|')[-1].replace(' ', '')

    text_for_message = f'🔗<b>Ссылка:</b> {response_comp_id}\n' \
                       f'🆔<b>ID ссылки:</b>  {original_link}\n' \
                       f'🚶<b>Всего переходов:</b> {all_clicks}\n' \
                       f'🚶‍♂️<b>Уникальных переходов:</b> {unique_clicks}\n'

    # Даём ответ со статистикой
    await info_msg.edit_text(
        text=text_for_message,
        reply_markup=BACK_TO_HEAD_PAGE_FROM_STATISTIC_KBRD
    )
