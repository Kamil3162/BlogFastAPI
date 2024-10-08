import os
from pathlib import Path
from dotenv import load_dotenv
from BlogFastAPI.app.utils.utils import get_db, decode_jwt
from BlogFastAPI.app.core.enums import UserRoles
from BlogFastAPI.app.utils.deps import CustomHTTPExceptions
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from BlogFastAPI.app.schemas.token import TokenData, TokenStatus
from fastapi import Depends
from typing import Optional, Annotated
from jose import jwt, JWTError, exceptions
from sqlalchemy.orm import Session
from BlogFastAPI.app.api.deps import authenticate_user_from_token
import datetime

from ..models.user import User

config_file = Path(__file__).parent.parent / 'config.env'
load_dotenv(config_file)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
DB = get_db()

async def check_token_status(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)  # Injecting the database session here
):
    try:
        decoded_jwt = decode_jwt(token)

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
        print(user)
        print(self.verify_password(password, user.hashed_password))
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):

            return False
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[datetime.timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta  # Use UTC time
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=150)  # Use UTC time
        to_encode.update({"exp": expire.timestamp()})  # Convert datetime to timestamp
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(
            self, data: dict,
            expires_delta: Optional[datetime.timedelta] = None
    ):
        to_encode = data.copy()
        if not expires_delta:
            expires_delta = datetime.timedelta(days=2)
        expire = datetime.datetime.utcnow() + expires_delta  # Use UTC time
        to_encode.update({"exp": expire.timestamp()})  # Convert datetime to timestamp
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def create_reset_password_token(self, email):
        data = {
            "sub": email,
            # Use UTC time
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        }
        return jwt.encode(data, self.SECRET_KEY, self.ALGORITHM)

    def decode_reset_password_token(self, token):
        try:
            token_data = jwt.decode(token, self.SECRET_KEY, self.ALGORITHM)
            return token_data
        except exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid token")

    def decode_access_token(self, token):
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])



USER_AUTH = UserAuth(oauth2_scheme=oauth2_scheme)


