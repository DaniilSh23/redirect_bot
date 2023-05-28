import datetime

from glQiwiApi import QiwiP2PClient
from secondary_functions.crystalpay_sdk import CrystalPAY, InvoiceType

from secondary_functions.req_to_bot_api import post_for_create_payment, post_for_change_balance
from settings.config import SECRET_QIWI_P2P, CRYSTAL_PAY_LOGIN, CRYSTAL_PAY_SECRET1, CRYSTAL_PAY_SECRET2, MY_LOGGER


class UserPayments:
    """
    Класс для хранения инфы о платежах и реализации некоторых действий с ними.
    """
    def __init__(self, pay_system_type, tlg_id, amount=None, bill_id=None, bill_expire_at=None, bill_status=False,
                 bill_url=None):
        self.tlg_id = tlg_id
        self.pay_system_type = pay_system_type
        self.amount = amount
        self.bill_id = bill_id
        self.bill_expire_at = bill_expire_at
        self.bill_status = bill_status
        self.bill_url = bill_url

    async def qiwi_create_invoice(self):
        """
        Создание счёта на оплату через QIWI
        """
        # Создание платежа и взаимодействие по нему с пользователем
        async with QiwiP2PClient(secret_p2p=SECRET_QIWI_P2P) as p2p:
            bill = await p2p.create_p2p_bill(amount=self.amount)
            self.bill_id = bill.id
            self.bill_expire_at = bill.expire_at
            self.bill_url = bill.pay_url
        return self.bill_url

    async def check_qiwi_invoice(self):
        """
        Проверка статуса оплаты счёта.
        """
        async with QiwiP2PClient(secret_p2p=SECRET_QIWI_P2P) as p2p:
            bill_status = await p2p.get_bill_status(bill_id=self.bill_id)
            if bill_status == 'WAITING':
                return 'ожидает оплаты'
            elif bill_status == 'PAID':
                self.bill_status = True
                return 'оплачен'
            elif bill_status == 'REJECTED':
                return 'отклонён'
            elif bill_status == 'EXPIRED':
                return 'истёк'

    async def crystalpay_create_invoice(self):
        """
        Создание платежного счёта в crystal pay.
        """
        crystalpay_api = CrystalPAY(CRYSTAL_PAY_LOGIN, CRYSTAL_PAY_SECRET1, CRYSTAL_PAY_SECRET2)
        bill = crystalpay_api.Invoice.create(amount=self.amount,
                                             type_=InvoiceType.purchase,
                                             lifetime=15,
                                             description=f"Пополнение баланса на {self.amount} руб.")
        self.bill_id = bill.get("id")
        self.bill_url = bill.get("url")
        # Получаем инфу о счёте, чтобы достать expire_at
        bill_info = crystalpay_api.Invoice.getinfo(self.bill_id)
        # Преобразуем строку в объект datetime и сохраняем в классе
        # self.bill_expire_at = datetime.datetime.strptime(bill_info.get("expired_at"), '%Y-%m-%d %H:%M:%S')
        self.bill_expire_at = bill_info.get("expired_at")
        return self.bill_url

    async def check_crystalpay_invoice(self):
        """
        Проверка статуса счёта crystal pay.
        """
        crystalpay_api = CrystalPAY(CRYSTAL_PAY_LOGIN, CRYSTAL_PAY_SECRET1, CRYSTAL_PAY_SECRET2)
        # Получаем инфу о счёте, достаём статус оплаты
        bill_info = crystalpay_api.Invoice.getinfo(self.bill_id)

        bill_state = bill_info.get('state')
        MY_LOGGER.debug(f'Ответ crystalpay при запросе статуса платежа: {bill_state}')

        if bill_state == 'notpayed':
            pay_status = 'Не оплачен'
        elif bill_state == 'payed':
            self.bill_status = True
            pay_status = 'Оплачен'
        elif bill_state == 'processing':
            pay_status = 'Платёж в обработке'
        elif bill_state == 'wrongamount':
            pay_status = 'Требуется доплата, поступила не вся сумма'
        elif bill_state == 'failed':
            pay_status = 'Ошибка с платежом, подробнее на странице оплаты'
        return pay_status

    async def create_payment_in_db(self):
        """
        Метод для создания записи о платеже в БД.
        """
        data = {
            "tlg_id": self.tlg_id,
            "pay_system_type": self.pay_system_type,
            "amount": self.amount,
            "bill_id": self.bill_id,
            "bill_expire_at": self.bill_expire_at,
            "bill_status": self.bill_status,
            "bill_url": self.bill_url,
        }
        MY_LOGGER.debug(f'Данные, которые отправляем при создании/изменении записи о платеже в БД: {data}')
        response = await post_for_create_payment(data=data)
        MY_LOGGER.debug(f'Результат при создании/изменении записи о платеже в БД: {response}')
        if response:
            return True

    async def add_funds_to_balance(self, description):
        """
        Метод для начисления средств на баланс юзера.
        """
        data = {
            "action": "+",
            "tlg_id": self.tlg_id,
            "value": self.amount,
            "description": description,
        }
        MY_LOGGER.debug(f'Данные, которые отправляем при начислении средств на баланс: {data}')
        return await post_for_change_balance(data=data)
