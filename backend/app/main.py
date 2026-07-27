from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine

# Models
from app.models.user import User
from app.models.brand import Brand
from app.models.category import Category
from app.models.product import Product
from app.models.wishlist import Wishlist
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.review import Review
from app.models.coupon import Coupon

# Routers
from app.api.auth import router as auth_router
from app.api.products import router as product_router
from app.api.recommendation import router as recommendation_router
from app.api.search import router as search_router
from app.api.autocomplete import router as autocomplete_router
from app.api.filter import router as filter_router
from app.api.cart import router as cart_router
from app.api.wishlist import router as wishlist_router
from app.api.orders import router as order_router
from app.api.payments import router as payment_router
from app.api.reviews import router as review_router
from app.api.invoice import router as invoice_router
from app.api.coupons import router as coupon_router
from app.api.admin import router as admin_router
from app.api.upload import router as upload_router
from app.api.dashboard import router as dashboard_router
from app.api.assistant import router as assistant_router
from app.api import categories


# Create FastAPI App
app = FastAPI(
    title="ElectroHub AI",
    version="1.0.0",
    description="AI Powered Electronics Shopping Platform"
)

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Static Files
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# Home Route
@app.get("/")
def home():
    return {
        "message": "ElectroHub AI Backend Running"
    }

# Register Routers
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(recommendation_router)
app.include_router(search_router)
app.include_router(autocomplete_router)
app.include_router(filter_router)
app.include_router(cart_router)
app.include_router(wishlist_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(review_router)
app.include_router(invoice_router)
app.include_router(coupon_router)
app.include_router(admin_router)
app.include_router(upload_router)
app.include_router(dashboard_router)
app.include_router(assistant_router)
app.include_router(categories.router)