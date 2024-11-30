from typing import Optional
from redis import Redis, ConnectionPool
from contextlib import contextmanager

from ..core.config import RedisSettings, settings_redis

class RedisClient:
    def __init__(self, config: RedisSettings = settings_redis):
        self._config = config
        self._client = self._create_connection()

    def _create_connection(self) -> Redis:
        return Redis(
            host=self._config.host,
            port=self._config.port,
            password=self._config.password,
            db=self._config.db_name,
            decode_responses=self._config.decode_responses,
        )

    def get(self, key: str) -> Optional[str]:
        return self._client.get(key)

    def set(self, key: str, value: str, expiration: Optional[int] = None) -> bool:
        return self._client.set(key, value, ex=expiration)

    def delete(self, key: str) -> int:
        return self._client.delete(key)

class RedisPoolClient:
    def __init__(self, config: RedisSettings, max_connections: int = 10):
        self._config = config
        self._pool = self._create_pool(max_connections)

    def _create_pool(self, RedisSettings: int) -> ConnectionPool:
        return ConnectionPool(
            host=self._config.host,
            port=self._config.port,
            password=self._config.password,
            db=self._config.db_name,
            decode_responses=self._config.decode_responses,
            max_connections=max_connections
        )

    @contextmanager
    def get_connection(self) -> Redis:
        connection = redis.Redis(connection_pool=self._pool)
        try:
            yield connection
        finally:
            connection.close()