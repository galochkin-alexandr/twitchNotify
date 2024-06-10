from threading import Thread

import telebot
from telebot import types

from data_service import DataService
from settings import get_settings
from twitch_service import TwitchService
from executor import Executor

"""Достаём конфиги"""
settings = get_settings()

twitch_id = settings.twitch_id
twitch_key = settings.twitch_key
telegram_token = settings.telegram_token
path_to_streamers_file = settings.path_to_streamers_file
path_to_users_file = settings.path_to_users_file

data_service = DataService(path_to_streamers_file, path_to_users_file)

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
    btn2 = types.KeyboardButton("Отписаться от стримера")
    markup.add(btn1, btn2)
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
            if users_action[user_id] == 'D':
                executor.unsubscribe_to_streamer(message.text, user_id)
                users_action[user_id] = '-'


print('Бот запущен')
bot_thread = Thread(target=bot.polling)
exec_thread = Thread(target=executor.check_status)
bot_thread.start()
exec_thread.start()
bot_thread.join()
