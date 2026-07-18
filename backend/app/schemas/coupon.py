from pydantic import BaseModel


class CouponCreate(BaseModel):

    code: str

    discount: float


class CouponResponse(BaseModel):

    id: int

    code: str

    discount: float

    active: bool

    class Config:

        from_attributes = True