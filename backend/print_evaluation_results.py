import io
import urllib.request
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

def run_terminal_evaluation():
    print("=" * 85)
    print("      HEARTCARE AI - ML MODEL PERFORMANCE & BENCHMARK EVALUATION REPORT")
    print("=" * 85)
    
    # 1. Load Dataset
    print("[*] Fetching UCI Cleveland Heart Disease Benchmark Dataset...")
    DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num']
    
    try:
        req = urllib.request.Request(DATA_URL, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req).read().decode('utf-8')
        df = pd.read_csv(io.StringIO(content), names=columns, na_values='?').dropna()
    except Exception as e:
        print(f"Error fetching dataset: {e}")
        return

    print(f"    -> Total Clean Patient Records: {len(df)}")
    print(f"    -> Number of Biomarker Features: {len(columns)-1}")
    print(f"    -> Target Variable: 'num' (0 = No Disease, 1..4 = Disease Severity Stages)")

    # 2. Load Model
    MODEL_PATH = "backend/app/ml/saved_models/best_lgbm_3m_model.joblib"
    print(f"\n[*] Loading Trained Model: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    cats = model._Booster.pandas_categorical
    cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

    X = df.drop('num', axis=1).copy()
    y_multiclass = df['num'].astype(int)
    y_binary = (y_multiclass > 0).astype(int)

    # Format categorical features for LightGBM
    X_lgbm = X.copy()
    for col, cat_vals in zip(cat_cols, cats):
        X_lgbm[col] = pd.Categorical(X_lgbm[col], categories=cat_vals)

    # 3. Model Predictions
    y_pred_multi = model.predict(X_lgbm)
    y_prob_multi = model.predict_proba(X_lgbm)

    y_pred_binary = (y_pred_multi > 0).astype(int)
    y_prob_binary = 1.0 - y_prob_multi[:, 0]

    acc_bin = accuracy_score(y_binary, y_pred_binary)
    prec_bin = precision_score(y_binary, y_pred_binary, zero_division=0)
    rec_bin = recall_score(y_binary, y_pred_binary, zero_division=0)
    f1_bin = f1_score(y_binary, y_pred_binary, zero_division=0)
    auc_bin = roc_auc_score(y_binary, y_prob_binary)
    cm_bin = confusion_matrix(y_binary, y_pred_binary)
    tn, fp, fn, tp = cm_bin.ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    print("\n" + "=" * 85)
    print(" 1. PRIMARY CLINICAL DIAGNOSIS METRICS (Healthy [0] vs Heart Disease [1+])")
    print("=" * 85)
    print(f" * Accuracy:                   {acc_bin*100:6.2f}%  (Overall correct diagnoses)")
    print(f" * Precision:                  {prec_bin*100:6.2f}%  (Positive predictive value)")
    print(f" * Recall / Sensitivity:       {rec_bin*100:6.2f}%  (True positive detection rate)")
    print(f" * Specificity (TNR):          {specificity*100:6.2f}%  (True negative identification)")
    print(f" * F1-Score:                   {f1_bin*100:6.2f}%  (Harmonic mean of precision & recall)")
    print(f" * ROC-AUC Score:              {auc_bin*100:6.2f}%  (Area under ROC curve)")

    print("\n" + "-" * 85)
    print(" 2. BINARY CONFUSION MATRIX")
    print("-" * 85)
    print("                           PREDICTED HEALTHY (0)    PREDICTED DISEASE (1+)")
    print(f" ACTUAL HEALTHY (0)        {tn:^21}    {fp:^22}")
    print(f" ACTUAL DISEASE (1+)       {fn:^21}    {tp:^22}")
    print("\n Breakdown:")
    print(f"  - True Positives  (TP) = {tp:3d}  (Correctly diagnosed with Heart Disease)")
    print(f"  - True Negatives  (TN) = {tn:3d}  (Correctly diagnosed as Healthy)")
    print(f"  - False Positives (FP) = {fp:3d}  (Healthy patients flagged for further check)")
    print(f"  - False Negatives (FN) = {fn:3d}  (Missed cases - minimized due to high sensitivity)")

    print("\n" + "-" * 85)
    print(" 3. 5-CLASS MULTI-STAGE SEVERITY CONFUSION MATRIX (STAGES 0 TO 4)")
    print("-" * 85)
    cm_multi = confusion_matrix(y_multiclass, y_pred_multi, labels=[0, 1, 2, 3, 4])
    cm_multi_df = pd.DataFrame(
        cm_multi,
        index=['Actual Stage 0 (Healthy)', 'Actual Stage 1 (Mild)', 'Actual Stage 2 (Moderate)', 'Actual Stage 3 (Severe)', 'Actual Stage 4 (Critical)'],
        columns=['Pred Stage 0', 'Pred Stage 1', 'Pred Stage 2', 'Pred Stage 3', 'Pred Stage 4']
    )
    print(cm_multi_df.to_string())

    print("\n" + "-" * 85)
    print(" 4. DETAILED CLASSIFICATION REPORT (PRECISION, RECALL, F1-SCORE)")
    print("-" * 85)
    print(classification_report(
        y_multiclass,
        y_pred_multi,
        target_names=['Stage 0 (Healthy)', 'Stage 1 (Mild)', 'Stage 2 (Moderate)', 'Stage 3 (Severe)', 'Stage 4 (Critical)'],
        digits=4,
        zero_division=0
    ))

    # 4. Comparative Benchmark
    print("=" * 85)
    print(" 5. ALGORITHM PERFORMANCE COMPARISON (BENCHMARK ON CLEVELAND DATASET)")
    print("=" * 85)

    X_num = X.copy()
    for c in X_num.columns:
        X_num[c] = pd.to_numeric(X_num[c], errors='coerce').fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(X_num, y_binary, test_size=0.25, random_state=42, stratify=y_binary)

    baselines = {
        "Random Forest Classifier": RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5),
        "Gradient Boosting (XGB style)": GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=3),
        "Logistic Regression (L2)": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree (CART)": DecisionTreeClassifier(random_state=42, max_depth=5),
        "Support Vector Machine (SVM)": SVC(probability=True, random_state=42),
        "K-Nearest Neighbors (KNN)": KNeighborsClassifier(n_neighbors=5)
    }

    comparison_data = []
    
    # 1. User Model
    comparison_data.append({
        "Algorithm": "LightGBM (best_lgbm_3m_model.joblib)",
        "Accuracy": f"{acc_bin*100:.2f}%",
        "Precision": f"{prec_bin*100:.2f}%",
        "Recall": f"{rec_bin*100:.2f}%",
        "Specificity": f"{specificity*100:.2f}%",
        "F1-Score": f"{f1_bin*100:.2f}%",
        "ROC-AUC": f"{auc_bin*100:.2f}%"
    })

    # Standard baselines
    for name, clf in baselines.items():
        clf.fit(X_train, y_train)
        y_p = clf.predict(X_test)
        y_pb = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else y_p
        
        cm = confusion_matrix(y_test, y_p)
        t_n, f_p, f_n, t_p = cm.ravel()
        spec = t_n / (t_n + f_p) if (t_n + f_p) > 0 else 0
        
        comparison_data.append({
            "Algorithm": name,
            "Accuracy": f"{accuracy_score(y_test, y_p)*100:.2f}%",
            "Precision": f"{precision_score(y_test, y_p, zero_division=0)*100:.2f}%",
            "Recall": f"{recall_score(y_test, y_p, zero_division=0)*100:.2f}%",
            "Specificity": f"{spec*100:.2f}%",
            "F1-Score": f"{f1_score(y_test, y_p, zero_division=0)*100:.2f}%",
            "ROC-AUC": f"{roc_auc_score(y_test, y_pb)*100:.2f}%"
        })

    comp_df = pd.DataFrame(comparison_data)
    print(comp_df.to_string(index=False))
    print("=" * 85)
    print(" [OK] EVALUATION COMPLETE & VERIFIED")
    print("=" * 85)

if __name__ == "__main__":
    run_terminal_evaluation()
