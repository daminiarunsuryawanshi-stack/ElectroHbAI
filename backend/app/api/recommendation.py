from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.product import ProductResponse

from app.services.recommendation_service import RecommendationService


router = APIRouter(

    prefix="/recommendation",

    tags=["Recommendation"]

)


@router.get(

    "/{product_id}",

    response_model=list[ProductResponse]

)

def recommend(

    product_id: int,

    db: Session = Depends(get_db)

):

    return RecommendationService.get_recommendations(

        db,

        product_id

    )