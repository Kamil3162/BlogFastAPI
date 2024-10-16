import json
from dotenv import load_dotenv
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# from BlogFastAPI.app.core.config import settings
from .core.config import settings
from BlogFastAPI.app.db.session import engine
from BlogFastAPI.app.utils.utils import get_db
from BlogFastAPI.app.db.init_db import init_db
from BlogFastAPI.app.api.v1.router import api_router
from BlogFastAPI.app.middleware.database import DataBaseErrorMiddleware
from BlogFastAPI.app.middleware.docs import DocsBlockMiddleware


init_db(Session)

app = FastAPI(docs_url='/docs', redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    # Adjust this to your React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_origin_regex="https?://.*",
    allow_headers=[
        "Access-Control-Allow-Headers","Content-Type", "Authorization",
        "Access-Control-Allow-Origin", "Set-Cookie"],
)

app.add_middleware(DocsBlockMiddleware)
app.add_middleware(DataBaseErrorMiddleware)

app.include_router(api_router)

env_path = Path(__file__).parent / 'config.env'

load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
