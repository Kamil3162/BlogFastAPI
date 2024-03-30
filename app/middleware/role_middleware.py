from BlogFastAPI.app.auth.user_manager.user_auth import get_current_user
from BlogFastAPI.app.db.models.enums import UserRoles
from BlogFastAPI.app.utils.exceptions_functions import CustomHTTPExceptions
from fastapi import Depends
class UserMiddleware:

    @staticmethod
    def check_permission(role: UserRoles):
        def check_user_permission(user = Depends(get_current_user)):
            if user.role.value != role.value:
                print("czeker permisji")
                raise CustomHTTPExceptions.forbidden()
            return user
        return check_user_permission

