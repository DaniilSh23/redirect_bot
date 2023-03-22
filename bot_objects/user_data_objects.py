import re
from secondary_functions.req_to_bot_api import post_user_data


class User:
    """Класс пользователя бота"""

    def __init__(self, tlg_id, deal_id, tlg_username, is_staff=False,
                 telephone=None, email=None, state_name=None, passport_data=None, snils=None,
                 passport_issued_by=None,
                 ):
        """
        Конструктор класса пользователя бота
        :param tlg_id: int - Telegram ID пользователя
        :param deal_id: int - ID сделки, с которым пользователь запустил бота
        :param tlg_username: str - Telegram username пользователя бота
        :param is_staff: bool - Флаг, является ли пользователь персоналом(на перспективу)
        :param telephone: str - Контактный номер телефона клиента
        :param email: str - Контактный email клиента
        """
        self.tlg_id = tlg_id
        self.deal_id = deal_id
        self.tlg_username = tlg_username
        self.is_staff = is_staff
        self.telephone = telephone
        self.email = email
        self.state_name = state_name

    async def get_telephone(self):
        """Геттер для аттрибута telephone"""
        return self.telephone

    async def set_telephone(self, telephone):
        """
        Сеттер для аттрибута telephone.
        Проверяет на соответствие регулярке и возвращает True/False.
        :param telephone: str - Номер телефона
        :return: bool
        """

        reg = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        if re.match(reg, telephone):
            self.telephone = telephone
            return True
        else:
            return False

    async def get_email(self):
        """Геттер для email"""
        return self.email

    async def set_email(self, email):
        """
        Сеттер для email. Проверяет на соответствие регулярке и возвращает True/False
        :param email:
        :return: bool
        """
        reg = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.match(reg, email):
            self.email = email
            return True
        else:
            return False

    async def write_user_in_db(self):
        """Метод для записи информации о пользователе в БД"""
        fields_for_req = {
            'tlg_id': self.tlg_id,
            'tlg_username': self.tlg_username,
            'telephone': self.telephone,
            'email': self.email,
            'deal_id': self.deal_id,
            'is_staff': self.is_staff,
        }
        user_data = dict()
        for i_key, i_value in fields_for_req.items():
            if i_value:
                user_data[i_key] = i_value
        result = await post_user_data(user_data)
        return result
