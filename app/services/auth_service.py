
import token

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.database.models import user
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import UserSignup
from app.core.email import send_welcome_email

from fastapi import BackgroundTasks
from app.schemas.user_schema import LoginRequest
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.repository.token_repository import TokenRepository
from datetime import datetime, timedelta

from app.database.models.password_reset_otp import PasswordResetOTP
from app.repository.otp_repository import OTPRepository
from app.utils.otp_generator import generate_otp
from app.core.email import send_otp_email
from app.schemas.user_schema import ForgotPasswordRequest
from app.schemas.user_schema import VerifyOTPRequest
from app.schemas.user_schema import ResetPasswordRequest
from app.core.security import hash_password
from app.schemas.user_schema import ChangePasswordRequest
from app.core.security import verify_password, hash_password

class AuthService:

    @staticmethod
    def signup(
        db: Session,
        user: UserSignup,
        background_tasks: BackgroundTasks
    ):

        existing_email = UserRepository.get_user_by_email(
            db,
            user.email
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered."
            )

        existing_phone = UserRepository.get_user_by_phone(
            db,
            user.phone
        )

        if existing_phone:
            raise HTTPException(
                status_code=400,
                detail="Phone number already registered."
            )

        new_user = UserRepository.create_user(
            db,
            user
        )

        background_tasks.add_task(
            send_welcome_email,
            new_user.name,
            new_user.email
        )

        return {
            "status": True,
            "message": "User registered successfully. Welcome email is being sent.",
            "data": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "phone": new_user.phone
            }
        }

    @staticmethod
    def login(db: Session, user: LoginRequest):

        db_user = UserRepository.get_user_by_email(
            db,
            user.email
            )

        if not db_user:
            raise HTTPException(
            status_code=404,
            detail="Email not registered."
        )

        if not verify_password(
        user.password,
        db_user.password
    ):
            raise HTTPException(
            status_code=401,
            detail="Invalid password."
        )

        token = create_access_token(
        {
            "sub": db_user.email,
            "user_id": db_user.id
        }
    )

        return {
        "status": True,
        "message": "Login successful.",
        "access_token": token,
        "token_type": "Bearer",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }

    
    @staticmethod
    def logout(db: Session, token: str):

        TokenRepository.blacklist_token(
        db,
        token
    )

        return {
        "status": True,
        "message": "Logout successful."
    }


    @staticmethod
    def forgot_password(
    db: Session,
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks
):

        user = UserRepository.get_user_by_email(
        db,
        request.email
    )

        if not user:
            raise HTTPException(
            status_code=404,
            detail="Email not registered."
        )

        otp = generate_otp()

        otp_record = PasswordResetOTP(
        user_id=user.id,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )

        OTPRepository.create(
        db,
        otp_record
    )

        background_tasks.add_task(
        send_otp_email,
        user.name,
        user.email,
        otp
    )

        return {
        "status": True,
        "message": "OTP has been sent to your email."
    }


    @staticmethod
    def verify_otp(
    db: Session,
    request: VerifyOTPRequest
):

        user = UserRepository.get_user_by_email(
        db,
        request.email
    )

        if not user:
            raise HTTPException(
            status_code=404,
            detail="Email not registered."
        )

        otp_record = OTPRepository.get_valid_otp(
        db,
        user.id,
        request.otp
    )

        if not otp_record:
            raise HTTPException(
            status_code=400,
            detail="Invalid OTP."
        )

        if otp_record.expires_at < datetime.utcnow():
            raise HTTPException(
            status_code=400,
            detail="OTP has expired."
        )

        return {
        "status": True,
        "message": "OTP verified successfully."
    }


    @staticmethod
    def reset_password(
    db: Session,
    request: ResetPasswordRequest
):

        user = UserRepository.get_user_by_email(
        db,
        request.email
    )

        if not user:
            raise HTTPException(
            status_code=404,
            detail="Email not found."
        )

        otp_record = OTPRepository.get_valid_otp(
        db,
        user.id,
        request.otp
    )

        if not otp_record:
            raise HTTPException(
            status_code=400,
            detail="Invalid OTP."
        )

        if otp_record.expires_at < datetime.utcnow():
            raise HTTPException(
            status_code=400,
            detail="OTP expired."
        )

        hashed = hash_password(
        request.new_password
    )

        UserRepository.update_password(
        db,
        user,
        hashed
    )

        OTPRepository.mark_used(
        db,
        otp_record
    )

        return {
        "status": True,
        "message": "Password reset successfully."
    }


    @staticmethod
    def change_password(
    db: Session,
    current_user,
    request: ChangePasswordRequest
):

        if not verify_password(
        request.current_password,
        current_user.password
    ):
            raise HTTPException(
            status_code=400,
            detail="Current password is incorrect."
        )

        if verify_password(
        request.new_password,
        current_user.password
    ):
            raise HTTPException(
            status_code=400,
            detail="New password cannot be the same as the current password."
        )

        hashed_password = hash_password(
        request.new_password
    )

        UserRepository.update_password(
        db,
        current_user,
        hashed_password
    )

        return {
        "status": True,
        "message": "Password changed successfully."
    }