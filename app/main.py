import json
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.orm import Session
from .core.config import settings
from .auth.routers.blacklist import router
from .auth.routers.authentication import auth_router
from .auth.routers.posts import create_post_router
from .auth.routers.comments import comment_routers
from .auth.routers.ws import create_ws_app
from .db.session import (
    engine
)
from BlogFastAPI.app.db.init_db import init_db
from .utils.utils import get_db
from fastapi.middleware.cors import CORSMiddleware
from BlogFastAPI.app.auth.routers.category import category_router

init_db(Session)

app = FastAPI(docs_url='/docs', redoc_url=None)
# app.add_middleware(DocsBlockMiddleware)

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:3000"],
                   # Adjust this to your React app's origin
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_origin_regex='https?://.*',
                   allow_headers=["Access-Control-Allow-Headers",
                                  "Content-Type", "Authorization",
                                  "Access-Control-Allow-Origin", "Set-Cookie"],
                   )

app.include_router(router)
app.include_router(auth_router)
app.include_router(create_post_router)
app.include_router(comment_routers)
app.include_router(create_ws_app)
app.include_router(category_router)

env_path = Path(__file__).parent / 'config.env'

load_dotenv(dotenv_path=env_path)


if __name__ == "__main__":
    pass
