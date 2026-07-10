from sqlalchemy.orm import Session
from app.database.models.password_reset_otp import PasswordResetOTP


class OTPRepository:

    @staticmethod
    def create(db: Session, otp_data: PasswordResetOTP):
        db.add(otp_data)
        db.commit()
        db.refresh(otp_data)
        return otp_data

    @staticmethod
    def get_latest_otp(db: Session, user_id: int):
        return (
            db.query(PasswordResetOTP)
            .filter(
                PasswordResetOTP.user_id == user_id,
                PasswordResetOTP.is_used == False
            )
            .order_by(PasswordResetOTP.created_at.desc())
            .first()
        )

    @staticmethod
    def mark_as_used(db: Session, otp_record: PasswordResetOTP):
        otp_record.is_used = True
        db.commit()

    @staticmethod
    def get_valid_otp(db: Session, user_id: int, otp: str):
        return (
            db.query(PasswordResetOTP)
            .filter(
                PasswordResetOTP.user_id == user_id,
                PasswordResetOTP.otp == otp,
                PasswordResetOTP.is_used == False
            )
            .first()
        )
    
    @staticmethod
    def mark_used(
       db: Session,
       otp_record
):

       otp_record.is_used = True

       db.commit()