import json

import requests
from fabric import Connection, task


@task
def fenix(ctx):
    """
   Функция для восстановления бота, после сноса.
   """
    # Открываем json с данными для восстановления
    with open('bot_restart.json') as json_file:
        resurrection_data = json.load(json_file)
        env_data = f'''
API_ID=6
API_HASH=eb06d4abfb49dc3eeb1aeb98ae0f581e
TOKEN={resurrection_data.get("TOKEN")}
BASE_HOST_URL=http://45.12.237.138/
SECRET_QIWI_P2P=write_it_when_the_time_comes
CRYSTAL_PAY_LOGIN={resurrection_data.get("CRYSTAL_PAY_LOGIN")}
CRYSTAL_PAY_SECRET1={resurrection_data.get("CRYSTAL_PAY_SECRET1")}
CRYSTAL_PAY_SECRET2={resurrection_data.get("CRYSTAL_PAY_SECRET2")}
SECNDS_BETWEEN_REQUEST=1
REQ_COUNT=4
FEEDBACK_CHAT_URL={resurrection_data.get("FEEDBACK_CHAT_URL")}
              '''

    url = "http://45.12.237.138/get_up_bot/"

    payload = {
        "recovery_token": resurrection_data.get("recovery_token"),
        "bot_token": resurrection_data.get("TOKEN"),
        "feedback_link": resurrection_data.get("FEEDBACK_CHAT_URL"),
        "support_username": resurrection_data.get("support_username"),
        "who_approves_payments": resurrection_data.get("who_approves_payments"),
        "redirect_bot_admin": resurrection_data.get("redirect_bot_admin")
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print('НЕУДАЧНЫЙ ЗАПРОС К ВЕБ-ПРИЛОЖЕНИЮ ДЛЯ ИЗМЕНЕНИЯ НАСТРОЕК БОТА!')
        return

    with Connection(host='45.12.237.138', user='root',
                    connect_kwargs={"key_filename": "./redir_bot_ssh_key"}) as connection:
        with connection.cd(path='/home/redirect_bot/redirect_bot/'):
            connection.run(f"echo '{env_data}' > .env")
            connection.run("docker-compose down")   # Останавливаем контейнер
            connection.run("docker-compose up --build -d")  # Перезапускаем и собираем контейнер
