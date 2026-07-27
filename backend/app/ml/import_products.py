import pandas as pd

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product

db: Session = SessionLocal()

csv_file = "app/ml/dataset/DatafinitiElectronicsProductsPricingData.csv"

df = pd.read_csv(csv_file)

print("Rows Found:", len(df))

count = 0

for _, row in df.iterrows():

    try:

        image = ""

        if pd.notna(row.get("imageURLs")):
            image = str(row["imageURLs"]).split(",")[0]

        product = Product(
            name=str(row.get("name", ""))[:255],
            description=str(row.get("manufacturer", "")),
            price=float(row.get("prices.amountMax", 0)),
            original_price=float(row.get("prices.amountMax", 0)),
            image=image,
            stock=50,
            category_id=1,
            brand_id=1,
            ram="",
            storage="",
            processor="",
            battery="",
            display="",
            camera="",
            rating=4.5,
            review_count=100,
        )

        db.add(product)

        count += 1

        if count % 100 == 0:
            db.commit()
            print(f"Imported {count}")

    except Exception as e:
        print(e)

db.commit()
db.close()

print("Finished")
print("Total Imported:", count)