from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from app.core.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255)
    )

    description = Column(
        String(1000)
    )

    price = Column(
        Float
    )

    original_price = Column(
        Float
    )

    image = Column(
        String(500)
    )

    rating = Column(
        Float,
        default=0
    )

    review_count = Column(
        Integer,
        default=0
    )

    stock = Column(
        Integer
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    brand_id = Column(
        Integer,
        ForeignKey("brands.id")
    )

    ram = Column(
        String(50)
    )

    storage = Column(
        String(50)
    )

    processor = Column(
        String(100)
    )

    battery = Column(
        String(100)
    )

    display = Column(
        String(100)
    )

    camera = Column(
        String(100)
    )