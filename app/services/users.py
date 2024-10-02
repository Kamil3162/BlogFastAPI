from sqlalchemy.orm import Session

from BlogFastAPI.app.schemas.token import ResetTokenSchemas
from ..models.user import User, BlacklistedUser
from BlogFastAPI.app.core.security import USER_AUTH
from BlogFastAPI.app.utils.deps import CustomHTTPExceptions
from BlogFastAPI.app.core.enums import UserRoles
from BlogFastAPI.app.schemas.user import UserSchemeOfficial
from typing import List
class UserService:

    @staticmethod
    def create_user(db: Session, user):
        # test does it work properly and rolled back
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

    @staticmethod
    def update_user(db: Session, user, user_id):
        # test update user
        db_user = UserService.get_user_by_id(db, user_id)

        for key, value in user.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
        db.commit()

        return db_user

    @staticmethod
    def blacklisted_users(db: Session, page=0):
        # imporve using pagination
        blacklisted_users = db.query(BlacklistedUser).slice(
            page*10, (page+1)*10).all()
        return blacklisted_users

    @staticmethod
    def get_user_by_id(db: Session, user_id):
        try:
            user = db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            CustomHTTPExceptions.handle_db_exeception(exception=e)
        else:
            return user

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

    @staticmethod
    def get_all_users(db: Session) -> List[UserSchemeOfficial]:
        db_users = db.query(User).all()
        return [UserSchemeOfficial.model_validate(user) for user in db_users]

    @staticmethod
    def get_user_by_email(email_user: str, db: Session):
        db_user = db.query(User).filter(User.email == email_user).first()
        return db_user

    @staticmethod
    def set_new_password(email, db, password_data: ResetTokenSchemas):
        db_user = UserService.get_user_by_email(email, db)
        hashed_password = USER_AUTH.get_hash_password(password_data.password)

        db_user.password = hashed_password

        db.commit()
