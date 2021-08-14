from typing import Dict

start_message: str = "Hi! I'm a travel agency bot Too Easy Travel!"
low_message: str = "Find the top of the cheapest hotels in the city"
high_message: str = "Find the top of the most expensive hotels in the city"
best_message: str = "Find the top hotels most suitable for the price and location from the center" \
               "(the cheapest) and are closest to the center"
cancel: str = "Cancell bot"

help_message: str = f'Available commands: \n/lowprice - {low_message}, ' \
               f'\n/highprice - {high_message}, \n/bestdeal - {best_message}, \n/cancel - {cancel}'


MESSAGES: Dict = {
    'start': start_message,
    'help': help_message,
    'cancel': cancel
}
