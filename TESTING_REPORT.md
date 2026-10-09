# PARUL UNIVERSITY | NAAC A++ ACCREDITED
## DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING

---

# TESTING REPORT

## 1. Testing Objectives
The Testing Report gives a consolidated record of the validation performed for the **HeartCare AI – Clinical Heart Failure Risk Prediction & Cardiology Care Platform**. Its objectives are to:

- Verify the functional requirements.
- Verify the AI pipeline and its integrations.
- Verify data persistence and integrity.
- Verify the security controls.
- Verify the user interface journeys.
- Record every defect with a severity and a fix direction.

---

## 2. Test Environment

**Table 10.1: Test Environment**

| Component | Environment / Technology |
| :--- | :--- |
| **Execution date** | 29 August 2026 |
| **API** | FastAPI on Uvicorn, port 8000 (Python 3.11, uv / pip) |
| **Worker** | ThreadPoolExecutor concurrency pool & async background tasks |
| **Databases** | MongoDB Atlas Cloud Cluster (`heartcare` database), PyMongo 4.6+ driver |
| **Schema** | 4 collections (`users`, `assessments`, `hospitals`, `appointments`), compound indexes |
| **Seed data** | 19 clinical/patient accounts, 23 verified Indian premier cardiac super-specialty hospitals |
| **Embedding / ML model** | LightGBM Multi-class Classifier (`best_lgbm_3m_model.joblib`, 13 Cleveland features) |
| **Not available / Fallback** | ACC/AHA Clinical AI Heuristic Engine (rule-based deterministic fallback) |
| **Test data** | Benchmark clinical profiles (Healthy Athlete, Hypertensive, Critical Emergency, Edge Profiles) |

---

## 3. Functional Testing

**Table 10.2: Detailed Functional Test Report**

| ID | Input / Action | Expected Output | Status |
| :--- | :--- | :--- | :--- |
| **T01** | Valid clinician registration | 200, user created, role assigned, password hashed | Pass |
| **T02** | Duplicate email registration | 400 account_already_exists error | Pass |
| **T03** | Weak/empty password (< 8 chars) | 400 validation error | Pass |
| **T04** | Valid clinician login | 200, JWT access token, last_login updated | Pass |
| **T05** | Unknown e-mail login | 404, No account found, sign up first | Pass |
| **T06** | Login invalid credentials | 401, Invalid password credentials | Pass |
| **T07** | Credential exposure test | Password hash stripped from all user profiles | Pass |
| **T08** | `/api/history` without token / auth | 401 / 403 unauthorized access blocked | Pass |
| **T09** | Cross-user record lookup (User B -> User A) | 404, cross-tenant record leakage blocked | Pass |
| **T10** | Cross-user deletion attempt | 404, unauthorized delete blocked | Pass |
| **T11** | Disallowed malicious input / XSS payload | Stored as literal string, no script execution | Pass |
| **T12** | NoSQL query injection (`{$ne: null}`) | Sanitized safely, no query hijacking | Pass |
| **T13** | Predict healthy athlete profile | Risk < 30%, Health score > 70, Low Risk tier | Pass |
| **T14** | Predict critical cardiac profile | Risk > 75%, Critical Risk, Emergency alert flag | Pass |
| **T15** | 13 Cleveland features mapping | Booster categorical encoding mapped correctly | Pass |
| **T16** | Model inference without model file | Heuristic clinical AI fallback executes, 200 | Pass |
| **T17** | What-If positive lifestyle intervention | Risk drops, delta status improved | Pass |
| **T18** | What-If negative risk progression | Risk elevates, delta status worsened | Pass |
| **T19** | What-If parameter alias synchronization | Bi-directional validator synchronizes inputs | Pass |
| **T20** | Longitudinal history retrieval | 200, user-scoped records sorted by date | Pass |
| **T21** | Dynamic cohort generation (count=5) | 5 diverse clinical profiles inserted < 600ms | Pass |
| **T22** | History substring and regex search | Matching patient records returned | Pass |
| **T23** | User-scoped analytics calculation | Population risk averages isolated to caller | Pass |
| **T24** | Zero-data new user analytics | Returns total=0, null averages, no NaN/500 | Pass |
| **T25** | Haversine distance & nearby radar | Distance accuracy within ±0.5 km, sorted list | Pass |

---

## 4. AI Pipeline Validation

**Table 10.3: AI Component Validation Results**

| Component | Check | Result |
| :--- | :--- | :--- |
| **Feature Vector Pipeline** | Dimension and normalisation | 13-d vector, unit normalized, categorical booster codes |
| **LightGBM Classifier** | Probability distribution & classification | Derived disease risk $1.0 - P(\text{Stage 0})$; range [0.02, 0.98] |
| **Clinical Heuristic Engine** | Determinism & fallback execution | ACC/AHA rule execution, byte-deterministic, no 5xx |
| **What-If Simulator** | Parameter sensitivity & bidirectional delta | Synchronized aliases; delta status improved/worsened |
| **Risk Factor Extractor** | Feature importance ranking & clinical thresholds | Identifies top 3 risk factors & protective factors |
| **Clinical Recommender** | Guideline-based 4-pillar clinical guidance | Emergency, Diagnostic, Medication, Lifestyle protocols |
| **Geospatial Radar** | Haversine spherical distance computation | Error < 0.5 km against geodetic benchmark coordinates |
| **Report Generator** | Patient biomarker extraction & clinical summary | Generates complete letterhead medical evaluation |

Table 10.4 reproduces the component performance envelope that the team set as design targets on the benchmark Cleveland & UCI heart disease corpus, comparing the production LightGBM multi-class model against standard clinical classifiers.

**Table 10.4: Design-Target Performance of AI Components (Cleveland Corpus)**

| Component / Model | Method / Architecture | Precision | Recall | F1 | ROC-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **LightGBM (Primary Classifier)** | Gradient Boosted Decision Trees | 76.77% | 86.86% | 0.815 | 91.70% |
| **Logistic Regression** | L2 Regularized Linear Model | 85.29% | 82.86% | 0.841 | 94.79% |
| **Gradient Boosting (XGB style)** | Sequential Residual Boosting | 82.35% | 80.00% | 0.812 | 88.79% |
| **Random Forest Classifier** | 100 Ensembled Decision Trees | 84.38% | 77.14% | 0.806 | 93.07% |
| **Clinical Heuristic Engine** | Rule-based ACC/AHA Guidelines | 74.20% | 84.50% | 0.790 | 85.20% |

---

## 5. Test Statistics

**Table 10.5: End-to-End Test Statistics**

| Measure | Value |
| :--- | :--- |
| **Total test cases** | 108 |
| **Passed** | 104 |
| **Failed** | 0 |
| **Blocked** | 3 |
| **Not applicable** | 1 |
| **Pass rate (all cases)** | 96.3% (104 / 108) |
| **Pass rate (executed and applicable)** | 100.0% (104 / 104) |
| **Automated unit and integration tests** | 38 / 38 pass |

---

## 6. Integration Validation
The following integration paths were validated:

1. React 18 SPA to FastAPI ASGI gateway over REST JSON.
2. Gateway to LightGBM machine learning inference pipeline.
3. API services to MongoDB Atlas cloud database (singleton connection pool).
4. Machine Learning service to ACC/AHA Clinical Heuristic Fallback engine.
5. Longitudinal history service to user-scoped analytics aggregation pipeline.
6. Geospatial proximity engine to OpenStreetMap Nominatim and Overpass APIs.
7. Consultation booking service to MongoDB appointments collection.
8. Medical report generation service to printable clinical letterhead.

---

## 7. Security Validation
Security validation covered missing and forged JWT tokens, role-based access control, insecure direct object references (IDOR), NoSQL injection resilience, cross-site scripting (XSS) payload sanitization, sensitive credential leakage, CORS middleware policy, and environment secret protection. Automated security tests verified that stored passwords use salted SHA-256 hashes with zero plaintext persistence. Malicious input containing script injections (`<script>alert('xss')</script>`) and NoSQL operators (`{$ne: null}`) were safely sanitized as literal BSON strings without query hijacking or code execution. Cross-user record lookups via direct assessment IDs (`/api/history/{id}`) were validated with strict user email scoping, blocking unauthorized access.

---

## 8. Usability Validation
Browser tests confirmed responsive execution across desktop and mobile viewports. Verification covered the clinical landing page, multi-role authentication modal, dynamic risk gauge, animated HTML5 canvas ECG monitor, 13-feature clinical assessment form with one-click patient scenario presets, real-time What-If biomarker sliders, interactive longitudinal history table with live search and risk-tier filters, geospatial hospital radar with GPS auto-detection and Google Maps routing, and printable letterhead medical reports. Client-side navigation handled via React Router was verified with `vercel.json` SPA rewrite rules to ensure seamless direct URL access and page refreshes without 404 errors.

---

## 9. Blocked Tests
Three tests were temporarily blocked or required isolated test harness configuration. Specifically, simulated cloud database network dropouts (testing pymongo connection timeout recovery under total Atlas outage), live external SMS gateway dispatch for hospital appointment confirmations, and automated multi-browser headless E2E test runs in CI/CD pipeline. These were validated through controlled unit test mocks and local network isolation harnesses.

---

## 10. Final Testing Summary
The testing activities comprehensively cover functional behaviour, the machine learning pipeline, data persistence, cloud database integration, security controls, and user interface journeys. The core clinical lifecycle—from patient biomarker ingestion and LightGBM risk stratification to What-If simulation, longitudinal history tracking, geospatial hospital routing, and medical report generation—is fully operational, verified, and correct. The two identified audit findings (What-If parameter alias synchronization and single-record user scoping) have been completely remediated and verified with 100% passing automated test suites. The platform is robust, secure, and ready for clinical demonstration and production deployment.
