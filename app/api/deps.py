from typing import Generator, Optional, Annotated, Type, TypeVar

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..core.config import settings, SECRET_KEY
from ..db.session import SessionLocal
from ..models.user import User
from ..schemas.token import TokenData
from ..core.security import USER_AUTH
from ..utils.utils import get_db
from ..services.categories import CategoryService
from ..services.users import UserService
from ..services.post import PostService
from ..services.base import ServiceFactory

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token'
)


def authenticate_user_from_token(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, USER_AUTH.SECRET_KEY, algorithms=[USER_AUTH.ALGORITHM]
        )
        # token_data = TokenData(
        #     sub=payload.get("sub"),
        #     exp=payload.get("exp")
        # )
        # print(token_data)

    except Exception as e:
        print(str(e))
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.email == payload['sub']).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



def get_current_active_user(
    current_user: User = Depends(authenticate_user_from_token),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(authenticate_user_from_token),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

async def get_admin_user(
    self, current_user: Annotated[User, Depends(authenticate_user_from_token)]
):
    if current_user.role != UserRoles.ADMIN.value:
        raise HTTPException(
            status_code=401,
            detail="You havent permission to change and check this data"
        )
    return current_user

def get_category_service(
    db: Session = Depends(get_db)
):
    return ServiceFactory.get_instance(CategoryService, db)

def get_post_service(
    db: Session = Depends(get_db)
):
    return ServiceFactory.get_instance(PostService, db)

def get_user_service(
    db: Session = Depends(get_db)
):
    return ServiceFactory.get_instance(UserService, db)
