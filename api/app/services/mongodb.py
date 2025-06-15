from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.async_client = None
        self.async_db = None

    def connect(self):
        """Connect to MongoDB"""
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client[os.getenv("MONGODB_DATABASE")]
        return self.db

    async def async_connect(self):
        """Connect to MongoDB asynchronously"""
        self.async_client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
        self.async_db = self.async_client[os.getenv("MONGODB_DATABASE")]
        return self.async_db

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
        if self.async_client:
            self.async_client.close()

# Create a global instance
mongodb = MongoDB()
