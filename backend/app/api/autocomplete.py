from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product

router = APIRouter(
    prefix="/autocomplete",
    tags=["Autocomplete"]
)


@router.get("/")
def autocomplete(
    q: str,
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product.name)
        .filter(
            Product.name.ilike(f"{q}%")
        )
        .limit(10)
        .all()
    )

    return [p[0] for p in products]