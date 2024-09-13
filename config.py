import os

# Database
DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "ace")

MUST_JOIN = ["Anime_Edge", "Anime_Edge_Ongoing"]

# Admins
try:
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "1374857816 1350488685").split()]
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

API_ID = '19099900'
API_HASH = '2b445de78e5baf012a0793e60bd4fbf5'

TOKEN = ''
