from fastapi import APIRouter

from .endpoints import (
    users,
    auth,
    posts,
    comments,
    category,
    test,
    ws,
    images
)


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(comments.router,
                          prefix="/comments",
                          tags=["comments"])
api_router.include_router(category.router,
                          prefix="/categories",
                          tags=["categories"])
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(ws.router, prefix="/ws", tags=["ws"])
api_router.include_router(images.router, prefix="/image", tags=["images"])
