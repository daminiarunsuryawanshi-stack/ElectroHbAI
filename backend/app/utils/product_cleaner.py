from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product


def find_duplicates():

    db: Session = SessionLocal()

    try:

        products = db.query(Product).all()

        seen = set()
        duplicates = []

        for product in products:

            key = (
                product.name,
                product.image
            )

            if key in seen:
                duplicates.append(product)

            else:
                seen.add(key)


        print("--------------------------------")
        print("Total Products:", len(products))
        print("Duplicate Products:", len(duplicates))
        print("--------------------------------")


        print("\nFirst 20 duplicates:\n")

        for item in duplicates[:20]:

            print(
                item.id,
                "|",
                item.name
            )


    finally:

        db.close()


if __name__ == "__main__":

    find_duplicates()