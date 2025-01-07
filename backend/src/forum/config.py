from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int = 587

    class Config:
        env_file = ".env"


settings = Settings()
