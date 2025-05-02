import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    boavizta_api_data_dir: str = os.path.join(os.path.dirname(__file__), 'data')

    model_config=SettingsConfigDict(env_file=".env")

settings: Settings = Settings()