import os
import uuid
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

from app.core.config import MODELS_DIR
from app.schemas.prediction import PatientInput, PredictionResponse
from app.ml.clinical_engine import run_clinical_heuristic_model
from app.ml.recommendations import generate_recommendations

# ==============================================================================
# LIGHTGBM / SCIKIT-LEARN TRAINED MODEL INTEGRATION
# ==============================================================================
# Model: best_lgbm_3m_model.joblib
# Features: [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
# Categories:
#   - sex: [0, 1]
#   - cp: [1, 2, 3, 4]
#   - fbs: [0, 1]
#   - restecg: [0, 1, 2]
#   - exang: [0, 1]
#   - slope: [1, 2, 3]
#   - ca: [0.0, 1.0, 2.0, 3.0]
#   - thal: [3.0, 6.0, 7.0]
# ==============================================================================

CUSTOM_MODEL_FILENAMES = [
    "best_lgbm_3m_model.joblib",
    "heart_model.joblib",
    "heart_model.pkl",
    "model.joblib",
    "model.pkl"
]

class MLModelService:
    def __init__(self):
        self.model = None
        self.is_custom_loaded = False
        self.loaded_model_name = "AHA/Cleveland Clinical AI Heuristic Engine"
        self.cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']
        self.cat_categories = None
        self._try_load_custom_model()

    def _try_load_custom_model(self):
        """Scans saved_models/ and loads custom trained model."""
        for fname in CUSTOM_MODEL_FILENAMES:
            target_path = MODELS_DIR / fname
            if target_path.exists():
                try:
                    import joblib
                    self.model = joblib.load(target_path)
                    self.is_custom_loaded = True
                    self.loaded_model_name = f"Trained LightGBM Classifier ({fname})"
                    
                    # Check if LightGBM has booster categoricals
                    if hasattr(self.model, "_Booster") and hasattr(self.model._Booster, "pandas_categorical"):
                        self.cat_categories = self.model._Booster.pandas_categorical
                        print(f"[ML Service] Successfully loaded trained LightGBM model from {fname} with {len(self.cat_categories)} categorical feature encodings.")
                    else:
                        print(f"[ML Service] Successfully loaded model from {fname}.")
                    return
                except Exception as e:
                    print(f"[ML Service] Notice: Error loading {fname} ({e}). Using Clinical Engine.")
                    self.is_custom_loaded = False
        
        self.is_custom_loaded = False
        print("[ML Service] Custom model not found. Running Clinical AI Engine.")

    def _prepare_lgbm_dataframe(self, data: PatientInput) -> pd.DataFrame:
        """
        Converts PatientInput to a pandas DataFrame formatted with exact LightGBM categorical types.
        """
        # Map sex: 0 = Female, 1 = Male
        v_sex = 1 if (data.sex == 1 or (data.gender and data.gender.lower() == "male")) else 0

        # Map cp: Model trained with [1, 2, 3, 4]
        # (1 = Typical Angina, 2 = Atypical Angina, 3 = Non-anginal, 4 = Asymptomatic)
        if data.cp is not None and data.cp in [0, 1, 2, 3]:
            v_cp = data.cp + 1  # 0->1, 1->2, 2->3, 3->4
        elif data.chest_pain:
            cp_l = data.chest_pain.lower()
            if "typical" in cp_l or "severe" in cp_l:
                v_cp = 1
            elif "atypical" in cp_l or "moderate" in cp_l:
                v_cp = 2
            elif "non-anginal" in cp_l or "mild" in cp_l:
                v_cp = 3
            else:
                v_cp = 4
        else:
            v_cp = 1

        # trestbps
        v_trestbps = float(data.trestbps or data.systolic_bp or 125)

        # chol
        v_chol = float(data.chol or data.cholesterol or 195)

        # fbs (0/1)
        if data.fbs is not None:
            v_fbs = 1 if data.fbs == 1 else 0
        elif data.fasting_blood_sugar:
            v_fbs = 1 if data.fasting_blood_sugar > 120 else 0
        else:
            v_fbs = 0

        # restecg (0, 1, 2)
        if data.restecg is not None and data.restecg in [0, 1, 2]:
            v_restecg = data.restecg
        elif data.resting_ecg:
            recg_l = data.resting_ecg.lower()
            if "hypertrophy" in recg_l:
                v_restecg = 2
            elif "st-t" in recg_l or "abnormality" in recg_l:
                v_restecg = 1
            else:
                v_restecg = 0
        else:
            v_restecg = 0

        # thalach (Max HR)
        v_thalach = float(data.thalach or ((220 - data.age) * 0.85 if data.heart_rate else 150))

        # exang (0/1)
        if data.exang is not None:
            v_exang = 1 if data.exang == 1 else 0
        elif data.exercise_angina:
            v_exang = 1 if data.exercise_angina.lower() == "yes" else 0
        else:
            v_exang = 0

        # oldpeak (ST depression)
        v_oldpeak = float(data.oldpeak if data.oldpeak is not None else (data.st_depression or 0.0))

        # slope: Model trained with [1, 2, 3] (1 = Upsloping, 2 = Flat, 3 = Downsloping)
        if data.slope is not None and data.slope in [0, 1, 2]:
            v_slope = data.slope + 1  # 0->1, 1->2, 2->3
        elif data.st_slope:
            slope_l = data.st_slope.lower()
            if "flat" in slope_l:
                v_slope = 2
            elif "down" in slope_l:
                v_slope = 3
            else:
                v_slope = 1
        else:
            v_slope = 1

        # ca (0.0, 1.0, 2.0, 3.0)
        v_ca = float(data.ca if data.ca in [0, 1, 2, 3] else 0.0)

        # thal: Model trained with [3.0, 6.0, 7.0] (3.0 = Normal, 6.0 = Fixed defect, 7.0 = Reversible defect)
        if data.thal in [1, 3, 3.0]:
            v_thal = 3.0
        elif data.thal in [2, 6, 6.0]:
            v_thal = 6.0
        elif data.thal in [3, 7, 7.0]:
            v_thal = 7.0
        else:
            v_thal = 3.0

        row_dict = {
            'age': float(data.age),
            'sex': v_sex,
            'cp': v_cp,
            'trestbps': v_trestbps,
            'chol': v_chol,
            'fbs': v_fbs,
            'restecg': v_restecg,
            'thalach': v_thalach,
            'exang': v_exang,
            'oldpeak': v_oldpeak,
            'slope': v_slope,
            'ca': v_ca,
            'thal': v_thal
        }

        df = pd.DataFrame([row_dict])

        # Convert to categorical matching the Booster's exact categories
        if self.cat_categories and len(self.cat_categories) == len(self.cat_cols):
            for col, cat_vals in zip(self.cat_cols, self.cat_categories):
                df[col] = pd.Categorical(df[col], categories=cat_vals)

        return df

    def predict(self, data: PatientInput) -> PredictionResponse:
        """
        Executes inference using the uploaded LightGBM model.
        """
        # Baseline explainability from clinical engine
        analysis = run_clinical_heuristic_model(data)

        # Run LightGBM inference if custom model is loaded
        if self.is_custom_loaded and self.model is not None:
            try:
                df = self._prepare_lgbm_dataframe(data)
                
                # Multi-class probabilities: [P(Stage 0: Healthy), P(Stage 1), P(Stage 2), P(Stage 3), P(Stage 4)]
                prob_dist = self.model.predict_proba(df)[0]
                pred_class = int(self.model.predict(df)[0])
                
                # Disease probability is 1.0 - P(Healthy)
                disease_prob = float(1.0 - prob_dist[0])
                disease_prob = max(0.02, min(0.98, disease_prob))
                
                risk_score = int(round(disease_prob * 100))
                prob_pct = round(disease_prob * 100, 1)

                analysis["risk_score"] = risk_score
                analysis["probability_percentage"] = prob_pct
                analysis["heart_health_score"] = max(0, 100 - risk_score)
                
                # Risk level mapping incorporating predicted disease stage
                if pred_class == 0 and risk_score < 30:
                    analysis["risk_level"] = "Low Risk (Normal Baseline)"
                    analysis["urgency_level"] = "low"
                elif pred_class == 1 or (risk_score >= 30 and risk_score < 55):
                    analysis["risk_level"] = "Moderate Risk (Stage 1 Indicator)"
                    analysis["urgency_level"] = "medium"
                elif pred_class == 2 or (risk_score >= 55 and risk_score < 75):
                    analysis["risk_level"] = "High Risk (Stage 2 Marker)"
                    analysis["urgency_level"] = "high"
                else:
                    analysis["risk_level"] = f"Critical Risk (Stage {max(pred_class, 3)} Severity)"
                    analysis["urgency_level"] = "emergency"

                analysis["confidence_interval"] = {
                    "lower": round(max(0.0, prob_pct - 4.5), 1),
                    "upper": round(min(100.0, prob_pct + 4.5), 1)
                }
                analysis["model_source"] = self.loaded_model_name
                
            except Exception as e:
                print(f"[ML Service] LGBM inference notice ({e}). Falling back to Clinical AI Engine.")
                analysis["model_source"] = "AHA/Cleveland Clinical AI Heuristic Engine"

        recommendations = generate_recommendations(data, analysis)
        pred_id = f"PRED-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        return PredictionResponse(
            prediction_id=pred_id,
            timestamp=timestamp,
            patient_name=data.name or "Anonymous Patient",
            risk_score=analysis["risk_score"],
            risk_level=analysis["risk_level"],
            probability_percentage=analysis["probability_percentage"],
            confidence_interval=analysis["confidence_interval"],
            heart_health_score=analysis["heart_health_score"],
            model_source=analysis.get("model_source", self.loaded_model_name),
            bmi=analysis["bmi"],
            bmi_category=analysis["bmi_category"],
            top_risk_factors=analysis["top_risk_factors"],
            protective_factors=analysis["protective_factors"],
            all_factor_impacts=analysis["all_factor_impacts"],
            recommendations=recommendations,
            urgency_level=analysis["urgency_level"],
            summary_message=analysis["summary_message"]
        )

ml_service = MLModelService()
