from typing import Generator, Optional, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from BlogFastAPI.app.core.config import settings
from BlogFastAPI.app.core.security import UserAuth
from BlogFastAPI.app.db.session import SessionLocal
from BlogFastAPI.app.models.user import User
from BlogFastAPI.app.schemas.token import Token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token'
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )

        print(payload)

        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

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

async def get_admin_user(
    self, current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.role != UserRoles.ADMIN.value:
        raise HTTPException(status_code=401, detail="You havent permission to change and check this data")
    return current_user