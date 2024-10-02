from BlogFastAPI.app.api.deps import get_current_user
from BlogFastAPI.app.core.enums import UserRoles
from BlogFastAPI.app.utils.deps import CustomHTTPExceptions
from fastapi import Depends
class UserMiddleware:

    @staticmethod
    def check_permission(role: UserRoles):
        def check_user_permission(user = Depends(get_current_user)):
            if user.role.value != role.value:
                raise CustomHTTPExceptions.forbidden()
            return user
        return check_user_permission

