from sqlalchemy.orm import Session

from app.database.models.token_blacklist import BlacklistedToken


class TokenRepository:

    @staticmethod
    def blacklist_token(db: Session, token: str):

        blacklist = BlacklistedToken(
            token=token
        )

        db.add(blacklist)
        db.commit()

    @staticmethod
    def is_blacklisted(db: Session, token: str):

        return (
            db.query(BlacklistedToken)
            .filter(
                BlacklistedToken.token == token
            )
            .first()
        )