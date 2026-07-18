from pydantic import BaseModel


class ReviewCreate(BaseModel):

    product_id: int

    rating: float

    comment: str


class ReviewResponse(BaseModel):

    id: int

    user_id: int

    product_id: int

    rating: float

    comment: str

    class Config:

        from_attributes = True