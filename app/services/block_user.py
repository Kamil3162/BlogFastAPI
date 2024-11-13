from sqlalchemy.orm import Session
from ..db.repositories.user import UserRepository, UserDoesntExists
from ..core.enums import BlacklistReason

class BlockUserService:
    def __init__(self, db: Session):
        self._db = db
        self._repository = BlockUserRepository
        self._user_repository = UserRepository
    def update_user(self, id: int, user_data: dict):
        obj_user = self._user_repository.get_user(id)

        if not obj_user:
            raise UserDoesntExists(
                f"User with following id:{id} doesnt exists"
            )

        for field, value in user_data.items():
            setattr(obj_user, field, value)

        return user_data

    def change_user_status(self, id: int, user_data: dict):
        obj_user = self._user_repository.get_user(id)

        if not obj_user:
            raise UserDoesntExists(
                f"User with following id:{id} doesnt exists"
            )

        for field, value in user_data.items():
            setattr(obj_user, field, value)

        return user_data

    def delete_blacklisted_flag(self):
        pass
