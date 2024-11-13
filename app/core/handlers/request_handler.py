import logging
import typing
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    DataError,
    DatabaseError,
    ProgrammingError,
    NoResultFound
)
from .exceptions import ServiceError

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    """Configure all exception handlers for the FastAPI application"""

    @app.exception_handler(ServiceError)
    async def service_error_handler(
            request: Request,
            exc: ServiceError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "Service is unavailable"
            }
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
            request: Request,
            exc: IntegrityError
    ) -> JSONResponse:
        """
            Handle database integrity errors (unique constraints, foreign keys)
        """

        error_detail = _parse_integrity_error(exc)

        logger.error(
            "Database integrity error",
            extra={
                "error_type": "integrity_error",
                "detail": error_detail,
                "path": request.url.path
            },
            exc_info=exc
        )

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "status": "error",
                "message": "Database constraint violation",
                "error_code": "DB_INTEGRITY_ERROR",
                "detail": error_detail,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(OperationalError)
    async def operational_error_handler(
            request: Request,
            exc: OperationalError
    ) -> JSONResponse:
        """
            Handle database operational errors (connection, timeout)
        """
        logger.error(
            "Database operational error",
            extra={"path": request.url.path},
            exc_info=exc
        )

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "message": "Database is temporarily unavailable",
                "error_code": "DB_OPERATIONAL_ERROR",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(DataError)
    async def data_error_handler(
            request: Request,
            exc: DataError
    ) -> JSONResponse:
        """Handle invalid data errors"""
        error_detail = str(exc.__cause__ or exc)

        logger.error(
            "Database data error",
            extra={
                "error_type": "data_error",
                "detail": error_detail,
                "path": request.url.path
            },
            exc_info=exc
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "message": "Invalid data provided",
                "error_code": "DB_DATA_ERROR",
                "detail": error_detail,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(NoResultFound)
    async def not_found_error_handler(
            request: Request,
            exc: NoResultFound
    ) -> JSONResponse:
        """Handle not found errors"""
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "error",
                "message": "Resource not found",
                "error_code": "NOT_FOUND",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(ProgrammingError)
    async def programming_error_handler(
            request: Request,
            exc: ProgrammingError
    ) -> JSONResponse:
        """Handle SQL programming errors"""
        logger.error(
            "Database programming error",
            extra={"path": request.url.path},
            exc_info=exc
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "Internal database error",
                "error_code": "DB_PROGRAMMING_ERROR",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(
            request: Request,
            exc: SQLAlchemyError
    ) -> JSONResponse:
        """Handle all other SQLAlchemy errors"""
        logger.error(
            "Unhandled database error",
            extra={
                "error_type": exc.__class__.__name__,
                "path": request.url.path
            },
            exc_info=exc
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "An unexpected database error occurred",
                "error_code": "DB_ERROR",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(Exception)
    async def exception_error_handler(
            request: Request,
            exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "message": "Unexpected server error",
                "error_code": "SERVER_ERROR",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


def _parse_integrity_error(exc: IntegrityError) -> Dict[str, Any]:
    """Parse details from IntegrityError"""
    error_msg = str(exc).lower()

    if "unique violation" in error_msg:
        return {
            "type": "unique_violation",
            "constraint": exc.orig.diag.constraint_name
        }
    elif "foreign key violation" in error_msg:
        return {
            "type": "foreign_key_violation",
            "constraint": exc.orig.diag.constraint_name
        }
    elif "not null violation" in error_msg:
        return {
            "type": "not_null_violation",
            "column": exc.orig.diag.column_name
        }

    return {"type": "unknown_violation"}
