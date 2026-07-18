from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository


class ProductService:

    @staticmethod
    def get_products(
        db: Session,
        skip: int,
        limit: int,
        sort_by: str,
        order: str
    ):
        return ProductRepository.get_all(
            db,
            skip,
            limit,
            sort_by,
            order
        )

    @staticmethod
    def get_product(
        db: Session,
        product_id: int
    ):
        return ProductRepository.get_by_id(
            db,
            product_id
        )

    @staticmethod
    def search_products(
        db: Session,
        keyword: str,
        skip: int,
        limit: int
    ):
        return ProductRepository.search(
            db,
            keyword,
            skip,
            limit
        )

    @staticmethod
    def products_by_brand(
        db: Session,
        brand_id: int,
        skip: int,
        limit: int
    ):
        return ProductRepository.by_brand(
            db,
            brand_id,
            skip,
            limit
        )

    @staticmethod
    def products_by_category(
        db: Session,
        category_id: int,
        skip: int,
        limit: int
    ):
        return ProductRepository.by_category(
            db,
            category_id,
            skip,
            limit
        )