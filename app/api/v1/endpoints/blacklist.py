from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.schemas import BlacklistedUserSchema
from ..user_manager.user_auth import oauth2_scheme
from BlogFastAPI.app.utils.utils import get_db
from BlogFastAPI.app.services.users import UserService
from typing import Annotated, List

router = APIRouter()

@router.get('/blacklisted-user/', response_model=BlacklistedUserSchema)
async def blacklisted_users(db: Session = Depends(get_db)):
    return {"message": "Function entered"}  # Temporary line for testing


@router.get('/blacklisted-users/', response_model=List[BlacklistedUserSchema])
async def blacklisted_users(token: Annotated[str, Depends(oauth2_scheme)],
                            db: Session = Depends(get_db)):
    users = UserService.blacklisted_users(db)
    return users


