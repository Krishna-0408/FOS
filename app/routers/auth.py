from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user_schema import UserSignup
from app.services.auth_service import AuthService
from fastapi import APIRouter, Depends, BackgroundTasks
from app.schemas.user_schema import LoginRequest
from app.core.dependencies import get_current_user
from app.database.models.user import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user_schema import ForgotPasswordRequest
from app.schemas.user_schema import VerifyOTPRequest
from app.schemas.user_schema import ResetPasswordRequest
security = HTTPBearer()


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/signup", status_code=201)
def signup(
    user: UserSignup,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return AuthService.signup(
        db,
        user,
        background_tasks
    )

@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login(
        db,
        user
    )

@router.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "status": True,
        "data": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "phone": current_user.phone,
            "city": current_user.city
        }
    }
@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    return AuthService.logout(
        db,
        token
    )

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    return AuthService.forgot_password(
        db,
        request,
        background_tasks
    )

@router.post("/verify-otp")
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):

    return AuthService.verify_otp(
        db,
        request
    )

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    return AuthService.reset_password(
        db,
        request
    )