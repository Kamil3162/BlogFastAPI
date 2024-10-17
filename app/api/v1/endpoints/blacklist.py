
# Import builtin modules
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....schemas.user import BlacklistedUserSchema
from ....core.security import oauth2_scheme
from ....utils.utils import get_db
from ....services.users import UserService

router = APIRouter()

@router.get('/blacklisted-user/', response_model=BlacklistedUserSchema)
async def blacklisted_users(db: Session = Depends(get_db)):
    return {"message": "Function entered"}  # Temporary line for testing


@router.get('/blacklisted-users/', response_model=List[BlacklistedUserSchema])
async def blacklisted_users(token: Annotated[str, Depends(oauth2_scheme)],
                            db: Session = Depends(get_db)):
    users = UserService.blacklisted_users(db)
    return users


