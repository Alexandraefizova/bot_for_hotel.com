from botrequests.main import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode
from loguru import logger
from botrequests.messages import MESSAGES
from botrequests.rapidapi import RapidApi
from botrequests.settings import ADMIN_ID, WEBHOOK_URL


async def send_to_admin(dp):
    """
    Menu with commands
    :param dp:
    :return:
    """
    await bot.send_message(ADMIN_ID, text='Bot launched click '
                                          '\n/start - see Bot description'
                                          ' \n/help - go directly to commands')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    await send_to_admin(dp)


async def on_shutdown(dp):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.warning('Bye!')


class Form(StatesGroup):
    """
    States
    """
    city = State()  # Will be represented in storage as 'Form:city'
    count = State()  # Will be represented in storage as 'Form:count_hotels'


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message) -> None:
    """
    Start command
    :param message:
    :return:
    """
    logger.info(MESSAGES['start'])
    await message.reply(MESSAGES['start'])


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    """
    Help command
    :param message:
    :return:
    """
    logger.info(MESSAGES['help'])
    await message.reply(MESSAGES['help'], parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
async def cmd_start(message: types.Message) -> None:
    """
    City to search
    :param message:
    :return:
    """
    await message.reply("Please enter the city to search for?")
    await Form.city.set()


@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext) -> None:
    """
    The number of hotels
    :param message:
    :param state:
    :return:
    """
    answer = message.text
    async with state.proxy() as data:
        data['city'] = answer

    await message.answer("Please enter the number of hotels to search for?")
    await Form.next()


@dp.message_handler(lambda message: not message.text.isdigit(),
                    state=Form.count)
async def process_count_invalid(message: types.Message):
    """
    Check count hotels
    :param message:
    :return:
    """
    text = "Age gotta be a number.\n" \
           " Please enter the number of hotels to search for? (digits only)"
    logger.info(text)
    return await message.reply(text)


@dp.message_handler(state='*')
async def process_count_hotels(message: types.Message, state: FSMContext) -> None:
    """
    Hotel search by request
    :param message:
    :param state:
    :return:
    """
    answer = message.text
    async with state.proxy() as data:
        data['count'] = answer
        if int(answer) > 25:
            await message.answer('You have exceeded the limit,'
                                 ' enter a number up to 25')
        else:
            await message.answer('Answers received generating suggestions!')
            result = list(data.values())
            rapid_api = RapidApi(count=str(result[1]), city=str(result[0]))
            list_hotels = rapid_api.lower_price()
            for i_res in list_hotels:
                logger.info(f'{i_res[0]} - {i_res[1]}')
            await message.answer('Data on your request')
            await message.answer('\n'.join([x[0] for x in list_hotels]))

    await state.finish()
