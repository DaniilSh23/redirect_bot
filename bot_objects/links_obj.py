import datetime

from secondary_functions.req_to_bot_api import post_for_create_link_set, update_or_create_link, post_for_start_wrapping


class RedirectLinks:
    """
    Класс, в котором храним инфу, необходимую для создания редиректа для ссылок.
    """
    def __init__(self, tlg_id, links: str, tariff, balance, redirect_numb, total_price, short_link_service=None):
        self.tlg_id = tlg_id    # TG ID юзера
        self.links = links  # ссылки через пробел
        self.tariff = float(tariff)     # тариф
        self.balance = float(balance)   # баланс
        self.redirect_numb = float(redirect_numb)   # кол-во редиректов
        self.total_price = float(total_price)   # итоговая цена
        self.short_link_service = short_link_service    # сервис для сокращения ссылок
        self.link_set_id = None     # ID набора ссылок (из БД)

    async def create_link_set(self):
        """
        Метод для создания в БД набора ссылок.
        """
        response = await post_for_create_link_set(data={
            'id': None,
            'tlg_id': self.tlg_id,
            'title': f'Набор ссылок от {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'
        })
        if response:
            self.link_set_id = response.get('id')
            return True
        else:
            return False

    async def create_links(self):
        """
        Метод для создания в БД записей о ссылках.
        """
        # Через list comprehension наполняем запрос списком из данных, необходимых для создания записи об 1 ссылке
        response = await update_or_create_link(data=[{
            'id': None,
            'tlg_id': self.tlg_id,
            'link_set_id': self.link_set_id,
            'link': i_link,
            'redirect_numb': self.redirect_numb,
        } for i_link in self.links.split()])
        if response:
            return True
        else:
            return False

    async def start_wrapping(self):
        """
        Метод для старта обёртки ссылок.
        """
        return await post_for_start_wrapping(data={
            'link_set_id': self.link_set_id
        })
