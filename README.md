Telegram-бот для анализа сайта Hotels.com и поиска подходящих пользователю отелей.

Список доступных команд:
1. Узнать топ самых дешёвых отелей в городе (команда /lowprice).
2. Узнать топ самых дорогих отелей в городе (команда /highprice).
3. Узнать топ отелей, наиболее подходящих по цене и расположению от центра
(самые дешёвые и находятся ближе всего к центру) (команда /bestdeal).
4. Посмотреть описание бота (команда /start)
5. Завершить работу (команда /cancel)

Запуск проекта:
pipenv lock --requirements
В файле .env указать 
1. Открытый API Hotels
2. NGROK_TOKEN - с помощью команды ngrok http 3001
3. Токен в телеграмм 
