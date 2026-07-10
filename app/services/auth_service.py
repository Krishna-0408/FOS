
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
