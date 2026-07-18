from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse

router = APIRouter(
    prefix="/filter",
    tags=["Filters"]
)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def filter_products(

    min_price: float = 0,

    max_price: float = 999999,

    brand_id: int | None = None,

    category_id: int | None = None,

    rating: float = 0,

    availability: str | None = None,

    sort_by: str = "price",

    order: str = "asc",

    skip: int = 0,

    limit: int = 20,

    db: Session = Depends(get_db)

):

    query = db.query(Product)

    query = query.filter(

        Product.price >= min_price,

        Product.price <= max_price,

        Product.rating >= rating

    )

    if brand_id:

        query = query.filter(

            Product.brand_id == brand_id

        )

    if category_id:

        query = query.filter(

            Product.category_id == category_id

        )

    if availability:

        query = query.filter(

            Product.availability.ilike(

                f"%{availability}%"

            )

        )

    if hasattr(Product, sort_by):

        column = getattr(Product, sort_by)

        if order == "desc":

            query = query.order_by(

                column.desc()

            )

        else:

            query = query.order_by(

                column.asc()

            )

    return (

        query

        .offset(skip)

        .limit(limit)

        .all()

    )