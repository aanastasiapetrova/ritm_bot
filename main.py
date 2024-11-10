import logging
import asyncio

from aiogram import Bot, Dispatcher

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.db import db_start
from config import BOT_TOKEN
from router import basic_router
from app.db import db_start

dp = Dispatcher()
logger = logging.getLogger(__name__)
dp = Dispatcher()
dp.include_router(basic_router)


async def on_startup() -> None:
    await db_start()

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp.startup.register(on_startup)
    await dp.start_polling(bot, skip_updtes=False)


if __name__ == '__main__':
    logger.info('[RITM BOT] BOT LAUNCHED...')
    asyncio.run(main())
    logger.info('[RITM BOT] BOT SHUT DOWN!')