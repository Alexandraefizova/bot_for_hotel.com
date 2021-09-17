import aiogram
from aiogram.utils import executor
from decouple import UndefinedValueError
from loguru import logger

from botrequests.middleware import ThrottlingMiddleware

try:
    from botrequests.settings import TOKEN, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
except (UndefinedValueError, aiogram.exceptions.Unauthorized):
    logger.warning('Token can not be empty')


if __name__ == '__main__':
    from botrequests.handlers import on_startup, on_shutdown
    from botrequests.loader import dp

    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
