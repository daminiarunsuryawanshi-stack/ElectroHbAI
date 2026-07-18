from pydantic import BaseModel


from typing import Optional
from pydantic import BaseModel


class OrderCreate(BaseModel):

    shipping_address: str

    coupon_code: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    shipping_address: str

    class Config:
        from_attributes = True