from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.cart import Cart
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.coupon import Coupon

from app.schemas.order import (
    OrderCreate,
    OrderResponse
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/")
def place_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total = 0

    # Check products and calculate total
    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"{product.name} is out of stock"
            )

        total += product.price * item.quantity

    # Apply Coupon
    discount = 0

    if order.coupon_code:

        coupon = db.query(Coupon).filter(
            Coupon.code == order.coupon_code.upper(),
            Coupon.active == True
        ).first()

        if not coupon:
            raise HTTPException(
                status_code=404,
                detail="Invalid Coupon"
            )

        discount = total * (coupon.discount / 100)
        total -= discount

    # Create Order
    new_order = Order(
        user_id=current_user.id,
        total_amount=total,
        shipping_address=order.shipping_address,
        status="Pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Save Order Items and Reduce Stock
    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

        # Reduce stock
        product.stock -= item.quantity

    db.commit()

    # Clear Cart
    for item in cart_items:
        db.delete(item)

    db.commit()

    return {
        "message": "Order Placed Successfully",
        "order_id": new_order.id,
        "original_total": total + discount,
        "discount": discount,
        "final_total": total
    }


@router.get(
    "/",
    response_model=list[OrderResponse]
)
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()


@router.delete("/{order_id}")
def cancel_order(
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

    db.delete(order)
    db.commit()

    return {
        "message": "Order Cancelled Successfully"
    }