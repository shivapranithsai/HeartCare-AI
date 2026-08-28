import json
from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import PatientInput, PredictionResponse, SimulationInput
from app.ml.model_loader import ml_service
from app.db.database import get_db

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def run_prediction(data: PatientInput):
    try:
        # Run ML inference
        result = ml_service.predict(data)

        # Persist to MongoDB assessments collection
        db = get_db()
        
        sbp = data.systolic_bp or (150 if data.blood_pressure == "High" else 135 if data.blood_pressure == "Elevated" else 120)
        dbp = data.diastolic_bp or (95 if data.blood_pressure == "High" else 85 if data.blood_pressure == "Elevated" else 78)

        clean_user_email = data.user_email.strip().lower() if data.user_email and isinstance(data.user_email, str) and data.user_email.strip() else None

        input_dict = data.model_dump()
        result_dict = result.model_dump()

        assessment_doc = {
            "id": result.prediction_id,
            "user_email": clean_user_email,
            "patient_name": result.patient_name,
            "timestamp": result.timestamp,
            "age": data.age,
            "gender": data.gender,
            "risk_score": result.risk_score,
            "risk_level": result.risk_level,
            "probability_percentage": result.probability_percentage,
            "heart_health_score": result.heart_health_score,
            "systolic_bp": sbp,
            "diastolic_bp": dbp,
            "cholesterol": data.cholesterol,
            "ejection_fraction": data.ejection_fraction,
            "serum_creatinine": data.serum_creatinine,
            "smoking": data.smoking,
            "chest_pain": data.chest_pain,
            "model_source": result.model_source,
            "summary_message": result.summary_message,
            "input_data": input_dict,
            "input_data_json": json.dumps(input_dict),
            "response_data": result_dict,
            "response_data_json": json.dumps(result_dict)
        }

        db.assessments.insert_one(assessment_doc)

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
