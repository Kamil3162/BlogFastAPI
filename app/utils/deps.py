from fastapi import HTTPException, status
from sqlalchemy import exc


class CustomHTTPExceptions:

    @staticmethod
    def handle_db_exceptiopn(exception:Exception):
        if isinstance(exception, exc.OperationalError):
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            error_detail = "A database operational error occurred"
        elif isinstance(exception, exc.DisconnectionError):
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            error_detail = "Problem with connection to database"
        elif isinstance(exception, exc.IntegrityError):
            status_code = status.HTTP_409_CONFLICT
            error_detail = "Data integrity error"
        elif isinstance(exception, exc.DataError):
            status_code = status.HTTP_400_BAD_REQUEST
            error_detail = "Invalid data provided"
        elif isinstance(exception, exc.ProgrammingError):
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_detail = "Database programming error"
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_detail = "An unexpected database error occured"

        raise HTTPException(
            status_code=status_code,
            detail=error_detail
        )
