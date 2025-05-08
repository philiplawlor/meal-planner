from pymongo import MongoClient
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('DATABASE_NAME', 'recipes')]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def insert_one(self, collection_name: str, document: dict):
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def find(self, collection_name: str, query: dict, projection: Optional[dict] = None):
        collection = self.get_collection(collection_name)
        return collection.find(query, projection)

    def find_one(self, collection_name: str, query: dict, projection: Optional[dict] = None):
        collection = self.get_collection(collection_name)
        return collection.find_one(query, projection)

    def update_one(self, collection_name: str, query: dict, update: dict):
        collection = self.get_collection(collection_name)
        return collection.update_one(query, update)

    def delete_one(self, collection_name: str, query: dict):
        collection = self.get_collection(collection_name)
        return collection.delete_one(query)

    def close(self):
        self.client.close()

# Create a singleton instance of the client
mongodb_client = MongoDBClient()
