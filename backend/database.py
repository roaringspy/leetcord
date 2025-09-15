# database.py
import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.social_leetcode

# Collections
problems_collection = database.get_collection("problems")
submissions_collection = database.get_collection("submissions")
users_collection = database.get_collection("users")