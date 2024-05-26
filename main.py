import asyncio
import logging
from aiogram import Bot, Dispatcher

from juridical_bot.bot_dir.bot import wbot
from juridical_bot.bot_dir.config import BOT_TOKEN

logging.basicConfig(
    filename=LOGS,
    level=logging.INFO,
    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s",
    filemode="w",
)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(wbot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())