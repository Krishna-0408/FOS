from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repository.user_repository import UserRepository
from app.schemas.user_schema import UserSignup
from app.core.email import send_welcome_email

from fastapi import BackgroundTasks
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