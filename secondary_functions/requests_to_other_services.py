import aiohttp
from loguru import logger


async def post_req_to_keitaro_for_get_stat_by_comp_id(company_id):
    """
    POST запрос к KEITARO для получения статистике по ID компании.
    """
    url = "http://45.9.40.104/admin/?bulk="
    payload = [
        # {
        #     "method": "GET",
        #     "object": "reports.parameterAliases",
        #     "campaign_id": f"{company_id}"
        # },
        # Получаем данные по кликам на ссылку
        {
            "method": "POST",
            "postData": {
                'range': {'interval': 'today', 'timezone': 'UTC'},
                'columns': [],
                'metrics': ['clicks', 'stream_unique_clicks', 'bots'],
                'grouping': ['stream'],
                'filters': [{'name': 'campaign_id', 'operator': 'EQUALS', 'expression': f"{company_id}"}],
                'summary': True,
                'limit': 100,
                'offset': 0
            },
            "object": "reports.build"
        },
        # Получаем  данные о компании (нужна оригинальная ссылка и ID компании
        {
            "method": "GET",
            "object": "campaigns.show",
            "id": f"{company_id}"
        }
    ]
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/json;charset=utf-8",
        "Cookie": "states=v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjhkMTk0NjRiMTY3ZTZkMjljZTQ5NGFhYWRjNGJm"
                  "NWZkIiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0RmlpVUNaV1FKdDh4SG96YWlBMVJRZUppaUFEZE9PNEs0biUyRmJ1TGw3aE"
                  "xyS1Y4SiUyRkwuQlF1IiwidGltZXN0YW1wIjoxNjgwMjU5NjUyfQ.G-V2Fju3RSC0OrGUytXxPsMH16YsxdKFaA_v9aFr4Zc",
        "Referer": "http://45.9.40.104/admin/?",
        "Connection": "keep-alive",
        "Origin": "http://45.9.40.104",
        "Accept-Encoding": "gzip, deflate",
        "Host": "45.9.40.104"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, json=payload) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос к KEITARO для сбора статистики')
                return await response.json()
            else:
                logger.warning(f'Неудачный запрос к KEITARO для сбора статистики. company_id == {company_id}')
                return False
