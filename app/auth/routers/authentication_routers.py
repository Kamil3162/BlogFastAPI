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
from ..schemas.schemas import UserCreate
from BlogFastAPI.app.services.user_service import UserService

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

@auth_router.post('/register', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # success - create a new account for our blog user
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = USER_AUTH.get_hash_password(user.password)
    db_user = User(email=user.email, first_name=user.first_name,
                   last_name=user.last_name, hashed_password=hashed_password)

    print(db_user.email)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


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

@auth_router.get('/logout')
async def logout(token: Annotated[str, Depends(oauth2_scheme)],
                 db: Session = Depends(get_db)):
    blocked_token = revoke_token(db, token)
    return {'blocked_token': blocked_token, 'logout': 'success'}



# urls resposible for generate data for users


@auth_router.get("/users/me/", response_model=UserSchemeOfficial)
async def read_users_me(
        current_user: User = Depends(USER_AUTH.get_current_active_user)
):
    return current_user

@auth_router.get("/user/{user_id}/", response_model=UserSchemeOfficial)
async def get_user(
        user_id: int,
        current_user: User = Depends(USER_AUTH.get_current_active_user),
        db: Session = Depends(get_db)
):
    user = UserService.get_user_by_id(db, user_id)
    return user

@auth_router.get("/user-role/{user_id}/", response_model=UserRoleScheme)
async def get_user(
        user_id: int,
        current_user: User = Depends(USER_AUTH.get_admin_user),
        db: Session = Depends(get_db)
):
    print("funkcja get user")
    user = UserService.get_user_by_id(db, user_id)
    return user

