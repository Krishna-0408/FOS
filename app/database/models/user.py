import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Text
)
from sqlalchemy.sql import func

from app.database.database import Base


class UserRole(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    RESTAURANT_ADMIN = "RESTAURANT_ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    phone = Column(
        String(10),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    address = Column(Text, nullable=False)

    place = Column(String(100), nullable=False)

    city = Column(String(100), nullable=False)

    district = Column(String(100), nullable=False)

    pincode = Column(String(6), nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.CUSTOMER
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )