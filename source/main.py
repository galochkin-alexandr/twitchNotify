import asyncio
import threading
from threading import Thread

import telebot
from telebot import types

from data_service import DataService
from twitch_service import TwitchService
from executor import Executor

twitch_id = 'syelrqvdt63gsutrz9mdfwbw40refw'
twitch_key = 'lg2sz3j5805520gw3py0eg5zd1156w'
telegram_token = '7463673517:AAGkVz4wumFSEIg_Lva7rADQ26kIg2FDp1g'

data_service = DataService('../data/streamers.txt', '../data/users.txt')

twitch_service = TwitchService(twitch_id, twitch_key)
bot = telebot.TeleBot(telegram_token)
executor = Executor(twitch_service, data_service, bot)
users_action = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    print(user_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Подписаться на стримера")
    markup.add(btn1)
    bot.send_message(user_id, "Привет", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id
    if message.text == "Подписаться на стримера":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(user_id, "Имя?", reply_markup=markup)
        users_action[user_id] = 'I'
    elif message.text == "Отписаться от стримера":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(user_id, "Имя?", reply_markup=markup)
        users_action[user_id] = 'D'
    else:
        if user_id in users_action:
            if users_action[user_id] == 'I':
                executor.subscribe_to_streamer(message.text, user_id)
                users_action[user_id] = '-'


# loop = asyncio.new_event_loop()
# loop.create_task(executor.check_status())

print('Бот запущен')
bot_thread = Thread(target=bot.polling)
exec_thread = Thread(target=executor.check_status)
bot_thread.start()
exec_thread.start()
bot_thread.join()
