import os
from dotenv import load_dotenv
from pathlib import Path

env_path1 = Path(__file__).parent.parent / 'config.env'
load_dotenv(dotenv_path=env_path1)

class Settings:
    PROJECT_NAME: str = "BlogFastAPI"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432) # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

class BrokerSettings:
    PROJECT_NAME: str = "BlogBroker"
    API_V1_STR: str = "/api/v1"

    # RabbitMQ settings
    RABBITMQ_HOST = "localhost"
    RABBITMQ_PORT = "5672"
    RABBITMQ_USER = "USER"
    RABBITMQ_PASS = "PASS"

    # Celery settings
    CELERY_BROKER_URL: str = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
    CELERY_RESULT_BACKEND: str = "rpc://"

    class Config:
        env_file = ".env"

settings = Settings()
broker_settings = BrokerSettings()

