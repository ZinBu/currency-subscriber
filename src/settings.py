from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Subscriber'
    database_uri: str


settings = Settings()
