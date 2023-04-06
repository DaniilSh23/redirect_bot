import datetime
import time

from pyrogram import filters

from settings.config import BLACK_LIST, USERS_REQ_DCT, SECNDS_BETWEEN_REQUEST, REQ_COUNT


async def throttling_middleware(_, __, update):
    """
    Throttling middleware, реализованный через фильтр.
    Если юзер делает много запросов, то тормозим его.
    """
    if update.from_user.id not in BLACK_LIST.keys():  # Если tlg_id нет в чёрном списке
        last_user_request = USERS_REQ_DCT.get(update.from_user.id)

        if last_user_request:   # Если юзер ранее делал запросы
            last_user_request[1] += 1   # Добавляем один запрос
            seconds_between_req = time.time() - last_user_request[0]

            # Если юзер нарушает
            if seconds_between_req <= SECNDS_BETWEEN_REQUEST and last_user_request[1] >= REQ_COUNT:
                USERS_REQ_DCT.pop(update.from_user.id)
                return True
            # Если не нарушает правила по флуду, но нужно обнулить счётчик запросов
            elif seconds_between_req > SECNDS_BETWEEN_REQUEST and last_user_request[1] < REQ_COUNT:
                USERS_REQ_DCT[update.from_user.id] = [time.time(), 1]
                return False
            # Если временной интервал ещё не закончился, но и запросов немного
            elif seconds_between_req < SECNDS_BETWEEN_REQUEST and last_user_request[1] < REQ_COUNT:
                return False

        else:   # Если юзер ещё не делал запросов
            USERS_REQ_DCT[update.from_user.id] = [time.time(), 1]
            return False

    else:   # Если юзер есть в блэк-листе
        block_time = BLACK_LIST[update.from_user.id]
        delta = datetime.datetime.now() - block_time
        if delta.days < 0:  # Если блокировка ещё действует
            return True
        else:   # Блокировка закончилась
            BLACK_LIST.pop(update.from_user.id)     # Удаляем юзера из блэк-листа
            USERS_REQ_DCT[update.from_user.id] = [time.time(), 1]   # Устанавливаем ему стартовую точку
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
