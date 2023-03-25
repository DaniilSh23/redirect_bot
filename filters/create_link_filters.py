from pyrogram import filters

from settings.config import STATES_STORAGE_DCT


async def func_create_link_btn(_, __, query):
    """
    Функция для фильтра, используемого в хэндлере create_link_btn_handler.
    """
    return query.data == 'create_link'


async def func_get_doc_with_links(_, __, message):
    """
    Функция для фильтрации сообщений с документами.
    Ловим документ, в котором должны быть ссылки.
    Для этого проверяем установленный стэйт для юзера.
    """
    if STATES_STORAGE_DCT.get(message.from_user.id):
        return STATES_STORAGE_DCT[message.from_user.id] == 'upload_file_with_links'


async def func_waiting_file_processing(_, __, message):
    """
    Функция, которая фильтрует сообщения для хэндлера waiting_file_processing.
    """
    if STATES_STORAGE_DCT.get(message.from_user.id):
        return STATES_STORAGE_DCT[message.from_user.id][0] == 'waiting_file_processing'


async def func_minus_redirect(_, __, query):
    """
    Функция, которая фильтрует колбэки для хэндлера minus_redirect_handler.
    """
    if len(query.data.split()) == 2:
        return query.data.split()[0] == 'minus_redirect'


async def func_plus_redirect(_, __, query):
    """
    Функция, которая фильтрует колбэки для хэндлера plus_redirect_handler.
    """
    if len(query.data.split()) == 2:
        return query.data.split()[0] == 'plus_redirect'


async def func_link_shortening(_, __, query):
    """
    Функция для фильтрации колбэков для хэндлера choosing_link_shortening_service_handler
    """
    return query.data == 'to_link_shortening'


filter_for_create_link_btn_handler = filters.create(func_create_link_btn)
filter_for_get_doc_with_links_handler = filters.create(func_get_doc_with_links)
filter_for_waiting_file_processing_handler = filters.create(func_waiting_file_processing)
filter_minus_redirect_handler = filters.create(func_minus_redirect)
filter_plus_redirect_handler = filters.create(func_plus_redirect)
filter_link_shortening_handler = filters.create(func_link_shortening)
