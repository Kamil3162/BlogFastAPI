import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
from BlogFastAPI.app.utils.utils import get_db, decode_jwt
# from app.utils.utils import getdb, decode_jwt
from BlogFastAPI.app.utils.utils import get_db, decode_jwt
from BlogFastAPI.app.utils.exceptions import HTTP_EXCEPTION
from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import FastAPI, HTTPException, status
from ..schemas.token_schemas import TokenData, TokenStatus
from fastapi import Depends
from typing import Optional, Annotated
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import datetime

from BlogFastAPI.app.db.models.models import User

config_file = Path(__file__).parent.parent / 'config.env'
load_dotenv(config_file)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
DB = get_db()

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)  # Injecting the database session here
):
    try:
        payload = decode_jwt(token)
        email = payload["sub"]
        token_data = TokenData(email=email)
    except JWTError:
        raise JWTError("Problem with JWT TOKEN")

    user = USER_AUTH.get_user(email=token_data.email, db=db)
    if user is None:
        raise HTTP_EXCEPTION
    return user

async def check_token_status(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)  # Injecting the database session here
):
    try:
        decoded_jwt = decode_jwt(token)

        print(decoded_jwt)

        token_data = TokenStatus(is_valid=True)
        return token_data
    except JWTError:
        return TokenStatus(is_valid=False)


class UserAuth:
    def __init__(self, oauth2_scheme):
        self.ALGORITHM = "HS256"
        self.SECRET_KEY = str(os.getenv("SECRET_KEY"))
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = oauth2_scheme

    def get_hash_password(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_user(self, email: str, db):
        print("tto jest funkcja get user")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            return False
        return user

    def authenticate_user(self, db, email: str, password: str):
        user = self.get_user(email=email, db=db)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict,
                            expires_delta: Optional[datetime.timedelta] = None):
        """

        :param data:
        :param expires_delta:
        :return:
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token):
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

    async def get_current_active_user(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ):
        print("wykonywanie")
        print(current_user)
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user


USER_AUTH = UserAuth(oauth2_scheme=oauth2_scheme)


