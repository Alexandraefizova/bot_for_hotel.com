import telebot
from settings import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message) -> telebot.types.Message:
    return bot.reply_to(message, 'Hi there, I am Telegram bot for Too Easy Travel. '
                                 'I am here to help you find the right hotel for you!'
                                 ' Please write to get started: '
                                 '\'Привет\' or \'/hello-world\'')


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message) -> telebot.types.Message:
    return bot.send_message(message.from_user.id, 'Can I help You?')


@bot.message_handler(content_types=['text'])
def get_messages(message: telebot.types.Message) -> telebot.types.Message:
    if message.text == 'Привет':
        return bot.send_message(message.from_user.id, 'Hello!')
    elif message.text == '/hello-world':
        return bot.send_message(message.from_user.id, 'Hello!')
    else:
        return bot.send_message(message.from_user.id, "I don't understand, try again!")


