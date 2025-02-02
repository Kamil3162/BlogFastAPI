from http.client import HTTPResponse

from fastapi import APIRouter, Depends

from ....api.deps import get_post_service, get_post_view_service
from ....services.post import PostService, PostViewService
from ....services.users import UserService
router = APIRouter()


@router.get("/posts/info")
async def get_posts_by_category(
    user_id: int,
    post_service: PostService = Depends(get_post_service),
    post_view_service: PostViewService = Depends(get_post_view_service),
    #user: User = Depends(get_current_active_user)
):
    posts = post_view_service.get_views_by_user(user_id)
    return posts


@router.get("/statistic-total/{user_id}")
def get_trading_post(
    user_id: int,
    post_view_service: PostViewService = Depends(get_post_view_service),
    #user: User = Depends(get_current_active_user)
):
    result = post_view_service.generate_views_monthly(user_id)
    return result


@router.get("/statistic/{user_id}")
async def user_post_statistic(
    user_id: int,
    post_view_service: PostViewService = Depends(get_post_view_service),
    # user: UserService = Depends(UserService)
):
    result = post_view_service.generate_posts_views_monthly(user_id)
    return result


@router.get("/admin/rating/{post_id}")
async def admin_rating(
    post_id: int,
    post_view_service: PostViewService = Depends(get_post_view_service)
):
    result = post_view_service.revenue_by_months(post_id)
    return result

