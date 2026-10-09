from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Any

class PatientInput(BaseModel):
    """
    Patient health input schema.
    Supports standard 13 UCI Cleveland Heart Disease features
    as well as complementary clinical biomarkers (EF, Serum Creatinine, etc.).
    """
    @model_validator(mode="before")
    @classmethod
    def sync_feature_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # 1. Blood Pressure: trestbps <-> systolic_bp
            if "systolic_bp" in data and ("trestbps" not in data or data["trestbps"] is None):
                data["trestbps"] = data["systolic_bp"]
            elif "trestbps" in data and ("systolic_bp" not in data or data["systolic_bp"] is None):
                data["systolic_bp"] = data["trestbps"]

            # 2. Cholesterol: chol <-> cholesterol
            if "cholesterol" in data and ("chol" not in data or data["chol"] is None):
                data["chol"] = data["cholesterol"]
            elif "chol" in data and ("cholesterol" not in data or data["cholesterol"] is None):
                data["cholesterol"] = data["chol"]

            # 3. Heart Rate: thalach <-> heart_rate
            if "thalach" in data and ("heart_rate" not in data or data["heart_rate"] is None):
                data["heart_rate"] = data["thalach"]
            elif "heart_rate" in data and ("thalach" not in data or data["thalach"] is None):
                data["thalach"] = data["heart_rate"]

            # 4. ST Depression: oldpeak <-> st_depression
            if "st_depression" in data and ("oldpeak" not in data or data["oldpeak"] is None):
                data["oldpeak"] = data["st_depression"]
            elif "oldpeak" in data and ("st_depression" not in data or data["st_depression"] is None):
                data["st_depression"] = data["oldpeak"]

            # 5. Fasting Blood Sugar: fbs <-> fasting_blood_sugar
            if "fasting_blood_sugar" in data and ("fbs" not in data or data["fbs"] is None):
                data["fbs"] = 1 if data["fasting_blood_sugar"] > 120 else 0
            elif "fbs" in data and ("fasting_blood_sugar" not in data or data["fasting_blood_sugar"] is None):
                data["fasting_blood_sugar"] = 140 if data["fbs"] == 1 else 95

            # 6. Chest pain
            cp_map = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-anginal", 3: "Asymptomatic"}
            if "cp" in data and ("chest_pain" not in data or not data["chest_pain"]):
                data["chest_pain"] = cp_map.get(data["cp"], "None")
        return data

    name: Optional[str] = "Anonymous Patient"
    user_email: Optional[str] = None

    # 13 Standard Cleveland / UCI Dataset Features:
    # 1. age (years)
    age: int = Field(default=50, ge=18, le=110, description="Age in years")

    # 2. sex (1 = Male, 0 = Female)
    sex: Optional[int] = Field(default=1, description="1 = Male, 0 = Female")
    gender: Optional[str] = Field(default="Male", description="Male or Female")

    # 3. cp (Chest Pain Type: 0 = Typical Angina, 1 = Atypical Angina, 2 = Non-anginal, 3 = Asymptomatic)
    cp: Optional[int] = Field(default=0, ge=0, le=3, description="Chest Pain Type (0-3)")
    chest_pain: Optional[str] = Field(default="None", description="Text description of chest pain")

    # 4. trestbps (Resting Blood Pressure in mmHg)
    trestbps: Optional[int] = Field(default=125, ge=70, le=240, description="Resting Blood Pressure (mmHg)")
    systolic_bp: Optional[int] = Field(default=125, ge=70, le=240)
    diastolic_bp: Optional[int] = Field(default=80, ge=40, le=140)

    # 5. chol (Serum Cholesterol in mg/dL)
    chol: Optional[int] = Field(default=195, ge=90, le=600, description="Serum Cholesterol (mg/dL)")
    cholesterol: Optional[int] = Field(default=195)

    # 6. fbs (Fasting Blood Sugar > 120 mg/dL: 1 = True, 0 = False)
    fbs: Optional[int] = Field(default=0, ge=0, le=1, description="Fasting Blood Sugar > 120 mg/dL (1/0)")
    fasting_blood_sugar: Optional[int] = Field(default=95)

    # 7. restecg (Resting ECG: 0 = Normal, 1 = ST-T wave abnormality, 2 = Left ventricular hypertrophy)
    restecg: Optional[int] = Field(default=0, ge=0, le=2, description="Resting ECG (0-2)")
    resting_ecg: Optional[str] = Field(default="Normal")

    # 8. thalach (Maximum Heart Rate achieved in BPM)
    thalach: Optional[int] = Field(default=150, ge=50, le=240, description="Max Heart Rate (BPM)")
    heart_rate: Optional[int] = Field(default=75)

    # 9. exang (Exercise Induced Angina: 1 = Yes, 0 = No)
    exang: Optional[int] = Field(default=0, ge=0, le=1, description="Exercise Induced Angina (1/0)")
    exercise_angina: Optional[str] = Field(default="No")

    # 10. oldpeak (ST depression induced by exercise relative to rest)
    oldpeak: Optional[float] = Field(default=0.0, ge=0.0, le=10.0, description="ST depression (Oldpeak)")
    st_depression: Optional[float] = Field(default=0.0)

    # 11. slope (Slope of peak exercise ST segment: 0 = Upsloping, 1 = Flat, 2 = Downsloping)
    slope: Optional[int] = Field(default=0, ge=0, le=2, description="Slope of ST segment (0-2)")
    st_slope: Optional[str] = Field(default="Upsloping")

    # 12. ca (Number of major vessels (0-3) colored by fluoroscopy)
    ca: Optional[int] = Field(default=0, ge=0, le=3, description="Number of major vessels (0-3)")

    # 13. thal (Thalassemia defect: 1 = Normal, 2 = Fixed defect, 3 = Reversible defect)
    thal: Optional[int] = Field(default=1, ge=1, le=7, description="Thalassemia defect")

    # Complementary Clinical Biomarkers
    ejection_fraction: Optional[int] = Field(default=55, ge=10, le=80, description="Ejection Fraction (%)")
    serum_creatinine: Optional[float] = Field(default=1.0, ge=0.2, le=12.0, description="Serum Creatinine (mg/dL)")
    height: Optional[float] = Field(default=170.0)
    weight: Optional[float] = Field(default=70.0)
    smoking: Optional[str] = Field(default="Never")
    physical_activity: Optional[str] = Field(default="Moderate")
    exercise_days: Optional[str] = Field(default="2-3 days")
    sleep_hours: Optional[str] = Field(default="7-9 hours")
    stress_level: Optional[str] = Field(default="Medium")
    previous_heart_condition: Optional[str] = Field(default="No")
    diabetes: Optional[str] = Field(default="No")
    blood_pressure: Optional[str] = Field(default="Normal")

class FeatureImpact(BaseModel):
    """Represents the attribution of an individual feature to cardiovascular risk."""
    feature: str
    label: str
    value: Any
    impact_score: float
    direction: str
    category: str
    severity: str
    explanation: str

class Recommendation(BaseModel):
    """Represents a clinical lifestyle or medical recommendation."""
    category: str
    title: str
    description: str
    urgency: str
    icon: str

class PredictionResponse(BaseModel):
    """Complete prediction output returned to the frontend."""
    prediction_id: str
    timestamp: str
    patient_name: str
    risk_score: int
    risk_level: str
    probability_percentage: float
    confidence_interval: Dict[str, float]
    heart_health_score: int
    model_source: str
    bmi: float
    bmi_category: str
    top_risk_factors: List[FeatureImpact]
    protective_factors: List[FeatureImpact]
    all_factor_impacts: List[FeatureImpact]
    recommendations: List[Recommendation]
    urgency_level: str
    summary_message: str

class SimulationInput(BaseModel):
    """Input for real-time What-If scenario simulations."""
    base_input: PatientInput
    modified_params: Dict[str, Any]
