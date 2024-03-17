from pyrogram import filters


async def func_faq_handler(_, __, query):
    """
    Фильтр для хэндлера faq_handler
    """
    return query.data == 'faq_btn'


async def func_support_handler(_, __, query):
    """
    Фильтр для хэндлера support_btn
    """
    return query.data == 'support_btn'


async def func_my_balance_handler(_, __, query):
    """
    Фильтр для хэндлера my_balance_handler
    """
    return query.data == 'my_balance'


async def get_transactions_func(_, __, query):
    """
    Фильтр для хэндлера получения транзакций.
    """
    return query.data == 'transactions_story'


async def change_language_func(_, __, query):
    """
    Фильтр для хэндлера смены языка.
    """
    return query.data == "change_lang"


async def set_new_language_func(_, __, query):
    """
    Фильтр для хэндлера установки нового языка интерфейса пользователя.
    """
    return query.data.startswith("set_lang")


filter_for_faq_handler = filters.create(func_faq_handler)
filter_for_support_handler = filters.create(func_support_handler)
filter_for_my_balance_handler = filters.create(func_my_balance_handler)
get_transactions_filter = filters.create(get_transactions_func)
change_language_filter = filters.create(change_language_func)
set_new_language_filter = filters.create(set_new_language_func)
