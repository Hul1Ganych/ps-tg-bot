"""Main telegram bot file."""

import asyncio
import logging
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from configs.bot_config import config
from src.handlers import prediction, welcome


async def main():
    """Bot event loop function."""
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(welcome.router)
    dp.include_router(prediction.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
