import time

from telebot import types


class Executor:
    """Класс с основными функциями"""

    twitch_service = None
    data_service = None
    telegram_bot = None

    def __init__(self, twitch_service, data_service, telegram_bot):
        self.twitch_service = twitch_service
        self.data_service = data_service
        self.telegram_bot = telegram_bot

    def notify_users(self, streamers_list):
        for current_streamer in streamers_list:
            for current_user in self.data_service.get_users_for_streamer(current_streamer):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                print(int(current_user))
                print(current_streamer)
                self.telegram_bot.send_message(int(current_user), current_streamer + ' запустил стрим', reply_markup=markup)

    def check_status(self):
        while True:
            starting_streamer = {}
            ending_streamer = {}
            all_streamers_dict = self.data_service.get_streamers()
            for current_login, current_status in all_streamers_dict.items():
                new_status = self.twitch_service.send_status_request(current_login)
                if current_status != new_status:
                    if new_status:
                        starting_streamer[current_login] = True
                    else:
                        ending_streamer[current_login] = False
            self.data_service.update_streamers_status(starting_streamer)
            self.data_service.update_streamers_status(ending_streamer)
            self.notify_users(starting_streamer.keys())
            time.sleep(5)

    def subscribe_to_streamer(self, streamer, user):
        streamer_upper = streamer.upper()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if not self.twitch_service.check_existing_streamer(streamer_upper):
            self.telegram_bot.send_message(int(user), 'стример ' + streamer + ' не найден', reply_markup=markup)
        else:
            self.data_service.add_user_for_streamer(streamer_upper, user)
            self.telegram_bot.send_message(int(user), 'подписка оформлена на ' + streamer, reply_markup=markup)

    def unsubscribe_to_streamer(self, streamer, user):
        streamer_upper = streamer.upper()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        result = self.data_service.delete_user_for_streamer(streamer_upper, user)
        if result:
            self.telegram_bot.send_message(int(user), 'подписка на ' + streamer + ' отменена', reply_markup=markup)
        else:
            self.telegram_bot.send_message(int(user), streamer + ' не найден', reply_markup=markup)
