from pymongo import MongoClient
from pymongo.collection import Collection

from src.config import MONGO_URI

_client = MongoClient(MONGO_URI)
_db = _client["internscout"]

jobs_collection: Collection = _db["jobs"]
jobs_collection.create_index("job_hash", unique=True)
