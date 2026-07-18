from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.dependencies import get_admin_user

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from sqlalchemy import extract
from app.models.order_item import OrderItem

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    total_products = db.query(Product).count()

    total_users = db.query(User).count()

    total_orders = db.query(Order).count()

    total_revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    if total_revenue is None:
        total_revenue = 0

    return {
        "total_products": total_products,
        "total_users": total_users,
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }

@router.get("/monthly-sales")
def monthly_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    sales = (
        db.query(
            extract("month", Order.created_at).label("month"),
            func.sum(Order.total_amount).label("sales")
        )
        .group_by(extract("month", Order.created_at))
        .order_by(extract("month", Order.created_at))
        .all()
    )

    return sales

@router.get("/top-products")
def top_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    products = (
        db.query(
            Product.name,
            func.sum(OrderItem.quantity).label("sold")
        )
        .join(OrderItem, Product.id == OrderItem.product_id)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(10)
        .all()
    )

    return products

@router.get("/low-stock")
def low_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    products = db.query(Product).filter(
        Product.stock <= 5
    ).all()

    return products

@router.get("/recent-orders")
def recent_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    orders = (
        db.query(Order)
        .order_by(Order.id.desc())
        .limit(10)
        .all()
    )

    return orders

