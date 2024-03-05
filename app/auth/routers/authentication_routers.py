import json
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import (
    HTTPException,
    Response,
    Request,
    APIRouter,
    status,
    Depends,
    BackgroundTasks,
    Cookie
)
from fastapi.routing import APIRouter
from ..schemas.schemas import(
    UserSchemeOfficial,
    UserHashPassword,
    UserRoleScheme,
    UserResponse)
from ..schemas.token_schemas import TokenData, Token, TokenStatus, \
    ResetTokenSchemas
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Annotated, Union
from BlogFastAPI.app.utils.utils import get_db, revoke_token
from datetime import datetime, timedelta
from BlogFastAPI.app.db.models.models import User
from ..user_manager.user_auth import USER_AUTH, oauth2_scheme, check_token_status
from ..schemas.schemas import UserCreate, UserUpdate
from BlogFastAPI.app.services.user_service import UserService
from BlogFastAPI.app.middleware.role_middleware import UserMiddleware, UserRoles
from BlogFastAPI.app.utils.exceptions import CustomHTTPExceptions
from BlogFastAPI.app.services.email_service import EmailService
from urllib.parse import quote

auth_router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = oauth2_scheme

@auth_router.post("/token")
async def login_for_access_token(
    response: Response,  # Add the response parameter to set cookies
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    print("to jest request na token")
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

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = USER_AUTH.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=7)
    refresh_token = USER_AUTH.create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    # Set access token in httpOnly cookie
    response.set_cookie(key="access_token",
                        value=access_token,
                        httponly=True,
                        max_age=int(access_token_expires.total_seconds()),
                        path='/')

    # Optionally set refresh token in httpOnly cookie if you're using refresh tokens
    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        httponly=True,
                        max_age=int(refresh_token_expires.total_seconds()),
                        path='/')

    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active
    }

    user_data_json = quote(json.dumps(user_data))

    response.set_cookie(key="user_data",
                        value=user_data_json)

    # Return a JSON response. FastAPI will handle the conversion to JSON.
    # No need to call response.json() directly, just return the dict.

    print("test")

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@auth_router.post('/register', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print(user)
    db_user = UserService.create_user(db, user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return db_user


@auth_router.get("/valid/token", response_model=TokenStatus)
async def token_valid(token_status = Depends(check_token_status)):
    return token_status

@auth_router.post("/token/refresh")
async def token_refresh():...

@auth_router.post("/password/reset")
async def password_reset(
        email: str,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
        ):
    print("test")
    user = UserService.get_user_by_email(email, db)
    if not user:
        raise CustomHTTPExceptions.not_found(f"User with email:{email} not found")

    reset_token = USER_AUTH.create_reset_password_token(email)
    reset_url = f"https://www.kamildev.pl/reset/password/{reset_token}/"

    background_tasks.add_task(EmailService.send_reset_email, email, reset_url)

    return {
        "message": "If a user with that email exists, a password reset link has been sent."}

@auth_router.put("/password/reset/{token}")
async def set_new_password(token: str, password_data: ResetTokenSchemas, db: Session = Depends(get_db)):
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

@auth_router.get('/logout')
async def logout(response: Response,
                 access_token: str = Cookie(None),
                 db: Session = Depends(get_db)):

    print("sensed request to logout")

    # code responsible for delete cookies from browser
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return {'logout': 'success'}


@auth_router.get("/validate")
async def validate_token(access_token: str = Cookie(None)):
    print(access_token)
    if access_token is None:
        return {"authenticated": False}

    try:
        # Assuming USER_AUTH.decode_access_token() is a method you've defined
        # to decode and validate your JWT token.
        decoded_token = USER_AUTH.decode_access_token(access_token)
        # You might want to check if the token is expired or invalid here
        # and raise an HTTPException if there are any issues.

        # If everything is fine, return the authenticated user's information.
        return {"authenticated": True,
                "user": "User information based on decoded token"}
    except Exception as e:  # You might want to catch more specific exceptions
        raise HTTPException(status_code=401, detail="Invalid token")


@auth_router.get('/test')
async def test(token: Annotated[str, Depends(oauth2_scheme)]):
    """
        Test function to generate a session
    :param token:
    :return:
    """
    return {'token_pass': token}




