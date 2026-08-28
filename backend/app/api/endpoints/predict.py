import json
from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import PatientInput, PredictionResponse, SimulationInput
from app.ml.model_loader import ml_service
from app.db.database import get_db_connection

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def run_prediction(data: PatientInput):
    try:
        # Run ML inference
        result = ml_service.predict(data)

        # Persist to SQLite DB
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sbp = data.systolic_bp or (150 if data.blood_pressure == "High" else 135 if data.blood_pressure == "Elevated" else 120)
        dbp = data.diastolic_bp or (95 if data.blood_pressure == "High" else 85 if data.blood_pressure == "Elevated" else 78)

        cursor.execute("""
        INSERT INTO assessments (
            id, user_email, patient_name, timestamp, age, gender, risk_score, risk_level, probability_percentage,
            heart_health_score, systolic_bp, diastolic_bp, cholesterol, ejection_fraction, serum_creatinine,
            smoking, chest_pain, model_source, summary_message, input_data_json, response_data_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.prediction_id,
            data.user_email,
            result.patient_name,
            result.timestamp,
            data.age,
            data.gender,
            result.risk_score,
            result.risk_level,
            result.probability_percentage,
            result.heart_health_score,
            sbp,
            dbp,
            data.cholesterol,
            data.ejection_fraction,
            data.serum_creatinine,
            data.smoking,
            data.chest_pain,
            result.model_source,
            result.summary_message,
            json.dumps(data.model_dump()),
            json.dumps(result.model_dump())
        ))
        conn.commit()
        conn.close()

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction computation error: {str(e)}"
        )

@router.post("/simulate")
def run_what_if_simulation(sim_data: SimulationInput):
    """
    Simulates changes to health parameters to demonstrate how interventions
    (e.g., lowering blood pressure, stopping smoking, exercising more) impact risk.
    """
    try:
        base = sim_data.base_input.model_dump()
        base_result = ml_service.predict(sim_data.base_input)
        
        # Apply modified parameters
        for k, v in sim_data.modified_params.items():
            if hasattr(sim_data.base_input, k):
                base[k] = v
                
        mod_input = PatientInput(**base)
        simulated_result = ml_service.predict(mod_input)
        
        delta_score = simulated_result.risk_score - base_result.risk_score
        delta_prob = round(simulated_result.probability_percentage - base_result.probability_percentage, 1)

        return {
            "baseline": {
                "risk_score": base_result.risk_score,
                "probability": base_result.probability_percentage,
                "risk_level": base_result.risk_level,
                "heart_health_score": base_result.heart_health_score
            },
            "simulated": {
                "risk_score": simulated_result.risk_score,
                "probability": simulated_result.probability_percentage,
                "risk_level": simulated_result.risk_level,
                "heart_health_score": simulated_result.heart_health_score
            },
            "delta": {
                "risk_score_diff": delta_score,
                "probability_diff": delta_prob,
                "status": "improved" if delta_score < 0 else "worsened" if delta_score > 0 else "unchanged"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation error: {str(e)}"
        )
