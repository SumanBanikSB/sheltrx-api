# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    database_name: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    smtp_from_email: str

    class Config:
        env_file = ".env"

settings = Settings()

# print("HERE",settings.dict())
