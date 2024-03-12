from fastapi import HTTPException, status
from sqlalchemy import exc

class CustomHTTPExceptions:

    @staticmethod
    def unauthorized(detail: str = "Unauthorized"):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def forbidden(detail: str = "Forbidden access"):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

    @staticmethod
    def not_found(detail: str = "Not found"):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
    )

    @staticmethod
    def bad_request(detail: str = "Bad request"):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def internal_server_error(status_code, detail: str = "Internal Server Error"):
        return HTTPException(
            status_code=status_code,
            detail="A post with this title already exists"
        )

    @staticmethod
    def exists_in_db(detail: str = "Base"):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A post with this title already exists"
        )

    @staticmethod
    def handle_db_exeception(exception: Exception):
        if isinstance(exception, exc.OperationalError):
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            error_detail = "A database operational error occured"
        elif isinstance(exception, exc.DisconnectionError):
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            error_detail = "Problem with connection with database"
        elif isinstance(exception, exc.IntegrityError):
            status_code = status.HTTP_409_CONFLICT
            error_detail = "Following data exists in database"
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_detail = "A database error occupied"
        raise CustomHTTPExceptions.internal_server_error(
                detail=error_detail,
                status_code=status_code
            )

