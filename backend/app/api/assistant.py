from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.assistant_service import AssistantService

router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    products = AssistantService.search_products(
        db,
        request.message
    )

    if not products:

        return {
            "reply": "No matching products found.",
            "products": []
        }

    result = []

    for product in products:

        result.append({

            "id": product.id,

            "name": product.name,

            "price": product.price,

            "image": product.image,

            "rating": product.rating

        })

    return {

        "reply": f"Found {len(result)} matching products.",

        "products": result

    }