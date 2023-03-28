from pyrogram import Client
from pyrogram.types import CallbackQuery, Message

from bot_objects.payments_objects import UserPayments
from filters.payment_filters import filters_choose_pay_method, filter_ask_pay_amount, filter_write_pay_amount, \
    confirm_payment_filter, cancel_payment_filter
from keyboards.bot_keyboards import PAY_METHODS_KBRD, CANCEL_AND_CLEAR_STATE_KBRD, BACK_TO_HEAD_PAGE_KBRD, \
    WAITING_FOR_PAYMENT_KBRD, ADMIN_KBRD
from secondary_functions.req_to_bot_api import req_for_get_payment, get_settings
from settings.config import PAYMENTS_OBJ_DCT, STATES_STORAGE_DCT


@Client.on_callback_query(filters_choose_pay_method)
async def choose_pay_method_handler(client, update: CallbackQuery):
    """
    Хэндлер для выбора способа оплаты.
    """
    await update.answer(f'Выберите способ оплаты')
    await update.edit_message_text(
        text=f'💳<b>Выберите способ оплаты</b>',
        reply_markup=PAY_METHODS_KBRD
    )


@Client.on_callback_query(filter_ask_pay_amount)
async def ask_pay_amount_handler(client, update: CallbackQuery):
    """
    Хэндлер для запроса суммы пополнения.
    """
    # Даём ответ
    await update.answer(f'Введите сумму пополнения')
    await update.edit_message_text(
        text=f'👇<b>Пришлите мне сумму пополнения баланса</b>\n\n'
             f'<i>Это должно быть целое число (рубли)</i>',
        reply_markup=CANCEL_AND_CLEAR_STATE_KBRD
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
    # Проверка неверного ввода суммы
    if not update.text.isdigit():
        await update.reply_text(
            text=f'⚠️<b>Неверное значение суммы пополнения:</b> <code>{update.text}</code>\n\n'
                 f'🔢Пожалуйста, введите целое число.\n\nНапример: <code>150</code> 👈 пополнение на 150 рублей.',
            reply_markup=CANCEL_AND_CLEAR_STATE_KBRD
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

    elif user_payment.pay_system_type == 'to_card':
        # TODO: продумать логику с оплатой переводом и сделать
        pass

    # Создаём в БД запись о платеже
    response = await user_payment.create_payment_in_db()
    if not response:
        await update.reply_text(
            text=f'🚧<b>Не удалось создать запись о платеже.</b>\n\n'
                 f'Будем благодарны, если сообщите нам об этой проблеме. Так мы сможем быстрее всё починить',
            reply_markup=BACK_TO_HEAD_PAGE_KBRD
        )
        return

    # Даём ответ со ссылкой на оплату и кнопками
    await update.reply_text(
        text=f'🌐<b>Ваша ссылка для оплаты:</b> {bill_url}\n\n'
             f'После платежа необходимо нажать кнопку '
             f'"✅Подтвердить оплату" - <u><b>это будет основанием для зачисления средств</b></u>.',
        reply_markup=WAITING_FOR_PAYMENT_KBRD
    )


@Client.on_callback_query(confirm_payment_filter)
async def confirm_payment_handler(client, update: CallbackQuery):
    """
    Хэндлер для подтверждения оплаты.
    """

    # Если в боте не хранится ссылка на объект класса UserPayment, то создаём её на основе данных из БД
    if not PAYMENTS_OBJ_DCT.get(update.from_user.id):
        payment_from_db = await req_for_get_payment(tlg_id=update.from_user.id)
        if not payment_from_db:  # Обработка на случай неудачного запроса
            await update.edit_message_text(
                text=f'🚧<b>Не удалось получить данные об активном платеже.</b>\n\n'
                     f'Будем благодарны, если сообщите нам об этой проблеме. Так мы сможем быстрее всё починить',
                reply_markup=BACK_TO_HEAD_PAGE_KBRD
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
        reply_markup=BACK_TO_HEAD_PAGE_KBRD
    )

    if user_payment_obj.bill_status:
        # Отправляем запрос на установку статуса "оплачен" для данного счёта
        await user_payment_obj.create_payment_in_db()

        # Зачисляем средства на баланс
        if not await user_payment_obj.add_funds_to_balance():  # Функция вызывается сразу в отрицательном условии

            # ОТПРАВЛЯЕМ АДМИНАМ ПРЕДУПРЕЖДЕНИЕ О ПРОБЛЕМЫ ЗАЧИСЛЕНИЯ СРЕДСТВ НА БАЛАНС
            bot_admins = await get_settings(key='redirect_bot_admin')
            if bot_admins:
                for i_bot_admin in bot_admins:
                    await client.send_message(
                        chat_id=i_bot_admin,
                        text=f'<b>СРОЧНО</b>‼️\n\n'
                             f'🛰Хьюстон, у нас проблемы!\n\n'
                             f'Юзер с TG ID {user_payment_obj.tlg_id} положил себе на баланс '
                             f'{user_payment_obj.amount} рублей. Оплата прошла, но средства на баланс не '
                             f'зачислены. Надо зайти в админку и вручную прибавить ему эту сумму, '
                             f'а также искать причину этой проблемы. Также рекомендуется приостановить оплату, '
                             f'чтобы проблемы не плодились.',
                        reply_markup=ADMIN_KBRD,
                    )
                    break


@Client.on_callback_query(cancel_payment_filter)
async def cancel_payment_handler(client, update: CallbackQuery):
    """
    Хэндлер для отмены платежа. Архивируем платёж в БД.
    """
    user_payment_obj = PAYMENTS_OBJ_DCT[update.from_user.id]
    delete_rslt = await req_for_get_payment(payment_for_dlt_id=user_payment_obj.bill_id)
    if not delete_rslt:     # Если не удалось удалить
        await update.edit_message_text(
            text=f'🚧<b>Не удалось отменить платёж.</b>\n\n'
                 f'Будем благодарны, если сообщите нам об этой проблеме. Так мы сможем быстрее всё починить',
            reply_markup=BACK_TO_HEAD_PAGE_KBRD
        )
        return

    await update.edit_message_text(
        text=f'🗑Платёж удалён.',
        reply_markup=BACK_TO_HEAD_PAGE_KBRD
    )


