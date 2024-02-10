from sqlalchemy.orm import Session
from BlogFastAPI.app.db.models.models import User, BlacklistedUser
from BlogFastAPI.app.auth.user_manager.user_auth import USER_AUTH
from BlogFastAPI.app.utils.exceptions import CustomHTTPExceptions
from BlogFastAPI.app.db.models.enums import UserRoles
from BlogFastAPI.app.auth.schemas.schemas import UserSchemeOfficial
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
        # return exception not only none , its not good approach
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise CustomHTTPExceptions.not_found(f"User with ID:{user_id} not found")
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