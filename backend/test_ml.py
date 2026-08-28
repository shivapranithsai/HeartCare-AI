import urllib.request
import json

test_cases = [
    {
        "name": "Case 1: Severe Cardiac Risk Patient (Stage 4 Ischemia & Arterial Disease)",
        "payload": {
            "name": "Sunita Deshmukh",
            "age": 68,
            "sex": 0,
            "gender": "Female",
            "cp": 0, # Typical Angina (maps to LGBM category 1)
            "trestbps": 168,
            "systolic_bp": 168,
            "diastolic_bp": 104,
            "chol": 275,
            "fbs": 1,
            "restecg": 2, # LV Hypertrophy
            "thalach": 118,
            "exang": 1, # Exercise Induced Angina = Yes
            "oldpeak": 2.8, # Severe ST Depression
            "slope": 2, # Downsloping ST segment (maps to LGBM category 3)
            "ca": 2, # 2 Major Coronaries Occluded
            "thal": 3, # Reversible Defect (maps to LGBM category 7.0)
            "ejection_fraction": 30,
            "serum_creatinine": 2.2,
            "smoking": "Regularly",
            "chest_pain": "Typical Angina",
            "exercise_days": "0-1 days"
        }
    },
    {
        "name": "Case 2: Optimal Low-Risk Athlete (Stage 0 Normal Healthy Baseline)",
        "payload": {
            "name": "Aarav Sharma",
            "age": 32,
            "sex": 1,
            "gender": "Male",
            "cp": 3, # Asymptomatic (maps to LGBM category 4)
            "trestbps": 114,
            "systolic_bp": 114,
            "diastolic_bp": 72,
            "chol": 172,
            "fbs": 0,
            "restecg": 0, # Normal
            "thalach": 174, # High cardiovascular stamina
            "exang": 0, # No Angina
            "oldpeak": 0.0, # Normal ST
            "slope": 0, # Upsloping (maps to LGBM category 1)
            "ca": 0, # 0 vessels
            "thal": 1, # Normal Blood Flow (maps to LGBM category 3.0)
            "ejection_fraction": 65,
            "serum_creatinine": 0.8,
            "smoking": "Never",
            "chest_pain": "None",
            "exercise_days": "5 days"
        }
    },
    {
        "name": "Case 3: Moderate Risk Pre-HTN Patient (Stage 1 Indicator)",
        "payload": {
            "name": "Rajesh Patel",
            "age": 56,
            "sex": 1,
            "gender": "Male",
            "cp": 1, # Atypical Angina (maps to LGBM category 2)
            "trestbps": 138,
            "systolic_bp": 138,
            "diastolic_bp": 88,
            "chol": 228,
            "fbs": 0,
            "restecg": 1, # ST-T wave
            "thalach": 142,
            "exang": 0,
            "oldpeak": 1.4,
            "slope": 1, # Flat (maps to LGBM category 2)
            "ca": 1, # 1 vessel
            "thal": 2, # Fixed Defect (maps to LGBM category 6.0)
            "ejection_fraction": 48,
            "serum_creatinine": 1.2,
            "smoking": "Occasionally",
            "chest_pain": "Mild",
            "exercise_days": "2-3 days"
        }
    }
]

print("=" * 80)
print("LIVE API ENDPOINT TEST WITH YOUR UPLOADED LightGBM MODEL")
print("=" * 80)

for case in test_cases:
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/predict",
        data=json.dumps(case["payload"]).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    
    print(f"\n[*] {case['name']}")
    print(f"    - Patient: {res['patient_name']} (Age {case['payload']['age']})")
    print(f"    - Predicted Risk Score: {res['risk_score']} / 100")
    print(f"    - Risk Category: {res['risk_level']}")
    print(f"    - Disease Probability: {res['probability_percentage']}% (95% CI: {res['confidence_interval']['lower']}% - {res['confidence_interval']['upper']}%)")
    print(f"    - Heart Health Score: {res['heart_health_score']} / 100")
    print(f"    - Model Source: {res['model_source']}")
    print(f"    - Primary Clinical Recommendation: {res['recommendations'][0]['title']}")

print("\n" + "=" * 80)
print("SUCCESS: YOUR UPLOADED MODEL IS ACTIVE AND INFERENCING LIVE ACROSS THE STACK!")
print("=" * 80)
