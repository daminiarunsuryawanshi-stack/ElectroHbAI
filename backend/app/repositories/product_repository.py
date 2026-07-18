from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "id",
        order: str = "asc"
    ):

        query = db.query(Product)

        sort_column = getattr(Product, sort_by, Product.id)

        if order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        return (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: int
    ):
        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def search(
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 20
    ):
        return (
            db.query(Product)
            .filter(Product.name.ilike(f"%{keyword}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def by_brand(
        db: Session,
        brand_id: int,
        skip: int = 0,
        limit: int = 20
    ):
        return (
            db.query(Product)
            .filter(Product.brand_id == brand_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def by_category(
        db: Session,
        category_id: int,
        skip: int = 0,
        limit: int = 20
    ):
        return (
            db.query(Product)
            .filter(Product.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )