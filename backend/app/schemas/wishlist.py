from typing import Optional

from pydantic import BaseModel


class WishlistCreate(BaseModel):
    product_id: int


class WishlistResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    name: str
    image: Optional[str] = None
    price: float
    rating: Optional[float] = None

    class Config:
        from_attributes = True