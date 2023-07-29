FROM python:3.10-slim

RUN mkdir /bot

COPY requirements.txt /bot/

RUN python -m pip install -r /bot/requirements.txt

COPY . /bot/

WORKDIR /bot

RUN ["python", "bot_authorization.py"]

ENTRYPOINT ["python", "main.py"]
