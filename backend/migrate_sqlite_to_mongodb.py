#!/usr/bin/env python3
"""
Migration Utility: SQLite3 (backend/data/heartcare.db) -> MongoDB Atlas
Preserves and migrates:
- Users collection (19 accounts)
- Assessments collection (35 assessments)
- Hospitals collection (23 cardiology centers)
"""

import sqlite3
import json
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.config import DB_PATH, MONGODB_URI, MONGODB_DB_NAME
from app.db.database import get_db, init_db

def migrate():
    print("=" * 60)
    print(" HEARTCARE AI: SQLITE -> MONGODB ATLAS DATA MIGRATION")
    print("=" * 60)

    if not DB_PATH.exists():
        print(f"[!] SQLite database not found at {DB_PATH}. Initializing fresh MongoDB collections.")
        init_db()
        return

    print(f"[*] Reading source SQLite database: {DB_PATH}")
    sqlite_conn = sqlite3.connect(DB_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    db = get_db()
    
    # Drop any existing collections to ensure a clean migration from source SQLite
    db.users.drop()
    db.assessments.drop()
    db.hospitals.drop()
    print("[*] Cleared pre-existing MongoDB collections for clean migration.")

    print("[*] Initializing MongoDB database and creating indexes...")
    init_db()

    # -------------------------------------------------------------
    # 1. Migrate Users
    # -------------------------------------------------------------
    sqlite_cur.execute("SELECT * FROM users")
    user_rows = sqlite_cur.fetchall()
    migrated_users = 0
    for r in user_rows:
        user_doc = {
            "id": r["id"],
            "email": r["email"].strip().lower(),
            "password_hash": r["password_hash"],
            "name": r["name"],
            "role": r["role"],
            "created_at": r["created_at"],
            "last_login": r["last_login"]
        }
        db.users.update_one({"id": user_doc["id"]}, {"$set": user_doc}, upsert=True)
        migrated_users += 1
    print(f"[OK] Users Migrated: {migrated_users} / {len(user_rows)} from SQLite. Total in MongoDB: {db.users.count_documents({})}")

    # -------------------------------------------------------------
    # 2. Migrate Assessments
    # -------------------------------------------------------------
    sqlite_cur.execute("SELECT * FROM assessments")
    assessment_rows = sqlite_cur.fetchall()
    migrated_assessments = 0
    for r in assessment_rows:
        input_data = {}
        if r["input_data_json"]:
            try:
                input_data = json.loads(r["input_data_json"])
            except Exception:
                pass

        resp_data = {}
        if r["response_data_json"]:
            try:
                resp_data = json.loads(r["response_data_json"])
            except Exception:
                pass

        user_email = r["user_email"].strip().lower() if r["user_email"] else None

        assessment_doc = {
            "id": r["id"],
            "user_email": user_email,
            "patient_name": r["patient_name"],
            "timestamp": r["timestamp"],
            "age": r["age"],
            "gender": r["gender"],
            "risk_score": r["risk_score"],
            "risk_level": r["risk_level"],
            "probability_percentage": r["probability_percentage"],
            "heart_health_score": r["heart_health_score"],
            "systolic_bp": r["systolic_bp"],
            "diastolic_bp": r["diastolic_bp"],
            "cholesterol": r["cholesterol"],
            "ejection_fraction": r["ejection_fraction"],
            "serum_creatinine": r["serum_creatinine"],
            "smoking": r["smoking"],
            "chest_pain": r["chest_pain"],
            "model_source": r["model_source"],
            "summary_message": r["summary_message"],
            "input_data": input_data,
            "input_data_json": r["input_data_json"],
            "response_data": resp_data,
            "response_data_json": r["response_data_json"]
        }
        db.assessments.update_one({"id": assessment_doc["id"]}, {"$set": assessment_doc}, upsert=True)
        migrated_assessments += 1
    print(f"[OK] Assessments Migrated: {migrated_assessments} / {len(assessment_rows)} from SQLite. Total in MongoDB: {db.assessments.count_documents({})}")

    # -------------------------------------------------------------
    # 3. Migrate Hospitals
    # -------------------------------------------------------------
    sqlite_cur.execute("SELECT * FROM hospitals")
    hospital_rows = sqlite_cur.fetchall()
    migrated_hospitals = 0
    for r in hospital_rows:
        hosp_doc = {
            "id": r["id"],
            "name": r["name"],
            "city": r["city"],
            "address": r["address"],
            "phone": r["phone"],
            "rating": r["rating"],
            "review_count": r["review_count"],
            "emergency_available": bool(r["emergency_available"]),
            "specialties": r["specialties"],
            "distance_km": None,
            "latitude": r["latitude"],
            "longitude": r["longitude"]
        }
        db.hospitals.update_one({"id": hosp_doc["id"]}, {"$set": hosp_doc}, upsert=True)
        migrated_hospitals += 1
    print(f"[OK] Hospitals Migrated: {migrated_hospitals} / {len(hospital_rows)} from SQLite. Total in MongoDB: {db.hospitals.count_documents({})}")

    sqlite_conn.close()

    print("=" * 60)
    print(" MIGRATION COMPLETED SUCCESSFULLY")
    print(f" MongoDB Database Name: '{MONGODB_DB_NAME}'")
    print(f" - Users: {db.users.count_documents({})}")
    print(f" - Assessments: {db.assessments.count_documents({})}")
    print(f" - Hospitals: {db.hospitals.count_documents({})}")
    print("=" * 60)

if __name__ == "__main__":
    migrate()
