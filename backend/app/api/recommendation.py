from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.product import ProductResponse

from app.services.recommendation_service import RecommendationService
from fastapi import HTTPException
from pydantic import BaseModel
from app.ml.apriori_utils import recommend_next
from app.models.product import Product


router = APIRouter(

    prefix="/recommendation",

    tags=["Recommendation"]

)


@router.get(

    "/{product_id}",

    response_model=list[ProductResponse]

)

def recommend(

    product_id: int,

    db: Session = Depends(get_db)

):

    print(f"Recommendation request received for product_id={product_id}")

    recs = RecommendationService.get_recommendations(
        db,
        product_id
    )

    try:
        print(f"Returning {len(recs)} recommendations for product_id={product_id}")
    except Exception:
        print("Returning recommendations (unable to determine length)")

    return recs


class CartIn(BaseModel):
    item_ids: list[int] | None = None
    item_names: list[str] | None = None
    top_n: int = 5


@router.post("/cart")
def recommend_for_cart(cart: CartIn, db: Session = Depends(get_db)):
    # Map item_ids to names if provided
    names = []
    if cart.item_ids:
        prods = db.query(Product).filter(Product.id.in_(cart.item_ids)).all()
        names = [p.name for p in prods]
    elif cart.item_names:
        names = cart.item_names
    else:
        raise HTTPException(status_code=400, detail="Provide item_ids or item_names")

    recs = recommend_next(names, top_n=cart.top_n)
    # recs is list of tuples (item_name, confidence, lift, support)
    results = []
    for item, conf, lift, sup in recs:
        # attempt to find product by name
        prod = db.query(Product).filter(Product.name == item).first()
        if prod:
            prod_data = {"id": prod.id, "name": prod.name, "price": prod.price, "image": prod.image}
        else:
            prod_data = None
        results.append({
            "item_name": item,
            "product": prod_data,
            "confidence": conf,
            "lift": lift,
            "support": sup,
        })

    return results