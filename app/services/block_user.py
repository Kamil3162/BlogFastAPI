from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError
from fastapi import status
from fastapi.responses import HTMLResponse

from ..db.repositories.user import UserRepository
from ..db.repositories.block_user import BlackUserRepository
from ..schemas.user import BlacklistedUserSchema
from ..models.user import BlacklistedUser
from ..exceptions.user import UserDoesntExists


class BlockUserService:
    def __init__(self, db: Session):
        self._db = db
        self._repository = BlackUserRepository
        self._user_repository = UserRepository

    def change_user_status(self, user_data: BlacklistedUserSchema):
        obj_user = self._user_repository.get_user(user_data.id)

        if not obj_user:
            raise UserDoesntExists(
                f"User with following id:{id} doesnt exists"
            )

        for field, value in user_data.items():
            setattr(obj_user, field, value)

        return user_data

    def create_blackuser(
            self,
            user_data: BlacklistedUserSchema
    ) -> Optional[BlacklistedUser]:

        obj_user = self._repository.get_black_list_info(user_data.id)

        if obj_user:
            raise IntegrityError(
                f"User with id:{user_data.id} already exsists"
            )

        reason = user_data.reason
        user = self._repository.create_black_user(user_data.id, reason)

        return user

    def delete_black_user(self, user_id):
        obj_user = self._repository.get_black_list_info(user_id=user_id)

        if not obj_user:
            raise DataError(
                f"You cant delete user with id:{user_id}, it doesnt exists"
            )

        result = self._repository.del_black_flag(user_id)

        if result:
            return HTMLResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "Black user success delete"
                }
            )

        return HTMLResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "Not found user"
            }
        )



