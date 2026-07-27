from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.models.user import User
from app.models.product import Product
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
import shutil
import os
from typing import Optional

from app.schemas.product import (
    ProductCreate,
    ProductResponse
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/")
def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    stock: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    os.makedirs("uploads", exist_ok=True)

    filename = file.filename

    filepath = os.path.join(
        "uploads",
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        stock=stock,
        image=f"/uploads/{filename}"
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product Created Successfully",
        "product": new_product
    }



@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products(
    category_id: int = None,
    search: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):

    query = db.query(Product)


    # Category Filter
    if category_id:

        query = query.filter(
            Product.category_id == category_id
        )


    # Search Filter
    if search:

        query = query.filter(
            Product.name.ilike(
                f"%{search}%"
            )
        )


    products = query.all()

    seen = set()
    final_products = []

    for product in products:

        key = (
            product.name,
            product.image
        )

        if key not in seen:
            seen.add(key)
            final_products.append(product)

    return final_products[:limit]


@router.put(
    "/{product_id}"
)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    db_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.original_price = product.original_price
    db_product.image = product.image
    db_product.stock = product.stock
    db_product.category_id = product.category_id
    db_product.brand_id = product.brand_id
    db_product.ram = product.ram
    db_product.storage = product.storage
    db_product.processor = product.processor
    db_product.battery = product.battery
    db_product.display = product.display
    db_product.camera = product.camera

    return {
        "message": "Product Updated Successfully"
    }

@router.delete(
    "/{product_id}"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product Deleted Successfully"
    }

