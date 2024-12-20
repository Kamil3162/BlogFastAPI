import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..db.base import RedisConnectionClient

class BlackListTokenService:
    def __init__(self, redis_client: RedisConnectionClient):
        self._redis = redis_client
        self.blacklist_timeout = 20 * 60

    def blacklist_token(
        self,
        token: str,
        jti: str,
        expires_at: datetime,
        token_type: str = 'access',
    ) -> bool:
        """
            Add token to blacklist in Redis with 20-minute expiry
        """
        try:
            redis_key = f"blacklist:token:{jti}"
            return self._redis.set(redis_key, token, self.blacklist_timeout)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Faioled to blacklist token: {str(e)}"
            )

    def is_token_blacklisted(
        self,
        jti: str
    ) -> bool:
        try:
            redis_key = f"blacklist:token:{jti}"
            return bool(self._redis.get(redis_key))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Faioled to blacklist token: {str(e)}"
            )