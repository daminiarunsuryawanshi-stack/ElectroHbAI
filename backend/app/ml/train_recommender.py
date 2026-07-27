import joblib
import pandas as pd
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sqlalchemy.orm import Session
from app.core.database import SessionLocal

from app.models.brand import Brand
from app.models.category import Category
from app.models.product import Product

# Get the directory where this script is located
ML_DIR = os.path.dirname(os.path.abspath(__file__))


db: Session = SessionLocal()

products = db.query(Product).all()

rows = []

for p in products:

    text = f"""
    {p.name}
    {p.description if p.description else ''}
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
    os.path.join(ML_DIR, "vectorizer.pkl")
)

joblib.dump(
    similarity,
    os.path.join(ML_DIR, "similarity.pkl")
)

df.to_pickle(
    os.path.join(ML_DIR, "products.pkl")
)

db.close()

print("Recommendation model trained successfully.")
