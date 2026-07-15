from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.database.models.user import User, UserRole


def customer_only(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access only."
        )

    return current_user


def restaurant_admin_only(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.RESTAURANT_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Restaurant Admin access only."
        )

    return current_user


def super_admin_only(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin access only."
        )

    return current_user