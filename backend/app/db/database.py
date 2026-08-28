import os
import json
import uuid
import datetime
import hashlib
from typing import Optional
import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.core.config import MONGODB_URI, MONGODB_DB_NAME

_mongo_client: Optional[MongoClient] = None

def hash_password(password: str) -> str:
    """Generates a secure SHA-256 hash for authentication."""
    salt = "heartcare_secure_salt_v1"
    return hashlib.sha256(f"{password}{salt}".encode('utf-8')).hexdigest()

def get_mongo_client() -> MongoClient:
    """
    Returns a thread-safe singleton MongoClient instance.
    Avoids creating unnecessary connections for every request.
    """
    global _mongo_client
    if _mongo_client is None:
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable is missing or empty. Please check your .env file.")
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

def get_db_connection():
    """
    Legacy compatibility alias for existing routes, returns MongoDB Database instance.
    """
    return get_db()

# Default Seed Indian Premier Cardiology Centers
DEFAULT_INDIAN_HOSPITALS = [
    {
        "id": "IN-HOSP-01",
        "name": "All India Institute of Medical Sciences (AIIMS)",
        "city": "New Delhi",
        "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi, Delhi 110029",
        "phone": "+91 11 2658 8500",
        "rating": 4.9,
        "review_count": 1420,
        "emergency_available": True,
        "specialties": "Interventional Cardiology, CTVS, 24/7 Cardiac Emergency, Heart Transplants",
        "distance_km": None,
        "latitude": 28.5672,
        "longitude": 77.2100
    },
    {
        "id": "IN-HOSP-02",
        "name": "Fortis Escorts Heart Institute",
        "city": "New Delhi",
        "address": "Okhla Road, Sukhdev Vihar, New Delhi, Delhi 110025",
        "phone": "+91 11 4713 5000",
        "rating": 4.9,
        "review_count": 980,
        "emergency_available": True,
        "specialties": "Pediatric & Adult Cardiology, 24/7 Rapid Chest Pain Clinic, Electrophysiology",
        "distance_km": None,
        "latitude": 28.5606,
        "longitude": 77.2796
    },
    {
        "id": "IN-HOSP-03",
        "name": "Medanta - The Medicity Heart Institute",
        "city": "Gurugram / NCR",
        "address": "CH Bakhtawar Singh Road, Sector 38, Gurugram, Haryana 122001",
        "phone": "+91 124 414 1414",
        "rating": 4.8,
        "review_count": 1150,
        "emergency_available": True,
        "specialties": "Robotic Cardiac Surgery, Heart Valve Repair, TAVR/TAVI, Cardiac Critical Care",
        "distance_km": None,
        "latitude": 28.4393,
        "longitude": 77.0426
    },
    {
        "id": "IN-HOSP-04",
        "name": "Max Super Speciality Hospital",
        "city": "New Delhi",
        "address": "1, 2, Press Enclave Road, Saket, New Delhi, Delhi 110017",
        "phone": "+91 11 2651 5050",
        "rating": 4.8,
        "review_count": 870,
        "emergency_available": True,
        "specialties": "Primary Angioplasty, Heart Failure Management, Cardiac ICU",
        "distance_km": None,
        "latitude": 28.5283,
        "longitude": 77.2125
    },
    {
        "id": "IN-HOSP-05",
        "name": "Asian Heart Institute (AHI)",
        "city": "Mumbai",
        "address": "G/N Block, Bandra Kurla Complex (BKC), Bandra East, Mumbai, Maharashtra 400051",
        "phone": "+91 22 6698 6666",
        "rating": 4.9,
        "review_count": 1280,
        "emergency_available": True,
        "specialties": "Coronary Artery Bypass Graft (CABG), 24/7 Cardiac Trauma, Preventive Cardiology",
        "distance_km": None,
        "latitude": 19.0664,
        "longitude": 72.8687
    },
    {
        "id": "IN-HOSP-06",
        "name": "Kokilaben Dhirubhai Ambani Hospital",
        "city": "Mumbai",
        "address": "Rao Saheb Achutrao Patwardhan Marg, Four Bungalows, Andheri West, Mumbai 400053",
        "phone": "+91 22 4269 6969",
        "rating": 4.8,
        "review_count": 920,
        "emergency_available": True,
        "specialties": "Full Time Specialist System, LVAD Implantation, Nuclear Cardiology",
        "distance_km": None,
        "latitude": 19.1311,
        "longitude": 72.8252
    },
    {
        "id": "IN-HOSP-07",
        "name": "Ruby Hall Clinic Heart Care Center",
        "city": "Pune",
        "address": "40, Sassoon Road, Sangamvadi, Pune, Maharashtra 411001",
        "phone": "+91 20 6645 5100",
        "rating": 4.7,
        "review_count": 740,
        "emergency_available": True,
        "specialties": "Structural Heart Interventions, Heart Failure Clinic, Holter Monitoring",
        "distance_km": None,
        "latitude": 18.5332,
        "longitude": 73.8777
    },
    {
        "id": "IN-HOSP-08",
        "name": "Narayana Institute of Cardiac Sciences",
        "city": "Bengaluru",
        "address": "258/A, Bommasandra Industrial Area, Anekal Taluk, Bengaluru, Karnataka 560099",
        "phone": "+91 80 7122 2222",
        "rating": 4.9,
        "review_count": 2100,
        "emergency_available": True,
        "specialties": "Complex Valve Repair, Heart Transplants, Largest Cardiac ICU in Asia",
        "distance_km": None,
        "latitude": 12.8094,
        "longitude": 77.6974
    },
    {
        "id": "IN-HOSP-09",
        "name": "Manipal Hospital Heart Institute",
        "city": "Bengaluru",
        "address": "98, HAL Old Airport Rd, Kodihalli, Bengaluru, Karnataka 560017",
        "phone": "+91 80 2502 4444",
        "rating": 4.8,
        "review_count": 890,
        "emergency_available": True,
        "specialties": "TAVI/TAVR, Emergency Cath Lab, 24/7 Rapid Cardiac Resuscitation",
        "distance_km": None,
        "latitude": 12.9592,
        "longitude": 77.6492
    },
    {
        "id": "IN-HOSP-10",
        "name": "Sri Jayadeva Institute of Cardiovascular Sciences",
        "city": "Bengaluru",
        "address": "Bannerghatta Main Rd, 9th Block, Jayanagar, Bengaluru, Karnataka 560069",
        "phone": "+91 80 2297 7400",
        "rating": 4.9,
        "review_count": 1850,
        "emergency_available": True,
        "specialties": "Autonomous Government Cardiac Super-Speciality Institute, 24/7 Emergency",
        "distance_km": None,
        "latitude": 12.9174,
        "longitude": 77.5997
    },
    {
        "id": "IN-HOSP-11",
        "name": "Apollo Hospitals (Main & Greams Road)",
        "city": "Chennai",
        "address": "21 Greams Lane, Thousand Lights, Chennai, Tamil Nadu 600006",
        "phone": "+91 44 2829 0200",
        "rating": 4.9,
        "review_count": 1620,
        "emergency_available": True,
        "specialties": "Pioneers in Interventional Cardiology, Minimally Invasive Cardiac Surgery, TAVR",
        "distance_km": None,
        "latitude": 13.0601,
        "longitude": 80.2526
    },
    {
        "id": "IN-HOSP-12",
        "name": "Madras Medical Mission (MMM Hospital)",
        "city": "Chennai",
        "address": "4-A, Dr. J. Jayalalitha Nagar, Mogappair, Chennai, Tamil Nadu 600037",
        "phone": "+91 44 2656 8000",
        "rating": 4.8,
        "review_count": 810,
        "emergency_available": True,
        "specialties": "Advanced Heart Failure, Pediatric Cardiology, Cardiac Electrophysiology",
        "distance_km": None,
        "latitude": 13.0858,
        "longitude": 80.1772
    },
    {
        "id": "IN-HOSP-13",
        "name": "Apollo Health City",
        "city": "Hyderabad",
        "address": "Road No 72, Opp. Bharatiya Vidya Bhavan School, Jubilee Hills, Hyderabad, Telangana 500033",
        "phone": "+91 40 2360 7777",
        "rating": 4.9,
        "review_count": 1340,
        "emergency_available": True,
        "specialties": "24/7 Chest Pain Triage, MitraClip Interventions, Cardiac Rehabilitation",
        "distance_km": None,
        "latitude": 17.4168,
        "longitude": 78.4116
    },
    {
        "id": "IN-HOSP-14",
        "name": "CARE Hospitals (Institute of Cardiac Sciences)",
        "city": "Hyderabad",
        "address": "Road No. 1, Banjara Hills, Hyderabad, Telangana 500034",
        "phone": "+91 40 6165 6565",
        "rating": 4.8,
        "review_count": 910,
        "emergency_available": True,
        "specialties": "Interventional Cardiology, Heart Failure & Transplant Unit",
        "distance_km": None,
        "latitude": 17.4156,
        "longitude": 78.4487
    },
    {
        "id": "IN-HOSP-15",
        "name": "BM Birla Heart Research Centre",
        "city": "Kolkata",
        "address": "1/1, National Library Ave, Alipore, Kolkata, West Bengal 700027",
        "phone": "+91 33 2456 7890",
        "rating": 4.8,
        "review_count": 1050,
        "emergency_available": True,
        "specialties": "Dedicated Super-Speciality Heart Hospital, 24/7 Primary PCI Emergency",
        "distance_km": None,
        "latitude": 22.5317,
        "longitude": 88.3308
    },
    {
        "id": "IN-HOSP-16",
        "name": "Apollo Gleneagles Hospitals",
        "city": "Kolkata",
        "address": "58, Canal Circular Rd, Kadapara, Phool Bagan, Kankurgachi, Kolkata, West Bengal 700054",
        "phone": "+91 33 2320 3040",
        "rating": 4.7,
        "review_count": 760,
        "emergency_available": True,
        "specialties": "Comprehensive Cardiac Surgery, Electrophysiology & Pacemaker Clinic",
        "distance_km": None,
        "latitude": 22.5735,
        "longitude": 88.3978
    },
    {
        "id": "IN-HOSP-17",
        "name": "U.N. Mehta Institute of Cardiology & Research",
        "city": "Ahmedabad",
        "address": "Civil Hospital (Medicity) Campus, Asarwa, Ahmedabad, Gujarat 380016",
        "phone": "+91 79 2268 4200",
        "rating": 4.9,
        "review_count": 1780,
        "emergency_available": True,
        "specialties": "Premier State Cardiac Super-Speciality Hospital, 24/7 Emergency Resuscitation",
        "distance_km": None,
        "latitude": 23.0526,
        "longitude": 72.6033
    },
    {
        "id": "IN-HOSP-18",
        "name": "Marengo CIMS Hospital",
        "city": "Ahmedabad",
        "address": "Off Science City Road, Sola, Ahmedabad, Gujarat 380060",
        "phone": "+91 79 3010 1200",
        "rating": 4.8,
        "review_count": 690,
        "emergency_available": True,
        "specialties": "Transcatheter Valve Therapies, Cardiac Critical Care, Heart Transplants",
        "distance_km": None,
        "latitude": 23.0763,
        "longitude": 72.5132
    },
    {
        "id": "IN-HOSP-19",
        "name": "Postgraduate Institute of Medical Education & Research (PGIMER)",
        "city": "Chandigarh",
        "address": "Sector 12, Chandigarh, 160012",
        "phone": "+91 172 274 7585",
        "rating": 4.9,
        "review_count": 1530,
        "emergency_available": True,
        "specialties": "Advanced Cardiac Center, Adult & Pediatric Cath Lab, 24/7 Emergency",
        "distance_km": None,
        "latitude": 30.7656,
        "longitude": 76.7745
    },
    {
        "id": "IN-HOSP-20",
        "name": "Sree Chitra Tirunal Institute for Medical Sciences",
        "city": "Thiruvananthapuram",
        "address": "Medical College PO, Thiruvananthapuram, Kerala 695011",
        "phone": "+91 471 252 4444",
        "rating": 4.9,
        "review_count": 1120,
        "emergency_available": True,
        "specialties": "National Premier Cardiovascular Institute, Advanced Electrophysiology & Surgery",
        "distance_km": None,
        "latitude": 8.5218,
        "longitude": 76.9281
    },
    {
        "id": "IN-HOSP-21",
        "name": "Fortis Escorts Hospital",
        "city": "Jaipur",
        "address": "Jawaharlal Nehru Marg, Malviya Nagar, Jaipur, Rajasthan 302017",
        "phone": "+91 141 254 7000",
        "rating": 4.8,
        "review_count": 840,
        "emergency_available": True,
        "specialties": "24/7 Heart Attack Response Team, Valve Clinics, Pacemaker Implantation",
        "distance_km": None,
        "latitude": 26.8524,
        "longitude": 75.8054
    },
    {
        "id": "IN-HOSP-22",
        "name": "KIMS Super Speciality Hospital",
        "city": "Bhubaneswar",
        "address": "Kushabhadra Campus 5, KIIT University, Bhubaneswar, Odisha 751024",
        "phone": "+91 674 710 5300",
        "rating": 4.8,
        "review_count": 780,
        "emergency_available": True,
        "specialties": "Comprehensive Interventional Cardiology, CTVS, 24/7 Cardiac ER",
        "distance_km": None,
        "latitude": 20.3543,
        "longitude": 85.8189
    },
    {
        "id": "IN-HOSP-23",
        "name": "Medanta Super Speciality Hospital",
        "city": "Lucknow",
        "address": "Sector B, Pocket 1, Amar Shaheed Path, Golf City, Lucknow, Uttar Pradesh 226030",
        "phone": "+91 522 450 5050",
        "rating": 4.8,
        "review_count": 920,
        "emergency_available": True,
        "specialties": "Heart Failure Clinic, Primary Angioplasty, Dedicated Heart ICU",
        "distance_km": None,
        "latitude": 26.7735,
        "longitude": 80.9575
    }
]

def init_db():
    """
    Initializes MongoDB Atlas connection, ensures indexes, and seeds initial datasets if collections are empty.
    """
    try:
        db = get_db()
        # Verify connection with ping
        db.command("ping")
        print("[MongoDB] MongoDB connected successfully")

        # 1. Users collection & indexes
        db.users.create_index("email", unique=True)
        db.users.create_index("id", unique=True)

        # Seed initial accounts if empty
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
            print("[MongoDB] Seeded default clinical user accounts.")

        # 2. Assessments collection & indexes
        db.assessments.create_index("id", unique=True)
        db.assessments.create_index("user_email")
        db.assessments.create_index([("timestamp", pymongo.DESCENDING)])
        db.assessments.create_index([("user_email", pymongo.ASCENDING), ("timestamp", pymongo.DESCENDING)])

        # 3. Hospitals collection & indexes
        db.hospitals.create_index("id", unique=True)
        db.hospitals.create_index("city")
        db.hospitals.create_index("name")

        # Seed hospitals if empty
        if db.hospitals.count_documents({}) == 0:
            db.hospitals.insert_many(DEFAULT_INDIAN_HOSPITALS)
            print(f"[MongoDB] Seeded {len(DEFAULT_INDIAN_HOSPITALS)} Indian cardiology centers.")

        # 4. Appointments collection & indexes
        db.appointments.create_index("booking_id", unique=True)
        db.appointments.create_index("hospital_id")

        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"[MongoDB Connection Error] Failed to connect to MongoDB Atlas: {e}")
        return False
    except Exception as e:
        print(f"[MongoDB Initialization Error] {e}")
        return False
