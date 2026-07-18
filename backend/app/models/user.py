from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100)
    )

    email = Column(
        String(255),
        unique=True,
        index=True
    )

    password = Column(
        String(255)
    )

    role = Column(
        String(50)
    )

    phone = Column(
        String(20)
    )

    address = Column(
        String(255)
    )