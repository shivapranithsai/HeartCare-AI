import json
import random
import uuid
import datetime
from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
import pymongo
from app.db.database import get_db
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
    db = get_db()

    query = {}

    clean_email = str(user_email).strip().lower() if isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none" else None
    clean_search = str(search).strip() if isinstance(search, str) and search.strip() else None
    clean_risk = str(risk_level).strip() if isinstance(risk_level, str) and risk_level.strip() and risk_level.strip() != "All" else None
    clean_limit = int(limit) if isinstance(limit, (int, str)) and str(limit).isdigit() else 100

    if clean_email:
        query["user_email"] = clean_email

    if clean_search:
        query["$or"] = [
            {"patient_name": {"$regex": clean_search, "$options": "i"}},
            {"summary_message": {"$regex": clean_search, "$options": "i"}},
            {"id": {"$regex": clean_search, "$options": "i"}}
        ]

    if clean_risk:
        query["risk_level"] = {"$regex": clean_risk, "$options": "i"}

    cursor = db.assessments.find(query).sort([("timestamp", pymongo.DESCENDING)]).limit(clean_limit)
    rows = list(cursor)
    total_count = db.assessments.count_documents(query)

    items = []
    for r in rows:
        input_data = r.get("input_data") or {}
        if not input_data and r.get("input_data_json"):
            try:
                input_data = json.loads(r["input_data_json"])
            except Exception:
                pass

        items.append(AssessmentHistoryItem(
            id=r.get("id", ""),
            timestamp=r.get("timestamp", ""),
            patient_name=r.get("patient_name", ""),
            age=r.get("age") or 0,
            gender=r.get("gender") or "Unspecified",
            risk_score=r.get("risk_score", 0),
            risk_level=r.get("risk_level", "Unknown"),
            probability_percentage=r.get("probability_percentage", 0.0),
            heart_health_score=r.get("heart_health_score", 0),
            systolic_bp=r.get("systolic_bp"),
            diastolic_bp=r.get("diastolic_bp"),
            cholesterol=r.get("cholesterol"),
            ejection_fraction=r.get("ejection_fraction"),
            serum_creatinine=r.get("serum_creatinine"),
            smoking=r.get("smoking"),
            chest_pain=r.get("chest_pain"),
            model_source=r.get("model_source", "HeartCare Heuristic"),
            summary_message=r.get("summary_message") or "",
            input_data=input_data
        ))

    return HistoryListResponse(total=total_count, items=items)

@router.post("/generate-dynamic")
def generate_dynamic_history(
    count: int = Query(default=5, ge=1, le=20),
    user_email: Optional[str] = Query(default=None)
):
    """
    Generates dynamic clinical patient records evaluated with the LightGBM ML model and persists to MongoDB.
    """
    clean_count = int(count) if isinstance(count, (int, str)) and str(count).isdigit() else 5
    clean_user_email = str(user_email).strip().lower() if isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none" else None

    db = get_db()

    male_first_names = ["Aarav", "Rohan", "Vikram", "Aditya", "Rahul", "Siddharth", "Amit", "Rajesh", "Manoj", "Suresh", "Arjun", "Alok", "Devendra", "Kiran", "Nikhil", "Pranav", "Harish", "Ashok", "Gaurav", "Sunil"]
    female_first_names = ["Priya", "Ananya", "Sneha", "Pooja", "Kavita", "Neha", "Deepika", "Sunita", "Anjali", "Meera", "Ritu", "Divya", "Swati", "Shalini", "Rekha", "Lakshmi", "Preeti", "Tanvi", "Gayatri", "Suman"]
    last_names = ["Sharma", "Verma", "Patel", "Reddy", "Gupta", "Deshmukh", "Nair", "Iyer", "Mehta", "Singh", "Mukherjee", "Joshi", "Bose", "Rao", "Chowdhury", "Kapoor", "Banerjee", "Kulkarni", "Aggarwal", "Pillai", "Mishra", "Chatterjee", "Bhattacharya", "Menon", "Saxena"]

    now = datetime.datetime.now()
    generated = []
    docs_to_insert = []

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

        input_dict = patient_input.model_dump()
        result_dict = pred_res.model_dump()

        doc = {
            "id": pred_id,
            "user_email": clean_user_email,
            "patient_name": name,
            "timestamp": timestamp,
            "age": age,
            "gender": gender,
            "risk_score": pred_res.risk_score,
            "risk_level": pred_res.risk_level,
            "probability_percentage": pred_res.probability_percentage,
            "heart_health_score": pred_res.heart_health_score,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "cholesterol": cholesterol,
            "ejection_fraction": ejection_fraction,
            "serum_creatinine": serum_creatinine,
            "smoking": smoking,
            "chest_pain": chest_pain,
            "model_source": pred_res.model_source,
            "summary_message": pred_res.summary_message,
            "input_data": input_dict,
            "input_data_json": json.dumps(input_dict),
            "response_data": result_dict,
            "response_data_json": json.dumps(result_dict)
        }
        docs_to_insert.append(doc)

        generated.append({
            "id": pred_id,
            "patient_name": name,
            "timestamp": timestamp,
            "risk_score": pred_res.risk_score,
            "risk_level": pred_res.risk_level
        })

    if docs_to_insert:
        db.assessments.insert_many(docs_to_insert)

    return {
        "status": "success",
        "message": f"Successfully generated {len(generated)} dynamic clinical assessments in MongoDB!",
        "generated": generated,
        "items": generated
    }

@router.get("/{id}")
def get_assessment_by_id(id: str):
    db = get_db()
    row = db.assessments.find_one({"id": id})

    if not row:
        raise HTTPException(status_code=404, detail="Assessment record not found")

    resp_data = row.get("response_data") or {}
    if not resp_data and row.get("response_data_json"):
        try:
            resp_data = json.loads(row["response_data_json"])
        except Exception:
            pass

    return {
        "id": row.get("id"),
        "patient_name": row.get("patient_name"),
        "timestamp": row.get("timestamp"),
        "age": row.get("age"),
        "gender": row.get("gender"),
        "risk_score": row.get("risk_score"),
        "risk_level": row.get("risk_level"),
        "probability_percentage": row.get("probability_percentage"),
        "heart_health_score": row.get("heart_health_score"),
        "systolic_bp": row.get("systolic_bp"),
        "diastolic_bp": row.get("diastolic_bp"),
        "cholesterol": row.get("cholesterol"),
        "ejection_fraction": row.get("ejection_fraction"),
        "serum_creatinine": row.get("serum_creatinine"),
        "smoking": row.get("smoking"),
        "chest_pain": row.get("chest_pain"),
        "model_source": row.get("model_source"),
        "summary_message": row.get("summary_message"),
        "details": resp_data
    }

@router.delete("/{id}")
def delete_assessment(id: str):
    db = get_db()
    result = db.assessments.delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "success", "message": f"Assessment record {id} deleted", "id": id}

@router.delete("")
def clear_all_history():
    db = get_db()
    db.assessments.delete_many({})
    return {"status": "success", "message": "All assessment records cleared from MongoDB"}
