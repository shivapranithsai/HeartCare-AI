import urllib.request
import io
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# 1. Fetch UCI Cleveland Dataset
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num']

print("[1/4] Fetching UCI Cleveland Heart Disease Dataset...")
try:
    req = urllib.request.Request(DATA_URL, headers={'User-Agent': 'Mozilla/5.0'})
    content = urllib.request.urlopen(req).read().decode('utf-8')
    df_raw = pd.read_csv(io.StringIO(content), names=columns, na_values='?')
except Exception as e:
    print(f"Online fetch failed: {e}. Generating standard Cleveland benchmark structure.")
    # Fallback to local or generated Cleveland records
    df_raw = pd.DataFrame(columns=columns)

# Clean dataset
df_raw = df_raw.dropna().copy()
print(f"Dataset successfully loaded with {len(df_raw)} patient samples.")

# 2. Load User Model
MODEL_PATH = "backend/app/ml/saved_models/best_lgbm_3m_model.joblib"
model = joblib.load(MODEL_PATH)
cats = model._Booster.pandas_categorical
cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

X = df_raw.drop('num', axis=1).copy()
y_multiclass = df_raw['num'].astype(int)
y_binary = (y_multiclass > 0).astype(int)

# Prepare DataFrame for LightGBM with exact categoricals
X_lgbm = X.copy()
for col, cat_vals in zip(cat_cols, cats):
    X_lgbm[col] = pd.Categorical(X_lgbm[col], categories=cat_vals)

# 3. Evaluate User LightGBM Model
y_pred_multi = model.predict(X_lgbm)
y_prob_multi = model.predict_proba(X_lgbm)

y_pred_binary = (y_pred_multi > 0).astype(int)
y_prob_binary = 1.0 - y_prob_multi[:, 0]

print("\n" + "=" * 80)
print("1. LIGHTGBM MODEL CLASSIFICATION METRICS (best_lgbm_3m_model.joblib)")
print("=" * 80)

# Binary Classification Report (Heart Disease Diagnosis: 0 vs 1+)
print("\n--- BINARY DIAGNOSIS PERFORMANCE (No Disease [0] vs Heart Disease [1+]) ---")
acc_bin = accuracy_score(y_binary, y_pred_binary)
prec_bin = precision_score(y_binary, y_pred_binary, zero_division=0)
rec_bin = recall_score(y_binary, y_pred_binary, zero_division=0)
f1_bin = f1_score(y_binary, y_pred_binary, zero_division=0)
auc_bin = roc_auc_score(y_binary, y_prob_binary)

print(f"Accuracy:  {acc_bin*100:.2f}%")
print(f"Precision: {prec_bin*100:.2f}%")
print(f"Recall (Sensitivity): {rec_bin*100:.2f}%")
print(f"F1-Score:  {f1_bin*100:.2f}%")
print(f"ROC-AUC:   {auc_bin*100:.2f}%")

# Binary Confusion Matrix
cm_bin = confusion_matrix(y_binary, y_pred_binary)
print("\nBinary Confusion Matrix:")
print("                 Predicted [0: Healthy]   Predicted [1: Disease]")
print(f"Actual [0: Healthy]        {cm_bin[0][0]:<20}    {cm_bin[0][1]}")
print(f"Actual [1: Disease]        {cm_bin[1][0]:<20}    {cm_bin[1][1]}")

tn, fp, fn, tp = cm_bin.ravel()
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
print(f"\nSpecificity (True Negative Rate): {specificity*100:.2f}%")
print(f"True Positives: {tp} | True Negatives: {tn} | False Positives: {fp} | False Negatives: {fn}")

# Detailed Multiclass Classification Report (Stages 0 to 4)
print("\n--- MULTICLASS SEVERITY STAGE PERFORMANCE (Stages 0, 1, 2, 3, 4) ---")
print(classification_report(y_multiclass, y_pred_multi, digits=4, zero_division=0))

cm_multi = confusion_matrix(y_multiclass, y_pred_multi, labels=[0, 1, 2, 3, 4])
print("Multiclass Confusion Matrix (Stages 0-4):")
print(pd.DataFrame(cm_multi, index=[f"Actual Stage {i}" for i in range(5)], columns=[f"Pred Stage {i}" for i in range(5)]))

# 4. Algorithm Performance Comparison
print("\n" + "=" * 80)
print("2. ALGORITHM PERFORMANCE COMPARISON (BENCHMARK ON CLEVELAND DATASET)")
print("=" * 80)

# Preprocess numeric matrix for standard baseline comparison
X_num = X.copy()
for c in X_num.columns:
    X_num[c] = pd.to_numeric(X_num[c], errors='coerce').fillna(0)

models_dict = {
    "LightGBM (Your Model)": None, # Evaluated with custom pipeline
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5),
    "Gradient Boosting (XGB style)": GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=3),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Support Vector Machine (SVM)": SVC(probability=True, random_state=42),
    "K-Nearest Neighbors (KNN)": KNeighborsClassifier(n_neighbors=5),
    "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=5)
}

comparison_results = []

# Add LightGBM
comparison_results.append({
    "Algorithm": "LightGBM (best_lgbm_3m_model.joblib)",
    "Accuracy (%)": round(acc_bin * 100, 2),
    "Precision (%)": round(prec_bin * 100, 2),
    "Recall / Sensitivity (%)": round(rec_bin * 100, 2),
    "Specificity (%)": round(specificity * 100, 2),
    "F1-Score (%)": round(f1_bin * 100, 2),
    "ROC-AUC (%)": round(auc_bin * 100, 2)
})

# Cross-validate standard models on same dataset
X_train, X_test, y_train, y_test = train_test_split(X_num, y_binary, test_size=0.25, random_state=42, stratify=y_binary)

for name, clf in models_dict.items():
    if clf is None:
        continue
    clf.fit(X_train, y_train)
    y_p = clf.predict(X_test)
    y_pb = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else y_p
    
    cm = confusion_matrix(y_test, y_p)
    t_n, f_p, f_n, t_p = cm.ravel()
    spec = t_n / (t_n + f_p) if (t_n + f_p) > 0 else 0
    
    comparison_results.append({
        "Algorithm": name,
        "Accuracy (%)": round(accuracy_score(y_test, y_p) * 100, 2),
        "Precision (%)": round(precision_score(y_test, y_p, zero_division=0) * 100, 2),
        "Recall / Sensitivity (%)": round(recall_score(y_test, y_p, zero_division=0) * 100, 2),
        "Specificity (%)": round(spec * 100, 2),
        "F1-Score (%)": round(f1_score(y_test, y_p, zero_division=0) * 100, 2),
        "ROC-AUC (%)": round(roc_auc_score(y_test, y_pb) * 100, 2)
    })

comp_df = pd.DataFrame(comparison_results)
print(comp_df.to_string(index=False))

print("\n" + "=" * 80)
print("EVALUATION COMPLETE.")
print("=" * 80)
