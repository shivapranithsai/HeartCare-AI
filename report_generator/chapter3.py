from report_generator.styles import (
    add_chapter_title, add_section_heading, add_subsection_heading,
    add_paragraph, add_bullet, add_styled_table, add_diagram_box
)

def add_chapter_3(doc):
    """Generates Chapter 3 – Project Flow and Methodology."""
    add_chapter_title(doc, "3", "PROJECT FLOW AND METHODOLOGY")

    # 3.1 Introduction
    add_section_heading(doc, "3.1", "Introduction")
    add_paragraph(
        doc,
        "The development of HeartCare AI follows a disciplined, evidence-based software engineering and machine learning methodology designed to ensure "
        "clinical validity, computational efficiency, and operational resilience. Translating medical biomarker inputs into actionable risk intelligence requires "
        "a rigorous multi-stage pipeline: from benchmark data ingestion and feature engineering to gradient-boosted decision tree inference, explainable AI attribution, "
        "asynchronous API routing, and geospatial emergency navigation. This chapter details each methodological phase based strictly on the verified project codebase."
    )

    # 3.2 Overall Project Workflow
    add_section_heading(doc, "3.2", "Overall Project Workflow")
    add_paragraph(
        doc,
        "The overall workflow of HeartCare AI is architected into five cohesive lifecycle phases: Data Ingestion & Preprocessing, Machine Learning Modeling, "
        "Backend API Service Construction, Reactive User Interface Engineering, and Geospatial Integration. Figure 3.1 illustrates this end-to-end clinical dataflow."
    )

    ascii_workflow = """
+-------------------------------------------------------------------------------------------------+
|                                 1. CLINICAL DATA INGESTION & PREPROCESSING                       |
|   UCI Cleveland Heart Disease Benchmark (297 records) + Cardiorenal Biomarkers (EF, Creatinine)  |
|   - Missing Value Handling   - Categorical Code Mapping   - Booster Type Alignment              |
+------------------------------------------------+------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
|                                2. MACHINE LEARNING & HEURISTIC MODELING                         |
|   - Primary Engine: LightGBM Multi-Class Classifier (best_lgbm_3m_model.joblib)                 |
|   - Risk Formulation: Disease Probability = 1.0 - P(Stage 0: Healthy)                           |
|   - Resilient Fallback: AHA / Framingham Clinical AI Heuristic Engine (clinical_engine.py)      |
|   - Explainable AI: Biomarker Impact Attribution (Risk Drivers vs. Protective Factors)          |
+------------------------------------------------+------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
|                                3. FASTAPI ASYNCHRONOUS BACKEND SERVICES                         |
|   - Lifespan DB Pool   - /auth (Salted SHA-256)   - /predict & /simulate   - /history & /analytics|
|   - Pydantic v2 Schema Validation   - Strict Cross-User Data Isolation Filters                  |
+------------------------------------------------+------------------------------------------------+
                         |                                                |
                         v                                                v
+------------------------------------------------+ +----------------------------------------------+
|        4. MONGODB ATLAS CLOUD PERSISTENCE      | |        5. GEOSPATIAL & EMERGENCY TRIAGE      |
|  - Users Collection (Auth Credentials)         | |  - OpenStreetMap Overpass & Nominatim APIs   |
|  - Assessments Collection (Telemetry History)  | |  - Geodesic Haversine Distance Formula       |
|  - Hospitals Collection (23 Seeded Centers)    | |  - Dynamic ETA & Direct Google Maps Routing  |
|  - Appointments Collection (Bookings)          | |  - In-App Cardiology Appointment Booking     |
+------------------------------------------------+ +----------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
|                                 6. REACT 19 / VITE SINGLE-PAGE FRONTEND                         |
|   - Glassmorphic Dashboard   - HTML5 Canvas ECG Monitor   - SVG Radial Risk Gauge               |
|   - What-If Dynamic Intervention Sliders   - Printable Official Medical Letterhead Reports      |
+-------------------------------------------------------------------------------------------------+
"""
    add_diagram_box(doc, ascii_workflow, "HeartCare AI End-to-End High-Level System Workflow")

    # 3.3 Proposed Methodology
    add_section_heading(doc, "3.3", "Proposed Methodology")
    add_paragraph(
        doc,
        "The proposed methodology adopts an iterative, test-driven approach combining supervised machine learning with clinical domain knowledge. "
        "Rather than treating machine learning as an isolated black box, the platform tightly couples algorithmic probability estimation with established "
        "medical decision thresholds formulated by the American College of Cardiology (ACC) and American Heart Association (AHA). "
        "Furthermore, the methodology embeds an automatic dual-engine architecture: if the primary LightGBM serialized model encounters any deserialization "
        "or runtime anomaly, the system automatically falls back to the deterministic clinical heuristic engine without interrupting user workflows."
    )

    # 3.4 Data Collection
    add_section_heading(doc, "3.4", "Data Collection")
    add_paragraph(
        doc,
        "The primary training and validation dataset utilized in this project is the internationally recognized UCI Cleveland Heart Disease Database, "
        "originally assembled by Detrano et al. (1989). The raw dataset contains 303 patient records with 76 raw attributes, of which a standardized "
        "subset of 14 core features (13 clinical predictors and 1 target diagnosis variable) is universally adopted in cardiovascular machine learning research."
    )
    add_paragraph(
        doc,
        "In addition to the standard 13 Cleveland features, HeartCare AI incorporates extended cardiorenal biomarkers based on the clinical findings of "
        "Chicco and Jurman (2020), specifically Left Ventricular Ejection Fraction (EF, normal range 50–70%) and Serum Creatinine (normal range 0.7–1.3 mg/dL). "
        "Table 3.1 delineates the complete 13 Cleveland feature specification and clinical value ranges."
    )

    headers_clev = ["Feature Name", "Variable", "Clinical Description", "Data Type", "Value Domain / Units"]
    data_clev = [
        ["Age", "age", "Age of patient in years", "Continuous", "29 – 77 years"],
        ["Sex", "sex", "Biological sex of patient", "Categorical", "0: Female, 1: Male"],
        ["Chest Pain Type", "cp", "Symptomatic angina classification", "Categorical", "1: Typical, 2: Atypical, 3: Non-anginal, 4: Asymptomatic"],
        ["Resting Blood Pressure", "trestbps", "Resting systolic arterial pressure on admission", "Continuous", "94 – 200 mmHg"],
        ["Serum Cholesterol", "chol", "Total serum cholesterol concentration", "Continuous", "126 – 564 mg/dL"],
        ["Fasting Blood Sugar", "fbs", "Fasting blood glucose > 120 mg/dL", "Binary", "0: False (<= 120), 1: True (> 120)"],
        ["Resting ECG", "restecg", "Resting electrocardiographic results", "Categorical", "0: Normal, 1: ST-T wave abnormality, 2: Left Ventricular Hypertrophy"],
        ["Max Heart Rate", "thalach", "Maximum heart rate achieved during exercise stress", "Continuous", "71 – 202 BPM"],
        ["Exercise Induced Angina", "exang", "Occurrence of angina during exercise", "Binary", "0: No, 1: Yes"],
        ["ST Depression (Oldpeak)", "oldpeak", "ST depression induced by exercise relative to rest", "Continuous", "0.0 – 6.2 mm"],
        ["Slope of Peak ST", "slope", "Slope of the peak exercise ST-segment", "Categorical", "1: Upsloping, 2: Flat, 3: Downsloping"],
        ["Major Vessels (Fluoroscopy)", "ca", "Number of major vessels (0-3) colored by fluoroscopy", "Discrete", "0.0, 1.0, 2.0, 3.0 vessels"],
        ["Thallium Scintigraphy", "thal", "Myocardial perfusion scintigraphy defect", "Categorical", "3.0: Normal, 6.0: Fixed defect, 7.0: Reversible defect"],
        ["Diagnosis Target", "num", "Coronary artery disease severity status", "Multi-class", "0: Healthy (<50% stenosis), 1..4: Disease Severity Stages"]
    ]
    col_widths_clev = [1.2, 0.7, 1.9, 0.8, 1.65]
    add_styled_table(doc, headers_clev, data_clev, col_widths_clev, "Table 3.1: Description of 13 Cleveland Clinical Features and Encodings")

    # 3.5 Data Preprocessing
    add_section_heading(doc, "3.5", "Data Preprocessing")
    add_paragraph(
        doc,
        "Data preprocessing is implemented directly within the evaluation pipelines (`backend/evaluate_model_performance.py`, `backend/print_evaluation_results.py`) "
        "and inference service (`backend/app/ml/model_loader.py`):"
    )
    add_bullet(
        doc,
        "1. Missing Value Elimination: ",
        "In the raw UCI Cleveland dataset, six records contained missing values represented by the '?' symbol (four records in the fluoroscopy vessel count 'ca' and two records in the thallium scintigraphy feature 'thal'). Following established clinical benchmark protocol, these six incomplete instances were removed, yielding a clean dataset of exactly 297 patient samples."
    )
    add_bullet(
        doc,
        "2. Numeric Casting & Normalization: ",
        "All continuous variables (`age`, `trestbps`, `chol`, `thalach`, `oldpeak`, `ca`, `thal`) were parsed as high-precision 64-bit floating-point values to ensure numerical consistency across platforms."
    )
    add_bullet(
        doc,
        "3. Target Variable Stratification: ",
        "The target variable `num` in the raw dataset represents five ordinal categories: 0 (no significant stenosis) and 1, 2, 3, 4 (increasing angiographic severity stages). For binary diagnosis, the target is partitioned into $y_{\\text{binary}} = (y_{\\text{multi}} > 0) \\in \\{0, 1\\}$, while multi-class severity retains all five ordinal levels."
    )

    # 3.6 Feature Engineering
    add_section_heading(doc, "3.6", "Feature Engineering")
    add_paragraph(
        doc,
        "A critical engineering requirement for LightGBM models serialized with booster categoricals is strict categorical type alignment. "
        "As implemented in `MLModelService._prepare_lgbm_dataframe()`, input dictionaries are dynamically mapped to exact pandas `CategoricalDtype` structures:"
    )
    add_bullet(
        doc,
        "Categorical Alignment: ",
        "The model's underlying booster object exposes `model._Booster.pandas_categorical` across eight specific columns: `['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']`. When receiving client requests, raw values (such as text strings 'Typical Angina' or numeric 0-indexed values) are mapped directly to the booster's category values: `cp` mapped to `[1, 2, 3, 4]`, `slope` mapped to `[1, 2, 3]`, and `thal` mapped to `[3.0, 6.0, 7.0]`."
    )
    add_bullet(
        doc,
        "Biomarker Aliasing: ",
        "To accommodate both clinical laboratory terminology and standard Cleveland dataset nomenclature, the Pydantic input schema (`PatientInput`) provides bidirectional alias resolution: `systolic_bp` aliases to `trestbps`, `cholesterol` aliases to `chol`, `resting_ecg` aliases to `restecg`, and `st_depression` aliases to `oldpeak`."
    )
    add_bullet(
        doc,
        "Cardiorenal Telemetry Integration: ",
        "In addition to the 13 Cleveland features, the system computes Body Mass Index (BMI) using the standard Quetelet formula: $\\text{BMI} = \\frac{\\text{Weight (kg)}}{(\\text{Height (m)})^2}$, categorizing patients into Underweight ($<18.5$), Normal ($18.5–24.9$), Overweight ($25–29.9$), and Obese ($\\ge 30$)."
    )

    # 3.7 Machine Learning Methodology
    add_section_heading(doc, "3.7", "Machine Learning Methodology")
    add_paragraph(
        doc,
        "The core predictive algorithm employed in HeartCare AI is the Light Gradient Boosting Machine (LightGBM) classifier, stored in serialized format as "
        "`backend/app/ml/saved_models/best_lgbm_3m_model.joblib`. LightGBM builds an ensemble of shallow decision trees in a sequential boosting framework:"
    )
    add_paragraph(
        doc,
        "At each boosting iteration $m$, given training dataset $\\mathcal{D} = \\{(x_i, y_i)\\}_{i=1}^N$ and current ensemble prediction $F_{m-1}(x)$, the algorithm "
        "fits a new decision tree $h_m(x)$ to minimize a differentiable multi-class loss function $\\mathcal{L}(y, F(x))$:"
    )
    add_paragraph(
        doc,
        "$$F_m(x) = F_{m-1}(x) + \\eta \\cdot h_m(x)$$"
    )
    add_paragraph(
        doc,
        "where $\\eta \\in (0, 1]$ represents the learning rate. LightGBM distinguishes itself from conventional tree ensembles through two core mechanisms:"
    )
    add_bullet(
        doc,
        "1. Leaf-Wise (Best-First) Tree Growth: ",
        "Unlike standard level-wise tree growth (which splits all nodes at a given depth simultaneously), LightGBM chooses the leaf that produces the maximum reduction in loss (maximum $\\Delta \\mathcal{L}$), resulting in deeper, asymmetric trees that achieve lower loss with fewer leaves."
    )
    add_bullet(
        doc,
        "2. Gradient-based One-Side Sampling (GOSS): ",
        "GOSS sorts instances by absolute gradient magnitude $|g_i|$. It retains the top $a \\times 100\\%$ instances with large gradients and randomly samples a subset $b \\times 100\\%$ from the remaining instances with small gradients, weighting the small-gradient subset by $\\frac{1-a}{b}$ to preserve the original data distribution without loss of accuracy."
    )

    # 3.8 Model Training and Evaluation
    add_section_heading(doc, "3.8", "Model Training and Evaluation")
    add_paragraph(
        doc,
        "The LightGBM model outputs a multi-class probability distribution vector across all five disease severity stages: "
        "$$\\mathbf{P} = [P(\\text{Stage 0: Healthy}), P(\\text{Stage 1: Mild}), P(\\text{Stage 2: Moderate}), P(\\text{Stage 3: Severe}), P(\\text{Stage 4: Critical})]$$"
    )
    add_paragraph(
        doc,
        "In clinical practice, the primary screening determination is binary: does the patient have significant cardiovascular pathology ($P(\\text{Disease}) > 0.5$)? "
        "The composite cardiovascular risk probability is derived as the complementary probability of being completely disease-free (Stage 0):"
    )
    add_paragraph(
        doc,
        "$$P(\\text{Disease Risk}) = 1.0 - P(\\text{Stage 0: Healthy})$$"
    )
    add_paragraph(
        doc,
        "To ensure numerical stability and avoid extreme boundary overconfidence, the disease probability is bounded within $[0.02, 0.98]$:"
    )
    add_paragraph(
        doc,
        "$$\\text{Risk Score} = \\text{round}\\Big(\\min\\big(0.98, \\max(0.02, P(\\text{Disease Risk}))\\big) \\times 100\\Big)$$"
    )
    add_paragraph(
        doc,
        "$$\\text{Heart Health Score} = \\max(0, 100 - \\text{Risk Score})$$"
    )
    add_paragraph(
        doc,
        "Risk levels are subsequently categorized into four clinical tiers based on predicted class and risk percentage:"
    )
    add_bullet(doc, "Low Risk (Normal Baseline): ", "Predicted Class = 0 and Risk Score < 30%. Routine annual monitoring.")
    add_bullet(doc, "Moderate Risk (Stage 1 Indicator): ", "Predicted Class = 1 or Risk Score between 30% and 54%. Outpatient lifestyle and medical follow-up.")
    add_bullet(doc, "High Risk (Stage 2 Marker): ", "Predicted Class = 2 or Risk Score between 55% and 74%. Comprehensive cardiology consultation and diagnostic stress imaging.")
    add_bullet(doc, "Critical Risk (Stage 3/4 Severity): ", "Predicted Class >= 3 or Risk Score >= 75%. Urgent clinical triage and emergency evaluation.")

    # 3.9 Explainable AI Methodology
    add_section_heading(doc, "3.9", "Explainable AI Methodology")
    add_paragraph(
        doc,
        "To overcome the clinical opacity of gradient boosting, HeartCare AI implements a two-tier explainability methodology:"
    )
    add_bullet(
        doc,
        "1. Dynamic Clinical Heuristic Attribution (`clinical_engine.py`): ",
        "Every biomarker is individually evaluated against ACC/AHA clinical reference thresholds. If a biomarker deviates into an unhealthy zone (e.g., SBP >= 160 mmHg, EF < 35%, or ST depression > 2.0 mm), the engine generates an explicit `FeatureImpact` record containing an impact score (e.g., +26 points), severity flag ('critical'), direction ('increases_risk'), and a clinical explanation narrative."
    )
    add_bullet(
        doc,
        "2. Protective Factor Recognition: ",
        "Conversely, if a patient exhibits favorable biomarkers (e.g., EF >= 55%, optimal BP <= 120/80 mmHg, or active physical exercise), the engine recognizes these as protective factors (e.g., -12 points), visually rendering them in green on the patient dashboard to encourage ongoing healthy lifestyle adherence."
    )

    # 3.10 Backend and Frontend Workflow
    add_section_heading(doc, "3.10", "Backend and Frontend Workflow")
    add_paragraph(
        doc,
        "The interaction between frontend and backend is orchestrated through asynchronous REST JSON contracts:"
    )
    add_bullet(
        doc,
        "Asynchronous FastAPI Routing: ",
        "FastAPI handles requests via non-blocking async coroutines. Lifespan event managers initialize the MongoDB connection pool and verify LightGBM model readiness upon server boot."
    )
    add_bullet(
        doc,
        "Client Timeout & Fallback Protection (`api.js`): ",
        "All frontend requests to `/api/predict` are wrapped in an `AbortController` with a 6-second timeout threshold. If network transit fails or times out, the client invokes `localFallbackPrediction()`, executing client-side risk estimation so the user is never confronted with an unhandled exception or blank screen."
    )

    # 3.11 Database Workflow
    add_section_heading(doc, "3.11", "Database Workflow")
    add_paragraph(
        doc,
        "The data layer is managed via a thread-safe singleton `MongoClient` connection pool (`backend/app/db/database.py`). "
        "Upon initialization (`init_db()`), the system sends an administrative ping to verify connectivity and ensures unique indexes across four collections: "
        "`users` (unique index on `email`, `id`), `assessments` (indexes on `id`, `user_email`, `timestamp`), `hospitals` (indexes on `id`, `city`, `name`), "
        "and `appointments` (unique index on `booking_id`)."
    )
    add_paragraph(
        doc,
        "A legacy migration script (`migrate_sqlite_to_mongodb.py`) successfully migrated 19 user accounts, 35 historical assessment records, "
        "and 23 verified Indian premier cardiology centers from the original SQLite file (`heartcare.db`) to the production MongoDB Atlas cloud cluster."
    )

    # 3.12 Overall System Flow
    add_section_heading(doc, "3.12", "Overall System Flow")
    add_paragraph(
        doc,
        "The complete end-to-end clinical workflow follows a seamless path: a user authenticates via `/api/auth`, enters 13 clinical biomarkers via the multi-step "
        "assessment wizard (`NewPrediction.jsx`), receives calibrated ML probabilities and explainability attributions (`PredictionResult.jsx`), explores "
        "interactive What-If lifestyle interventions, reviews longitudinal health trajectories on their dashboard (`Dashboard.jsx`), and if required, "
        "locates the nearest cardiac hospital sorted by GPS distance (`Hospitals.jsx`) and books a consultation."
    )
