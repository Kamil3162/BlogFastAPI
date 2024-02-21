import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
from BlogFastAPI.app.utils.utils import get_db, decode_jwt
from BlogFastAPI.app.db.models.enums import UserRoles
from BlogFastAPI.app.utils.exceptions import CustomHTTPExceptions
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
    """
        Function return user instance based on valid token and decoded email
        from jwt-token
    :param token:
    :param db:
    :return:
    """
    try:
        payload = decode_jwt(token)
        print(payload)
        email = payload["sub"]  # this line return our email encoded in jwt
        token_data = TokenData(email=email)
    except JWTError:
        raise JWTError("Problem with JWT TOKEN")

    user = USER_AUTH.get_user(email=token_data.email, db=db)
    if user is None:
        raise CustomHTTPExceptions.unauthorized()
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
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            return False
        return user

    def check_user_admin_permission(self, email: str, db):
        user = db.query(User).filter(User.email == email).first()
        if user.role is UserRoles.ADMIN.value:
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

    def create_refresh_token(self, data: dict,
                             expires_delta: Optional[datetime.datetime] = None):
        to_encode = data.copy()
        if not expires_delta:
            expires_delta = datetime.timedelta(days=2)
        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def create_reset_password_token(self, email):
        data = {"sub": email, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=20)}
        return jwt.encode(data, self.SECRET_KEY, self.ALGORITHM)

    def decode_access_token(self, token):
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

    async def get_current_active_user(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ):
        print(current_user)
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    async def get_admin_user(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ):
        if current_user.role != UserRoles.ADMIN.value:
            raise HTTPException(status_code=401, detail="You havent permission to change and check this data")
        return current_user

USER_AUTH = UserAuth(oauth2_scheme=oauth2_scheme)


