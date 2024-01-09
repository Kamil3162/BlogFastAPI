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
                status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
)

HTTP_POST_EXCEPTION = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found",
)

HTTP_POST_EXISTANCE_EXCEPTION = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="A post with this title already exists"
)

HTTP_POST_SERVER_ERROR = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="A post with this title already exists"
)
