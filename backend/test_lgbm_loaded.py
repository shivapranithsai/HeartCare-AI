import joblib
import pandas as pd
import numpy as np

model_path = 'backend/app/ml/saved_models/best_lgbm_3m_model.joblib'
model = joblib.load(model_path)
cats = model._Booster.pandas_categorical
cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

test_cases = [
    {
        'name': 'High Risk Case (Elderly with Ischemia & Vessels)',
        'data': {'age': 68.0, 'sex': 0, 'cp': 1, 'trestbps': 168.0, 'chol': 275.0, 'fbs': 1, 'restecg': 2, 'thalach': 118.0, 'exang': 1, 'oldpeak': 2.8, 'slope': 3, 'ca': 2.0, 'thal': 7.0}
    },
    {
        'name': 'Healthy Low Risk Athlete',
        'data': {'age': 32.0, 'sex': 1, 'cp': 4, 'trestbps': 114.0, 'chol': 172.0, 'fbs': 0, 'restecg': 0, 'thalach': 174.0, 'exang': 0, 'oldpeak': 0.0, 'slope': 1, 'ca': 0.0, 'thal': 3.0}
    },
    {
        'name': 'Moderate Risk Pre-HTN Patient',
        'data': {'age': 56.0, 'sex': 1, 'cp': 2, 'trestbps': 138.0, 'chol': 228.0, 'fbs': 0, 'restecg': 1, 'thalach': 142.0, 'exang': 0, 'oldpeak': 1.4, 'slope': 2, 'ca': 1.0, 'thal': 6.0}
    }
]

print("=" * 80)
print("TESTING YOUR UPLOADED LightGBM MODEL (best_lgbm_3m_model.joblib)")
print("=" * 80)

for tc in test_cases:
    df = pd.DataFrame([tc['data']])
    for col, cat_vals in zip(cat_cols, cats):
        df[col] = pd.Categorical(df[col], categories=cat_vals)
    pred_class = int(model.predict(df)[0])
    prob_dist = model.predict_proba(df)[0]
    disease_prob = round((1.0 - prob_dist[0]) * 100, 1)
    
    print(f"\n[*] {tc['name']}")
    print(f"    - Predicted Diagnosis: Stage {pred_class} {'(No Disease / Healthy)' if pred_class == 0 else '(Heart Disease Risk)'}")
    print(f"    - Overall Disease Risk: {disease_prob}% (Healthy prob: {round(prob_dist[0]*100, 1)}%)")
    print(f"    - Stage Probabilities [0=Healthy, 1, 2, 3, 4]: {[round(p, 3) for p in prob_dist]}")

print("\n" + "=" * 80)
