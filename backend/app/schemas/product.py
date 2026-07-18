from pydantic import BaseModel


class ProductCreate(BaseModel):

    name: str
    description: str

    price: float
    original_price: float

    image: str

    stock: int

    category_id: int
    brand_id: int

    ram: str
    storage: str
    processor: str
    battery: str
    display: str
    camera: str


class ProductResponse(ProductCreate):

    id: int

    rating: float
    review_count: int

    class Config:
        from_attributes = True