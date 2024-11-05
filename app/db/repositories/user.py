from sqlalchemy.orm import Session
from sqlalchemy import exc

from ...models.user import User

class UserDoesntExists(Exception):
    """
        Exception during user was not found
    """
    pass


class UserRepository:

    def __init__(self, db):
        self._db = db

    def get_user(self, user_id: int):
        try:
            user = self._db.query(User) \
                       .filter(User.id == user_id).first() is not None
            return user
        except Exception as e:
            raise UserDoesntExists(f"User with ID:{user_id} doesnt exists")




