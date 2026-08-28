import json
from fastapi import APIRouter, Query
from typing import Optional
import pymongo
from app.db.database import get_db

router = APIRouter()

@router.get("")
def get_analytics_overview(user_email: Optional[str] = Query(None, description="Filter by logged-in user email")):
    db = get_db()

    match_filter = {}
    clean_email = str(user_email).strip().lower() if isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none" else None
    if clean_email:
        match_filter["user_email"] = clean_email

    total = db.assessments.count_documents(match_filter)

    if total == 0:
        return {
            "has_assessments": False,
            "latest_assessment": None,
            "total_assessments": 0,
            "average_risk_score": None,
            "average_health_score": None,
            "risk_distribution": {"Low Risk": 0, "Moderate Risk": 0, "High Risk": 0, "Critical Risk": 0},
            "timeline": []
        }

    # Aggregate averages and distribution
    pipeline = [
        {"$match": match_filter},
        {
            "$group": {
                "_id": None,
                "avg_risk": {"$avg": "$risk_score"},
                "avg_health": {"$avg": "$heart_health_score"}
            }
        }
    ]
    agg_res = list(db.assessments.aggregate(pipeline))
    avg_risk = agg_res[0]["avg_risk"] if agg_res else None
    avg_health = agg_res[0]["avg_health"] if agg_res else None

    # Distribution pipeline
    dist_pipeline = [
        {"$match": match_filter},
        {
            "$group": {
                "_id": "$risk_level",
                "count": {"$sum": 1}
            }
        }
    ]
    dist_rows = list(db.assessments.aggregate(dist_pipeline))
    dist = {"Low Risk": 0, "Moderate Risk": 0, "High Risk": 0, "Critical Risk": 0}
    for row in dist_rows:
        level = row.get("_id") or ""
        cnt = row.get("count", 0)
        for k in dist:
            if k.lower() in level.lower():
                dist[k] += cnt
                break

    # Fetch latest evaluation for this user
    latest_row = db.assessments.find_one(match_filter, sort=[("timestamp", pymongo.DESCENDING), ("_id", pymongo.DESCENDING)])
    latest_assessment = None
    if latest_row:
        resp_data = latest_row.get("response_data") or {}
        if not resp_data and latest_row.get("response_data_json"):
            try:
                resp_data = json.loads(latest_row["response_data_json"])
            except Exception:
                pass

        input_data = latest_row.get("input_data") or {}
        if not input_data and latest_row.get("input_data_json"):
            try:
                input_data = json.loads(latest_row["input_data_json"])
            except Exception:
                pass

        fbs_val = input_data.get("fasting_blood_sugar") or (140 if input_data.get("fbs") == 1 else 95)

        latest_assessment = {
            "id": latest_row.get("id"),
            "patient_name": latest_row.get("patient_name"),
            "timestamp": latest_row.get("timestamp"),
            "risk_score": latest_row.get("risk_score"),
            "heart_health_score": latest_row.get("heart_health_score"),
            "probability_percentage": latest_row.get("probability_percentage"),
            "risk_level": latest_row.get("risk_level"),
            "bmi": resp_data.get("bmi", 24.2),
            "bmi_category": resp_data.get("bmi_category", "Normal"),
            "systolic_bp": latest_row.get("systolic_bp"),
            "diastolic_bp": latest_row.get("diastolic_bp"),
            "cholesterol": latest_row.get("cholesterol"),
            "ejection_fraction": latest_row.get("ejection_fraction"),
            "serum_creatinine": latest_row.get("serum_creatinine"),
            "fasting_blood_sugar": fbs_val,
            "smoking": latest_row.get("smoking"),
            "chest_pain": latest_row.get("chest_pain"),
            "top_risk_factors": resp_data.get("top_risk_factors", []),
            "protective_factors": resp_data.get("protective_factors", []),
            "recommendations": resp_data.get("recommendations", []),
            "summary_message": latest_row.get("summary_message") or resp_data.get("summary_message", ""),
            "model_source": latest_row.get("model_source", "HeartCare LightGBM")
        }

    # Recent timeline points for graph
    timeline_cursor = db.assessments.find(
        match_filter,
        projection={"id": 1, "timestamp": 1, "risk_score": 1, "heart_health_score": 1, "patient_name": 1, "risk_level": 1}
    ).sort([("timestamp", pymongo.ASCENDING)]).limit(20)

    timeline_rows = list(timeline_cursor)
    timeline = [
        {
            "id": r.get("id", ""),
            "date": r.get("timestamp", "").split(" ")[0] if " " in r.get("timestamp", "") else r.get("timestamp", ""),
            "risk_score": r.get("risk_score"),
            "health_score": r.get("heart_health_score"),
            "patient": r.get("patient_name"),
            "risk_level": r.get("risk_level")
        }
        for r in timeline_rows
    ]

    return {
        "has_assessments": True,
        "latest_assessment": latest_assessment,
        "total_assessments": total,
        "average_risk_score": round(avg_risk, 1) if avg_risk is not None else None,
        "average_health_score": round(avg_health, 1) if avg_health is not None else None,
        "risk_distribution": dist,
        "timeline": timeline
    }
