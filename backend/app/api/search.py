from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def search_products(
    q: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):

    return (
        db.query(Product)
        .filter(
            or_(
                Product.name.ilike(f"%{q}%"),
                Product.manufacturer.ilike(f"%{q}%")
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )