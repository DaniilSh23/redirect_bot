from pyrogram import Client
from pyrogram.types import CallbackQuery, Message

from bot_objects.payments_objects import UserPayments
from filters.payment_filters import filters_choose_pay_method, filter_ask_pay_amount, filter_write_pay_amount, \
    confirm_payment_filter, cancel_payment_filter, pay_to_card_send_data_filter, ask_pay_to_card_confirmation_filter, \
    pay_to_card_confirmation_filter, decline_card_payment_filter, ask_amount_for_confirm_card_payment_filter, \
    confirm_card_payment_filter
from keyboards.bot_keyboards import (ADMIN_KBRD, card_payment_processing_kbrd, back_to_headpage_keyboard,
                                     waiting_for_payment_keyboard, pay_methods_keyboard,
                                     cancel_and_clear_state_keyboard, pay_to_card_keyboard)
from resources.messages import MESSAGES
from secondary_functions.req_to_bot_api import req_for_get_payment, get_settings, post_for_change_balance, \
    get_interface_language
from settings.config import PAYMENTS_OBJ_DCT, STATES_STORAGE_DCT, TEMP_STORAGE_DCT, MY_LOGGER


@Client.on_callback_query(filters_choose_pay_method)
async def choose_pay_method_handler(client, update: CallbackQuery):
    """
    Хэндлер для выбора способа оплаты.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Проверяем наличие в БД активного счёта
    payment_from_db = await req_for_get_payment(tlg_id=update.from_user.id)
    if not payment_from_db:  # Обработка на случай неудачного запроса
        await update.edit_message_text(
            text=f'🚧<b>Не удалось получить данные об активном платеже.</b>\n\n'
                 f'Будем благодарны, если сообщите нам об этой проблеме. Так мы сможем быстрее всё починить',
            reply_markup=await back_to_headpage_keyboard(language_code)
        )
        return

    # Если данные о платеже есть в БД
    if payment_from_db != 404 and payment_from_db.get('tlg_id'):
        payment_obj = UserPayments(  # Создаём объект класса UserPayments
            tlg_id=update.from_user.id,
            pay_system_type=payment_from_db.get("pay_system_type"),
            amount=payment_from_db.get("amount"),
            bill_id=payment_from_db.get("bill_id"),
            bill_url=payment_from_db.get("bill_url"),
            bill_status=payment_from_db.get("bill_status"),
            bill_expire_at=payment_from_db.get("bill_expire_at"),
        )
        PAYMENTS_OBJ_DCT[update.from_user.id] = payment_obj
        # Даём ответ со ссылкой на оплату и кнопками
        await update.edit_message_text(
            text=f'🌐<b>Ваша ссылка для оплаты:</b> {payment_obj.bill_url}\n\n'
                 f'☝️<b>Будьте внимательны</b> - когда в Crystal Pay будет "✅<u>Подтверждено</u>" - нужно нажать на '
                 f'кнопку "✅<u>Подтвердить оплату</u>" - <b><u>это будет основанием для зачисления средств.</u></b>',
            reply_markup=await waiting_for_payment_keyboard(language_code)
        )

    else:  # Если активного счёта нет, то ведём на 1-й шаг оплаты
        await update.answer(f'Выберите способ оплаты')
        await update.edit_message_text(
            text=f'🌕 <b>Перевод на карту:</b>\n- Перевод на карту (РУБ.) с предоставлением скриншота\n\n'
                 f'❗️<b>Платеж зачисляется в ручном режиме Администрацией</b>\n‼️<b>Оплата в любом размере в РУБ.</b>',
            reply_markup=await pay_methods_keyboard(language_code)
        )


'''ПЛАТЕЖИ QIWI и CRYSTAL PAY'''


@Client.on_callback_query(filter_ask_pay_amount)
async def ask_pay_amount_handler(client, update: CallbackQuery):
    """
    Хэндлер для запроса суммы пополнения.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Даём ответ
    await update.answer(f'Введите сумму пополнения')
    await update.edit_message_text(
        text=f'👇<b>Пришлите мне сумму пополнения баланса</b>\n\n'
             f'<i>Это должно быть целое число (рубли)</i>',
        reply_markup=await cancel_and_clear_state_keyboard(language_code)
    )

    # Создаём объект класса UserPayments и сохраняем его в словарь
    PAYMENTS_OBJ_DCT[update.from_user.id] = UserPayments(
        tlg_id=update.from_user.id,
        pay_system_type=update.data.split()[1]
    )
    # Устанавливаем стэйт для ввода суммы пополнения баланса
    STATES_STORAGE_DCT[update.from_user.id] = 'send_amount_for_replenish_balance'


@Client.on_message(filter_write_pay_amount)
async def write_pay_amount_handler(client, update: Message):
    """
    Хэндлер для получения сообщения с суммой оплаты
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.reply_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                            " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Проверка неверного ввода суммы
    if not update.text.isdigit():
        await update.reply_text(
            text=f'⚠️<b>Неверное значение суммы пополнения:</b> <code>{update.text}</code>\n\n'
                 f'🔢Пожалуйста, введите целое число.\n\nНапример: <code>150</code> 👈 пополнение на 150 рублей.',
            reply_markup=await cancel_and_clear_state_keyboard(language_code)
        )

    # Очищаем стэйт юзера
    STATES_STORAGE_DCT.pop(update.from_user.id)

    # Получаем объект класса и устанавливаем сумму пополнения
    user_payment = PAYMENTS_OBJ_DCT[update.from_user.id]
    user_payment.amount = update.text

    # Определяем платежную систему и по ней отрабатываем
    if user_payment.pay_system_type == 'qiwi':
        bill_url = await user_payment.qiwi_create_invoice()

    elif user_payment.pay_system_type == 'crystal':
        bill_url = await user_payment.crystalpay_create_invoice()

    # Создаём в БД запись о платеже
    response = await user_payment.create_payment_in_db()
    if not response:
        await update.reply_text(
            text=f'🚧<b>Не удалось создать запись о платеже.</b>\n\n'
                 f'Будем благодарны, если сообщите нам об этой проблеме. Так мы сможем быстрее всё починить',
            reply_markup=await back_to_headpage_keyboard(language_code)
        )
        return

    # Даём ответ со ссылкой на оплату и кнопками
    await update.reply_text(
        text=f'🌐<b>Ваша ссылка для оплаты:</b> {bill_url}\n\n'
             f'☝️<b>Будьте внимательны</b> - когда в Crystal Pay будет "✅<u>Подтверждено</u>" - нужно нажать на '
             f'кнопку "✅<u>Подтвердить оплату</u>" - <b><u>это будет основанием для зачисления средств.</u></b>',
        reply_markup=await waiting_for_payment_keyboard(language_code)
    )


@Client.on_callback_query(confirm_payment_filter)
async def confirm_payment_handler(client, update: CallbackQuery):
    """
    Хэндлер для подтверждения оплаты.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Если в боте не хранится ссылка на объект класса UserPayment, то создаём её на основе данных из БД
    if not PAYMENTS_OBJ_DCT.get(update.from_user.id):
        payment_from_db = await req_for_get_payment(tlg_id=update.from_user.id)
        if not payment_from_db:  # Обработка на случай неудачного запроса
            await update.edit_message_text(
                text=f'🚧<b>Не удалось получить данные об активном платеже.</b>\n\n'
                     f'Будем благодарны, если сообщите нам об этой проблеме. Так мы сможем быстрее всё починить',
                reply_markup=await back_to_headpage_keyboard(language_code)
            )
            return

        PAYMENTS_OBJ_DCT[update.from_user.id] = UserPayments(
            tlg_id=update.from_user.id,
            pay_system_type=payment_from_db.get("pay_system_type"),
            amount=payment_from_db.get("amount"),
            bill_id=payment_from_db.get("bill_id"),
            bill_url=payment_from_db.get("bill_url"),
            bill_status=payment_from_db.get("bill_status"),
            bill_expire_at=payment_from_db.get("bill_expire_at"),
        )

    user_payment_obj = PAYMENTS_OBJ_DCT[update.from_user.id]  # Берём объект UserPayment
    # Получаем статус платежа
    if user_payment_obj.pay_system_type == 'crystal':
        check_result = await user_payment_obj.check_crystalpay_invoice()
    elif user_payment_obj.pay_system_type == 'qiwi':
        check_result = await user_payment_obj.check_qiwi_invoice()
    else:
        check_result = 'не определён...'

    await update.edit_message_text(
        text=f'🧾Статус платежа: {check_result}',
        reply_markup=await back_to_headpage_keyboard(language_code)
    )

    if user_payment_obj.bill_status:
        # Отправляем запрос на установку статуса "оплачен" для данного счёта
        MY_LOGGER.debug(f'Отправка запрос на установку статуса "оплачен" для счёта.')
        await user_payment_obj.create_payment_in_db()

        # Зачисляем средства на баланс
        add_funds_rslt = await user_payment_obj.add_funds_to_balance(
            description=f"Пополнение баланса, через {user_payment_obj.pay_system_type}"
        )
        MY_LOGGER.debug(f'Результат запроса для зачисления средств на баланс: {add_funds_rslt}')

        if not add_funds_rslt:
            # ОТПРАВЛЯЕМ АДМИНАМ ПРЕДУПРЕЖДЕНИЕ О ПРОБЛЕМЫ ЗАЧИСЛЕНИЯ СРЕДСТВ НА БАЛАНС
            bot_admins = await get_settings(key='redirect_bot_admin')
            if bot_admins:
                for i_bot_admin in bot_admins:
                    await client.send_message(
                        chat_id=i_bot_admin.get('value'),
                        text=f'<b>СРОЧНО</b>‼️\n\n'
                             f'🛰Хьюстон, у нас проблемы!\n\n'
                             f'Юзер с TG ID {user_payment_obj.tlg_id} положил себе на баланс '
                             f'{user_payment_obj.amount} рублей. Оплата прошла, но средства на баланс не '
                             f'зачислены. Надо зайти в админку и вручную прибавить ему эту сумму, '
                             f'а также искать причину этой проблемы. Также рекомендуется приостановить оплату, '
                             f'чтобы проблемы не плодились.',
                        reply_markup=ADMIN_KBRD,
                    )


@Client.on_callback_query(cancel_payment_filter)
async def cancel_payment_handler(client, update: CallbackQuery):
    """
    Хэндлер для отмены платежа. Архивируем платёж в БД.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    user_payment_obj = PAYMENTS_OBJ_DCT[update.from_user.id]
    delete_rslt = await req_for_get_payment(payment_for_dlt_id=user_payment_obj.bill_id)
    if not delete_rslt:  # Если не удалось удалить
        await update.edit_message_text(
            text=f'🚧<b>Не удалось отменить платёж.</b>\n\n'
                 f'Будем благодарны, если сообщите нам об этой проблеме. Так мы сможем быстрее всё починить',
            reply_markup=await back_to_headpage_keyboard(language_code)
        )
        return

    await update.edit_message_text(
        text=f'🗑Платёж удалён.',
        reply_markup=await back_to_headpage_keyboard(language_code)
    )


'''ПЛАТЕЖИ ПЕРЕВОДОМ НА КАРТУ'''


@Client.on_callback_query(pay_to_card_send_data_filter)
async def pay_to_card_send_data_handler(client, update: CallbackQuery):
    """
    Платёж переводом на карту, отправляем данные для перевода
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Получаем текст для перевода
    pay_method_text = update.data.split()[1]
    settings_lst = await get_settings(key=pay_method_text)    # [{"key": "value"}, ...]
    msg_text = settings_lst[0].get("value")

    await update.edit_message_text(
        text=msg_text,
        reply_markup=await pay_to_card_keyboard(language_code)
    )


@Client.on_callback_query(ask_pay_to_card_confirmation_filter)
async def ask_pay_to_card_confirmation_handler(client, update: CallbackQuery):
    """
    Хэндлер для запроса подтверждения платежа переводом на карту.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    await update.edit_message_text(
        text=MESSAGES[f"send_me_check_message_{language_code}"],
        reply_markup=await cancel_and_clear_state_keyboard(language_code)
    )
    STATES_STORAGE_DCT[update.from_user.id] = 'pay_to_card_confirmation'


@Client.on_message(pay_to_card_confirmation_filter)
async def pay_to_card_confirmation_handler(client, update: Message):
    """
    Хэндлер для получения от юзера чека, в качестве подтверждения платежа.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.reply_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                            " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Просим повторить, если не обнаружено фотки в сообщении
    if not update.photo:
        await update.reply_text(
            text=f'🖼🤷‍♂️<b>Не обнаружено фото в Вашем сообщении.</b>\n\n'
                 f'✉️Пожалуйста, <b>отправьте мне чек(скрин, фото)</b> для подтверждения оплаты.',
            reply_markup=await cancel_and_clear_state_keyboard(language_code)
        )
        return

    # Ответ юзеру
    await update.reply_text(
        text=f'👌Ваши средства будут зачислены сразу, после обработки платежа.',
        reply_markup=await back_to_headpage_keyboard(language_code)
    )
    STATES_STORAGE_DCT.pop(update.from_user.id)  # Очищаем стэйт

    # Получаем ID того, кто подтверждает платежи
    who_approves_payments = await get_settings(key='who_approves_payments')
    if not who_approves_payments:
        pass  # TODO: сделать обработку неудачного запроса

    who_approves_payments = who_approves_payments[0].get("value")
    await update.copy(
        chat_id=who_approves_payments,
        caption=f'<b>Подтверждение платежа</b> от юзера:\n🔹TG_ID: <code>{update.from_user.id}</code>|'
                f'\n🔹username: @{update.from_user.username}',
        reply_markup=await card_payment_processing_kbrd(tlg_id=update.from_user.id)
    )


@Client.on_callback_query(decline_card_payment_filter)
async def decline_card_payment_handler(client, update: CallbackQuery):
    """
    Хэндлер для отклонения платежа по карте
    """
    # Информирование юзера об отклонении платежа
    await client.send_message(
        chat_id=update.data.split()[1],
        text=f'❌Ваш платёж был отклонён'
    )

    # Уведомление тому, кто отклонил
    await update.edit_message_text(
        text=f'Юзер проинформирован об отклонении платежа❌'
    )


@Client.on_callback_query(ask_amount_for_confirm_card_payment_filter)
async def ask_amount_for_confirm_card_payment_handler(client, update: CallbackQuery):
    """
    Хэндлер для запроса суммы платежа по карте.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    await client.send_message(
        chat_id=update.from_user.id,
        text=f'💵<b>Введите сумму, которую оплатил пользователь</b>\n\n'
             f'☝️Это должно быть <b>целое число</b>\n\n'
             f'<i>Если кто-то умудрился оплатить с копейками, то, как выдающейся личности👩‍🎓,'
             f' можно округлить его сумму в бОльшую сторону до очередного рубля</i>',
        reply_markup=await cancel_and_clear_state_keyboard(language_code)
    )
    STATES_STORAGE_DCT[update.from_user.id] = 'ask_card_replenish_amount'  # Устанавливаем стэйт для админа
    # Записываем tlg_id плательщика во временное хранилище
    TEMP_STORAGE_DCT[update.from_user.id] = {'payer_id': update.data.split()[1]}


@Client.on_message(confirm_card_payment_filter)
async def confirm_card_payment_handler(client, update: Message):
    """
    Хэндлер подтверждения платежа и зачисления средств на баланс.
    """
    # Получаем язык интерфейса пользователя
    interface_lang_response = await get_interface_language(tlg_id=update.from_user.id)
    if not interface_lang_response:
        return await update.edit_message_text(text="🛠 Sorry...The bot has problems with translation. Please try"
                                                   " again later, we are already solving this problem")
    language_code = interface_lang_response["language_code"]

    # Проверка, если введено не целое число
    if not update.text.isdigit():
        await update.reply_text(
            text=f'❗️<b>Введено не целое число.</b>\n❌<code>{update.text}</code> - не подходит\n\n'
                 f'💵<b>Введите сумму, которую оплатил пользователь</b>\n'
                 f'☝️Это должно быть <b>целое число</b>\n',
            reply_markup=await cancel_and_clear_state_keyboard(language_code)
        )
        return

    # Очищаем стэйт админа
    STATES_STORAGE_DCT.pop(update.from_user.id)

    # Получаем tlg_id плательщика
    payer_id = TEMP_STORAGE_DCT.get(update.from_user.id).get('payer_id')
    # Посылаем запрос на изменение баланса юзера
    response = await post_for_change_balance(data={
        "action": "+",
        "value": update.text,
        "tlg_id": payer_id,
        "description": "Пополнение баланса переводом на карту."
    })
    if not response:  # Обработка неудачного запроса
        await update.reply_text(
            text=f'Не удалось выполнить запрос для изменения баланса юзера {payer_id} на +{update.text} руб.\n\n'
                 f'Рекомендую сейчас пополнить баланс юзерая вручную в админке и далее решать проблему.',
        )
    else:
        await update.reply_text(
            text=f'💵<b>+{update.text} руб. зачислено на баланс юзера <code>{payer_id}</code></b>',
        )
        await client.send_message(
            chat_id=payer_id,
            text=f'💵<b>+{update.text} руб. зачислено на Ваш баланс!</b>\n🤝Спасибо, что выбрали нас.'
        )
