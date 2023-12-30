import os

# Database
DB_URI = os.environ.get("DB_URI", "mongodb+srv://owais:glassone1@cluster0.cx7psr5.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "lumffy")

MUST_JOIN = ["logo_planet", "solo_leveling_dual", "chained_soldier_ao"]

# Admins
try:
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "1608353423 1350488685 5507193256").split()]
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

API_ID = '19099900'
API_HASH = '2b445de78e5baf012a0793e60bd4fbf5'

TOKEN = '6420934896:AAH7VZB0ZSoewO_hBwN4v2SE3xPG7A1b79Y'
