from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean

from app.core.database import Base


class Coupon(Base):

    __tablename__ = "coupons"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String(50),
        unique=True
    )

    discount = Column(
        Float
    )

    active = Column(
        Boolean,
        default=True
    )