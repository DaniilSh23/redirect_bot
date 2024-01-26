import math
import random
from urllib.parse import urlparse
from decimal import Decimal

from loguru import logger
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from bot_objects.links_obj import RedirectLinks
from filters.create_link_filters import filter_for_create_link_btn_handler, filter_for_get_doc_with_links_handler, \
    filter_for_waiting_file_processing_handler, filter_minus_redirect_handler, filter_plus_redirect_handler, \
    filter_link_shortening_handler, filter_processing_links_handler
from keyboards.bot_keyboards import CANCEL_AND_CLEAR_STATE_KBRD, choose_numb_of_redirect_kbrd, CHOOSE_SHORT_LINK_KBRD, \
    BACK_TO_HEAD_PAGE_KBRD, MY_BALANCE_PART_KBRD
from secondary_functions.req_to_bot_api import update_or_create_link, get_settings, get_user_data
from settings.config import STATES_STORAGE_DCT, LINKS_OBJ_DCT


@Client.on_callback_query(filter_for_create_link_btn_handler)
async def create_link_btn_handler(client, update):
    """
    Хэндлер на нажатие кнопки "СОЗДАТЬ ССЫЛКУ".
    Устанавливаем состояние, в котором ожидаем получить файл со ссылками,
    запрашиваем сам файл и даём кнопку "Отменить".
    """
    # Получаем баланс юзера и тариф из БД
    user_balance = await get_user_data(tlg_id=update.from_user.id)
    user_balance = Decimal(user_balance.get('balance'))
    tariff = await get_settings(key='tariff')
    tariff = Decimal(tariff[0].get('value'))
    # Если баланс меньше тарифа
    if tariff > user_balance:
        await update.edit_message_text(     # Предлагаем пополнить счёт
            text=f"❗️Недостаточно средств для создания ссылок.\n💰<b>Ваш баланс: {user_balance} руб.</b>\n"
                 f"🪙<b>Цена одного редиректа для ссылки: {tariff} руб.</b>",
            reply_markup=MY_BALANCE_PART_KBRD
        )
        return

    STATES_STORAGE_DCT[update.from_user.id] = 'upload_file_with_links'
    await update.answer(
        text=f"📄Пришлите файл со ссылками:\n\n🔹 каждая ссылка с новой строки;\n"
             f"🔹 все ссылки должны начинаться с http:// https:// ftp:// и т.п.",
        show_alert=True
    )
    await update.edit_message_text(
        text=f"📄Пожалуйста, пришлите мне <b><u>TXT</u> файл со ссылками</b>:\n\n"
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
        links = ''
        for i_line in links_file:
            all_lines_count += 1
            i_line = i_line.replace(' ', '')

            # проверка, что строка в файле - это ссылка
            is_link = False
            i_line = i_line.replace('\ufeff', '')   # Устраняем BOM символ, если он будет
            parsed_lnk = urlparse(i_line)
            logger.debug(f'Разбираемся ссылку на детали : {i_line}')
            if parsed_lnk.scheme and parsed_lnk.netloc and '.' in parsed_lnk.netloc:
                # Проверяем, чтобы в адресе не было 2х точек подряд
                for i_indx, i_elem in enumerate(parsed_lnk.netloc):
                    if i_indx == len(parsed_lnk.netloc) - 1:
                        is_link = True
                        break
                    if i_elem == '.' and parsed_lnk.netloc[i_indx + 1] == '.':
                        break
            if is_link:
                if len(links) == 0:
                    links = i_line
                else:
                    links = ' '.join([links, i_line])
                valid_links_count += 1

                # # Записываем ссылку в БД через запрос API
                # write_link_rslt = await update_or_create_link(data={
                #     'tlg_id': update.from_user.id,
                #     'link': i_line
                # })

    STATES_STORAGE_DCT.pop(update.from_user.id)     # Очищаем стэйт ожидания обработки файла

    tariff = await get_settings(key='tariff')  # Получаем цену тарифа в БД
    user_data = await get_user_data(tlg_id=update.from_user.id)  # Получаем данные об юзере (нужен баланс)
    # Рассчитываем итоговую стоимость 1_редирект * число_ссылок * тариф
    total_price = 1 * len(links.split(' ')) * int(tariff[0].get("value"))
    # Создаём инстанс класса с данными о редиректе для ссылок
    links_obj = RedirectLinks(
        tlg_id=update.from_user.id,
        links=links,
        tariff=tariff[0].get("value"),
        balance=user_data.get("balance"),
        redirect_numb=1,
        total_price=total_price,
    )
    LINKS_OBJ_DCT[update.from_user.id] = links_obj  # Сохраняем ссылку на объект класса в словаре

    # Если итоговая цена для одного редиректа больше баланса
    if links_obj.total_price > links_obj.balance:
        await update.reply_text(
            text=f"❗️<b>Недостаточно средств.</b>\n\n💰Ваш баланс: <b>{links_obj.balance} руб.</b>\n"
                 f"🧾Общая стоимость одного редиректа для {len(links.split(' '))} ссылок: "
                 f"<b>{links_obj.total_price} руб.</b>\n\nПожалуйста, пополните баланс.",
            reply_markup=MY_BALANCE_PART_KBRD
        )
        return

    # Даём ответ по окончании обработки файла
    await update.reply_text(
        text=f'✅<b>Обработка файла завершена.</b>\n\n'
             f"💾<b>Записано: {len(links.split(' '))} ссылок</b>\n\n"
             f'💲Цена редиректа для 1 ссылки: <b>{links_obj.tariff} руб.</b>\n'
             f'💰Баланс: <b>{links_obj.balance} руб.</b>\n'
             f'🧾Общая стоимость: <b>{links_obj.total_price} руб.</b>\n\n'
             f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?',
        reply_markup=await choose_numb_of_redirect_kbrd()
    )


@Client.on_callback_query(filter_minus_redirect_handler)
async def minus_redirect_handler(client, update: CallbackQuery):
    """
    Хэндлер для кнопок 'минус редирект(ы)'
    """
    links_obj = LINKS_OBJ_DCT[update.from_user.id]  # Достаём из словаря объект класса
    # Уменьшяем кол-во редиректов
    links_obj.redirect_numb -= float(update.data.split()[1])

    if links_obj.redirect_numb < 1:  # Если выбрано менее 1 редиректа
        links_obj.redirect_numb = 1
        # Общая стоимость (число_редиректов * число_ссылок * тариф)
        links_obj.total_price = links_obj.redirect_numb * len(links_obj.links.split(' ')) * links_obj.tariff
        text_for_message = f'❗️<b>Редиректов не может быть меньше 1</b>\n' \
                           f'☑️<b>Выбрано {int(links_obj.redirect_numb)} ' \
                           f'редиректов для каждой ссылки</b>\n\n' \
                           f"💾Записано: <b>{len(links_obj.links.split(' '))}</b> ссылок\n\n" \
                           f'💲Цена редиректа для 1 ссылки: <b>{links_obj.tariff} руб.</b>\n' \
                           f'💰Баланс: <b>{links_obj.balance} руб.</b>\n' \
                           f'🧾Общая стоимость: <b>{links_obj.total_price} руб.</b>\n\n' \
                           f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?'
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            redirect_numb=str(links_obj.redirect_numb),
            replenish_balance=False
        )
    else:
        # Общая стоимость (число_редиректов * число_ссылок * тариф)
        links_obj.total_price = links_obj.redirect_numb * len(links_obj.links.split(' ')) * links_obj.tariff
        text_for_message = f'☑️<b>Выбрано {int(links_obj.redirect_numb)} ' \
                           f'редиректов для каждой ссылки</b>\n\n' \
                           f"💾<b>Записано: {len(links_obj.links.split(' '))} ссылок</b>\n\n" \
                           f'💲Цена редиректа для 1 ссылки: {links_obj.tariff} руб.\n' \
                           f'💰Баланс: {links_obj.balance} руб.\n' \
                           f'🧾Общая стоимость: {links_obj.total_price} руб.\n\n' \
                           f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?'
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            redirect_numb=str(int(links_obj.redirect_numb)),
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
    links_obj = LINKS_OBJ_DCT[update.from_user.id]  # Достаём из словаря объект класса
    # Увеличиваем кол-во редиректов
    links_obj.redirect_numb += float(update.data.split()[1])
    # Общая стоимость (число_редиректов * число_ссылок * тариф)
    links_obj.total_price = links_obj.redirect_numb * len(links_obj.links.split(' ')) * links_obj.tariff

    if float(links_obj.total_price) > float(links_obj.balance):  # Если общая стоимость больше баланса
        # Разница итоговой цены и баланса
        price_difference = links_obj.total_price - links_obj.balance
        # число_редиректов = разница цены / (число_сылок * тариф)
        numb_of_redirects = math.ceil(price_difference / (len(links_obj.links.split(' ')) * links_obj.tariff))

        # Отнимаем кол-во редиректов, чтобы было не больше текущего баланса
        links_obj.redirect_numb -= numb_of_redirects
        # Общая стоимость (число_редиректов * число_ссылок * тариф)
        links_obj.total_price = links_obj.redirect_numb * len(links_obj.links.split(' ')) * links_obj.tariff
        text_for_message = f'❗️<b>Недостаточно средств, пополните баланс на {price_difference} руб.</b>\n\n' \
                           f'☑️<b>Выбрано {int(links_obj.redirect_numb)} ' \
                           f'редиректов для каждой ссылки</b>\n\n' \
                           f"💾Записано: <b>{len(links_obj.links.split(' '))} ссылок</b>\n\n" \
                           f'💲Цена редиректа для 1 ссылки: <b>{links_obj.tariff} руб.</b>\n' \
                           f'💰Баланс: <b>{links_obj.balance} руб.</b>\n' \
                           f'🧾Общая стоимость: <b>{links_obj.total_price} руб.</b>\n\n' \
                           f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?'
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            redirect_numb=str(int(links_obj.redirect_numb)),
            replenish_balance=True
        )
    else:
        # Общая стоимость (число_редиректов * число_ссылок * тариф)
        links_obj.total_price = links_obj.redirect_numb * len(links_obj.links.split(' ')) * links_obj.tariff
        text_for_message = f'☑️<b>Выбрано {int(links_obj.redirect_numb)} ' \
                           f'редиректов для каждой ссылки</b>\n\n' \
                           f"💾<b>Записано: {len(links_obj.links.split(' '))} ссылок</b>\n\n" \
                           f'💲Цена редиректа для 1 ссылки: {links_obj.tariff} руб.\n' \
                           f'💰Баланс: {links_obj.balance} руб.\n' \
                           f'🧾Общая стоимость: {links_obj.total_price} руб.\n\n' \
                           f'🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?'
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            redirect_numb=str(int(links_obj.redirect_numb)),
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
    Попадаем сюда после нажатия кнопки с callback_data='to_link_shortening'.
    Отдаём клавиатуру со списком сервисов для сокращения ссылок.
    """
    # await update.answer(f'❗️Пожалуйста, обратите внимание: в последнее время сервис cutt.us долго прогружает ссылки.\n'
    #                     f'‼️Поэтому просим учитывать данный факт при его выборе.', show_alert=True)
    await update.answer(f'🔗Выбор сервиса для сокращения ссылок')
    await update.edit_message_text(
        text=f'🔗Пожалуйста, выберите <b>сервис для сокращения ссылок</b>.\n\n'
             f'Будьте внимательны! Некоторые сокращалки открывают ссылку спустя n-oe кол-во времени!\n\n'
             f'haa.su - переход в теч. 3 сек.',
        reply_markup=CHOOSE_SHORT_LINK_KBRD
    )


@Client.on_callback_query(filter_processing_links_handler)
async def processing_links_for_redirect_handler(client, update: CallbackQuery):
    """
    Хэндлер, в котором мы непосредственно осуществляем процесс обработки каждой ссылки для обёртки их в редирект.
    Как итог работы отправляем файл, в котором будут указаны ссылки с их редиректом и ID компании(для сбора статистики)
    """
    links_obj = LINKS_OBJ_DCT[update.from_user.id]  # Достаём из словаря объект класса
    links_obj.short_link_service = update.data.split()[1]
    await update.edit_message_text(
        text=f'🆗Окей.\n'
             f'🎁Начинаю оборачивать Ваши ссылки в редирект.\n'
             f'🧘‍♀️Ожидайте, я пришлю Вам файл с результатами📄, когда всё будет готово.',
        reply_markup=BACK_TO_HEAD_PAGE_KBRD
    )
    err_flag = False
    # Создаём в БД набор для ссылок
    result = await links_obj.create_link_set()
    if result:
        # Создаём в БД записи для ссылок
        result = await links_obj.create_links()
        if not result:  # Неудачный запрос для создания ссылок
            logger.error(f'Неудачный запрос для создания в БД ссылок. TG_ID=={update.from_user.id}')
            err_flag = True
    else:   # Неудачный запрос для создания набора ссылок
        logger.error(f'Неудачный запрос для создания в БД набора ссылок. TG_ID=={update.from_user.id}')
        err_flag = True

    # Кидаем запрос для старта обёртки ссылок(задачка Celery)
    if not await links_obj.start_wrapping():
        logger.error(f'Неудачный запрос старта задачи по обёртки ссылок. TG_ID=={update.from_user.id}')
        err_flag = True

    if err_flag:    # Отправляем уведомление о неисправности бота
        await update.edit_message_text(
            text=f'🔧<b>Техническая неисправность бота.</b>\n'
                 f'Пожалуйста, сообщите нам через раздел поддержки, чтобы мы могли оперативно устранить проблему.',
            reply_markup=BACK_TO_HEAD_PAGE_KBRD
        )


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
        '🍹Пока я обрабатываю файл, Вы можете потратить время с пользой для себя.',
        '🥃Почему бы не сделать небольшую паузу, пока я занят обработкой файла?',
        '🧉Вы можете расслабиться, пока я занят обработкой Вашего файла. '
        'Согласитесь, намного лучше когда Вам не приходится делать это самостоятельно.',
    ]
    await update.reply_text(
        text=f"{random.choice(answers_lst)}\n\n"
             f"📖<b>Прочитано: {STATES_STORAGE_DCT[update.from_user.id][1]} строк файла</b>\n"
             f"💾<b>Записано: {STATES_STORAGE_DCT[update.from_user.id][2]} ссылок</b>"
    )
