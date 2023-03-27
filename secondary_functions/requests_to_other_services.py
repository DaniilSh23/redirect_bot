import aiohttp
from loguru import logger


async def post_req_to_keitaro_for_get_stat_by_comp_id(company_id):
    """
    POST запрос к KEITARO для получения статистике по ID компании.
    """
    url = "http://185.198.167.20/admin/?bulk="
    payload = [
        {
            "method": "GET",
            "object": "reports.parameterAliases",
            "campaign_id": f"{company_id}"
        },
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
        {
            "method": "GET",
            "object": "campaigns.show",
            "id": f"{company_id}"
        }
    ]
    headers = {
        "cookie": "keitaro=jaa79fju1sil2umql63d2m6653",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/json;charset=utf-8",
        "Cookie": "states=v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjhkMTk0NjRiMTY3ZTZkMjljZTQ5NGFhYWRj"
                  "NGJmNWZkIiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0bDZvQmFTaFN6TTl0Lm9ISDBjR1k1LkQybUh6dlR6Ljl5aGVPNSUyRk"
                  "RtYWl6Mlp4LkxEbTNBeSIsInRpbWVzdGFtcCI6MTY3OTEzNDEzNH0.PCDnkcFsZWg7C5fuGDsswE6ohyr2s1DnYETg17SJp_U;"
                  " streamsView=true; streamsSharesVisible=false; keitaro=c6mtduund16i8qdj8tt5ef52m1",
        "Referer": "http://185.198.167.20/admin/",
        "Connection": "keep-alive",
        "Origin": "http://185.198.167.20",
        "Content-Length": "473",
        "Accept-Encoding": "gzip, deflate",
        "Host": "185.198.167.20"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, json=payload) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос к KEITARO для сбора статистики')
                return await response.json()
            else:
                logger.warning(f'Неудачный запрос к KEITARO для сбора статистики. company_id == {company_id}')
                return False
