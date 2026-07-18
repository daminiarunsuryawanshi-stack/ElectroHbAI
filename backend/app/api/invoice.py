from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.payment import Payment

router = APIRouter(
    prefix="/invoice",
    tags=["Invoice"]
)


@router.get("/{order_id}")
def get_invoice(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    payment = db.query(Payment).filter(
        Payment.order_id == order.id
    ).first()

    order_items = db.query(OrderItem).filter(
        OrderItem.order_id == order.id
    ).all()

    items = []

    for item in order_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        items.append({
            "product": product.name,
            "price": item.price,
            "quantity": item.quantity,
            "subtotal": item.price * item.quantity
        })

    return {
        "invoice_number": order.id,
        "customer": current_user.username,
        "email": current_user.email,
        "shipping_address": order.shipping_address,
        "order_status": order.status,
        "payment_status": payment.payment_status if payment else "Pending",
        "transaction_id": payment.transaction_id if payment else None,
        "items": items,
        "total_amount": order.total_amount
    }