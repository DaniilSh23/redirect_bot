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
from keyboards.bot_keyboards import (choose_numb_of_redirect_kbrd, back_to_headpage_keyboard,
                                     cancel_and_clear_state_keyboard, my_balance_part_keyboard,
                                     choose_short_link_keyboard)
from resources.messages import ALERT_MESSAGES, MESSAGES, ERROR_MESSAGES
from secondary_functions.req_to_bot_api import get_settings, get_user_data, get_interface_language
from settings.config import STATES_STORAGE_DCT, LINKS_OBJ_DCT


@Client.on_callback_query(filter_for_create_link_btn_handler)
async def create_link_btn_handler(client, update):
    """
    Хэндлер на нажатие кнопки "СОЗДАТЬ ССЫЛКУ". Устанавливаем состояние, в котором ожидаем получить файл со ссылками,
    запрашиваем сам файл и даём кнопку "Отменить".
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.reply_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                            " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Получаем баланс юзера и тариф из БД
    user_balance = await get_user_data(tlg_id=update.from_user.id)
    user_balance = Decimal(user_balance.get('balance'))
    tariff = await get_settings(key='tariff')
    tariff = Decimal(tariff[0].get('value'))

    # Если баланс меньше тарифа
    if tariff > user_balance:
        await update.edit_message_text(  # Предлагаем пополнить счёт
            text=f"❗️Недостаточно средств для создания ссылок.\n💰<b>Ваш баланс: {user_balance} руб.</b>\n"
                 f"🪙<b>Цена одного редиректа для ссылки: {tariff} руб.</b>",
            reply_markup=await my_balance_part_keyboard(language_code)
        )
        return

    STATES_STORAGE_DCT[update.from_user.id] = 'upload_file_with_links'
    await update.answer(
        text=ALERT_MESSAGES[f"send_file_with_links_{language_code}"],
        show_alert=True,
    )
    await update.edit_message_text(
        text=MESSAGES[f"send_file_with_links_{language_code}"],
        reply_markup=await cancel_and_clear_state_keyboard(language_code)
    )


@Client.on_message(filters.document & filter_for_get_doc_with_links_handler)
async def get_doc_with_links_handler(client, update: Message):
    """
    Хэндлер для получения документа (txt файл) со ссылками. Каждая ссылка с новой строки.
    Отвечаем, что идёт обработка документа и это может занять время. Скачиваем документ из телеги, читаем его.
    Итерируемся по строкам, проверяем ссылки на валидность, записываем в БД.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.reply_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                            " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    await update.reply_text(
        text=MESSAGES[f"document_processing_{language_code}"]
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
            i_line = i_line.replace('\ufeff', '')  # Устраняем BOM символ, если он будет
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

    STATES_STORAGE_DCT.pop(update.from_user.id)  # Очищаем стэйт ожидания обработки файла

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
            reply_markup=await my_balance_part_keyboard(language_code)
        )
        return

    # Даём ответ по окончании обработки файла
    await update.reply_text(
        text=MESSAGES[f"file_processing_complete_{language_code}"].format(
            link_count=len(links.split(' ')),
            tariff=links_obj.tariff,
            balance=links_obj.balance,
            total_price=links_obj.total_price,
        ),
        reply_markup=await choose_numb_of_redirect_kbrd(language_code),
    )


@Client.on_callback_query(filter_minus_redirect_handler)
async def minus_redirect_handler(client, update: CallbackQuery):
    """
    Хэндлер для кнопок 'минус редирект(ы)'
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    links_obj = LINKS_OBJ_DCT[update.from_user.id]  # Достаём из словаря объект класса
    # Уменьшяем кол-во редиректов
    links_obj.redirect_numb -= float(update.data.split()[1])

    if links_obj.redirect_numb < 1:  # Если выбрано менее 1 редиректа
        links_obj.redirect_numb = 1
        # Общая стоимость (число_редиректов * число_ссылок * тариф)
        links_obj.total_price = links_obj.redirect_numb * len(links_obj.links.split(' ')) * links_obj.tariff
        text_for_message = "".join([
            MESSAGES[f"less_one_redirect_{language_code}"],
            MESSAGES[f"make_redirect_status_{language_code}"].format(
                redirect_numb=int(links_obj.redirect_numb),
                links_count=len(links_obj.links.split(' ')),
                tariff=links_obj.tariff,
                balance=links_obj.balance,
                total_price=links_obj.total_price,
            ),
        ])
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            language_code=language_code,
            redirect_numb=str(links_obj.redirect_numb),
            replenish_balance=False
        )
    else:
        # Общая стоимость (число_редиректов * число_ссылок * тариф)
        links_obj.total_price = links_obj.redirect_numb * len(links_obj.links.split(' ')) * links_obj.tariff
        text_for_message = MESSAGES[f"make_redirect_status_{language_code}"].format(
                redirect_numb=int(links_obj.redirect_numb),
                links_count=len(links_obj.links.split(' ')),
                tariff=links_obj.tariff,
                balance=links_obj.balance,
                total_price=links_obj.total_price,
            )
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            language_code=language_code,
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
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

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

        # Собираем строку для ответа пользователю
        text_for_message = "".join([
            MESSAGES[f"top_up_balance_for_redirect_{language_code}"].format(price_difference=price_difference),
            MESSAGES[f"make_redirect_status_{language_code}"].format(
                redirect_numb=int(links_obj.redirect_numb),
                links_count=len(links_obj.links.split(' ')),
                tariff=links_obj.tariff,
                balance=links_obj.balance,
                total_price=links_obj.total_price,
            ),
        ])
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            language_code=language_code,
            redirect_numb=str(int(links_obj.redirect_numb)),
            replenish_balance=True
        )
    else:
        # Общая стоимость (число_редиректов * число_ссылок * тариф)
        links_obj.total_price = links_obj.redirect_numb * len(links_obj.links.split(' ')) * links_obj.tariff
        text_for_message = MESSAGES[f"make_redirect_status_{language_code}"].format(
            redirect_numb=int(links_obj.redirect_numb),
            links_count=len(links_obj.links.split(' ')),
            tariff=links_obj.tariff,
            balance=links_obj.balance,
            total_price=links_obj.total_price,
        )
        inline_kbrd = await choose_numb_of_redirect_kbrd(
            language_code=language_code,
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
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    await update.answer(ALERT_MESSAGES[f"choose_shortener_{language_code}"])
    await update.edit_message_text(
        text=MESSAGES[f"choose_shortener_{language_code}"],
        reply_markup=await choose_short_link_keyboard(language_code),
    )


@Client.on_callback_query(filter_processing_links_handler)
async def processing_links_for_redirect_handler(client, update: CallbackQuery):
    """
    Хэндлер, в котором мы непосредственно осуществляем процесс обработки каждой ссылки для обёртки их в редирект.
    Как итог работы отправляем файл, в котором будут указаны ссылки с их редиректом и ID компании(для сбора статистики)
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    links_obj = LINKS_OBJ_DCT[update.from_user.id]  # Достаём из словаря объект класса
    links_obj.short_link_service = update.data.split()[1]
    await update.edit_message_text(
        text=MESSAGES[f"wrap_in_redirect_{language_code}"],
        reply_markup=await back_to_headpage_keyboard(language_code=language_code),
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
    else:  # Неудачный запрос для создания набора ссылок
        logger.error(f'Неудачный запрос для создания в БД набора ссылок. TG_ID=={update.from_user.id}')
        err_flag = True

    # Кидаем запрос для старта обёртки ссылок(задачка Celery)
    if not await links_obj.start_wrapping():
        logger.error(f'Неудачный запрос старта задачи по обёртки ссылок. TG_ID=={update.from_user.id}')
        err_flag = True

    if err_flag:  # Отправляем уведомление о неисправности бота
        await update.edit_message_text(
            text=ERROR_MESSAGES[f"base_error_{language_code}"],
            reply_markup=await back_to_headpage_keyboard(language_code=language_code)
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
