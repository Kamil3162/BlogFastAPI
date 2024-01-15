from fastapi import HTTPException, status

class CustomHTTPExceptions:

    @staticmethod
    def unauthorized(detail: str = "Unauthorized"):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
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
    def internal_server_error(detail: str = "Internal Server Error"):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A post with this title already exists"
        )

