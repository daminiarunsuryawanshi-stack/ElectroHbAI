from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_admin_user
)

from app.models.user import User
from app.models.coupon import Coupon

from app.schemas.coupon import (
    CouponCreate,
    CouponResponse
)

router = APIRouter(
    prefix="/coupons",
    tags=["Coupons"]
)


@router.post("/")
def create_coupon(
    coupon: CouponCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    existing = db.query(Coupon).filter(
        Coupon.code == coupon.code
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Coupon already exists"
        )

    new_coupon = Coupon(
        code=coupon.code.upper(),
        discount=coupon.discount,
        active=True
    )

    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)

    return {
        "message": "Coupon Created Successfully"
    }


@router.get(
    "/",
    response_model=list[CouponResponse]
)
def get_coupons(
    db: Session = Depends(get_db)
):

    return db.query(Coupon).all()


@router.post("/apply/{code}")
def apply_coupon(
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    coupon = db.query(Coupon).filter(
        Coupon.code == code.upper(),
        Coupon.active == True
    ).first()

    if not coupon:
        raise HTTPException(
            status_code=404,
            detail="Invalid Coupon"
        )

    return {
        "coupon": coupon.code,
        "discount": coupon.discount
    }


@router.put("/disable/{coupon_id}")
def disable_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    coupon = db.query(Coupon).filter(
        Coupon.id == coupon_id
    ).first()

    if not coupon:
        raise HTTPException(
            status_code=404,
            detail="Coupon not found"
        )

    coupon.active = False

    db.commit()

    return {
        "message": "Coupon Disabled Successfully"
    }


@router.delete("/{coupon_id}")
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    coupon = db.query(Coupon).filter(
        Coupon.id == coupon_id
    ).first()

    if not coupon:
        raise HTTPException(
            status_code=404,
            detail="Coupon not found"
        )

    db.delete(coupon)
    db.commit()

    return {
        "message": "Coupon Deleted Successfully"
    }