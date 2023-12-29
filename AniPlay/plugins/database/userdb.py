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

# Add this at the beginning of your code to define a cache
referral_cache = {}

# Function to initialize a user in the join_counts_collection with 0 points
def initialize_user(user_id):
    join_counts_collection.update_one({"user_id": user_id}, {"$set": {"count": 0}}, upsert=True)

# Function to update a user's points
def update_user_points(user_id, points):
    join_counts_collection.update_one({"user_id": user_id}, {"$inc": {"count": points}}, upsert=True)

# Function to get a user's points
def get_user_points(user_id):
    user_data = join_counts_collection.find_one({"user_id": user_id})
    print(f"User ID: {user_id}, User Data: {user_data}")
    return user_data.get("count", 0) if user_data else 0


async def ok(user_id, username, first_name, last_name, referrer_id=None):
    user_data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }

    # Additional check for referral logic
    if referrer_id:
        user_data["referrer_id"] = referrer_id

        # Assuming you have a separate collection to store join counts
        join_counts_collection.update_one({"user_id": referrer_id}, {"$inc": {"count": 1}}, upsert=True)

    user_collection.update_one({"user_id": user_id}, {"$set": user_data}, upsert=True)
