from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "ai_ceo")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

projects = db.projects
outputs = db.outputs
logs = db.logs
