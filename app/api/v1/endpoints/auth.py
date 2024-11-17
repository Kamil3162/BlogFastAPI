import json
from typing import Annotated
from datetime import timedelta
from urllib.parse import quote

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import (
    HTTPException,
    Response,
    status,
    Depends,
    BackgroundTasks,
    Cookie
)
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from ....schemas.user import UserResponse
from ....schemas.token import TokenStatus, ResetTokenSchemas
from ....utils.utils import get_db
from ....core.security import (
    USER_AUTH,
    oauth2_scheme,
    check_token_status
)
from ....schemas.user import UserCreate
from ....services.users import UserService
from ....utils.deps import CustomHTTPExceptions
from ....services.email import EmailService

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = oauth2_scheme

@router.post("/token")
async def login_for_access_token(
    response: Response,  # Add the response parameter to set cookies
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    try:
        user = USER_AUTH.authenticate_user(
            db,
            form_data.username,
            form_data.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=160)
        access_token = USER_AUTH.create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        refresh_token_expires = timedelta(days=7)
        refresh_token = USER_AUTH.create_refresh_token(
            data={"sub": user.email},
            expires_delta=refresh_token_expires)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,  # Adjust expiration time if needed
            secure=True,
            samesite="None",  # Allow cross-site requests
            # path='/',  # Optionally set path
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=1800,  # Adjust expiration time if needed
            secure=True,
            samesite="None",  # Allow cross-site requests
        )

        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active
        }

        user_data_json = quote(json.dumps(user_data))

        response.set_cookie(
            key="user_data",
            value=user_data_json,
            httponly=False,  # Adjust as needed
            secure=True,
            max_age=1800,  # Adjust expiration time if needed
            samesite="None",  # Allow cross-site requests

        )
        print(access_token)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except Exception as e:
        # Return a custom error response
        return {
            "error": "An unexpected error occurred",
            "detail": str(e)
        }, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post('/register', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.create_user(db, user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return db_user


@router.get("/valid/token", response_model=TokenStatus)
async def token_valid(token_status=Depends(check_token_status)):
    return token_status

@router.post("/token/refresh")
async def token_refresh():...

@router.post("/password/reset")
async def password_reset(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = UserService.get_user_by_email(email, db)
    if not user:
        raise CustomHTTPExceptions.not_found(f"User with email:{email} not found")

    reset_token = USER_AUTH.create_reset_password_token(email)
    reset_url = f"https://www.kamildev.pl/reset/password/{reset_token}/"

    background_tasks.add_task(EmailService.send_reset_email, email, reset_url)

    return {
        "message": "If a user with that email exists, a password reset link has been sent."}

@router.put("/password/reset/{token}")
async def set_new_password(
    token: str,
    password_data:
    ResetTokenSchemas,
    db: Session = Depends(get_db)
):
    try:
        if password_data.password != password_data.confim_password:
            raise HTTPException(status_code=400,
                                detail="Passwords do not match")
        decoded_token = USER_AUTH.decode_reset_password_token(token)

        username = decoded_token.get("sub")

        user = UserService.set_new_password(username, db, password_data)
        return {"message": "proper change password", "code": "200"}
    except HTTPException:
        raise HTTPException(status_code=404, detail="Problem with form")

@router.get('/logout')
async def logout(
    response: Response,
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    # code responsible for delete cookies from browser
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return {'logout': 'success'}


@router.get("/validate")
async def validate_token(access_token: str = Cookie(None)):
    if access_token is None:
        return {"authenticated": False}

    try:
        # Assuming USER_AUTH.decode_access_token() is a method you've defined
        # to decode and validate your JWT token.
        decoded_token = USER_AUTH.decode_access_token(access_token)

        # If everything is fine, return the authenticated user's information.
        return {"authenticated": True,
                "user": "User information based on decoded token"}
    except Exception as e:  # You might want to catch more specific exceptions
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get('/test')
async def test(token: Annotated[str, Depends(oauth2_scheme)]):
    """
        Test function to generate a session
    :param token:
    :return:
    """
    return {'token_pass': token}




