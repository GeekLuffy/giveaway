from pymongo import MongoClient
from config import DB_URI, DB_NAME

client = MongoClient(DB_URI)
db = client[DB_NAME]

USER_COLLECTION_NAME = "genvnano"
SELECTED_USERS_COLLECTION_NAME = "susers"
JOIN_COUNTS_COLLECTION_NAME = "jusers"

user_collection = db[USER_COLLECTION_NAME]
selected_users_collection = db[SELECTED_USERS_COLLECTION_NAME]
join_counts_collection = db[JOIN_COUNTS_COLLECTION_NAME]

async def ok(user_id, username, first_name, last_name):
    user_data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    user_collection.insert_one(user_data)
