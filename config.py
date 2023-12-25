import os

# Database
DB_URI = os.environ.get("DB_URI", "mongodb+srv://sonu55:sonu55@cluster0.vqztrvk.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "lumffy")

MUST_JOIN = ["username 1", "username 2", "username 3"]

# Admins
try:
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "6299128233").split()]
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

API_ID = '19099900'
API_HASH = '2b445de78e5baf012a0793e60bd4fbf5'

TOKEN = '6747088315:AAHTWg_fg7h6GXgpdE-0c2EORljrVT71SOA'
