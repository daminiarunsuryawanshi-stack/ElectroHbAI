import joblib
import pandas as pd
import os

from sqlalchemy.orm import Session

from app.models.product import Product

# Get the directory where this script is located
ML_DIR = os.path.dirname(os.path.abspath(__file__))


class RecommendationEngine:

    def __init__(self, db: Session):

        self.db = db

        self.df = pd.read_pickle(os.path.join(ML_DIR, "products.pkl"))

        self.similarity = joblib.load(
            os.path.join(ML_DIR, "similarity.pkl")
        )

    def recommend(
        self,
        product_id: int,
        top_n: int = 8
    ):

        if product_id not in self.df["id"].values:
            return []

        idx = self.df.index[
            self.df["id"] == product_id
        ][0]

        scores = list(
            enumerate(
                self.similarity[idx]
            )
        )

        scores = sorted(
            scores,
            key=lambda x: x[1],
            reverse=True
        )[1:top_n + 1]

        ids = [
            int(self.df.iloc[i]["id"])
            for i, _ in scores
        ]

        products = (
            self.db.query(Product)
            .filter(Product.id.in_(ids))
            .all()
        )

        return products