import uvicorn
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from core.config import env_path1, settings
from auth.routers.routers import router
from auth.routers.authentication_routers import auth_router
from db.database import (
    SQLALCHEMY_DATABASE_URL,
    Base,
    execute_db_migrations,
    connection_checker,
    SessionLocal,
    engine
)
from db.models import models
from utils.utils import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
app.include_router(auth_router)

env_path = Path(__file__).parent / 'config.env'

load_dotenv(dotenv_path=env_path)
# connection_checker()
# execute_db_migrations()


@app.get('/')
async def home():
    return {'key': 'value'}


@app.get('/web-chat')
async def webchat_app():
    print(settings.POSTGRES_DB)
    print(get_db())
    return {'web_chat':'application'}

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

@app.get("/users")
async def users():
    pass



# @app.post("/users/")
# def create_user(username: str, email: str, db: Session = Depends(get_db)):
#     db_user = User(username=username, email=email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


if __name__ == "__main__":
    uvicorn.run(app, port=10000)