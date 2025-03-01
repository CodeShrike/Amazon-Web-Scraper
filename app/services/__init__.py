from .manager import ProductManager
from app.db import Database


db = Database()
# Instantiate ProductManager
product_manager = ProductManager(db)
