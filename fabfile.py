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
API_ID={resurrection_data.get("API_ID")}
API_HASH={resurrection_data.get("API_HASH")}
TOKEN={resurrection_data.get("TOKEN")}
BASE_HOST_URL=http://31.129.107.237/
SECRET_QIWI_P2P=write_it_when_the_time_comes
CRYSTAL_PAY_LOGIN={resurrection_data.get("CRYSTAL_PAY_LOGIN")}
CRYSTAL_PAY_SECRET1={resurrection_data.get("CRYSTAL_PAY_SECRET1")}
CRYSTAL_PAY_SECRET2={resurrection_data.get("CRYSTAL_PAY_SECRET2")}
SECNDS_BETWEEN_REQUEST=1
REQ_COUNT=4
FEEDBACK_CHAT_URL={resurrection_data.get("FEEDBACK_CHAT_URL")}
BOT_VOLUME_PATH={resurrection_data.get("BOT_VOLUME_PATH")}
              '''

    url = "http://31.129.107.237/get_up_bot/"

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

    with Connection(host='31.129.107.237', user='root',
                    connect_kwargs={"key_filename": "./redir_bot_ssh_key"}) as connection:
        with connection.cd(path='/home/bot_usr/redirect_bot/'):
            connection.run(f"echo '{env_data}' > .env")
            connection.run("docker compose down")   # Останавливаем контейнер
            connection.run("docker compose up --build -d")  # Перезапускаем и собираем контейнер
