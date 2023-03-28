from pyrogram import filters

from settings.config import STATES_STORAGE_DCT


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


filters_choose_pay_method = filters.create(func_choose_pay_method)
filter_ask_pay_amount = filters.create(func_ask_pay_amount)
filter_write_pay_amount = filters.create(func_write_pay_amount)
confirm_payment_filter = filters.create(confirm_payment_func)
cancel_payment_filter = filters.create(cancel_payment_func)