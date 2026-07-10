from sqlalchemy.orm import Session

from app.core import email
from app.database.models.user import User
from app.schemas.user_schema import UserSignup
from app.core.security import hash_password


class UserRepository:

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_phone(db: Session, phone: str):
        return db.query(User).filter(User.phone == phone).first()

    @staticmethod
    def create_user(db: Session, user: UserSignup):

        new_user = User(
            name=user.name,
            phone=user.phone,
            email=user.email,
            address=user.address,
            place=user.place,
            city=user.city,
            district=user.district,
            pincode=user.pincode,
            password=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    

    @staticmethod
    def get_user_by_email(db: Session, email: str):

        return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


    @staticmethod
    def update_password(
    db: Session,
    user,
    hashed_password
):

        user.password = hashed_password

        db.commit()

        db.refresh(user)

        return user