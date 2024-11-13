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
        user = self._db.query(User) \
                   .filter(User.id == user_id).first() is not None
        return user




