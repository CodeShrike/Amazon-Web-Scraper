from pymongo import MongoClient

class Database:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="scraped_db"):
        self.uri = uri
        self.db_name = db_name
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        
    def connect(self):
        try:
            client = MongoClient(self.uri)
            return client[self.db_name]
        except Exception as e:
            raise Exception("The following error occurred: ", e)
    
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
    def close_connection(self):
        self.client.close()

