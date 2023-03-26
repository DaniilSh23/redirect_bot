import datetime

from pyrogram import filters

from settings.config import BLACK_LIST, USERS_REQ_DCT, SECNDS_BETWEEN_REQUEST


async def throttling_middleware(_, __, update):
    """
    Throttling middleware, реализованный через фильтр.
    Если юзер делает много запросов, то тормозим его.
    """
    if update.from_user.id not in BLACK_LIST.keys():  # Если tlg_id нет в чёрном списке
        last_user_request = USERS_REQ_DCT.get(update.from_user.id)
        if last_user_request:   # Если юзер ранее делал запросы
            seconds_between_req = (datetime.datetime.now() - last_user_request).seconds
            if seconds_between_req <= SECNDS_BETWEEN_REQUEST:    # Если крайний запрос был менее, чем N сек назад
                USERS_REQ_DCT[update.from_user.id] = datetime.datetime.now()
                return True
            else:   # Иначе, юзер действует в рамках правил
                USERS_REQ_DCT[update.from_user.id] = datetime.datetime.now()
                return False
        else:   # Если юзер ещё не делал запросов
            USERS_REQ_DCT[update.from_user.id] = datetime.datetime.now()
            return False
    else:   # Если юзер есть в блэк-листе
        block_time = BLACK_LIST[update.from_user.id]
        delta = datetime.datetime.now() - block_time
        if delta.days < 0:  # Если блокировка ещё действует
            return True
        else:   # Блокировка закончилась
            BLACK_LIST.pop(update.from_user.id)     # Удаляем юзера из блэк-листа
            return False


async def func_cancel_and_clear_state(_, __, query):
    """
    Функция фильтрации для нажатия кнопки 'Отменить.'.
    Это фильтр для хэндлера cancel_and_clear_state_handler.
    """
    return query.data == 'cancel_and_clear_state'


async def func_back_to_head_page(_, __, query):
    """
    Функция фильрации для хэндлера back_to_head_page_handler.
    """
    return query.data == 'back_to_head_page'


# filter_rating_without_comment = filters.create(func_filter_rating_without_comment)
filter_throttling_middleware = filters.create(throttling_middleware)
filter_for_cancel_and_clear_state = filters.create(func_cancel_and_clear_state)
filter_back_to_head_page = filters.create(func_back_to_head_page)
