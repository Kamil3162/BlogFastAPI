from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....schemas.user import UserSchemeOfficial, UserUpdate, UserRoleScheme
from ....core.security import USER_AUTH, oauth2_scheme, check_token_status
from ....api.deps import get_current_active_user, get_admin_user
from ....core.enums import UserRoles
from ....models.user import User
from ....middleware.role import UserMiddleware
from ....services.users import UserService
from ....utils.utils import get_db
from ...deps import get_user_service

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = oauth2_scheme

# Define common dependencies
CommonDeps = Depends(get_current_active_user)
AdminDeps = Depends(get_admin_user)
DBDeps = Depends(get_db)


@router.get("/users/me/", response_model=UserSchemeOfficial)
async def read_users_me(current_user: User = CommonDeps):
    return current_user


@router.get("/user/{user_id}/", response_model=UserSchemeOfficial)
async def get_user(
        user_id: int,
        current_user: User = CommonDeps,
        user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/user-update/{user_id}/", response_model=UserSchemeOfficial)
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        current_user: User = CommonDeps,
        user_service: UserService = Depends(get_user_service)
):
    if current_user.id != user_id and current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=403,
                            detail="Not authorized to update this user")

    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = user_service.update_user(user_id, user_data)
    return updated_user


@router.get("/user-role/{user_id}/", response_model=UserRoleScheme)
async def get_user_role(
        user_id: int,
        current_user: User = AdminDeps,
        user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users")
async def users(
    # user_role: Annotated[User,
    # Depends(UserMiddleware.check_permission(role=UserRoles.MODERATOR))],
    user_service: UserService = Depends(get_user_service)
):
    users = user_service.get_all_users()
    return users


@router.get("/mock")
async def users_mock(
    # user_role: Annotated[User,
    # Depends(UserMiddleware.check_permission(role=UserRoles.MODERATOR))],
    user_service: UserService = Depends(get_user_service)
):
    users = user_service.get_all_users()
    return users