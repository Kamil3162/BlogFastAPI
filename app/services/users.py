from typing import List

from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from ..schemas.token import ResetTokenSchemas
from ..models.user import User, BlacklistedUser
from ..core.security import USER_AUTH
from ..utils.deps import CustomHTTPExceptions
from ..core.enums import UserRoles
from ..schemas.user import UserSchemeOfficial
from ..db.repositories.user import UserRepository
from ..exceptions.user import UserDoesntExists
class UserService:
    def __init__(self, db):
        self._db = db
        self._user_repository = UserRepository(self._db)

    @staticmethod
    def create_user(db: Session, user):
        # test does it work properly and rolled back
        # self._user_repository.get_user(user)

        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            return None  # User already exists

        hashed_password = USER_AUTH.get_hash_password(
            user.password)  # Adjust as necessary
        db_user = User(email=user.email, first_name=user.first_name,
                       last_name=user.last_name,
                       hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_user(self, user, user_id):
        # test update user
        db_user = UserService.get_user_by_id(self._db, user_id)

        for key, value in user.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
        self._db.commit()

        return db_user

    @staticmethod
    def blacklisted_users(db: Session, page=0):
        # imporve using pagination
        blacklisted_users = db.query(BlacklistedUser).slice(
            page*10, (page+1)*10).all()
        return blacklisted_users

    def get_user_by_id(self, user_id):
        try:
            user = self._db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User doesnt exists"
                )

            return user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e
            )

    @staticmethod
    def check_post_create_permission(db: Session, user_id):
        try:
            user = UserService.get_user_by_id(db, user_id)
        except CustomHTTPExceptions as e:
            # Handle the case where the user does not exist.
            raise CustomHTTPExceptions.not_found(
                f"Cannot check permission: {e}")

        return UserService.has_valid_role_for_post_creation(user)

    @staticmethod
    def has_valid_role_for_post_creation(user):
        valid_roles = [role.value for role in UserRoles]
        return user.role in valid_roles

    def get_all_users(self) -> List[UserSchemeOfficial]:
        db_users = self._db.query(User).all()
        return [UserSchemeOfficial.model_validate(user) for user in db_users]

    @staticmethod
    def get_user_by_email(email_user: str, db: Session):
        db_user = db.query(User).filter(User.email == email_user).first()
        return db_user

    def set_new_password(self, email, password_data: ResetTokenSchemas):
        db_user = UserService.get_user_by_email(email, self._db)
        hashed_password = USER_AUTH.get_hash_password(password_data.password)

        db_user.password = hashed_password

        self._db.commit()
