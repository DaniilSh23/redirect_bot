import aiohttp
from loguru import logger


async def post_req_to_keitaro_for_get_stat_by_comp_id(company_id, period='today'):
    """
    POST запрос к KEITARO для получения статистике по ID компании.
    """

    # TODO: изменил запрос под API Keitaro, если будут проблемы, то старые строки пока оставлю закоменченными

    # url = "http://45.9.40.104/admin/?bulk="
    url = "http://212.8.244.17/admin_api/v1/report/build"

    # payload = [
    #     # {
    #     #     "method": "GET",
    #     #     "object": "reports.parameterAliases",qiwi_create_invoice
    #     #     "campaign_id": f"{company_id}"
    #     # },
    #     # Получаем данные по кликам на ссылку
    #     {
    #         "method": "POST",
    #         "postData": {
    #             'range': {'interval': period, 'timezone': 'Europe/Moscow', "from": None, "to": None},
    #             'columns': [],
    #             'metrics': ['clicks', 'stream_unique_clicks', 'bots'],
    #             'grouping': ['stream'],
    #             'filters': [{'name': 'campaign_id', 'operator': 'EQUALS', 'expression': f"{company_id}"}],
    #             'summary': True,
    #             'limit': 100,
    #             'offset': 0
    #         },
    #         "object": "reports.build"
    #     },
    #     # Получаем данные о компании (нужна оригинальная ссылка и ID компании
    #     {
    #         "method": "GET",
    #         "object": "campaigns.show",
    #         "id": f"{company_id}"
    #     }
    # ]

    payload = {
        "range": {
            "interval": period,
            "timezone": "Europe/Moscow",
            "from": None,
            "to": None
        },
        "columns": [],
        "metrics": ["clicks", "stream_unique_clicks", "bots"],
        "grouping": ["stream"],
        "filters": [
            {
                "name": "campaign_id",
                "operator": "EQUALS",
                "expression": company_id
            }
        ],
        "summary": True,
        "limit": 100,
        "offset": 0
    }

    # headers = {
    #     "Accept": "application/json, text/plain, */*",
    #     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
    #     "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    #     "Content-Type": "application/json;charset=utf-8",
    #     "Cookie": "states=v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjhkMTk0NjRiMTY3ZTZkMjljZTQ5NGFhYWRjNGJm"
    #               "NWZkIiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0a3FlTEh3TnNtOVJpUjBXbzRmcVNjLjRrZFczSW5WMTlxYWVnd0hIbUtXdEd"
    #               "2alF3WVFhZEMiLCJ0aW1lc3RhbXAiOjE2ODMwNTI3OTd9.sF1fc6r5ugMcKso4aPzVhbFlX5VxP04gnJqfoyKuHGk",
    #     "Referer": "http://45.9.40.104/admin/?",
    #     "Connection": "keep-alive",
    #     "Origin": "http://45.9.40.104",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Host": "45.9.40.104"
    # }

    headers = {
        "Accept": "application/json",
        "Api-Key": "75c0ed8290b1cfd6778c3c63c6db44e7",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, json=payload) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос к KEITARO для сбора статистики')
                return await response.json()
            else:
                logger.warning(f'Неудачный запрос к KEITARO для сбора статистики. company_id == {company_id}')
                return False
