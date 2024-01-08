from fastapi import HTTPException, Response, Request, APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..schemas.schemas import UserCreate, UserResponse, BlacklistedUserSchema
from ..user_manager.user_auth import USER_AUTH, oauth2_scheme
from BlogFastAPI.app.db.models.models import User
from BlogFastAPI.app.utils.utils import get_db
from BlogFastAPI.app.services.user_service import UserService
from typing import Annotated, List
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

@router.get('/blacklisted-user/', response_model=BlacklistedUserSchema)
async def blacklisted_users(db: Session = Depends(get_db)):
    # add here instance to return
    # print("testowanie")
    # print("testowanie")
    # print("testowanie")
    # users = UserService.blacklisted_users(db)
    # return users
    return {"message": "Function entered"}  # Temporary line for testing


@router.get('/blacklisted-users/', response_model=List[BlacklistedUserSchema])
async def blacklisted_users(token: Annotated[str, Depends(oauth2_scheme)],
                            db: Session = Depends(get_db)):
    users = UserService.blacklisted_users(db)
    return users


