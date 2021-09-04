from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    """
    States
    """
    command = State()  # Will be represented in storage as 'Form:command'
    city = State()  # Will be represented in storage as 'Form:city'
    count = State()  # Will be represented in storage as 'Form:count_hotels'
    price = State()  # Will be represented in storage as 'Form:price'
    distance = State()  # Will be represented in storage as 'Form:distance'
