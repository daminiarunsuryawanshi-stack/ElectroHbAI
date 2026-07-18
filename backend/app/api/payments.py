import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.order import Order
from app.models.payment import Payment

from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/")
def make_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = db.query(Order).filter(
        Order.id == payment.order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    existing = db.query(Payment).filter(
        Payment.order_id == order.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Payment already completed"
        )

    new_payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        payment_method=payment.payment_method,
        payment_status="Paid",
        transaction_id=str(uuid.uuid4())
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    order.status = "Confirmed"
    db.commit()

    return {
        "message": "Payment Successful",
        "transaction_id": new_payment.transaction_id
    }


@router.get(
    "/",
    response_model=list[PaymentResponse]
)
def payment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return (
        db.query(Payment)
        .join(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def payment_details(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    payment = (
        db.query(Payment)
        .join(Order)
        .filter(
            Payment.id == payment_id,
            Order.user_id == current_user.id
        )
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment