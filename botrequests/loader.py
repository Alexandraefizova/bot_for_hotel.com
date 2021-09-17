import asyncio
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from .settings import TOKEN

loop = asyncio.get_event_loop()

try:
    bot = Bot(TOKEN)
except NameError:
    logger.warning('Token can not be empty')
    sys.exit(1)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logger.add(os.sep.join(('log', 'file_{time}.log')))