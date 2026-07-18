from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.dependencies import get_admin_user

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.category import Category
from app.models.brand import Brand

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    total_users = db.query(func.count(User.id)).scalar()

    total_products = db.query(func.count(Product.id)).scalar()

    total_orders = db.query(func.count(Order.id)).scalar()

    total_categories = db.query(func.count(Category.id)).scalar()

    total_brands = db.query(func.count(Brand.id)).scalar()

    revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    if revenue is None:
        revenue = 0

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_categories": total_categories,
        "total_brands": total_brands,
        "total_revenue": revenue
    }