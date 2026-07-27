# backend/app/ml/check_db.py
from app.core.database import SessionLocal
from app.models.order_item import OrderItem
from app.models.product import Product
# import dependent models so SQLAlchemy relationship names are resolved
from app.models.order import Order

db = SessionLocal()
try:
    count = db.query(OrderItem).count()
    print("OrderItem count:", count)
    samples = db.query(OrderItem).limit(10).all()
    for oi in samples:
        prod = oi.product
        print("order_id:", oi.order_id, "product_id:", oi.product_id, "product_name:", getattr(prod, "name", None))
finally:
    db.close()