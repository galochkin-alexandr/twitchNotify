from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    twitch_id: str
    twitch_key: str
    telegram_token: str
    path_to_strimers_file: str
    path_to_users_file: str
    model_config = SettingsConfigDict(env_file='../data/credits.env')


def get_settings():
    return Settings()

