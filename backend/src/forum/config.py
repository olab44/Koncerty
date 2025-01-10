from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    EMAIL_ADDRESS: str = "service@megalodony-koncerty.iam.gserviceaccount.com"
    GMAIL_CREDENTIALS_FILE: str = "service_account.json"
    TOKEN_FILE: str = "token.json"  # File to store user's access tokens

    class Config:
        env_file = ".env"


settings = Settings()
