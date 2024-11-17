import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import select

from ...models.user import BlacklistedUser, BlacklistReason

class BlackUserRepository:
    def __init__(self, db: Session):
        self._db = db

    def create_black_user(
            self,
            user_id,
            reason: BlacklistReason
    ) -> Optional[BlacklistedUser]:
        existing_blacklist = self.get_black_list_info(user_id)
        if existing_blacklist:
            return None

        # Create blacklist entry
        blacklist_entry = BlacklistedUser(
            user_id=user_id,
            blocked_data=datetime.datetime.utcnow(),
            reason=reason
        )

        self._db.add(blacklist_entry)
        self._db.commit()
        self._db.refresh(blacklist_entry)

        return blacklist_entry

    def delete_black_flag(self, user_id: int) -> bool:
        """Remove blacklist entry for a user"""
        blacklist_entry = self.get_black_list_info(user_id)
        if not blacklist_entry:
            return False

        self._db.delete(blacklist_entry)
        self._db.commit()

        return True

    def get_black_list_info(self, user_id):
        query = select(BlacklistedUser).where(BlacklistedUser.id == user_id)
        result = self._db.execute(query)
        return result.scalar_one_or_none()

    def get_all_back_listed(
            self,
            skip: int = 0,
            limit: int = 100,
            reason: Optional[BlacklistReason] = None
    ) -> List[BlacklistedUser]:
        query = select(BlacklistedUser)

        if reason:
            query = query.where(BlacklistedUser.reason == reason)

        query = query.offset(skip).limit(limit=limit)
        result = self._db.execute(query)
        return result

    def del_black_flag(self, user_id):
        blacklisted_user = self.get_black_list_info(user_id)

        if not blacklisted_user:
            return False

        self._db.delete(blacklisted_user)
        self._db.commit()

    def update_black_flag(self, user_id, post_data: dict):
        user = self.get_black_list_info(user_id)

        if user:
            for key, value in post_data.items():
                setattr(user, key, value)

            self._db.commit()
            self._db.refresh(user)

        return user