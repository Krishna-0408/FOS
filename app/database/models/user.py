from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database.database import Base
from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    phone = Column(String(10), unique=True, nullable=False, index=True)

    email = Column(String(100), unique=True, nullable=False, index=True)

    address = Column(Text, nullable=False)

    place = Column(String(100), nullable=False)

    city = Column(String(100), nullable=False)

    district = Column(String(100), nullable=False)

    pincode = Column(String(6), nullable=False)

    password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )