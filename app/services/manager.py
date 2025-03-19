from app.db import Database

class ProductManager:
    # Initialise mongodb to store data as a collection
    def __init__(self, db:Database):
        self.db = db
        self.collection = db.get_collection("products")

    # Add products to self list with appropriate attributes 
    def add_product(self, timestamp, title, price, image, rating, rating_count, link):
        product = {
            "timestamp" : timestamp,
            "title": title,
            "price": price,
            "image": image,
            "rating": rating, 
            "rating_count": rating_count,
            "link": link,
        }
        # Prevent duplicates by using title as primary key and updating to newest listing
        product["_id"] = title
        self.collection.update_one({"_id": product["_id"]}, {"$set": product}, upsert= True)

    # Retrieve all products currently stored
    def get_all_products(self):
        #return mongo collection of products, removing the _id column
        return list(self.collection.find({}, {"_id":0}).sort({"timestamp": 1}))
    
    # Function to sort the products by attribute in either ascending or descending order
    def sort_products(self, attribute, order="asc"):
        sort_order = 1 if order == "asc" else -1
        cursor = self.collection.find({}, {"_id":0}).sort([(attribute, sort_order)])
        return list(cursor)
    
    def clear_products(self):
        self.db.get_collection("products").delete_many({})
