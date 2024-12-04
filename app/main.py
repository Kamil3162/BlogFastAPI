import json
from dotenv import load_dotenv
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import my packages
from .db.init_db import init_db
from .api.v1.router import api_router
from .middleware.database import DataBaseErrorMiddleware
from .middleware.docs import DocsBlockMiddleware
from .core.handlers.request_handler import setup_exception_handlers
from .core.handlers.req_handler import setup_server_exc_handler


app = FastAPI(docs_url='/docs', redoc_url=None)

@app.on_event("startup")
async def startup():
    init_db()

setup_exception_handlers(app=app)
setup_server_exc_handler(app=app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    #allow_origin_regex="https?://.*",
    allow_headers=[
        "Access-Control-Allow-Headers","Content-Type", "Authorization",
        "Access-Control-Allow-Origin", "Set-Cookie"],
)

# app.add_middleware(DocsBlockMiddleware)
# app.add_middleware(DataBaseErrorMiddleware)

app.include_router(api_router)

env_path = Path(__file__).parent / 'config.env'
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=10000)
