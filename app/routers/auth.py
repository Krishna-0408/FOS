from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user_schema import UserSignup
from app.services.auth_service import AuthService
from fastapi import APIRouter, Depends, BackgroundTasks
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