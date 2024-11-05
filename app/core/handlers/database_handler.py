from typing import Optional

from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from fastapi import status

from .exceptions import DatabaseErrorException


def handle_database_error(exc: Optional[SQLAlchemyError, Exception]) -> None:
    """
    Handle database errors following FastAPI's pattern.
    Based on FastAPI's error handling approach.
    """
    if isinstance(exc, IntegrityError):
        error_msg = str(exc.orig).lower()
        if "unique violation" in error_msg:
            raise DatabaseErrorException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A record with this value already exists",
                error_type="unique_violation",
                params={"constraint": exc.orig.diag.constraint_name}
            )
        elif "foreign key violation" in error_msg:
            raise DatabaseErrorException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Referenced record does not exist",
                error_type="foreign_key_violation",
                params={"constraint": exc.orig.diag.constraint_name}
            )
        else:
            raise DatabaseErrorException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Database constraint violation",
                error_type="integrity_error",
                params={"error": str(exc)}
            )

    elif isinstance(exc, OperationalError):
        raise DatabaseErrorException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database operation failed",
            error_type="operational_error",
            params={"error": str(exc)}
        )

    else:
        raise DatabaseErrorException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occurred",
            error_type="database_error",
            params={"error": str(exc)}
        )