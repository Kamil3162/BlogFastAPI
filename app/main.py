import json
import sys
sys.path.append("../app")

from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from api.file import EG
from core.config import env_path1, settings
from db.database import SQLALCHEMY_DATABASE_URL
import uvicorn
import os

app = FastAPI()
env_path = Path(__file__).parent / 'config.env'

load_dotenv(dotenv_path=env_path)
GLOBAL_VARIABLE = os.getenv('POSTGRES_USER')

@app.get('/')
async def home():
    return {'key': 'value'}


@app.get('/web-chat')
async def webchat_app():
    print(GLOBAL_VARIABLE)
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



if __name__ == "__main__":
    uvicorn.run(app, port=10000)