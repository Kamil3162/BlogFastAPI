import uvicorn
import sys
import json
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from .core.config import env_path1, settings
from .auth.routers.routers import router
from .auth.routers.authentication_routers import auth_router
from .auth.routers.create_routers import create_post_router
from .auth.routers.comments_routers import comment_routers
from .auth.routers.ws_routers import create_ws_app
from .db.database import (
    SQLALCHEMY_DATABASE_URL,
    Base,
    SessionLocal,
    engine
)
from .db.models import models
from .utils.utils import get_db
from .middleware.docs_middleware import DocsBlockMiddleware
from fastapi.middleware.cors import CORSMiddleware
from BlogFastAPI.app.auth.routers.categories_routers import category_router

models.Base.metadata.create_all(bind=engine)

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


@app.get('/')
async def home():
    return {'key': 'value'}


@app.get('/web-chat')
async def webchat_app():
    print(settings.POSTGRES_DB)
    print(get_db())
    return {'web_chat': 'application'}


@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    """
        Needy is obligatory and we have to pass this to our function
    :param item_id:
    :param needy:
    :return:
    """
    item = {"item_id": item_id, "needy": needy}
    return json.dump(item)


#
if __name__ == "__main__":
    pass
