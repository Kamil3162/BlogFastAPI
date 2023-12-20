from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import (
    HTTPException,
    Response,
    Request,
    APIRouter,
    status,
    Depends
)
from fastapi.routing import APIRouter
from ..schemas.schemas import UserSchemeOfficial, UserHashPassword, UserResponse
from ..schemas.token_schemas import TokenData, Token, TokenStatus
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Annotated, Union
from BlogFastAPI.app.utils.utils import get_db
from datetime import datetime, timedelta
from BlogFastAPI.app.db.models.models import User
from ..user_manager.user_auth import USER_AUTH, oauth2_scheme,check_token_status

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
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me/", response_model=UserSchemeOfficial)
async def read_users_me(
        current_user: User = Depends(USER_AUTH.get_current_active_user)
):
    # Assuming UserResponse is a Pydantic model that matches the structure of the User model
    return current_user


@auth_router.get("/valid/token", response_model=TokenStatus)
async def token_valid(token_status = Depends(check_token_status)):
    return token_status


@auth_router.get('/test')
async def test(token: Annotated[str, Depends(oauth2_scheme)]):
    """
        Test function to generate a session
    :param token:
    :return:
    """
    return {'token_pass': token}
