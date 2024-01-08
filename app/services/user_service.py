from sqlalchemy.orm import Session
from BlogFastAPI.app.db.models.models import User, BlacklistedUser
from BlogFastAPI.app.auth.user_manager.user_auth import USER_AUTH
class UserService:

    @staticmethod
    def create_user(db: Session, user):
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
    def blacklisted_users(db: Session, page=None):
        blacklisted_users = db.query(BlacklistedUser).all()
        return blacklisted_users

