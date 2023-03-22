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


async def func_filter_rating_without_comment(_, __, query):
    """Фильтр для обработки нажатия на кнопку БЕЗ КОММЕНТАРИЕВ. Это когда клиент не хочет комментировать свою оценку"""
    return query.data == 'no_rating_comments'


filter_rating_without_comment = filters.create(func_filter_rating_without_comment)
filter_throttling_middleware = filters.create(throttling_middleware)
