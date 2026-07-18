from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.cart import Cart
from app.models.product import Product
from app.models.user import User

from app.schemas.cart import CartCreate, CartResponse

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.post("/add")
def add_to_cart(
    cart: CartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    product = db.query(Product).filter(
        Product.id == cart.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_cart = Cart(
        user_id=current_user.id,
        product_id=cart.product_id,
        quantity=cart.quantity
    )

    db.add(new_cart)
    db.commit()

    return {
        "message": "Product Added To Cart"
    }

@router.put("/{cart_id}")
def update_cart(
    cart_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart Item Not Found"
        )

    cart.quantity = quantity

    db.commit()

    return {
        "message": "Cart Updated"
    }

@router.delete("/{cart_id}")
def delete_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart Item Not Found"
        )

    db.delete(cart)

    db.commit()

    return {
        "message": "Item Removed"
    }
@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart_items = (
        db.query(Cart, Product)
        .join(
            Product,
            Cart.product_id == Product.id
        )
        .filter(
            Cart.user_id == current_user.id
        )
        .all()
    )


    result = []

    for cart, product in cart_items:

        result.append({

            "id": cart.id,

            "product_id": product.id,

            "name": product.name,

            "image": product.image,

            "price": product.price,

            "quantity": cart.quantity

        })


    return result
