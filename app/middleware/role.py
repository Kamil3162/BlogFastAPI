from fastapi import Depends, HTTPException, status

from ..api.deps import authenticate_user_from_token
from ..core.enums import UserRoles

class UserMiddleware:

    @staticmethod
    def check_permission(role: UserRoles):
        def check_user_permission(
            current_user=Depends(authenticate_user_from_token)
        ):
            if current_user.role.value is role.value:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to perform this action"
                )
            return current_user
        return check_user_permission


