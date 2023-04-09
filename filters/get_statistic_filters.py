from pyrogram import filters

from settings.config import STATES_STORAGE_DCT


async def func_ask_user_for_comp_id(_, __, query):
    """
    Функция для фильтрации апдейтов, адресованных для ask_user_for_company_id_handler.
    """
    return query.data == 'get_statistic'


async def func_get_statistic_from_keitaro(_, __, message):
    """
    Функция для фильтрации апдейтов, когда юзер отправляет сообщением ID компании для получения статистики.
    """
    if STATES_STORAGE_DCT.get(message.from_user.id) == 'send_company_id_for_get_statistic':
        return True


async def get_statistic_from_period_filter_func(_, __, query):
    """
    Фукнция фильтрации для хэндлера get_statistic_from_period
    """
    return query.data.split()[0] == 'stat_period'


filter_ask_user_for_comp_id = filters.create(func_ask_user_for_comp_id)
filter_get_statistic_from_keitaro = filters.create(func_get_statistic_from_keitaro)
get_statistic_from_period_filter = filters.create(get_statistic_from_period_filter_func)
