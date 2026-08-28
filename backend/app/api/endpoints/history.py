import json
import random
import uuid
import datetime
from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from app.db.database import get_db_connection
from app.schemas.history import HistoryListResponse, AssessmentHistoryItem
from app.schemas.prediction import PatientInput
from app.ml.model_loader import ml_service

router = APIRouter()

@router.get("", response_model=HistoryListResponse)
def get_assessment_history(
    search: Optional[str] = Query(None, description="Search by patient name or summary"),
    risk_level: Optional[str] = Query(None, description="Filter by risk category"),
    user_email: Optional[str] = Query(None, description="Filter by logged-in user email"),
    limit: int = Query(100, ge=1, le=500)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM assessments WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM assessments WHERE 1=1"
    params = []
    count_params = []

    clean_email = str(user_email).strip().lower() if isinstance(user_email, str) and user_email.strip() else None
    clean_search = str(search).strip() if isinstance(search, str) and search.strip() else None
    clean_risk = str(risk_level).strip() if isinstance(risk_level, str) and risk_level.strip() and risk_level.strip() != "All" else None
    clean_limit = int(limit) if isinstance(limit, (int, str)) and str(limit).isdigit() else 100

    if clean_email:
        query += " AND user_email = ?"
        count_query += " AND user_email = ?"
        params.append(clean_email)
        count_params.append(clean_email)

    if clean_search:
        query += " AND (patient_name LIKE ? OR summary_message LIKE ? OR id LIKE ?)"
        count_query += " AND (patient_name LIKE ? OR summary_message LIKE ? OR id LIKE ?)"
        term = f"%{clean_search}%"
        params.extend([term, term, term])
        count_params.extend([term, term, term])

    if clean_risk:
        query += " AND risk_level LIKE ?"
        count_query += " AND risk_level LIKE ?"
        params.append(f"%{clean_risk}%")
        count_params.append(f"%{clean_risk}%")

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(clean_limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    items = []
    for r in rows:
        input_data = {}
        try:
            if r["input_data_json"]:
                input_data = json.loads(r["input_data_json"])
        except Exception:
            pass

        items.append(AssessmentHistoryItem(
            id=r["id"],
            timestamp=r["timestamp"],
            patient_name=r["patient_name"],
            age=r["age"] or 0,
            gender=r["gender"] or "Unspecified",
            risk_score=r["risk_score"],
            risk_level=r["risk_level"],
            probability_percentage=r["probability_percentage"],
            heart_health_score=r["heart_health_score"],
            systolic_bp=r["systolic_bp"],
            diastolic_bp=r["diastolic_bp"],
            cholesterol=r["cholesterol"],
            ejection_fraction=r["ejection_fraction"],
            serum_creatinine=r["serum_creatinine"],
            smoking=r["smoking"],
            chest_pain=r["chest_pain"],
            model_source=r["model_source"],
            summary_message=r["summary_message"] or "",
            input_data=input_data
        ))

    # Count total matching filters
    cursor.execute(count_query, count_params)
    total_count = cursor.fetchone()[0]

    conn.close()
    return HistoryListResponse(total=total_count, items=items)

@router.post("/generate-dynamic")
def generate_dynamic_history(
    count: int = Query(default=5, ge=1, le=20),
    user_email: Optional[str] = Query(default=None)
):
    """
    Generates dynamic clinical patient records evaluated with the LightGBM ML model.
    """
    clean_count = int(count) if isinstance(count, (int, str)) and str(count).isdigit() else 5
    clean_user_email = str(user_email).strip().lower() if isinstance(user_email, str) and user_email.strip() else None

    conn = get_db_connection()
    cursor = conn.cursor()

    male_first_names = ["Aarav", "Rohan", "Vikram", "Aditya", "Rahul", "Siddharth", "Amit", "Rajesh", "Manoj", "Suresh", "Arjun", "Alok", "Devendra", "Kiran", "Nikhil", "Pranav", "Harish", "Ashok", "Gaurav", "Sunil"]
    female_first_names = ["Priya", "Ananya", "Sneha", "Pooja", "Kavita", "Neha", "Deepika", "Sunita", "Anjali", "Meera", "Ritu", "Divya", "Swati", "Shalini", "Rekha", "Lakshmi", "Preeti", "Tanvi", "Gayatri", "Suman"]
    last_names = ["Sharma", "Verma", "Patel", "Reddy", "Gupta", "Deshmukh", "Nair", "Iyer", "Mehta", "Singh", "Mukherjee", "Joshi", "Bose", "Rao", "Chowdhury", "Kapoor", "Banerjee", "Kulkarni", "Aggarwal", "Pillai", "Mishra", "Chatterjee", "Bhattacharya", "Menon", "Saxena"]

    now = datetime.datetime.now()
    generated = []

    for i in range(clean_count):
        gender = random.choice(["Male", "Female"])
        first_name = random.choice(male_first_names) if gender == "Male" else random.choice(female_first_names)
        name = f"{first_name} {random.choice(last_names)}"
        age = random.randint(32, 79)
        sex = 1 if gender == "Male" else 0
        
        # Clinical risk profile distribution
        profile = random.choices(["healthy", "moderate", "high", "critical"], weights=[0.35, 0.30, 0.25, 0.10])[0]
        
        if profile == "healthy":
            cp = random.choice([0, 1])
            trestbps = random.randint(110, 128)
            chol = random.randint(160, 205)
            fbs = 0
            restecg = 0
            thalach = random.randint(145, 178)
            exang = 0
            oldpeak = round(random.uniform(0.0, 0.8), 1)
            slope = 0
            ca = 0
            thal = 1
            ejection_fraction = random.randint(58, 68)
            serum_creatinine = round(random.uniform(0.7, 1.0), 1)
            smoking = "Never"
            chest_pain = "None"
        elif profile == "moderate":
            cp = random.choice([1, 2])
            trestbps = random.randint(130, 148)
            chol = random.randint(210, 245)
            fbs = random.choice([0, 1])
            restecg = random.choice([0, 1])
            thalach = random.randint(128, 148)
            exang = random.choice([0, 1])
            oldpeak = round(random.uniform(0.9, 1.8), 1)
            slope = 1
            ca = random.choice([0, 1])
            thal = random.choice([1, 2])
            ejection_fraction = random.randint(46, 56)
            serum_creatinine = round(random.uniform(1.0, 1.3), 1)
            smoking = "Occasionally"
            chest_pain = "Mild"
        elif profile == "high":
            cp = random.choice([2, 3])
            trestbps = random.randint(148, 170)
            chol = random.randint(245, 290)
            fbs = 1
            restecg = random.choice([1, 2])
            thalach = random.randint(108, 130)
            exang = 1
            oldpeak = round(random.uniform(1.9, 3.2), 1)
            slope = random.choice([1, 2])
            ca = random.choice([1, 2])
            thal = random.choice([2, 3])
            ejection_fraction = random.randint(35, 45)
            serum_creatinine = round(random.uniform(1.3, 1.8), 1)
            smoking = "Regularly"
            chest_pain = "Moderate"
        else: # critical
            cp = 3
            trestbps = random.randint(168, 195)
            chol = random.randint(285, 360)
            fbs = 1
            restecg = 2
            thalach = random.randint(88, 115)
            exang = 1
            oldpeak = round(random.uniform(3.0, 4.8), 1)
            slope = 2
            ca = random.choice([2, 3])
            thal = 3
            ejection_fraction = random.randint(25, 34)
            serum_creatinine = round(random.uniform(1.8, 2.8), 1)
            smoking = "Regularly"
            chest_pain = "Severe"

        systolic_bp = trestbps
        diastolic_bp = int(trestbps * 0.65)
        cholesterol = chol

        patient_input = PatientInput(
            name=name,
            user_email=clean_user_email,
            age=age,
            sex=sex,
            gender=gender,
            cp=cp,
            chest_pain=chest_pain,
            trestbps=trestbps,
            systolic_bp=systolic_bp,
            diastolic_bp=diastolic_bp,
            chol=chol,
            cholesterol=chol,
            fbs=fbs,
            fasting_blood_sugar=140 if fbs == 1 else 95,
            restecg=restecg,
            thalach=thalach,
            heart_rate=random.randint(68, 92),
            exang=exang,
            oldpeak=oldpeak,
            st_depression=oldpeak,
            slope=slope,
            ca=ca,
            thal=thal,
            ejection_fraction=ejection_fraction,
            serum_creatinine=serum_creatinine,
            smoking=smoking
        )

        pred_res = ml_service.predict(patient_input)

        days_ago = (clean_count - i) * random.randint(1, 4)
        timestamp = (now - datetime.timedelta(days=days_ago, hours=random.randint(1, 12))).strftime("%Y-%m-%d %H:%M")

        pred_id = f"PRED-DYN{uuid.uuid4().hex[:6].upper()}"

        cursor.execute("""
        INSERT INTO assessments (
            id, user_email, patient_name, timestamp, age, gender, risk_score, risk_level, probability_percentage,
            heart_health_score, systolic_bp, diastolic_bp, cholesterol, ejection_fraction, serum_creatinine,
            smoking, chest_pain, model_source, summary_message, input_data_json, response_data_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pred_id,
            clean_user_email,
            name,
            timestamp,
            age,
            gender,
            pred_res.risk_score,
            pred_res.risk_level,
            pred_res.probability_percentage,
            pred_res.heart_health_score,
            systolic_bp,
            diastolic_bp,
            cholesterol,
            ejection_fraction,
            serum_creatinine,
            smoking,
            chest_pain,
            pred_res.model_source,
            pred_res.summary_message,
            json.dumps(patient_input.model_dump()),
            json.dumps(pred_res.model_dump())
        ))

        generated.append({
            "id": pred_id,
            "patient_name": name,
            "timestamp": timestamp,
            "risk_score": pred_res.risk_score,
            "risk_level": pred_res.risk_level
        })

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "message": f"Successfully generated {len(generated)} dynamic clinical assessments!",
        "generated": generated,
        "items": generated
    }

@router.get("/{id}")
def get_assessment_by_id(id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assessments WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Assessment record not found")

    resp_data = {}
    if row["response_data_json"]:
        try:
            resp_data = json.loads(row["response_data_json"])
        except Exception:
            pass

    return {
        "id": row["id"],
        "patient_name": row["patient_name"],
        "timestamp": row["timestamp"],
        "age": row["age"],
        "gender": row["gender"],
        "risk_score": row["risk_score"],
        "risk_level": row["risk_level"],
        "probability_percentage": row["probability_percentage"],
        "heart_health_score": row["heart_health_score"],
        "systolic_bp": row["systolic_bp"],
        "diastolic_bp": row["diastolic_bp"],
        "cholesterol": row["cholesterol"],
        "ejection_fraction": row["ejection_fraction"],
        "serum_creatinine": row["serum_creatinine"],
        "smoking": row["smoking"],
        "chest_pain": row["chest_pain"],
        "model_source": row["model_source"],
        "summary_message": row["summary_message"],
        "details": resp_data
    }

@router.delete("/{id}")
def delete_assessment(id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assessments WHERE id = ?", (id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "success", "message": f"Assessment record {id} deleted", "id": id}

@router.delete("")
def clear_all_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assessments")
    conn.commit()
    conn.close()
    return {"status": "success", "message": "All assessment records cleared"}
