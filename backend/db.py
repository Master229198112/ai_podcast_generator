import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["2way_podcast_db"]
podcast_collection = db["podcasts"]

# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["2way_podcast_db"]
# podcast_collection = db["podcasts"]

def save_podcast(title, summary, audio_path):
    podcast = {"title": title, "summary": summary, "audio": audio_path}
    result = podcast_collection.insert_one(podcast)
    return str(result.inserted_id)
