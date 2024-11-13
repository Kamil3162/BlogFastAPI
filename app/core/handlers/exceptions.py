from typing import Optional, Dict, Any

from fastapi.exceptions import HTTPException
from pydantic import BaseModel
class BaseException(Exception):
    """
        Base exception for handle other exceptions
    """
    def __init__(
            self,
            message: str = "Service is unavailable",
            name: str = "BaseException"
    ):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class ServiceError(BaseException):
    """
        Exception responsible for turn off service
    """

    pass

class ErrorDetail(BaseModel):
    detail: str
    error_type: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


class DatabaseErrorException(HTTPException):
    def __init__(self, status_code, detail, error_type, params):
        super().__init__(
            status_code=status_code,
            detail=ErrorDetail(
                detail=detail,
                error_type=error_type,
                params=params
            ).model_dump(exclude_none=True)
        )

