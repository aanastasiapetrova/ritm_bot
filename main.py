import logging
import asyncio

from aiogram import Bot, Dispatcher

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, TIMEZONE
from router import basic_router
from app.db import db_start
from script import track_subs

dp = Dispatcher()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
dp.include_router(basic_router)


async def on_startup() -> None:
    await db_start()

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # TODO: make a cron schedule (9 am)
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(track_subs, 'interval', seconds=20, kwargs={"bot": bot})
    scheduler.start()
    
    dp.startup.register(on_startup)
    await dp.start_polling(bot, skip_updtes=False)


if __name__ == '__main__':
    logger.info('[RITM BOT] BOT LAUNCHED...')
    asyncio.run(main())
    logger.info('[RITM BOT] BOT SHUT DOWN!')