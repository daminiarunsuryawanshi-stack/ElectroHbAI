from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.product import Product


class RecommendationService:

    @staticmethod
    def get_recommendations(db: Session, product_id: int):

        current = (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if not current:
            return []

        min_price = current.price * 0.7
        max_price = current.price * 1.3

        recommendations = (
            db.query(Product)
            .filter(
                Product.id != current.id,
                or_(
                    Product.category_id == current.category_id,
                    Product.brand_id == current.brand_id,
                    Product.price.between(min_price, max_price)
                )
            )
            .order_by(
                Product.rating.desc(),
                Product.price.asc()
            )
            .all()
        )

        return recommendations