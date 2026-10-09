import hashlib
import datetime
from typing import Optional
import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.core.config import MONGODB_URI, MONGODB_DB_NAME
from app.db.seed_hospitals import DEFAULT_INDIAN_HOSPITALS

_mongo_client: Optional[MongoClient] = None

def hash_password(password: str) -> str:
    """
    Generates a SHA-256 hash with a fixed salt for user authentication.
    """
    salt = "heartcare_secure_salt_v1"
    salted = f"{password}{salt}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()

def get_mongo_client() -> MongoClient:
    """
    Returns a singleton MongoClient instance to reuse connections across requests.
    """
    global _mongo_client
    if _mongo_client is None:
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable is missing. Please check your .env file.")
        _mongo_client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=8000,
            connectTimeoutMS=8000,
            socketTimeoutMS=10000,
            maxPoolSize=50,
            minPoolSize=5
        )
    return _mongo_client

def get_db() -> Database:
    """Returns the MongoDB database instance."""
    client = get_mongo_client()
    return client[MONGODB_DB_NAME]

def get_db_connection() -> Database:
    """Legacy alias for existing route handlers."""
    return get_db()

def init_db() -> bool:
    """
    Initializes the MongoDB connection, creates collection indexes,
    and seeds default clinical accounts and hospitals if collections are empty.
    """
    try:
        db = get_db()
        # Verify connection
        db.command("ping")
        print("[MongoDB] Connected successfully.")

        # 1. Users collection
        db.users.create_index("email", unique=True)
        db.users.create_index("id", unique=True)

        if db.users.count_documents({}) == 0:
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            seed_users = [
                {
                    "id": "USER-001",
                    "email": "dr.sharma@heartcare.ai",
                    "password_hash": hash_password("admin123"),
                    "name": "Dr. Rajesh Sharma, MD, DM (Cardiology)",
                    "role": "Cardiologist / Physician",
                    "created_at": now_str,
                    "last_login": now_str
                },
                {
                    "id": "USER-002",
                    "email": "patient@heartcare.ai",
                    "password_hash": hash_password("patient123"),
                    "name": "Aarav Patel",
                    "role": "Patient / Individual User",
                    "created_at": now_str,
                    "last_login": now_str
                }
            ]
            db.users.insert_many(seed_users)
            print("[MongoDB] Seeded default user accounts.")

        # 2. Assessments collection
        db.assessments.create_index("id", unique=True)
        db.assessments.create_index("user_email")
        db.assessments.create_index([("timestamp", pymongo.DESCENDING)])
        db.assessments.create_index([("user_email", pymongo.ASCENDING), ("timestamp", pymongo.DESCENDING)])

        # 3. Hospitals collection
        db.hospitals.create_index("id", unique=True)
        db.hospitals.create_index("city")
        db.hospitals.create_index("name")

        for h in DEFAULT_INDIAN_HOSPITALS:
            db.hospitals.update_one({"id": h["id"]}, {"$set": h}, upsert=True)
        print(f"[MongoDB] Synchronized {len(DEFAULT_INDIAN_HOSPITALS)} Indian cardiology centers.")

        # 4. Appointments collection
        db.appointments.create_index("booking_id", unique=True)
        db.appointments.create_index("hospital_id")

        return True

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"[MongoDB Error] Connection failed: {e}")
        return False
    except Exception as e:
        print(f"[MongoDB Error] Initialization failed: {e}")
        return False
