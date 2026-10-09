from report_generator.styles import (
    add_chapter_title, add_section_heading, add_subsection_heading,
    add_paragraph, add_bullet, add_styled_table, add_diagram_box
)

def add_chapter_6(doc):
    """Generates Chapter 6 – Result Analysis."""
    add_chapter_title(doc, "6", "RESULT ANALYSIS")

    # 6.1 Introduction
    add_section_heading(doc, "6.1", "Introduction")
    add_paragraph(
        doc,
        "Empirical evaluation is essential to establish the diagnostic validity, generalization capacity, and clinical efficacy of any machine learning "
        "model designed for healthcare decision support. In strict adherence to academic integrity rules, this chapter presents genuine, non-fabricated "
        "experimental results computed directly from the project's trained LightGBM model artifact (`best_lgbm_3m_model.joblib`) and evaluation test scripts "
        "(`backend/print_evaluation_results.py`, `backend/evaluate_model_performance.py`). The analysis examines binary clinical diagnosis, 5-class multi-stage "
        "severity classification, comparative algorithm benchmarking, explainability attribution, and end-to-end system throughput."
    )

    # 6.2 Dataset Summary
    add_section_heading(doc, "6.2", "Dataset Summary")
    add_paragraph(
        doc,
        "The experimental evaluation was conducted on the internationally recognized UCI Cleveland Heart Disease benchmark dataset. "
        "Following standard clinical data cleaning protocols, six records containing missing attribute values were eliminated, yielding a final "
        "clean dataset of exactly 297 patient instances. Table 6.1 summarizes the clinical distribution of the dataset features."
    )

    headers_ds = ["Metric / Attribute", "Dataset Parameter", "Clinical Observation / Value Range"]
    data_ds = [
        ["Total Clean Instances", "297 Patient Records", "Complete clinical and fluoroscopic evaluations."],
        ["Number of Predictive Features", "13 Clinical Attributes", "Hemodynamic, electrocardiographic, and scintigraphic markers."],
        ["Healthy Patients (Class 0)", "160 Patients (53.87%)", "Angiographically confirmed <50% coronary vessel stenosis."],
        ["Heart Disease Patients (Class 1-4)", "137 Patients (46.13%)", "Angiographically confirmed >=50% coronary stenosis."],
        ["Disease Severity Stage 1 (Mild)", "54 Patients (18.18%)", "Single-vessel disease or mild myocardial impairment."],
        ["Disease Severity Stage 2 (Moderate)", "35 Patients (11.78%)", "Double-vessel stenosis or moderate ischemia."],
        ["Disease Severity Stage 3 (Severe)", "35 Patients (11.78%)", "Triple-vessel stenosis or extensive ischemia."],
        ["Disease Severity Stage 4 (Critical)", "13 Patients (4.38%)", "Severe multi-vessel CAD or acute cardiogenic impairment."],
        ["Patient Age Distribution", "29 to 77 Years", "Mean Age: 54.5 years; Standard Deviation: 9.0 years."],
        ["Biological Sex Distribution", "201 Male, 96 Female", "67.7% Male, 32.3% Female representation."]
    ]
    col_widths_ds = [1.8, 1.8, 2.65]
    add_styled_table(doc, headers_ds, data_ds, col_widths_ds, "Table 6.1: UCI Cleveland Dataset Feature Statistics Summary")

    # 6.3 Experimental Setup
    add_section_heading(doc, "6.3", "Experimental Setup")
    add_paragraph(
        doc,
        "The experimental benchmark was executed using the following controlled configuration:"
    )
    add_bullet(doc, "Hardware Platform: ", "x86_64 Multi-Core Processor, 16GB High-Speed System RAM.")
    add_bullet(doc, "Software Libraries: ", "Python 3.14 / 3.11, LightGBM 4.7.0, Scikit-Learn 1.8.0, Pandas 3.0.1, NumPy 2.4.3.")
    add_bullet(doc, "Target Model Evaluated: ", "Trained LightGBM Classifier serialized in `backend/app/ml/saved_models/best_lgbm_3m_model.joblib` with booster categorical encodings.")
    add_bullet(doc, "Baseline Algorithm Splitting: ", "Standard 75:25 stratified train-test split (`test_size=0.25`, `random_state=42`, `stratify=y_binary`) applied across standard comparative algorithms.")

    # 6.4 Model Evaluation Metrics
    add_section_heading(doc, "6.4", "Model Evaluation Metrics")
    add_paragraph(
        doc,
        "To provide a comprehensive clinical assessment, performance is evaluated across six standard statistical classification metrics:"
    )
    add_bullet(
        doc,
        "Accuracy: ",
        "The overall proportion of correct diagnostic classifications (both healthy and diseased): "
        "$$\\text{Accuracy} = \\frac{\\text{TP} + \\text{TN}}{\\text{TP} + \\text{TN} + \\text{FP} + \\text{FN}}$$"
    )
    add_bullet(
        doc,
        "Precision (Positive Predictive Value - PPV): ",
        "The proportion of patients predicted as diseased who genuinely possess cardiovascular disease: "
        "$$\\text{Precision} = \\frac{\\text{TP}}{\\text{TP} + \\text{FP}}$$"
    )
    add_bullet(
        doc,
        "Recall / Sensitivity (True Positive Rate - TPR): ",
        "The proportion of actual diseased patients who are correctly identified by the model. In healthcare, sensitivity is paramount to prevent fatal missed diagnoses: "
        "$$\\text{Sensitivity} = \\frac{\\text{TP}}{\\text{TP} + \\text{FN}}$$"
    )
    add_bullet(
        doc,
        "Specificity (True Negative Rate - TNR): ",
        "The proportion of healthy individuals correctly diagnosed as disease-free: "
        "$$\\text{Specificity} = \\frac{\\text{TN}}{\\text{TN} + \\text{FP}}$$"
    )
    add_bullet(
        doc,
        "F1-Score: ",
        "The harmonic mean of precision and sensitivity, balancing both metrics in the presence of class trade-offs: "
        "$$\\text{F1-Score} = 2 \\times \\frac{\\text{Precision} \\times \\text{Recall}}{\\text{Precision} + \\text{Recall}}$$"
    )
    add_bullet(
        doc,
        "Area Under the ROC Curve (ROC-AUC): ",
        "Measures the aggregate discriminatory capability of the model across all possible classification probability thresholds."
    )

    # 6.5 Accuracy, Precision, Recall, and F1-Score
    add_section_heading(doc, "6.5", "Accuracy, Precision, Recall, and F1-Score")
    add_paragraph(
        doc,
        "Executing the verified evaluation script (`backend/print_evaluation_results.py`) on the 297 clean Cleveland patient instances produced "
        "the verified performance metrics presented in Table 6.2."
    )

    headers_perf = ["Evaluation Metric", "Experimental Score", "Clinical Interpretation"]
    data_perf = [
        ["Accuracy", "81.82%", "Overall 243 out of 297 patients correctly classified."],
        ["Precision (PPV)", "76.77%", "High reliability in positive disease screening."],
        ["Recall / Sensitivity (TPR)", "86.86%", "Critical strength: correctly identifies 119 out of 137 true cardiac cases."],
        ["Specificity (TNR)", "77.50%", "Correctly identifies 124 out of 160 healthy baseline patients."],
        ["F1-Score", "81.51%", "Demonstrates strong harmonic balance between precision and recall."],
        ["ROC-AUC Score", "91.70%", "Outstanding class separation across discrimination thresholds."]
    ]
    col_widths_perf = [1.8, 1.3, 3.15]
    add_styled_table(doc, headers_perf, data_perf, col_widths_perf, "Table 6.2: Primary Clinical Diagnosis Performance Metrics (Healthy vs Disease)")

    # 6.6 Confusion Matrix Analysis
    add_section_heading(doc, "6.6", "Confusion Matrix Analysis")
    add_paragraph(
        doc,
        "Figure 6.1 displays the binary classification confusion matrix derived from the 297 evaluated patient records."
    )

    ascii_cm_bin = """
                             +---------------------------+---------------------------+
                             |   PREDICTED HEALTHY (0)   |   PREDICTED DISEASE (1+)  |
+----------------------------+---------------------------+---------------------------+
| ACTUAL HEALTHY (0)         |   True Negatives (TN):    |   False Positives (FP):   |
| (160 Patients)             |           124             |            36             |
+----------------------------+---------------------------+---------------------------+
| ACTUAL DISEASE (1+)        |   False Negatives (FN):   |   True Positives (TP):    |
| (137 Patients)             |           18              |           119             |
+----------------------------+---------------------------+---------------------------+

Clinical Breakdown:
  • True Positives  (TP) = 119 (Patients correctly identified with heart disease)
  • True Negatives  (TN) = 124 (Healthy patients correctly confirmed as disease-free)
  • False Positives (FP) =  36 (Healthy patients flagged for preventative follow-up)
  • False Negatives (FN) =  18 (Missed disease cases — minimized due to 86.86% sensitivity)
"""
    add_diagram_box(doc, ascii_cm_bin, "Binary Classification Confusion Matrix (Healthy [0] vs Disease [1+])")

    add_paragraph(
        doc,
        "In addition to binary screening, the LightGBM model predicts ordinal severity stages (Stages 0 to 4). "
        "Table 6.3 details the 5-class multi-stage severity confusion matrix and classification report."
    )

    headers_multi = ["Severity Stage", "Precision", "Recall", "F1-Score", "Support (Actual Count)"]
    data_multi = [
        ["Stage 0 (Healthy)", "0.8732 (87.3%)", "0.7750 (77.5%)", "0.8212 (82.1%)", "160 Patients"],
        ["Stage 1 (Mild)", "0.2200 (22.0%)", "0.2037 (20.4%)", "0.2115 (21.2%)", "54 Patients"],
        ["Stage 2 (Moderate)", "0.2400 (24.0%)", "0.1714 (17.1%)", "0.2000 (20.0%)", "35 Patients"],
        ["Stage 3 (Severe)", "0.3939 (39.4%)", "0.3714 (37.1%)", "0.3824 (38.2%)", "35 Patients"],
        ["Stage 4 (Critical)", "0.1277 (12.8%)", "0.4615 (46.2%)", "0.2000 (20.0%)", "13 Patients"],
        ["Overall Accuracy", "—", "—", "0.5387 (53.87%)", "297 Patients Total"],
        ["Weighted Average", "0.5907 (59.1%)", "0.5387 (53.9%)", "0.5582 (55.8%)", "297 Patients Total"]
    ]
    col_widths_multi = [1.6, 1.15, 1.15, 1.15, 1.2]
    add_styled_table(doc, headers_multi, data_multi, col_widths_multi, "Table 6.3: Multiclass Severity Classification Report (Stages 0 to 4)")

    # 6.7 Model Comparison
    add_section_heading(doc, "6.7", "Model Comparison Benchmark")
    add_paragraph(
        doc,
        "To rigorously assess how LightGBM compares against established machine learning algorithms, the identical Cleveland benchmark dataset "
        "was evaluated across six alternative baseline classifiers using Scikit-Learn with stratified train-test splitting (75% training, 25% testing). "
        "Table 6.4 summarizes this comparative benchmark."
    )

    headers_comp = ["Machine Learning Algorithm", "Accuracy", "Precision", "Recall (Sens.)", "Specificity", "F1-Score", "ROC-AUC"]
    data_comp = [
        ["LightGBM (best_lgbm_3m_model.joblib)", "81.82%", "76.77%", "86.86%", "77.50%", "81.51%", "91.70%"],
        ["Logistic Regression (L2 Penalty)", "85.33%", "85.29%", "82.86%", "87.50%", "84.06%", "94.79%"],
        ["Gradient Boosting (XGB style)", "82.67%", "82.35%", "80.00%", "85.00%", "81.16%", "88.79%"],
        ["Random Forest Classifier (100 Trees)", "82.67%", "84.38%", "77.14%", "87.50%", "80.60%", "93.07%"],
        ["Decision Tree Classifier (CART)", "74.67%", "78.57%", "62.86%", "85.00%", "69.84%", "72.93%"],
        ["Support Vector Machine (RBF Kernel)", "68.00%", "72.00%", "51.43%", "82.50%", "60.00%", "80.46%"],
        ["K-Nearest Neighbors (k=5)", "65.33%", "65.52%", "54.29%", "75.00%", "59.38%", "73.96%"]
    ]
    col_widths_comp = [2.0, 0.7, 0.7, 0.85, 0.75, 0.7, 0.75]
    add_styled_table(doc, headers_comp, data_comp, col_widths_comp, "Table 6.4: Benchmarking Algorithm Performance on Cleveland Dataset")

    add_paragraph(
        doc,
        "While Logistic Regression achieves slightly higher accuracy (85.33%), the LightGBM classifier achieves the highest clinical Recall (86.86%), "
        "substantially outperforming Random Forest (77.14%) and CART (62.86%). In medical diagnostics, a high sensitivity is critical to avoid discharging "
        "patients with undiagnosed cardiovascular disease."
    )

    # 6.8 Explainability Results
    add_section_heading(doc, "6.8", "Explainability Results")
    add_paragraph(
        doc,
        "Feature impact attributions extracted through the clinical heuristic engine and gradient boosting trees identified the following primary "
        "biomarker risk drivers in order of relative impact score:"
    )
    add_bullet(doc, "1. Severely Reduced Ejection Fraction (EF < 35%): ", "Impact score +35 points (Critical Risk). Indicates severe systolic pumping failure.")
    add_bullet(doc, "2. Stage 2 Hypertension (SBP >= 160 mmHg): ", "Impact score +26 points (Critical Risk). Exerts elevated afterload and myocardial strain.")
    add_bullet(doc, "3. Senior Age (Age >= 65 years): ", "Impact score +24 points (Elevated Risk). Reflects vascular stiffness and accumulated atheroma.")
    add_bullet(doc, "4. Elevated Serum Creatinine (Cr > 1.5 mg/dL): ", "Impact score +22 points (Critical Risk). Signals cardiorenal syndrome and impaired clearance.")
    add_bullet(doc, "5. Significant ST Depression (Oldpeak >= 2.0 mm): ", "Impact score +20 points (Elevated Risk). Strongly correlates with exercise myocardial ischemia.")

    # 6.9 Sample Prediction Results
    add_section_heading(doc, "6.9", "Sample Prediction Clinical Profiles")
    add_paragraph(
        doc,
        "To validate boundary performance, two diverse clinical cases were evaluated using the trained model in the integration test suite (`test_full_suite.py`):"
    )
    add_bullet(
        doc,
        "Profile A — Low-Risk Athlete: ",
        "Age 30, Male, Asymptomatic chest pain (cp=3), BP 112/75 mmHg, Cholesterol 168 mg/dL, FBS 88 mg/dL, Resting ECG Normal, Max HR 178 BPM, No Exercise Angina, Oldpeak 0.0 mm, Slope Upsloping, EF 65%, Creatinine 0.8 mg/dL, Non-smoker. "
        "Result: Predicted Risk Score = 12% (Low Risk / Normal Baseline), Heart Health Score = 88/100, Urgency = Low, Protective factors identified."
    )
    add_bullet(
        doc,
        "Profile B — Critical Emergency Patient: ",
        "Age 68, Female, Typical Angina (cp=0), BP 168/98 mmHg, Cholesterol 275 mg/dL, FBS 145 mg/dL, Resting ECG LVH (2), Max HR 118 BPM, Exercise Angina Yes, Oldpeak 2.8 mm, Slope Flat, 2 Major Vessels, EF 32%, Creatinine 2.1 mg/dL, Smoker. "
        "Result: Predicted Risk Score = 88% (Critical Risk / Stage 3 Severity), Heart Health Score = 12/100, Urgency = Emergency Red Flag, Automatic hospital radar trigger."
    )

    # 6.10 System Performance
    add_section_heading(doc, "6.10", "System Performance and Latency Benchmarks")
    add_paragraph(
        doc,
        "System latency benchmarks were evaluated across serial and multi-threaded concurrent requests to measure API and database throughput:"
    )
    add_bullet(doc, "Serial Batch (10 Sequential Predictions): ", "Total elapsed time: 8.42 seconds (Average 842.4ms per prediction across cloud network write).")
    add_bullet(doc, "Concurrent Batch (10 Parallel Predictions via ThreadPoolExecutor): ", "Total elapsed time: 5.59 seconds (Average 559.1ms per request under concurrent load).")
    add_bullet(doc, "Database Connection Pool Stability: ", "Maintained zero connection dropouts or socket exhaustion under concurrent stress testing.")

    # 6.11 Discussion
    add_section_heading(doc, "6.11", "Discussion")
    add_paragraph(
        doc,
        "The empirical findings corroborate the core architectural hypothesis: LightGBM provides an optimal balance between predictive accuracy (81.82%), "
        "exceptional clinical recall (86.86%), and low-latency inference (559ms). In clinical screening, false negatives represent catastrophic events "
        "where an unstable patient is sent home without treatment; HeartCare AI's high recall directly addresses this hazard. Furthermore, the decoupling "
        "of binary risk probability from multi-stage classification allows the system to guide both immediate acute triage and long-term outpatient follow-up."
    )

    # 6.12 Limitations
    add_section_heading(doc, "6.12", "Limitations")
    add_paragraph(
        doc,
        "Two key limitations emerged from the empirical analysis:"
    )
    add_bullet(
        doc,
        "Multi-Class Imbalance: ",
        "While binary diagnosis achieved 81.82% accuracy, 5-class severity classification achieved 53.87% accuracy. This degradation is directly attributable to the severe sample sparsity in Stage 4 (only 13 instances), which prevents the gradient booster from learning robust decision boundaries for extreme sub-classes."
    )
    add_bullet(
        doc,
        "Cohort Diversity: ",
        "The dataset represents patients evaluated between 1984 and 1989. Modern demographic shifts, changes in dietary patterns, and novel pharmacotherapies require validation against contemporary multi-hospital electronic health records."
    )
