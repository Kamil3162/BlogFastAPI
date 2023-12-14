from fastapi import HTTPException, Response, Request, APIRouter


router = APIRouter()


@router.get('/register')
async def register():
    return {"konto": "utworzono"}


@router.post('/login')
async def login():
    return {"token": "zalogowano"}
