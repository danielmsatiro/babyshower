from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer

category_product = db.Table(
    "product_category",
    Column("id", Integer, primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)
