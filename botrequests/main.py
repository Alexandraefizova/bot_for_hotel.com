from aiogram.utils import executor
import os
import sys
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiogram
from aiogram import Bot, Dispatcher
from decouple import UndefinedValueError
from loguru import logger

try:
    from botrequests.settings import TOKEN, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
except (UndefinedValueError, aiogram.exceptions.Unauthorized):
    logger.warning('Token can not be empty')


loop = asyncio.get_event_loop()

try:
    bot = Bot(TOKEN)
except NameError:
    logger.warning('Token can not be empty')
    sys.exit(1)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logger.add(os.sep.join(('log', 'file_{time}.log')))

if __name__ == '__main__':
    from botrequests.handlers import dp, on_shutdown, on_startup

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )