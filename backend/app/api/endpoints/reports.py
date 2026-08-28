import json
from fastapi import APIRouter, HTTPException
from app.db.database import get_db_connection

router = APIRouter()

@router.get("/{id}")
def generate_clinical_report(id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assessments WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Assessment not found for report generation")

    resp_data = {}
    if row["response_data_json"]:
        try:
            resp_data = json.loads(row["response_data_json"])
        except Exception:
            pass

    return {
        "report_id": f"REP-{row['id']}",
        "assessment_id": row["id"],
        "generated_at": row["timestamp"],
        "patient": {
            "name": row["patient_name"],
            "age": row["age"],
            "gender": row["gender"],
            "blood_pressure": f"{row['systolic_bp']}/{row['diastolic_bp']} mmHg" if row['systolic_bp'] else "N/A",
            "cholesterol": f"{row['cholesterol']} mg/dL" if row['cholesterol'] else "N/A",
            "ejection_fraction": f"{row['ejection_fraction']}%" if row['ejection_fraction'] else "N/A",
            "serum_creatinine": f"{row['serum_creatinine']} mg/dL" if row['serum_creatinine'] else "N/A",
            "smoking_status": row["smoking"] or "N/A",
            "chest_pain": row["chest_pain"] or "None"
        },
        "clinical_summary": {
            "risk_score": row["risk_score"],
            "risk_level": row["risk_level"],
            "heart_health_score": row["heart_health_score"],
            "model_source": row["model_source"],
            "summary_statement": row["summary_message"]
        },
        "full_analysis": resp_data
    }
