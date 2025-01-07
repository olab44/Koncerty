from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int
    ANNOUNCEMENT_EMAIL_SUBJECT_TEMPLATE: str
    ANNOUNCEMENT_EMAIL_BODY_TEMPLATE: str


settings = Settings()
