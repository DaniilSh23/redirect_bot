from pyrogram import filters

from settings.config import MY_LOGGER, STATES_STORAGE_DCT


async def func_choose_pay_method(_, __, query):
    """
    Функция фильтрации для хэндлера choose_pay_method_handler
    """
    return query.data == 'replenish_balance'


async def func_ask_pay_amount(_, __, query):
    """
    Функция фильтрации для хэндлера ask_pay_amount_handler
    """
    return query.data.split()[0] == 'pay_method'


async def func_write_pay_amount(_, __, message):
    """
    Функция фильтрации для хэндлера write_pay_amount
    """
    if STATES_STORAGE_DCT.get(message.from_user.id):
        return STATES_STORAGE_DCT.get(message.from_user.id) == 'send_amount_for_replenish_balance'


async def confirm_payment_func(_, __, query):
    """
    Функция для фильтрации апдейтов для хэндлера confirm_payment_handler
    """
    return query.data == 'confirm_payment'


async def cancel_payment_func(_, __, query):
    """
    Функция фильтра для хэндлера cancel_payment_handler.
    """
    return query.data == 'cancel_payment'


async def pay_to_card_send_data_func(_, __, query):
    """
    Функция фильтра для хэндлера pay_to_card_send_data_handler.
    """
    return query.data.startswith("pay_to_card")


async def ask_pay_to_card_confirmation_func(_, __, query):
    """
    Фукнция фильтра для хэндлера ask_pay_to_card_confirmation_handler.
    """
    return query.data == 'i_payd_to_card'


async def pay_to_card_confirmation_func(_, __, query):
    """
    Фукнция фильтра для хэндлера pay_to_card_confirmation_handler.
    """
    if STATES_STORAGE_DCT.get(query.from_user.id):
        return STATES_STORAGE_DCT.get(query.from_user.id) == 'pay_to_card_confirmation'


async def decline_card_payment_func(_, __, query):
    """
    Фукнция фильтра для хэндлера decline_card_payment_handler.
    """
    if len(query.data.split()) == 2:
        return query.data.split()[0] == 'decline_card_payment'


async def ask_amount_for_confirm_card_payment_func(_, __, query):
    """
    Фукнция фильтра для хэндлера ask_amount_for_confirm_card_payment_handler.
    """
    if len(query.data.split()) == 2:
        return query.data.split()[0] == 'confirm_card_payment'


async def confirm_card_payment_func(_, __, query):
    """
    Фукнция фильтра для хэндлера confirm_card_payment_handler.
    """
    if STATES_STORAGE_DCT.get(query.from_user.id):
        return STATES_STORAGE_DCT.get(query.from_user.id) == 'ask_card_replenish_amount'


filters_choose_pay_method = filters.create(func_choose_pay_method)
filter_ask_pay_amount = filters.create(func_ask_pay_amount)
filter_write_pay_amount = filters.create(func_write_pay_amount)
confirm_payment_filter = filters.create(confirm_payment_func)
cancel_payment_filter = filters.create(cancel_payment_func)
pay_to_card_send_data_filter = filters.create(pay_to_card_send_data_func)
ask_pay_to_card_confirmation_filter = filters.create(ask_pay_to_card_confirmation_func)
pay_to_card_confirmation_filter = filters.create(pay_to_card_confirmation_func)
decline_card_payment_filter = filters.create(decline_card_payment_func)
ask_amount_for_confirm_card_payment_filter = filters.create(ask_amount_for_confirm_card_payment_func)
confirm_card_payment_filter = filters.create(confirm_card_payment_func)
