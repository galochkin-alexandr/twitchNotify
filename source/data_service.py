import threading


class DataService:
    """Класс для работы с данными пользователей"""

    path_to_streamers_file = ''
    path_to_users_file = ''
    streamer_dict = {}
    user_dict = {}
    lock = threading.Lock()

    @staticmethod
    def create_streamer_dict(path_to_streamers_file):
        streamers_file = open(path_to_streamers_file).readlines()
        streamers_file = [i.strip('\n') for i in streamers_file]
        streamer_dict = {i: False for i in streamers_file}
        return streamer_dict

    @staticmethod
    def create_user_dict(path_to_users_file):
        user_dict = {}
        users_file = open(path_to_users_file).readlines()
        users_file = [i.strip('\n').split(',') for i in users_file]
        for i in users_file:
            if i[0] in user_dict:
                user_dict[i[0]].append(i[1])
            else:
                user_dict[i[0]] = [i[1]]
        return user_dict

    def __init__(self, path_to_streamers_file, path_to_users_file):
        self.path_to_streamers_file = path_to_streamers_file
        self.path_to_users_file = path_to_users_file
        self.streamer_dict = self.create_streamer_dict(path_to_streamers_file)
        self.user_dict = self.create_user_dict(path_to_users_file)

    def add_streamer(self, streamer):
        if streamer in self.streamer_dict:
            return
        self.streamer_dict[streamer] = False
        streamers_file = open(self.path_to_streamers_file, 'a')
        streamers_file.write('\n' + streamer)
        streamers_file.close()

    def add_user(self, streamer, user):
        if streamer not in self.streamer_dict:
            self.add_streamer(streamer)
            if self.user_dict.get(streamer) is None:
                self.user_dict[streamer] = [user]
                users_file = open(self.path_to_users_file, 'a')
                users_file.write('\n' + str(streamer) + ',' + str(user))
                users_file.close()
            elif user not in self.user_dict.get(streamer):
                self.user_dict[streamer].append(user)
                users_file = open(self.path_to_users_file, 'a')
                users_file.write('\n' + str(streamer) + ',' + str(user))
                users_file.close()

    def get_users_for_streamer(self, streamer):
        if streamer not in self.streamer_dict:
            return []
        return self.user_dict[streamer]

    def get_streamers(self):
        return self.streamer_dict.keys()

    def get_streamer_status(self, streamer):
        return self.streamer_dict.get(streamer)

    def update_streamers_status(self, change_dict):
        self.streamer_dict.update(change_dict)