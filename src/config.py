from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import SecretStr
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_key:str
    Alogrithm:str
    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_SERVER:str
    MAIL_PORT:int
    MAIL_FROM: str
    MAIL_FROM_NAME :str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    Domain: str
    URL_REDIS:str
    REDIS_PORT:int
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND:str
    BetterStack: str
    
    model_config = SettingsConfigDict(env_file=".env")
configs=Settings() # type: ignore