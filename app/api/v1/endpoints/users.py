from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from BlogFastAPI.app.schemas.user import UserSchemeOfficial, UserUpdate, UserRoleScheme
from BlogFastAPI.app.core.security import USER_AUTH, oauth2_scheme
from BlogFastAPI.app.api.deps import check_token_status, get_current_active_user, get_admin_user
from BlogFastAPI.app.core.enums import UserRoles
from BlogFastAPI.app.models.user import User
from BlogFastAPI.app.middleware.role import UserMiddleware
from BlogFastAPI.app.services.users import UserService
from BlogFastAPI.app.utils.utils import get_db

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = oauth2_scheme


@router.get("/users/me/", response_model=UserSchemeOfficial)
async def read_users_me(
        current_user: User = Depends(get_current_active_user)
):
    return current_user

@router.get("/user/{user_id}/", response_model=UserSchemeOfficial)
async def get_user(
        user_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    user = UserService.get_user_by_id(db, user_id)
    return user

@router.put("/user-update/{user_id}/")
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
    ):
    user = UserService.get_user_by_id(db, user_id)
    hashed_password = USER_AUTH.get_hash_password(password=user_data.password)
    user.password = hashed_password
    return user

@router.get("/user-role/{user_id}/", response_model=UserRoleScheme)
async def get_user(
        user_id: int,
        current_user: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    user = UserService.get_user_by_id(db, user_id)
    return user


@router.get("/users")
async def users(user_role: Annotated[User,
                Depends(UserMiddleware.check_permission(role=UserRoles.ADMIN))],
                db: Session = Depends(get_db)
                ):
    users = UserService.get_all_users(db)
    return users