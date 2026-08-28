import json
from fastapi import APIRouter, Query
from typing import Optional
from app.db.database import get_db_connection

router = APIRouter()

@router.get("")
def get_analytics_overview(user_email: Optional[str] = Query(None, description="Filter by logged-in user email")):
    conn = get_db_connection()
    cursor = conn.cursor()

    where_clause = ""
    params = []
    clean_email = str(user_email).strip().lower() if isinstance(user_email, str) and user_email.strip() and user_email.strip().lower() != "none" else None
    if clean_email:
        where_clause = " WHERE user_email = ?"
        params.append(clean_email)

    cursor.execute(f"SELECT COUNT(*) FROM assessments{where_clause}", params)
    total = cursor.fetchone()[0]

    if total == 0:
        conn.close()
        return {
            "has_assessments": False,
            "latest_assessment": None,
            "total_assessments": 0,
            "average_risk_score": None,
            "average_health_score": None,
            "risk_distribution": {"Low Risk": 0, "Moderate Risk": 0, "High Risk": 0, "Critical Risk": 0},
            "timeline": []
        }

    cursor.execute(f"SELECT AVG(risk_score), AVG(heart_health_score) FROM assessments{where_clause}", params)
    avg_risk, avg_health = cursor.fetchone()

    cursor.execute(f"SELECT risk_level, COUNT(*) FROM assessments{where_clause} GROUP BY risk_level", params)
    dist_rows = cursor.fetchall()
    dist = {"Low Risk": 0, "Moderate Risk": 0, "High Risk": 0, "Critical Risk": 0}
    for level, count in dist_rows:
        for k in dist:
            if k.lower() in level.lower():
                dist[k] += count
                break

    # Fetch latest evaluation for this user
    cursor.execute(f"SELECT * FROM assessments{where_clause} ORDER BY timestamp DESC, rowid DESC LIMIT 1", params)
    latest_row = cursor.fetchone()
    latest_assessment = None
    if latest_row:
        resp_data = {}
        if latest_row["response_data_json"]:
            try:
                resp_data = json.loads(latest_row["response_data_json"])
            except Exception:
                pass

        input_data = {}
        if latest_row["input_data_json"]:
            try:
                input_data = json.loads(latest_row["input_data_json"])
            except Exception:
                pass

        fbs_val = input_data.get("fasting_blood_sugar") or (140 if input_data.get("fbs") == 1 else 95)

        latest_assessment = {
            "id": latest_row["id"],
            "patient_name": latest_row["patient_name"],
            "timestamp": latest_row["timestamp"],
            "risk_score": latest_row["risk_score"],
            "heart_health_score": latest_row["heart_health_score"],
            "probability_percentage": latest_row["probability_percentage"],
            "risk_level": latest_row["risk_level"],
            "bmi": resp_data.get("bmi", 24.2),
            "bmi_category": resp_data.get("bmi_category", "Normal"),
            "systolic_bp": latest_row["systolic_bp"],
            "diastolic_bp": latest_row["diastolic_bp"],
            "cholesterol": latest_row["cholesterol"],
            "ejection_fraction": latest_row["ejection_fraction"],
            "serum_creatinine": latest_row["serum_creatinine"],
            "fasting_blood_sugar": fbs_val,
            "smoking": latest_row["smoking"],
            "chest_pain": latest_row["chest_pain"],
            "top_risk_factors": resp_data.get("top_risk_factors", []),
            "protective_factors": resp_data.get("protective_factors", []),
            "recommendations": resp_data.get("recommendations", []),
            "summary_message": latest_row["summary_message"] or resp_data.get("summary_message", ""),
            "model_source": latest_row["model_source"]
        }

    # Recent timeline points for graph
    cursor.execute(f"SELECT id, timestamp, risk_score, heart_health_score, patient_name, risk_level FROM assessments{where_clause} ORDER BY timestamp ASC LIMIT 20", params)
    timeline_rows = cursor.fetchall()
    timeline = [
        {
            "id": r["id"],
            "date": r["timestamp"].split(" ")[0] if " " in r["timestamp"] else r["timestamp"],
            "risk_score": r["risk_score"],
            "health_score": r["heart_health_score"],
            "patient": r["patient_name"],
            "risk_level": r["risk_level"]
        }
        for r in timeline_rows
    ]

    conn.close()
    return {
        "has_assessments": True,
        "latest_assessment": latest_assessment,
        "total_assessments": total,
        "average_risk_score": round(avg_risk, 1) if avg_risk is not None else None,
        "average_health_score": round(avg_health, 1) if avg_health is not None else None,
        "risk_distribution": dist,
        "timeline": timeline
    }
