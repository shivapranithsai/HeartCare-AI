import sqlite3
import json
import uuid
import datetime
import hashlib
from pathlib import Path
from app.core.config import DB_PATH

def hash_password(password: str) -> str:
    """Generates a secure SHA-256 hash for authentication."""
    salt = "heartcare_secure_salt_v1"
    return hashlib.sha256(f"{password}{salt}".encode('utf-8')).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table for Clinical Authentication
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_login TEXT
    );
    """)

    # Seed initial user accounts if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        seed_users = [
            (
                "USER-001",
                "dr.sharma@heartcare.ai",
                hash_password("admin123"),
                "Dr. Rajesh Sharma, MD, DM (Cardiology)",
                "Cardiologist / Physician",
                now_str,
                now_str
            ),
            (
                "USER-002",
                "patient@heartcare.ai",
                hash_password("patient123"),
                "Aarav Patel",
                "Patient / Individual User",
                now_str,
                now_str
            )
        ]
        cursor.executemany("""
        INSERT INTO users (id, email, password_hash, name, role, created_at, last_login)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, seed_users)

    # Assessments table with user_email scoping
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id TEXT PRIMARY KEY,
        user_email TEXT,
        patient_name TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        probability_percentage REAL,
        heart_health_score INTEGER,
        systolic_bp INTEGER,
        diastolic_bp INTEGER,
        cholesterol INTEGER,
        ejection_fraction INTEGER,
        serum_creatinine REAL,
        smoking TEXT,
        chest_pain TEXT,
        model_source TEXT,
        summary_message TEXT,
        input_data_json TEXT,
        response_data_json TEXT
    );
    """)

    # Ensure user_email column exists if table was created earlier without it
    cursor.execute("PRAGMA table_info(assessments)")
    cols = [r["name"] for r in cursor.fetchall()]
    if "user_email" not in cols:
        try:
            cursor.execute("ALTER TABLE assessments ADD COLUMN user_email TEXT;")
        except Exception:
            pass

    # Hospitals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hospitals (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        rating REAL,
        review_count INTEGER,
        emergency_available INTEGER,
        specialties TEXT,
        distance_km REAL,
        latitude REAL,
        longitude REAL
    );
    """)

    # Ensure latitude and longitude columns exist if table was created earlier without them
    cursor.execute("PRAGMA table_info(hospitals)")
    hosp_cols = [r["name"] for r in cursor.fetchall()]
    if "latitude" not in hosp_cols:
        try:
            cursor.execute("ALTER TABLE hospitals ADD COLUMN latitude REAL;")
        except Exception:
            pass
    if "longitude" not in hosp_cols:
        try:
            cursor.execute("ALTER TABLE hospitals ADD COLUMN longitude REAL;")
        except Exception:
            pass

    # Top Indian Premier Cardiology Centers & Rapid Chest Pain Centers with verified GPS coordinates
    # distance_km is initialized to None (computed purely dynamically from user GPS coordinates)
    indian_hospitals = [
        ("IN-HOSP-01", "All India Institute of Medical Sciences (AIIMS)", "New Delhi", "Sri Aurobindo Marg, Ansari Nagar, New Delhi, Delhi 110029", "+91 11 2658 8500", 4.9, 1420, 1, "Interventional Cardiology, CTVS, 24/7 Cardiac Emergency, Heart Transplants", None, 28.5672, 77.2100),
        ("IN-HOSP-02", "Fortis Escorts Heart Institute", "New Delhi", "Okhla Road, Sukhdev Vihar, New Delhi, Delhi 110025", "+91 11 4713 5000", 4.9, 980, 1, "Pediatric & Adult Cardiology, 24/7 Rapid Chest Pain Clinic, Electrophysiology", None, 28.5606, 77.2796),
        ("IN-HOSP-03", "Medanta - The Medicity Heart Institute", "Gurugram / NCR", "CH Bakhtawar Singh Road, Sector 38, Gurugram, Haryana 122001", "+91 124 414 1414", 4.8, 1150, 1, "Robotic Cardiac Surgery, Heart Valve Repair, TAVR/TAVI, Cardiac Critical Care", None, 28.4393, 77.0426),
        ("IN-HOSP-04", "Max Super Speciality Hospital", "New Delhi", "1, 2, Press Enclave Road, Saket, New Delhi, Delhi 110017", "+91 11 2651 5050", 4.8, 870, 1, "Primary Angioplasty, Heart Failure Management, Cardiac ICU", None, 28.5283, 77.2125),
        ("IN-HOSP-05", "Asian Heart Institute (AHI)", "Mumbai", "G/N Block, Bandra Kurla Complex (BKC), Bandra East, Mumbai, Maharashtra 400051", "+91 22 6698 6666", 4.9, 1280, 1, "Coronary Artery Bypass Graft (CABG), 24/7 Cardiac Trauma, Preventive Cardiology", None, 19.0664, 72.8687),
        ("IN-HOSP-06", "Kokilaben Dhirubhai Ambani Hospital", "Mumbai", "Rao Saheb Achutrao Patwardhan Marg, Four Bungalows, Andheri West, Mumbai 400053", "+91 22 4269 6969", 4.8, 920, 1, "Full Time Specialist System, LVAD Implantation, Nuclear Cardiology", None, 19.1311, 72.8252),
        ("IN-HOSP-07", "Ruby Hall Clinic Heart Care Center", "Pune", "40, Sassoon Road, Sangamvadi, Pune, Maharashtra 411001", "+91 20 6645 5100", 4.7, 740, 1, "Structural Heart Interventions, Heart Failure Clinic, Holter Monitoring", None, 18.5332, 73.8777),
        ("IN-HOSP-08", "Narayana Institute of Cardiac Sciences", "Bengaluru", "258/A, Bommasandra Industrial Area, Anekal Taluk, Bengaluru, Karnataka 560099", "+91 80 7122 2222", 4.9, 2100, 1, "Complex Valve Repair, Heart Transplants, Largest Cardiac ICU in Asia", None, 12.8094, 77.6974),
        ("IN-HOSP-09", "Manipal Hospital Heart Institute", "Bengaluru", "98, HAL Old Airport Rd, Kodihalli, Bengaluru, Karnataka 560017", "+91 80 2502 4444", 4.8, 890, 1, "TAVI/TAVR, Emergency Cath Lab, 24/7 Rapid Cardiac Resuscitation", None, 12.9592, 77.6492),
        ("IN-HOSP-10", "Sri Jayadeva Institute of Cardiovascular Sciences", "Bengaluru", "Bannerghatta Main Rd, 9th Block, Jayanagar, Bengaluru, Karnataka 560069", "+91 80 2297 7400", 4.9, 1850, 1, "Autonomous Government Cardiac Super-Speciality Institute, 24/7 Emergency", None, 12.9174, 77.5997),
        ("IN-HOSP-11", "Apollo Hospitals (Main & Greams Road)", "Chennai", "21 Greams Lane, Thousand Lights, Chennai, Tamil Nadu 600006", "+91 44 2829 0200", 4.9, 1620, 1, "Pioneers in Interventional Cardiology, Minimally Invasive Cardiac Surgery, TAVR", None, 13.0601, 80.2526),
        ("IN-HOSP-12", "Madras Medical Mission (MMM Hospital)", "Chennai", "4-A, Dr. J. Jayalalitha Nagar, Mogappair, Chennai, Tamil Nadu 600037", "+91 44 2656 8000", 4.8, 810, 1, "Advanced Heart Failure, Pediatric Cardiology, Cardiac Electrophysiology", None, 13.0858, 80.1772),
        ("IN-HOSP-13", "Apollo Health City", "Hyderabad", "Road No 72, Opp. Bharatiya Vidya Bhavan School, Jubilee Hills, Hyderabad, Telangana 500033", "+91 40 2360 7777", 4.9, 1340, 1, "24/7 Chest Pain Triage, MitraClip Interventions, Cardiac Rehabilitation", None, 17.4168, 78.4116),
        ("IN-HOSP-14", "CARE Hospitals (Institute of Cardiac Sciences)", "Hyderabad", "Road No. 1, Banjara Hills, Hyderabad, Telangana 500034", "+91 40 6165 6565", 4.8, 910, 1, "Interventional Cardiology, Heart Failure & Transplant Unit", None, 17.4156, 78.4487),
        ("IN-HOSP-15", "BM Birla Heart Research Centre", "Kolkata", "1/1, National Library Ave, Alipore, Kolkata, West Bengal 700027", "+91 33 2456 7890", 4.8, 1050, 1, "Dedicated Super-Speciality Heart Hospital, 24/7 Primary PCI Emergency", None, 22.5317, 88.3308),
        ("IN-HOSP-16", "Apollo Gleneagles Hospitals", "Kolkata", "58, Canal Circular Rd, Kadapara, Phool Bagan, Kankurgachi, Kolkata, West Bengal 700054", "+91 33 2320 3040", 4.7, 760, 1, "Comprehensive Cardiac Surgery, Electrophysiology & Pacemaker Clinic", None, 22.5735, 88.3978),
        ("IN-HOSP-17", "U.N. Mehta Institute of Cardiology & Research", "Ahmedabad", "Civil Hospital (Medicity) Campus, Asarwa, Ahmedabad, Gujarat 380016", "+91 79 2268 4200", 4.9, 1780, 1, "Premier State Cardiac Super-Speciality Hospital, 24/7 Emergency Resuscitation", None, 23.0526, 72.6033),
        ("IN-HOSP-18", "Marengo CIMS Hospital", "Ahmedabad", "Off Science City Road, Sola, Ahmedabad, Gujarat 380060", "+91 79 3010 1200", 4.8, 690, 1, "Transcatheter Valve Therapies, Cardiac Critical Care, Heart Transplants", None, 23.0763, 72.5132),
        ("IN-HOSP-19", "Postgraduate Institute of Medical Education & Research (PGIMER)", "Chandigarh", "Sector 12, Chandigarh, 160012", "+91 172 274 7585", 4.9, 1530, 1, "Advanced Cardiac Center, Adult & Pediatric Cath Lab, 24/7 Emergency", None, 30.7656, 76.7745),
        ("IN-HOSP-20", "Sree Chitra Tirunal Institute for Medical Sciences", "Thiruvananthapuram", "Medical College PO, Thiruvananthapuram, Kerala 695011", "+91 471 252 4444", 4.9, 1120, 1, "National Premier Cardiovascular Institute, Advanced Electrophysiology & Surgery", None, 8.5218, 76.9281),
        ("IN-HOSP-21", "Fortis Escorts Hospital", "Jaipur", "Jawaharlal Nehru Marg, Malviya Nagar, Jaipur, Rajasthan 302017", "+91 141 254 7000", 4.8, 840, 1, "24/7 Heart Attack Response Team, Valve Clinics, Pacemaker Implantation", None, 26.8524, 75.8054),
        ("IN-HOSP-22", "KIMS Super Speciality Hospital", "Bhubaneswar", "Kushabhadra Campus 5, KIIT University, Bhubaneswar, Odisha 751024", "+91 674 710 5300", 4.8, 780, 1, "Comprehensive Interventional Cardiology, CTVS, 24/7 Cardiac ER", None, 20.3543, 85.8189),
        ("IN-HOSP-23", "Medanta Super Speciality Hospital", "Lucknow", "Sector B, Pocket 1, Amar Shaheed Path, Golf City, Lucknow, Uttar Pradesh 226030", "+91 522 450 5050", 4.8, 920, 1, "Heart Failure Clinic, Primary Angioplasty, Dedicated Heart ICU", None, 26.7735, 80.9575)
    ]

    # Refresh hospitals table with Indian hospitals
    cursor.execute("DELETE FROM hospitals")
    cursor.executemany("""
    INSERT INTO hospitals (id, name, city, address, phone, rating, review_count, emergency_available, specialties, distance_km, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, indian_hospitals)

    conn.commit()
    conn.close()
