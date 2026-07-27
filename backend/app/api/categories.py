from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category
from pydantic import BaseModel

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

class CategoryCreate(BaseModel):
    name: str


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category