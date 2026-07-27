from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.product import Product
from app.ml.recommendation import RecommendationEngine


class RecommendationService:

    @staticmethod
    def get_recommendations(db: Session, product_id: int, top_n: int = 8):

        # Try ML-based recommendations first
        try:
            engine = RecommendationEngine(db)
            ml_recommendations = engine.recommend(product_id, top_n=8)
            
            if ml_recommendations:
                return ml_recommendations
        except Exception as e:
            print(f"ML recommendation failed: {e}")
            # Fall back to database query
            pass

        # Fallback: Use database query (category/brand/price)
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

        # If no recommendations found from ML or DB heuristics, return top-rated products
        # excluding the current product so the UI shows something useful.
        if not recommendations:
            recommendations = (
                db.query(Product)
                .filter(Product.id != current.id)
                .order_by(Product.rating.desc(), Product.price.asc())
                .limit(top_n)
                .all()
            )

        return recommendations