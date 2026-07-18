import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sqlalchemy.orm import Session
from app.core.database import SessionLocal

from app.models.brand import Brand
from app.models.category import Category
from app.models.product import Product


db: Session = SessionLocal()

products = db.query(Product).all()

rows = []

for p in products:

    text = f"""
    {p.name}
    {p.manufacturer}
    {p.description}
    """

    rows.append({

        "id": p.id,

        "name": p.name,

        "text": text

    })

df = pd.DataFrame(rows)

vectorizer = TfidfVectorizer(
    stop_words="english"
)

matrix = vectorizer.fit_transform(
    df["text"]
)

similarity = cosine_similarity(
    matrix
)

joblib.dump(
    vectorizer,
    "app/ml/vectorizer.pkl"
)

joblib.dump(
    similarity,
    "app/ml/similarity.pkl"
)

df.to_pickle(
    "app/ml/products.pkl"
)

db.close()

print("Recommendation model trained successfully.")