import asyncio
import logging
from aiogram import Bot, Dispatcher

from juridical_bot.bot_dir.bot import wbot
from juridical_bot.bot_dir.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(wbot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())