from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repository.user_repository import UserRepository
from app.core.jwt import verify_access_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = verify_access_token(token, db)

    user = UserRepository.get_user_by_id(db, payload["user_id"])

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found."
        )

    return user