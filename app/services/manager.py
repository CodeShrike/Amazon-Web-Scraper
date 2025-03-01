from app.db import Database

class ProductManager:
    # Initialise a list to store data
    def __init__(self, db:Database):
        self.db = db
        self.collection = db.get_collection("products")
    #    self.products = []

    # Add products to self list with appropriate attributes 
    def add_product(self, timestamp, title, price, image, rating, rating_count, link):
        product = {
            "timestamp" : timestamp,
            "title": title,
            "price": price,
            "image": image,
            "rating": rating, ######### Look into extracting this as a float and just adding "out of 5 stars" during processing
            "rating_count": rating_count,
            "link": link,
        }
        self.collection.insert_one(product)
 #       print(product)
        print(self.collection)
      #  self.products.append(product)

    # Retrieve all products currently stored
    def get_all_products(self):
        #return self.products
        return list(self.collection.find({}))
    
    # Function to sort the products by attribute in either ascending or descending order
    def sort_products(self, attribute, order="asc"):
        sort_order = 1 if order == "asc" else -1
        cursor = self.collection.find({}, {"_id":0}).sort([(attribute, sort_order)])
        return list(cursor)
    
    """        # Ensure we aren't going through no products, then flag reverse depending on whether the order is set to desc
        if not self.products:
            return []
        reverse = True if order == "desc" else False

        # Leverage sorted function to sort products by attribute
        return sorted(
        self.products,
        key=lambda x: (
            # Adjust attributes accordingly (Use the float before the first space for rating, remove characters from price, use rating_count as an integer)
            float(x.get(attribute, "0").split()[0]) if attribute == "rating" else
            float(x.get(attribute, "0").replace("£", "").replace(",", "").strip()) if attribute == "price" else
            int(x.get(attribute, 0)) if attribute == "rating_count" else
            x.get(attribute, 0),
        ),
        reverse=reverse, 
    )"""


    def clear_products(self):
        self.products = []
        self.db.get_collection("products").delete_many({})
