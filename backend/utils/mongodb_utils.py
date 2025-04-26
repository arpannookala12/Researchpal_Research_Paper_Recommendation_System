# backend/utils/mongodb_utils.py
import pymongo
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class MongoDBClient:
    """Utility class for MongoDB operations."""
    
    def __init__(self, uri=None, db_name=None):
        """Initialize MongoDB connection parameters."""
        self.uri = uri or settings.MONGODB_URI
        self.db_name = db_name or self.uri.split('/')[-1]
        self.client = None
        self.db = None
    
    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = pymongo.MongoClient(self.uri)
            self.db = self.client[self.db_name]
            logger.info(f"Connected to MongoDB database: {self.db_name}")
            return self.db
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            raise
    
    def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            logger.info("Disconnected from MongoDB")
    
    def get_collection(self, collection_name):
        """Get a collection by name."""
        if not self.db:
            self.connect()
        return self.db[collection_name]
    
    def insert_one(self, collection_name, document):
        """Insert a single document into a collection."""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id
    
    def insert_many(self, collection_name, documents, ordered=True):
        """Insert multiple documents into a collection."""
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents, ordered=ordered)
        return result.inserted_ids
    
    def find(self, collection_name, query=None, projection=None, limit=0, sort=None):
        """Find documents in a collection."""
        collection = self.get_collection(collection_name)
        cursor = collection.find(query or {}, projection)
        
        if sort:
            cursor = cursor.sort(sort)
        
        if limit > 0:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    def update_one(self, collection_name, filter_dict, update_dict, upsert=False):
        """Update a single document in a collection."""
        collection = self.get_collection(collection_name)
        result = collection.update_one(filter_dict, update_dict, upsert=upsert)
        return result.modified_count
    
    def update_many(self, collection_name, filter_dict, update_dict, upsert=False):
        """Update multiple documents in a collection."""
        collection = self.get_collection(collection_name)
        result = collection.update_many(filter_dict, update_dict, upsert=upsert)
        return result.modified_count
    
    def delete_one(self, collection_name, filter_dict):
        """Delete a single document from a collection."""
        collection = self.get_collection(collection_name)
        result = collection.delete_one(filter_dict)
        return result.deleted_count
    
    def delete_many(self, collection_name, filter_dict):
        """Delete multiple documents from a collection."""
        collection = self.get_collection(collection_name)
        result = collection.delete_many(filter_dict)
        return result.deleted_count
    
    def count_documents(self, collection_name, filter_dict=None):
        """Count documents in a collection."""
        collection = self.get_collection(collection_name)
        return collection.count_documents(filter_dict or {})