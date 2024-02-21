from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import (
    HTTPException,
    Response,
    Request,
    APIRouter,
    status,
    Depends,
    BackgroundTasks
)
from fastapi.routing import APIRouter
from ..schemas.schemas import(
    UserSchemeOfficial,
    UserHashPassword,
    UserRoleScheme,
    UserResponse)
from ..schemas.token_schemas import TokenData, Token, TokenStatus
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
auth_router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = oauth2_scheme

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
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

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post('/register', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
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

@auth_router.get('/logout')
async def logout(token: Annotated[str, Depends(oauth2_scheme)],
                 db: Session = Depends(get_db)):
    blocked_token = revoke_token(db, token)
    return {'blocked_token': blocked_token, 'logout': 'success'}


@auth_router.get('/test')
async def test(token: Annotated[str, Depends(oauth2_scheme)]):
    """
        Test function to generate a session
    :param token:
    :return:
    """
    return {'token_pass': token}




