from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection
from dotenv import load_dotenv
import os

load_dotenv()

client: AsyncMongoClient = AsyncMongoClient(os.getenv("MONGODB-CONNECTION-URI"))
database: AsyncDatabase = client.user
collection: AsyncCollection = database["logs"]