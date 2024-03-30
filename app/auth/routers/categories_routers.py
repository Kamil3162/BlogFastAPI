from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from BlogFastAPI.app.auth.user_manager.user_auth import USER_AUTH
from BlogFastAPI.app.db.models.models import User
from BlogFastAPI.app.utils.utils import get_db
from BlogFastAPI.app.services.categories_service import CategoryService
from BlogFastAPI.app.middleware.role_middleware import UserMiddleware
from BlogFastAPI.app.db.models.enums import UserRoles
from BlogFastAPI.app.auth.schemas.category_schemas import (
    CategoryScheme,
    CategoryObject
)

category_router = APIRouter()

@category_router.get('/categories')
async def fetch_all_categories(
        current_user: User = Depends(USER_AUTH.get_current_active_user),
        db: Session = Depends(get_db)
):
    categories = CategoryService.all_categories(db)
    return categories

@category_router.post('/create-category')
async def category_create(
        category_scheme: CategoryScheme,
        current_user: User = Depends(
            UserMiddleware.check_permission(UserRoles.MODERATOR)
        ),
        db: Session = Depends(get_db)
):
    category = CategoryService.create_category(db, category_scheme)

    return category

@category_router.delete('/delete-category/{category_id}')
async def category_delete(
        category_id,
        current_user: User = Depends(
            UserMiddleware.check_permission(UserRoles.MODERATOR)
        ),
        db: Session = Depends(get_db)
):
    operation_result = CategoryService.category_delete(db, category_id)
    return operation_result

@category_router.put('/category-update/{category_id}')
async def category_update(
        category_id,
        category_data: CategoryScheme,
        current_user: User = Depends(
            UserMiddleware.check_permission(UserRoles.MODERATOR)
        ),
        db: Session = Depends(get_db)
):
    category = CategoryService.category_update(category_id, db, category_data)
    return category