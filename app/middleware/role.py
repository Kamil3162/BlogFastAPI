from fastapi import Depends, HTTPException, status
from BlogFastAPI.app.api.deps import get_current_user
from BlogFastAPI.app.core.enums import UserRoles
from BlogFastAPI.app.utils.deps import CustomHTTPExceptions
class UserMiddleware:

    @staticmethod
    def check_permission(roles: UserRoles):
        def check_user_permission(current_user = Depends(get_current_user)):
            if user.role.value not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to perform this action"
                )
            return current_user
        return check_user_permission

