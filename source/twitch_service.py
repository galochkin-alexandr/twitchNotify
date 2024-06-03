import requests


class TwitchService:
    """Класс для работы с Twitch"""

    twitch_id = ''
    twitch_key = ''
    twitch_token = ''

    @staticmethod
    def get_twitch_token(twitch_id, twitch_key):
        try:
            response = requests.post(
                f"https://id.twitch.tv/oauth2/token?client_id={twitch_id}&client_secret={twitch_key}&grant_type=client_credentials"
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            print(f"Error getting Twitch OAuth token: {str(e)}")
            return None

    def __init__(self, twitch_id, twitch_key):
        self.twitch_id = twitch_id
        self.twitch_key = twitch_key
        self.twitch_token = self.get_twitch_token(twitch_id, twitch_key)

    def send_status_request(self, streamer_name):
        headers = {"Client-ID": self.twitch_id, "Authorization": f"Bearer {self.twitch_token}"}
        url = f"https://api.twitch.tv/helix/streams?user_login={streamer_name}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if len(data["data"]) > 0:
                return True
        return False

    def check_existing_streamer(self, streamer_name):
        headers = {"Client-ID": self.twitch_id, "Authorization": f"Bearer {self.twitch_token}"}
        url = f"https://api.twitch.tv/helix/users?login={streamer_name}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return True
        return False
