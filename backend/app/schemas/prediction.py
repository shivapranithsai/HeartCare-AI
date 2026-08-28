from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PatientInput(BaseModel):
    name: Optional[str] = "Anonymous Patient"
    user_email: Optional[str] = None
    
    # 13 Standard Cleveland / UCI Dataset Features:
    # 1. age (Age in years)
    age: int = Field(default=50, ge=18, le=110, description="Age in years")
    
    # 2. sex (1 = Male, 0 = Female)
    sex: Optional[int] = Field(default=1, description="1 = Male, 0 = Female")
    gender: Optional[str] = Field(default="Male", description="Male, Female, Other")
    
    # 3. cp (Chest Pain Type: 0: Typical Angina, 1: Atypical Angina, 2: Non-anginal, 3: Asymptomatic)
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
    
    # 7. restecg (Resting ECG: 0: Normal, 1: ST-T wave abnormality, 2: Left ventricular hypertrophy)
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
    
    # 11. slope (Slope of peak exercise ST segment: 0: Upsloping, 1: Flat, 2: Downsloping)
    slope: Optional[int] = Field(default=0, ge=0, le=2, description="Slope of ST segment (0-2)")
    st_slope: Optional[str] = Field(default="Upsloping")
    
    # 12. ca (Number of major vessels (0-3) colored by flourosopy)
    ca: Optional[int] = Field(default=0, ge=0, le=3, description="Number of major vessels (0-3)")
    
    # 13. thal (Thalassemia defect: 1 = Normal, 2 = Fixed defect, 3 = Reversible defect / 3, 6, 7 in raw UCI)
    thal: Optional[int] = Field(default=1, ge=1, le=7, description="Thalassemia (1: Normal, 2: Fixed, 3: Reversible)")
    
    # Additional Complementary Clinical Biomarkers
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

    def get_cleveland_feature_vector(self) -> List[float]:
        """
        Extracts the exact 13 features matching:
        [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        """
        # 1. age
        v_age = float(self.age)
        
        # 2. sex (1 = male, 0 = female)
        v_sex = 1.0 if (self.sex == 1 or (self.gender and self.gender.lower() == "male")) else 0.0
        
        # 3. cp (0-3)
        if self.cp is not None:
            v_cp = float(self.cp)
        elif self.chest_pain:
            cp_lower = self.chest_pain.lower()
            if "typical" in cp_lower or "severe" in cp_lower:
                v_cp = 0.0
            elif "atypical" in cp_lower or "moderate" in cp_lower:
                v_cp = 1.0
            elif "non-anginal" in cp_lower or "mild" in cp_lower:
                v_cp = 2.0
            else:
                v_cp = 3.0 # asymptomatic
        else:
            v_cp = 0.0

        # 4. trestbps
        v_trestbps = float(self.trestbps or self.systolic_bp or 125)

        # 5. chol
        v_chol = float(self.chol or self.cholesterol or 195)

        # 6. fbs (1 if >120 mg/dl, else 0)
        if self.fbs is not None:
            v_fbs = float(self.fbs)
        elif self.fasting_blood_sugar:
            v_fbs = 1.0 if self.fasting_blood_sugar > 120 else 0.0
        else:
            v_fbs = 0.0

        # 7. restecg (0: normal, 1: ST-T abnormality, 2: LV hypertrophy)
        if self.restecg is not None:
            v_restecg = float(self.restecg)
        elif self.resting_ecg:
            ecg_lower = self.resting_ecg.lower()
            if "hypertrophy" in ecg_lower:
                v_restecg = 2.0
            elif "st-t" in ecg_lower or "abnormality" in ecg_lower:
                v_restecg = 1.0
            else:
                v_restecg = 0.0
        else:
            v_restecg = 0.0

        # 8. thalach (Max Heart Rate)
        v_thalach = float(self.thalach or (220 - self.age) * 0.85 if self.heart_rate else 150)

        # 9. exang (1 = Yes, 0 = No)
        if self.exang is not None:
            v_exang = float(self.exang)
        elif self.exercise_angina:
            v_exang = 1.0 if self.exercise_angina.lower() == "yes" else 0.0
        else:
            v_exang = 0.0

        # 10. oldpeak (ST depression)
        v_oldpeak = float(self.oldpeak if self.oldpeak is not None else (self.st_depression or 0.0))

        # 11. slope (0: upsloping, 1: flat, 2: downsloping)
        if self.slope is not None:
            v_slope = float(self.slope)
        elif self.st_slope:
            slope_lower = self.st_slope.lower()
            if "flat" in slope_lower:
                v_slope = 1.0
            elif "down" in slope_lower:
                v_slope = 2.0
            else:
                v_slope = 0.0
        else:
            v_slope = 0.0

        # 12. ca (0-3 major vessels)
        v_ca = float(self.ca or 0)

        # 13. thal (1: normal, 2: fixed defect, 3: reversible defect)
        v_thal = float(self.thal if self.thal in [1, 2, 3, 6, 7] else 1.0)

        return [v_age, v_sex, v_cp, v_trestbps, v_chol, v_fbs, v_restecg, v_thalach, v_exang, v_oldpeak, v_slope, v_ca, v_thal]

class FeatureImpact(BaseModel):
    feature: str
    label: str
    value: Any
    impact_score: float
    direction: str
    category: str
    severity: str
    explanation: str

class Recommendation(BaseModel):
    category: str
    title: str
    description: str
    urgency: str
    icon: str

class PredictionResponse(BaseModel):
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
    base_input: PatientInput
    modified_params: Dict[str, Any]
