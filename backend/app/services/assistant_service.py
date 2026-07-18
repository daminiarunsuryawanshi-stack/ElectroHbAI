import re

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models.product import Product
from app.models.brand import Brand
from app.models.category import Category


class AssistantService:

    @staticmethod
    def search_products(db: Session, message: str):

        message = message.lower()

        synonyms = {
            "tv": [
                "tv",
                "television",
                "smart tv",
                "oled",
                "led",
                "qled"
            ],

            "mobile": [
                "mobile",
                "phone",
                "smartphone",
                "iphone",
                "galaxy",
                "cell phone"
            ],

            "laptop": [
                "laptop",
                "notebook",
                "workstation"
            ],

            "headphones": [
                "headphones",
                "earphones",
                "earbuds",
                "headset"
            ],

            "camera": [
                "camera",
                "dslr",
                "mirrorless",
                "camcorder"
            ],

            "watch": [
                "watch",
                "smartwatch"
            ],

            "speaker": [
                "speaker",
                "bluetooth speaker"
            ],

            "charger": [
                "charger",
                "adapter",
                "power adapter"
            ]
        }

        expanded_words = []

        words = message.split()

        for word in words:

            if word in synonyms:

                expanded_words.extend(synonyms[word])

            else:

                expanded_words.append(word)

        query = (
            db.query(Product)
            .outerjoin(Category, Product.category_id == Category.id)
            .outerjoin(Brand, Product.brand_id == Brand.id)
        )

        conditions = []

        for word in expanded_words:

            conditions.append(Product.name.ilike(f"%{word}%"))
            conditions.append(Product.description.ilike(f"%{word}%"))
            conditions.append(Category.name.ilike(f"%{word}%"))
            conditions.append(Brand.name.ilike(f"%{word}%"))

        query = query.filter(or_(*conditions))

            # -----------------------------
        # PRICE FILTER
        # -----------------------------



        price = re.search(r"\d+", message)

        if price:

            value = float(price.group())

            if "under" in message or "below" in message or "less" in message:

                query = query.filter(Product.price <= value)

            elif "above" in message or "more" in message or "greater" in message:

                query = query.filter(Product.price >= value)

        # -----------------------------
        # SMART SORTING
        # -----------------------------

        if "cheap" in message or "cheapest" in message or "budget" in message:

            query = query.order_by(Product.price.asc())

        elif "expensive" in message or "premium" in message:

            query = query.order_by(Product.price.desc())

        elif "latest" in message or "new" in message:

            query = query.order_by(Product.id.desc())

        else:

            query = query.order_by(Product.rating.desc())

        return query.all()