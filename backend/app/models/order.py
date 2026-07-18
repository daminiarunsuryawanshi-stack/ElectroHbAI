from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    total_amount = Column(Float)

    status = Column(
        String(50),
        default="Pending"
    )

    shipping_address = Column(String(255))

    user = relationship("User")