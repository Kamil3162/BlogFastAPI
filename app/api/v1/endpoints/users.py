from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.schemas import UserSchemeOfficial, UserUpdate, UserRoleScheme
from ..user_manager.user_auth import USER_AUTH, oauth2_scheme, check_token_status
from ...db.models.enums import UserRoles
from ...db.models.models import User
from ...middleware.role_middleware import UserMiddleware
from ...services.users import UserService
from ...utils.utils import get_db

auth_router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = oauth2_scheme


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

@auth_router.put("/user-update/{user_id}/")
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
    ):
    user = UserService.get_user_by_id(db, user_id)
    hashed_password = USER_AUTH.get_hash_password(password=user_data.password)
    user.password = hashed_password
    return user

@auth_router.get("/user-role/{user_id}/", response_model=UserRoleScheme)
async def get_user(
        user_id: int,
        current_user: User = Depends(USER_AUTH.get_admin_user),
        db: Session = Depends(get_db)
):
    user = UserService.get_user_by_id(db, user_id)
    return user


@auth_router.get("/users")
async def users(user_role: Annotated[User,
                Depends(UserMiddleware.check_permission(role=UserRoles.ADMIN))],
                db: Session = Depends(get_db)
                ):
    users = UserService.get_all_users(db)
    return users