import json
import random
import uuid
import datetime
from typing import Optional, Annotated
from fastapi import APIRouter, HTTPException, Query, status
import pymongo

from app.db.database import get_db
from app.schemas.history import HistoryListResponse, AssessmentHistoryItem
from app.schemas.prediction import PatientInput
from app.ml.model_loader import ml_service

router = APIRouter()

@router.get("", response_model=HistoryListResponse)
def get_assessment_history(
    search: Annotated[Optional[str], Query(description="Search by patient name or summary")] = None,
    risk_level: Annotated[Optional[str], Query(description="Filter by risk category")] = None,
    user_email: Annotated[Optional[str], Query(description="Filter by logged-in user email")] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100
):
    """
    Retrieves previous heart failure risk assessments, with optional filters
    for patient name, risk category, and user email.
    """
    db = get_db()
    query = {}

    if user_email and isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none":
        query["user_email"] = user_email.strip().lower()

    if search and isinstance(search, str) and search.strip():
        term = search.strip()
        query["$or"] = [
            {"patient_name": {"$regex": term, "$options": "i"}},
            {"summary_message": {"$regex": term, "$options": "i"}},
            {"id": {"$regex": term, "$options": "i"}}
        ]

    if risk_level and isinstance(risk_level, str) and risk_level.strip() and risk_level.strip() != "All":
        query["risk_level"] = {"$regex": risk_level.strip(), "$options": "i"}

    effective_limit = limit if isinstance(limit, int) and limit > 0 else 100
    cursor = db.assessments.find(query).sort([("timestamp", pymongo.DESCENDING)]).limit(effective_limit)
    rows = list(cursor)
    total_count = db.assessments.count_documents(query)

    items = []
    for r in rows:
        # Load input data from native dict or legacy JSON string
        input_data = r.get("input_data") or {}
        if not input_data and r.get("input_data_json"):
            try:
                input_data = json.loads(r["input_data_json"])
            except Exception:
                pass

        items.append(AssessmentHistoryItem(
            id=r.get("id", ""),
            timestamp=r.get("timestamp", ""),
            patient_name=r.get("patient_name", "Anonymous"),
            age=r.get("age", 0),
            gender=r.get("gender", "Unspecified"),
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
            model_source=r.get("model_source", "HeartCare LightGBM"),
            summary_message=r.get("summary_message", ""),
            input_data=input_data
        ))

    return HistoryListResponse(total=total_count, items=items)

@router.post("/generate-dynamic")
def generate_dynamic_history(
    count: Annotated[int, Query(ge=1, le=20)] = 5,
    user_email: Annotated[Optional[str], Query()] = None
):
    """
    Generates synthetic patient records evaluated through the ML model
    for live demonstration and testing.
    """
    effective_count = count if isinstance(count, int) and count > 0 else 5
    clean_email = user_email.strip().lower() if user_email and isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none" else None
    db = get_db()

    male_first_names = ["Aarav", "Rohan", "Vikram", "Aditya", "Rahul", "Siddharth", "Amit", "Rajesh", "Manoj", "Suresh"]
    female_first_names = ["Priya", "Ananya", "Sneha", "Pooja", "Kavita", "Neha", "Deepika", "Sunita", "Anjali", "Meera"]
    last_names = ["Sharma", "Verma", "Patel", "Reddy", "Gupta", "Deshmukh", "Nair", "Iyer", "Mehta", "Singh"]

    now = datetime.datetime.now()
    generated = []
    docs_to_insert = []

    for i in range(effective_count):
        gender = random.choice(["Male", "Female"])
        first_name = random.choice(male_first_names) if gender == "Male" else random.choice(female_first_names)
        name = f"{first_name} {random.choice(last_names)}"
        age = random.randint(35, 75)
        sex = 1 if gender == "Male" else 0

        # Health profile tier
        profile = random.choices(["healthy", "moderate", "high"], weights=[0.4, 0.4, 0.2])[0]

        if profile == "healthy":
            trestbps, chol, thalach = random.randint(110, 125), random.randint(160, 200), random.randint(150, 175)
            ef, cr = random.randint(58, 68), round(random.uniform(0.7, 1.0), 1)
            oldpeak, cp, smoking = 0.0, 0, "Never"
            chest_pain = "None"
        elif profile == "moderate":
            trestbps, chol, thalach = random.randint(130, 145), random.randint(210, 245), random.randint(130, 150)
            ef, cr = random.randint(46, 55), round(random.uniform(1.0, 1.3), 1)
            oldpeak, cp, smoking = round(random.uniform(0.8, 1.6), 1), 1, "Occasionally"
            chest_pain = "Mild"
        else:
            trestbps, chol, thalach = random.randint(150, 175), random.randint(250, 310), random.randint(100, 125)
            ef, cr = random.randint(32, 44), round(random.uniform(1.4, 2.0), 1)
            oldpeak, cp, smoking = round(random.uniform(1.8, 3.2), 1), 2, "Regularly"
            chest_pain = "Severe"

        patient_input = PatientInput(
            name=name,
            user_email=clean_email,
            age=age,
            sex=sex,
            gender=gender,
            cp=cp,
            chest_pain=chest_pain,
            trestbps=trestbps,
            systolic_bp=trestbps,
            diastolic_bp=int(trestbps * 0.65),
            chol=chol,
            cholesterol=chol,
            fbs=1 if profile == "high" else 0,
            fasting_blood_sugar=140 if profile == "high" else 95,
            restecg=1 if profile == "high" else 0,
            thalach=thalach,
            heart_rate=random.randint(68, 88),
            exang=1 if profile == "high" else 0,
            oldpeak=oldpeak,
            st_depression=oldpeak,
            slope=2 if profile == "high" else 1 if profile == "moderate" else 0,
            ca=1 if profile == "high" else 0,
            thal=3 if profile == "high" else 1,
            ejection_fraction=ef,
            serum_creatinine=cr,
            smoking=smoking
        )

        pred_res = ml_service.predict(patient_input)

        days_ago = (effective_count - i) * random.randint(1, 3)
        timestamp = (now - datetime.timedelta(days=days_ago, hours=random.randint(1, 8))).strftime("%Y-%m-%d %H:%M")
        pred_id = f"PRED-DYN{uuid.uuid4().hex[:6].upper()}"

        doc = {
            "id": pred_id,
            "user_email": clean_email,
            "patient_name": name,
            "timestamp": timestamp,
            "age": age,
            "gender": gender,
            "risk_score": pred_res.risk_score,
            "risk_level": pred_res.risk_level,
            "probability_percentage": pred_res.probability_percentage,
            "heart_health_score": pred_res.heart_health_score,
            "systolic_bp": trestbps,
            "diastolic_bp": int(trestbps * 0.65),
            "cholesterol": chol,
            "ejection_fraction": ef,
            "serum_creatinine": cr,
            "smoking": smoking,
            "chest_pain": chest_pain,
            "model_source": pred_res.model_source,
            "summary_message": pred_res.summary_message,
            "input_data": patient_input.model_dump(),
            "response_data": pred_res.model_dump()
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
        "message": f"Successfully generated {len(generated)} dynamic clinical assessments.",
        "generated": generated,
        "items": generated
    }

@router.get("/{id}")
def get_assessment_by_id(
    id: str,
    user_email: Annotated[Optional[str], Query(description="Filter by user email for owner authorization")] = None
):
    """Fetches full assessment details by prediction ID."""
    db = get_db()
    query = {"id": id}
    if user_email and isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none":
        query["user_email"] = user_email.strip().lower()

    row = db.assessments.find_one(query)

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
def delete_assessment(
    id: str,
    user_email: Annotated[Optional[str], Query(description="Filter by user email for owner authorization")] = None
):
    """Deletes a specific assessment record."""
    db = get_db()
    query = {"id": id}
    if user_email and isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none":
        query["user_email"] = user_email.strip().lower()

    result = db.assessments.delete_one(query)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "success", "message": f"Assessment record {id} deleted", "id": id}

@router.delete("")
def clear_all_history(
    user_email: Annotated[Optional[str], Query(description="Filter by user email for owner authorization")] = None
):
    """Clears all assessment history records."""
    db = get_db()
    query = {}
    if user_email and isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none":
        query["user_email"] = user_email.strip().lower()
    db.assessments.delete_many(query)
    return {"status": "success", "message": "All assessment records cleared"}
