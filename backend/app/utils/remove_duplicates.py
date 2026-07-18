from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.product import Product
from app.models.wishlist import Wishlist
from app.models.review import Review


def remove_duplicates():

    db: Session = SessionLocal()

    try:

        products = db.query(Product).all()

        seen = {}

        duplicate_ids = []


        for product in products:

            key = (
                product.name,
                product.image
            )

            if key not in seen:

                seen[key] = product.id

            else:

                duplicate_ids.append(
                    (
                        product.id,
                        seen[key]
                    )
                )


        print(
            "Duplicates found:",
            len(duplicate_ids)
        )


        deleted = 0


        for duplicate_id, keep_id in duplicate_ids:


            # Update wishlist references

            db.query(Wishlist).filter(
                Wishlist.product_id == duplicate_id
            ).update(
                {
                    "product_id": keep_id
                }
            )


            # Update review references

            db.query(Review).filter(
                Review.product_id == duplicate_id
            ).update(
                {
                    "product_id": keep_id
                }
            )


            # Delete duplicate product

            db.query(Product).filter(
                Product.id == duplicate_id
            ).delete()


            deleted += 1


        db.commit()


        print("----------------------------")
        print(
            "Deleted:",
            deleted
        )

        print(
            "Remaining Products:",
            db.query(Product).count()
        )

        print("----------------------------")


    except Exception as e:

        db.rollback()

        print(
            "ERROR:",
            e
        )


    finally:

        db.close()



if __name__ == "__main__":

    remove_duplicates()