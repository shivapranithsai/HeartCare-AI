import json
from fastapi import APIRouter, HTTPException
from app.db.database import get_db

router = APIRouter()

@router.get("/{id}")
def generate_clinical_report(id: str):
    db = get_db()
    row = db.assessments.find_one({"id": id})

    if not row:
        raise HTTPException(status_code=404, detail="Assessment not found for report generation")

    resp_data = row.get("response_data") or {}
    if not resp_data and row.get("response_data_json"):
        try:
            resp_data = json.loads(row["response_data_json"])
        except Exception:
            pass

    sbp = row.get("systolic_bp")
    dbp = row.get("diastolic_bp")
    bp_str = f"{sbp}/{dbp} mmHg" if sbp and dbp else f"{sbp} mmHg" if sbp else "N/A"

    return {
        "report_id": f"REP-{row.get('id')}",
        "assessment_id": row.get("id"),
        "generated_at": row.get("timestamp"),
        "patient": {
            "name": row.get("patient_name"),
            "age": row.get("age"),
            "gender": row.get("gender"),
            "blood_pressure": bp_str,
            "cholesterol": f"{row.get('cholesterol')} mg/dL" if row.get("cholesterol") else "N/A",
            "ejection_fraction": f"{row.get('ejection_fraction')}%" if row.get("ejection_fraction") else "N/A",
            "serum_creatinine": f"{row.get('serum_creatinine')} mg/dL" if row.get("serum_creatinine") else "N/A",
            "smoking_status": row.get("smoking") or "N/A",
            "chest_pain": row.get("chest_pain") or "None"
        },
        "clinical_summary": {
            "risk_score": row.get("risk_score"),
            "risk_level": row.get("risk_level"),
            "heart_health_score": row.get("heart_health_score"),
            "model_source": row.get("model_source"),
            "summary_statement": row.get("summary_message")
        },
        "full_analysis": resp_data
    }
