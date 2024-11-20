from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import exc, or_
from sqlalchemy import select, delete

from ...models.user import User
from ...schemas.user import UserCreate, UserUpdate
from ...core.security import USER_AUTH
from ...core.enums import UserRoles

class UserRepository:

    def __init__(self, db: Session):
        self._db = db
        self.model = User
        self._user_manager = USER_AUTH

    def get_by_email(self, email: str):
        """
                Get a user by email address.

                Args:
                    email: User's email address

                Returns:
                    Optional[User]: User object if found, None otherwise
                """
        query = select(self.model).where(self.model.email == email)
        result = self._db.execute(query)
        return result.scalar_one_or_none()

    def get_by_id(self, user_id: int):
        """
                Get a user by email address.

                Args:
                    user_id: User ID in DB

                Returns:
                    Optional[User]: User object if found, None otherwise
                """
        query = select(self.model).where(self.model.id == user_id)
        result = self._db.execute(query)
        return result.scalar_one_or_none()

    def create_user(self, user_data: UserCreate) -> User:
        """
            Create a new user with ahshed password

            Args:
                user_data: UserCreate used to create a new user

            Returns:
                User: Created user object
        """
        hashed_password = self._user_manager.get_hash_password(
            user_data.password
        )

        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )

        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)

        return db_user

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """
            Update user information

            Args:
            user_id: ID of user to update
            user_data: UserUpdate schema with fields to update

        Returns:
            Optional[User]: Updated user object or None if not found
        """
        user_obj = self.get_by_id(user_id)

        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = self._user_manager.get_hash_password(
                update_data.pop("password")
            )

        for key, value in update_data.items():
            setattr(user_obj, key, value)

        self._db.commit()
        self._db.refresh()

        return user_obj

    def get_active_users(
            self,
            skip: int = 0,
            limit: int = 100,
            role: Optional[UserRoles] = None
    ) -> List[User]:
        """
        Get active users with optional role filter.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            role: Optional role filter

        Returns:
            List[User]: List of active users
        """
        query = select(self.model).where(self.model.is_active == True)

        if role:
            query = query.where(self.model.role == role)

        query = query.offset(skip).limit(limit)
        result = self._db.execute(query)

        return result.scalars().all()

    def search_user(self, search_term: str, skip:int = 0, limit:int = 10):
        search_pattern = f"%{search_term}%"
        query = (
            select(self.model).where(
                or_(
                    self.model.first_name.ilike(search_pattern),
                    self.model.email.ilike(search_pattern),
                    self.model.last_name.ilike(search_pattern)
                )
            ).offset(skip).limit(limit)
        )

        result = self._db.execute(query)

        return result.scalars().all()

    def delete_user(self, user_id):
        user = self.get_by_id(user_id)

        if not user:
            return False

        result = self._db.execute(
            delete(self.model).where(User.id == user_id)
        )
        return result.rowcount
