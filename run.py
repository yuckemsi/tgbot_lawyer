import os
import asyncio
import logging

from app.handlers import rt

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

import app.database.db as db



async def main():
    load_dotenv()
    await db.connect()
    dp = Dispatcher()
    bot = Bot(token=os.getenv('TOKEN'))
    dp.include_router(rt)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот отключен')