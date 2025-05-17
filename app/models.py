from pymongo import MongoClient
from pymongo.collection import Collection
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]

class MongoDBModel:
    """Base MongoDB model class"""
    
    @classmethod
    def get_collection(cls) -> Collection:
        """Get MongoDB collection instance"""
        return db[cls.collection_name]

class Pokemon(MongoDBModel):
    """Pokémon collection model"""
    collection_name = "pokemon"
    
    @classmethod
    def create_indexes(cls):
        """Create required indexes"""
        collection = cls.get_collection()
        collection.create_index("dexnum", unique=True)
        collection.create_index("name", unique=True)

class Move(MongoDBModel):
    """Move collection model"""
    collection_name = "moves"
    
    @classmethod
    def create_indexes(cls):
        """Create required indexes"""
        collection = cls.get_collection()
        collection.create_index("name", unique=True)
        collection.create_index("users")