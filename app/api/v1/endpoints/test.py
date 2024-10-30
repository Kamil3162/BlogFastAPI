from dotenv import load_dotenv
from fastapi import Request
from pathlib import Path
from fastapi.routing import APIRouter
from ....core.config import settings
from ....api.deps import get_db

router = APIRouter()

main_directory_name = Path(__name__).parent.parent

@router.get('/')
async def home():
    print(main_directory_name)
    return {'key': 'value'}

@router.get('/test-get')
async def test_req(request: Request):
    client = request.client.host
    return {"client:": client}


@router.get('/web-chat')
async def webchat_app():
    print(settings.POSTGRES_DB)
    print(get_db())
    return {'web_chat': 'application'}


@router.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    """
        Needy is obligatory and we have to pass this to our function
        :param item_id:
        :param needy:
        :return:
    """
    item = {"item_id": item_id, "needy": needy}
    return json.dump(item)

