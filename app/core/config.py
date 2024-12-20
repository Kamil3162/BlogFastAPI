import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings

env_path1 = Path(__file__).parent.parent / 'config.env'
SECRET_KEY = os.getenv("SECRET_KEY")

load_dotenv(dotenv_path=env_path1)

class Settings:
    PROJECT_NAME: str = "BlogFastAPI"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "127.0.0.1")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432) # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "FastApiBlogOfficial")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

class BrokerSettings:
    PROJECT_NAME: str = "BlogBroker"
    API_V1_STR: str = "/api/v1"

    # RabbitMQ settings
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")

    # Celery settings
    CELERY_BROKER_URL: str = f"amqp://\
    {RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
    CELERY_RESULT_BACKEND: str = "rpc://"

    class Config:
        env_file = ".env"

class RedisSettings(BaseSettings):
    host: str = "localhost"
    password: str = ""
    db_name: str = "redis-handler"
    port: int = 6379
    db: int = 0
    per_page: int = 10
    stats_cache_connection: int = 300  # 5 minutes
    decode_responses: bool = True

settings = Settings()
settings_redis = RedisSettings()
broker_settings = BrokerSettings()

