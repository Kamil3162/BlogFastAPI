from fastapi import HTTPException, Response, Request, APIRouter, status, Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas.schemas import UserCreate, UserResponse
from ..user_manager.user_auth import USER_AUTH
from db.models.models import User
from utils.utils import get_db

router = APIRouter()

@router.post('/register', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = USER_AUTH.get_hash_password(user.password)
    db_user = User(email=user.email, first_name=user.first_name,
                     last_name=user.last_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


