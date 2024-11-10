import logging
import asyncio

from aiogram import Bot, Dispatcher

from app.db import db_start

dp = Dispatcher()
logger = logging.getLogger(__name__)

async def on_startup() -> None:
    await db_start()

async def main() -> None:
    bot = Bot()
    
    dp.startup.register(on_startup)
    await dp.start_polling(bot, skip_updtes=False)


if __name__ == '__main__':
    logger.info('[RITM BOT] BOT LAUNCHED...')
    asyncio.run(main())
    logger.info('[RITM BOT] BOT SHUT DOWN!')