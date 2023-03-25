import datetime
import math
import random
from urllib.parse import urlparse

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from filters.create_link_filters import filter_for_create_link_btn_handler, filter_for_get_doc_with_links_handler, \
    filter_for_waiting_file_processing_handler, filter_minus_redirect_handler, filter_plus_redirect_handler, \
    filter_link_shortening_handler
from keyboards.bot_keyboards import CANCEL_AND_CLEAR_STATE_KBRD, choose_numb_of_redirect_kbrd
from secondary_functions.req_to_bot_api import update_or_create_link, get_settings, get_user_data
from settings.config import STATES_STORAGE_DCT, REDIRECT_NUMBERS_DCT


@Client.on_callback_query(filter_for_create_link_btn_handler)
async def create_link_btn_handler(client, update):
    """
    Хэндлер на нажатие кнопки "СОЗДАТЬ ССЫЛКУ".
    Устанавливаем состояние, в котором ожидаем получить файл со ссылками,
    запрашиваем сам файл и даём кнопку "Отменить".
    """
    STATES_STORAGE_DCT[update.from_user.id] = 'upload_file_with_links'
    await update.answer(
        text=f"📄Пришлите файл со ссылками:\n\n🔹 каждая ссылка с новой строки;\n"
             f"🔹 все ссылки должны начинаться с http:// https:// ftp:// и т.п.",
        show_alert=True
    )
    await update.edit_message_text(
        text=f"📄Пожалуйста, пришлите мне файл со ссылками:\n\n"
             f"🔹 каждая ссылка с новой строки;\n"
             f"🔹 ссылки должны начинаться с <code>http://</code> <code>https://</code> <code>ftp://</code> и т.п.;\n"
             f"🔹 <b>невалидные ссылки не будут прочитаны.</b>",
        reply_markup=CANCEL_AND_CLEAR_STATE_KBRD
    )


@Client.on_message(filters.document & filter_for_get_doc_with_links_handler)
async def get_doc_with_links_handler(client, update: Message):
    """
    Хэндлер для получения документа (txt файл) со ссылками. Каждая ссылка с новой строки.
    Отвечаем, что идёт обработка документа и это может занять время.
    Скачиваем документ из телеги, читаем его.
    Итерируемся по строкам, проверяем ссылки на валидность, записываем в БД.
    """
    await update.reply_text(
        text=f'🖍Обрабатываю Ваш документ.\n\n'
             f'⏳Это может занять некоторое время, если в документе много ссылок.\n'
             f'<b>Пожалуйста, ожидайте.</b>'
    )
    # [state name, всего строк в файле, обработано строк]
    STATES_STORAGE_DCT[update.from_user.id] = ['waiting_file_processing', 0, 0]

    # Обработка файла
    tlg_file = await update.download(
        file_name=f'files/link_files/{update.from_user.id}/links.txt',
        in_memory=False
    )
    with open(file=tlg_file, mode='r', encoding='utf-8') as links_file:
        all_lines_count = 0
        valid_links_count = 0
        for i_line in links_file:
            all_lines_count += 1
            i_line = i_line.replace(' ', '')

            # проверка, что строка в файле - это ссылка
            is_link = False
            parsed_lnk = urlparse(i_line)
            if parsed_lnk.scheme and parsed_lnk.netloc and '.' in parsed_lnk.netloc:
                # Проверяем, чтобы в адресе не было 2х точек подряд
                for i_indx, i_elem in enumerate(parsed_lnk.netloc):
                    if i_indx == len(parsed_lnk.netloc) - 1:
                        is_link = True
                        break
                    if i_elem == '.' and parsed_lnk.netloc[i_indx + 1] == '.':
                        break
            if is_link:
                # Записываем ссылку в БД через запрос API
                write_link_rslt = await update_or_create_link(data={
                    'tlg_id': update.from_user.id,
                    'link': i_line
                })
                if write_link_rslt:
                    valid_links_count += 1
            # Записываем рядом со стэйтом юзера, чтобы давать отчёт, если ему там не сидится спокойно
            STATES_STORAGE_DCT[update.from_user.id] = ['waiting_file_processing', all_lines_count, valid_links_count]

    # Даём ответ по окончании обработки файла
    tariff = await get_settings(key='tariff')  # Получаем цену тарифа в БД
    user_data = await get_user_data(tlg_id=update.from_user.id)  # Получаем данные об юзере (нужен баланс)
    REDIRECT_NUMBERS_DCT[update.from_user.id] = [1, user_data.get("balance"), tariff[0].get("value")]
    await update.reply_text(
        text=f'✅<b>Обработка файла завершена.</b>\n\n'
             f"📖<b>Прочитано: {STATES_STORAGE_DCT[update.from_user.id][1]} строк файла</b>\n"
             f"💾<b>Записано: {STATES_STORAGE_DCT[update.from_user.id][2]} ссылок</b>\n\n"
             f'💲Цена редиректа: {tariff[0].get("value")} руб.\n'
             f'💰Баланс: {user_data.get("balance")} руб.\n'
             f'🧾Общая стоимость: {1 * float(tariff[0].get("value"))} руб.\n\n'
             f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?',
        reply_markup=await choose_numb_of_redirect_kbrd()
    )


@Client.on_callback_query(filter_minus_redirect_handler)
async def minus_redirect_handler(client, update: CallbackQuery):
    """
    Хэндлер для кнопок 'минус редирект(ы)'
    """
    REDIRECT_NUMBERS_DCT[update.from_user.id][0] -= float(update.data.split()[1])

    if REDIRECT_NUMBERS_DCT[update.from_user.id][0] < 1:  # Если выбрано менее 1 редиректа
        REDIRECT_NUMBERS_DCT[update.from_user.id][0] = 1
        text_for_message = f'❗️<b>Редиректов не может быть меньше 1</b>\n' \
                           f'☑️<b>Выбрано {REDIRECT_NUMBERS_DCT[update.from_user.id][0]} ' \
                           f'редиректов для каждой ссылки</b>\n\n' \
                           f"📖<b>Прочитано: {STATES_STORAGE_DCT[update.from_user.id][1]} строк файла</b>\n" \
                           f"💾<b>Записано: {STATES_STORAGE_DCT[update.from_user.id][2]} ссылок</b>\n\n" \
                           f'💲Цена редиректа: {REDIRECT_NUMBERS_DCT[update.from_user.id][2]} руб.\n' \
                           f'💰Баланс: {REDIRECT_NUMBERS_DCT[update.from_user.id][1]} руб.\n' \
                           f'🧾Общая стоимость: {REDIRECT_NUMBERS_DCT[update.from_user.id][0] * float(REDIRECT_NUMBERS_DCT[update.from_user.id][2])} руб.\n\n' \
                           f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?'
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            redirect_numb=str(int(REDIRECT_NUMBERS_DCT[update.from_user.id][0])),
            replenish_balance=False
        )
    else:
        text_for_message = f'☑️<b>Выбрано {REDIRECT_NUMBERS_DCT[update.from_user.id][0]} ' \
                           f'редиректов для каждой ссылки</b>\n\n' \
                           f"📖<b>Прочитано: {STATES_STORAGE_DCT[update.from_user.id][1]} строк файла</b>\n" \
                           f"💾<b>Записано: {STATES_STORAGE_DCT[update.from_user.id][2]} ссылок</b>\n\n" \
                           f'💲Цена редиректа: {REDIRECT_NUMBERS_DCT[update.from_user.id][2]} руб.\n' \
                           f'💰Баланс: {REDIRECT_NUMBERS_DCT[update.from_user.id][1]} руб.\n' \
                           f'🧾Общая стоимость: {REDIRECT_NUMBERS_DCT[update.from_user.id][0] * float(REDIRECT_NUMBERS_DCT[update.from_user.id][2])} руб.\n\n' \
                           f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?'
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            redirect_numb=str(int(REDIRECT_NUMBERS_DCT[update.from_user.id][0])),
            replenish_balance=False
        )
    await update.edit_message_text(
        text=text_for_message,
        reply_markup=inline_kbrd
    )


@Client.on_callback_query(filter_plus_redirect_handler)
async def plus_redirect_handler(client, update: CallbackQuery):
    """
    Хэндлер для кнопок 'плюс редирект(ы)'.
    """
    REDIRECT_NUMBERS_DCT[update.from_user.id][0] += float(update.data.split()[1])
    total_price = REDIRECT_NUMBERS_DCT[update.from_user.id][0] * float(REDIRECT_NUMBERS_DCT[update.from_user.id][2])

    if total_price > float(REDIRECT_NUMBERS_DCT[update.from_user.id][1]):  # Если общая стоимость больше баланса
        # Небольшой расчёт
        difference = total_price - float(REDIRECT_NUMBERS_DCT[update.from_user.id][1])
        numb_of_redirects = math.ceil(difference / float(REDIRECT_NUMBERS_DCT[update.from_user.id][2]))

        # Отнимаем кол-во редиректов, чтобы было не больше текущего баланса, пересчитываем стоимость и даём ответ
        REDIRECT_NUMBERS_DCT[update.from_user.id][0] -= numb_of_redirects
        total_price = REDIRECT_NUMBERS_DCT[update.from_user.id][0] * float(REDIRECT_NUMBERS_DCT[update.from_user.id][2])
        text_for_message = f'❗️<b>Недостаточно средств, пожалуйста, пополните баланс на {difference} руб.</b>\n' \
                           f'☑️<b>Выбрано {REDIRECT_NUMBERS_DCT[update.from_user.id][0]} ' \
                           f'редиректов для каждой ссылки</b>\n\n' \
                           f"📖<b>Прочитано: {STATES_STORAGE_DCT[update.from_user.id][1]} строк файла</b>\n" \
                           f"💾<b>Записано: {STATES_STORAGE_DCT[update.from_user.id][2]} ссылок</b>\n\n" \
                           f'💲Цена редиректа: {REDIRECT_NUMBERS_DCT[update.from_user.id][2]} руб.\n' \
                           f'💰Баланс: {REDIRECT_NUMBERS_DCT[update.from_user.id][1]} руб.\n' \
                           f'🧾Общая стоимость: {total_price} руб.\n\n' \
                           f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?'
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            redirect_numb=str(int(REDIRECT_NUMBERS_DCT[update.from_user.id][0])),
            replenish_balance=True
        )
    else:
        text_for_message = f'☑️<b>Выбрано {REDIRECT_NUMBERS_DCT[update.from_user.id][0]} ' \
                           f'редиректов для каждой ссылки</b>\n\n' \
                           f"📖<b>Прочитано: {STATES_STORAGE_DCT[update.from_user.id][1]} строк файла</b>\n" \
                           f"💾<b>Записано: {STATES_STORAGE_DCT[update.from_user.id][2]} ссылок</b>\n\n" \
                           f'💲Цена редиректа: {REDIRECT_NUMBERS_DCT[update.from_user.id][2]} руб.\n' \
                           f'💰Баланс: {REDIRECT_NUMBERS_DCT[update.from_user.id][1]} руб.\n' \
                           f'🧾Общая стоимость: {total_price} руб.\n\n' \
                           f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?'
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            redirect_numb=str(int(REDIRECT_NUMBERS_DCT[update.from_user.id][0])),
            replenish_balance=False
        )
    await update.edit_message_text(
        text=text_for_message,
        reply_markup=inline_kbrd
    )


@Client.on_callback_query(filter_link_shortening_handler)
async def choosing_link_shortening_service_handler(client, update: CallbackQuery):
    """
    Хэндлер для выбора сервиса по сокращению ссылок.
    Попадаем сюда после нажатия кнопки с callback_data='to_link_shortening'
    """
    await update.answer(f'Перешли к выбору сервиса по сокращению ссылок.')


@Client.on_message(filter_for_waiting_file_processing_handler)
async def waiting_file_processing(client, update: Message):
    """
    Хэндлер для обработки сообщений, когда юзер ожидает обработки файла.
    Отвечаем, что процесс идёт, необходимо подождать.
    """
    # TODO: на перспективу можно сделать проверку, сколько уже обработано строк в файле
    answers_lst = [
        '⌛️Пожалуйста, ожидайте. Я занимаюсь обработкой Вашего файла',
        '⌛️К сожалению, Вам придётся ещё немного подождать, я занимаюсь обработкой Вашего файла.',
        # Нецензурные ответы
        'Будешь ебать мне голову, вообще нихуя делать не стану.',
        '<b>Пошёл нахуй</b>',
        'Ручонки свои шаловливые убери куда-нибудь в другое место. '
        'От того, что ты дрочить меня будешь процесс только замедлится. '
        'Потому, что я хоть и программа, но один хуй трачу время на то, чтобы ответить вот таким уебанам, '
        'которых бывает достаточно в каждый момент времени.',
        '☝️<b>Время лечит...</b>\nДаже таких долбоебов как ты. Поэтому сиди и жди.'
    ]
    await update.reply_text(
        text=f"{random.choice(answers_lst)}\n\n"
             f"📖<b>Прочитано: {STATES_STORAGE_DCT[update.from_user.id][1]} строк файла</b>\n"
             f"💾<b>Записано: {STATES_STORAGE_DCT[update.from_user.id][2]} ссылок</b>"
    )
