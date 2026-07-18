from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.product import Product
from app.models.review import Review

from app.schemas.review import (
    ReviewCreate,
    ReviewResponse
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/")
def add_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    product = db.query(Product).filter(
        Product.id == review.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.product_id == review.product_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this product"
        )

    new_review = Review(
        user_id=current_user.id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return {
        "message": "Review Added Successfully"
    }


@router.get(
    "/{product_id}",
    response_model=list[ReviewResponse]
)
def get_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Review).filter(
        Review.product_id == product_id
    ).all()


@router.put("/{review_id}")
def update_review(
    review_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db_review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == current_user.id
    ).first()

    if not db_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    db_review.rating = review.rating
    db_review.comment = review.comment

    db.commit()

    return {
        "message": "Review Updated Successfully"
    }


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db_review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == current_user.id
    ).first()

    if not db_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    db.delete(db_review)
    db.commit()

    return {
        "message": "Review Deleted Successfully"
    }