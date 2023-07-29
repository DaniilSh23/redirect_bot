import asyncio

from pyrogram import Client

from settings.config import TOKEN, API_ID, API_HASH

api_id = API_ID
api_hash = API_HASH
bot_token = TOKEN


# app = Client(
#     "test_bot",
#     api_id=api_id, api_hash=api_hash,
#     bot_token=bot_token
# )
#
# app.run()

async def main():
    async with Client("test_bot", api_id, api_hash, bot_token=bot_token) as app:
        rslt = await app.get_me()
        print(f'Создали сессию и получили инфу о себе: {rslt!r}')


asyncio.run(main())
