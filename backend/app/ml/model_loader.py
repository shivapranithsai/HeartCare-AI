import uuid
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import joblib

from app.core.config import MODELS_DIR
from app.schemas.prediction import PatientInput, PredictionResponse
from app.ml.clinical_engine import run_clinical_heuristic_model
from app.ml.recommendations import generate_recommendations

MODEL_FILENAME = "best_lgbm_3m_model.joblib"

class MLModelService:
    """
    Service responsible for loading the trained LightGBM heart disease model
    and executing multi-class inference.
    """
    def __init__(self):
        self.model = None
        self.is_custom_loaded = False
        self.loaded_model_name = "Clinical AI Heuristic Engine"
        self.cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']
        self.cat_categories = None
        self._load_model()

    def _load_model(self):
        """Loads the pre-trained LightGBM joblib model from saved_models directory."""
        model_path = MODELS_DIR / MODEL_FILENAME
        if model_path.exists():
            try:
                self.model = joblib.load(model_path)
                self.is_custom_loaded = True
                self.loaded_model_name = f"Trained LightGBM Classifier ({MODEL_FILENAME})"

                # If the LightGBM Booster preserved pandas categorical metadata, store it
                if hasattr(self.model, "_Booster") and hasattr(self.model._Booster, "pandas_categorical"):
                    self.cat_categories = self.model._Booster.pandas_categorical
                    print(f"[ML Service] Loaded LightGBM model with {len(self.cat_categories)} categorical feature encodings.")
                else:
                    print(f"[ML Service] Loaded model from {MODEL_FILENAME}.")
                return
            except Exception as e:
                print(f"[ML Service] Error loading model ({e}). Using heuristic fallback.")

        self.is_custom_loaded = False
        print("[ML Service] Custom model not found. Using Clinical AI Engine.")

    def _prepare_lgbm_dataframe(self, data: PatientInput) -> pd.DataFrame:
        """
        Transforms PatientInput into a single-row pandas DataFrame
        matching the exact 13 Cleveland features and categorical encodings
        used during model training.
        """
        # 1. Sex: 1 = Male, 0 = Female
        sex_val = 1 if (data.sex == 1 or (data.gender and data.gender.lower() == "male")) else 0

        # 2. Chest pain type (cp): Model trained with [1, 2, 3, 4]
        # (1: Typical Angina, 2: Atypical Angina, 3: Non-anginal, 4: Asymptomatic)
        if data.cp is not None and data.cp in [0, 1, 2, 3]:
            cp_val = data.cp + 1
        elif data.chest_pain:
            cp_str = data.chest_pain.lower()
            if "typical" in cp_str or "severe" in cp_str:
                cp_val = 1
            elif "atypical" in cp_str or "moderate" in cp_str:
                cp_val = 2
            elif "non-anginal" in cp_str or "mild" in cp_str:
                cp_val = 3
            else:
                cp_val = 4
        else:
            cp_val = 1

        # 3. Resting Blood Pressure (trestbps)
        trestbps_val = float(data.trestbps or data.systolic_bp or 125)

        # 4. Serum Cholesterol (chol)
        chol_val = float(data.chol or data.cholesterol or 195)

        # 5. Fasting Blood Sugar > 120 mg/dL (fbs: 0 or 1)
        if data.fbs is not None:
            fbs_val = 1 if data.fbs == 1 else 0
        elif data.fasting_blood_sugar:
            fbs_val = 1 if data.fasting_blood_sugar > 120 else 0
        else:
            fbs_val = 0

        # 6. Resting ECG (restecg: 0, 1, or 2)
        if data.restecg is not None and data.restecg in [0, 1, 2]:
            restecg_val = data.restecg
        elif data.resting_ecg:
            ecg_str = data.resting_ecg.lower()
            if "hypertrophy" in ecg_str:
                restecg_val = 2
            elif "st-t" in ecg_str or "abnormality" in ecg_str:
                restecg_val = 1
            else:
                restecg_val = 0
        else:
            restecg_val = 0

        # 7. Maximum Heart Rate (thalach)
        # Bounded by maximum predicted exercise heart rate (220 - age)
        max_physio_hr = max(80.0, 220.0 - float(data.age))
        if data.thalach is not None:
            raw_thalach = float(data.thalach)
        elif data.heart_rate:
            raw_thalach = float(max_physio_hr * 0.85)
        else:
            raw_thalach = float(max_physio_hr * 0.85)
        # Cap thalach so it does not exceed physiologically possible max heart rate for age
        thalach_val = min(raw_thalach, max_physio_hr * 0.98)

        # 8. Exercise Induced Angina (exang: 0 or 1)
        if data.exang is not None:
            exang_val = 1 if data.exang == 1 else 0
        elif data.exercise_angina:
            exang_val = 1 if data.exercise_angina.lower() == "yes" else 0
        else:
            exang_val = 0

        # 9. ST depression (oldpeak)
        oldpeak_val = float(data.oldpeak if data.oldpeak is not None else (data.st_depression or 0.0))

        # 10. Slope of ST segment (slope: 1 = Upsloping, 2 = Flat, 3 = Downsloping)
        if data.slope is not None and data.slope in [0, 1, 2]:
            slope_val = data.slope + 1
        elif data.st_slope:
            slope_str = data.st_slope.lower()
            if "flat" in slope_str:
                slope_val = 2
            elif "down" in slope_str:
                slope_val = 3
            else:
                slope_val = 1
        else:
            slope_val = 1

        # 11. Major vessels (ca: 0.0 to 3.0)
        ca_val = float(data.ca if data.ca in [0, 1, 2, 3] else 0.0)

        # 12. Thalassemia (thal: 3.0 = Normal, 6.0 = Fixed defect, 7.0 = Reversible defect)
        if data.thal in [1, 3, 3.0]:
            thal_val = 3.0
        elif data.thal in [2, 6, 6.0]:
            thal_val = 6.0
        elif data.thal in [3, 7, 7.0]:
            thal_val = 7.0
        else:
            thal_val = 3.0

        features_dict = {
            'age': float(data.age),
            'sex': sex_val,
            'cp': cp_val,
            'trestbps': trestbps_val,
            'chol': chol_val,
            'fbs': fbs_val,
            'restecg': restecg_val,
            'thalach': thalach_val,
            'exang': exang_val,
            'oldpeak': oldpeak_val,
            'slope': slope_val,
            'ca': ca_val,
            'thal': thal_val
        }

        df = pd.DataFrame([features_dict])

        # Apply categorical type specifications matching the LightGBM booster
        if self.cat_categories and len(self.cat_categories) == len(self.cat_cols):
            for col, categories in zip(self.cat_cols, self.cat_categories):
                df[col] = pd.Categorical(df[col], categories=categories)

        return df

    def predict(self, data: PatientInput) -> PredictionResponse:
        """
        Executes inference:
        1. Runs heuristic engine for clinical biomarker attribution (explainability).
        2. Runs trained LightGBM model for disease stage & probability estimation.
        3. Generates personalized recommendations.
        """
        # Baseline explainability factors from clinical engine
        analysis = run_clinical_heuristic_model(data)

        # Run LightGBM inference if loaded
        if self.is_custom_loaded and self.model is not None:
            try:
                df = self._prepare_lgbm_dataframe(data)

                # Predict probabilities across stages: [P(Stage 0: Healthy), P(Stage 1), P(Stage 2), P(Stage 3), P(Stage 4)]
                probabilities = self.model.predict_proba(df)[0]
                predicted_class = int(self.model.predict(df)[0])

                # Risk probability is 1.0 - P(Healthy)
                raw_disease_prob = float(1.0 - probabilities[0])

                # Clinical Age Calibration Layer:
                # The Cleveland cohort has referral bias where young catheterized patients had severe
                # early disease and older survivors had clean arteries, causing deep GBDTs to invert age splits.
                # In accordance with ACC/AHA & Framingham guidelines, baseline cardiovascular risk increases
                # monotonically with age. We calibrate the probability using age baseline relative to age 50:
                age_val = float(data.age)
                age_adjustment = (age_val - 50.0) * 0.0045
                disease_prob = max(0.03, min(0.98, raw_disease_prob + age_adjustment))

                risk_score = int(round(disease_prob * 100))
                prob_pct = round(disease_prob * 100, 1)

                analysis["risk_score"] = risk_score
                analysis["probability_percentage"] = prob_pct
                analysis["heart_health_score"] = max(0, 100 - risk_score)

                # Classify risk level incorporating predicted disease stage
                if predicted_class == 0 and risk_score < 30:
                    analysis["risk_level"] = "Low Risk (Normal Baseline)"
                    analysis["urgency_level"] = "low"
                elif predicted_class == 1 or (30 <= risk_score < 55):
                    analysis["risk_level"] = "Moderate Risk (Stage 1 Indicator)"
                    analysis["urgency_level"] = "medium"
                elif predicted_class == 2 or (55 <= risk_score < 75):
                    analysis["risk_level"] = "High Risk (Stage 2 Marker)"
                    analysis["urgency_level"] = "high"
                else:
                    analysis["risk_level"] = f"Critical Risk (Stage {max(predicted_class, 3)} Severity)"
                    analysis["urgency_level"] = "emergency"

                analysis["confidence_interval"] = {
                    "lower": round(max(0.0, prob_pct - 4.5), 1),
                    "upper": round(min(100.0, prob_pct + 4.5), 1)
                }
                analysis["model_source"] = self.loaded_model_name

            except Exception as e:
                print(f"[ML Service] Inference fallback to heuristic engine: {e}")
                analysis["model_source"] = "Clinical AI Heuristic Engine"

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
