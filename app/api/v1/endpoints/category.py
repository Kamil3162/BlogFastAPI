from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from ....api.deps import get_current_active_user
from ....models.user import User
from ....utils.utils import get_db
from ....services.categories import CategoryService
from ....middleware.role import UserMiddleware
from ....core.enums import UserRoles
from ....schemas.category import (
    CategoryScheme,
    CategoryObject
)
from ...deps import get_category_service

router = APIRouter()

@router.get('/categories')
async def fetch_all_categories(
    current_user: User = Depends(get_current_active_user),
    category_service: CategoryService = Depends(get_category_service)
):
    categories = category_service.all_categories()
    return categories

@router.post('/create-category')
async def category_create(
    category_scheme: CategoryScheme,
    # current_user: User = Depends(
    #     UserMiddleware.check_permission(UserRoles.MODERATOR)
    # ),
    category_service: CategoryService = Depends(get_category_service)
):
    category = category_service.create_category(category_scheme)
    return category

@router.delete('/delete-category/{category_id}')
async def category_delete(
    category_id,
    current_user: User = Depends(
        UserMiddleware.check_permission(UserRoles.MODERATOR)
    ),
    category_service: CategoryService = Depends(get_category_service)
):
    operation_result = category_service.category_delete(category_id)
    return operation_result

@router.put('/category-update/{category_id}')
async def category_update(
    category_id,
    category_data: CategoryObject,
    current_user: User = Depends(
        UserMiddleware.check_permission(UserRoles.MODERATOR)
    ),
    category_service: CategoryService = Depends(get_category_service)
):
    category = category_service.category_update(category_data)

    return category