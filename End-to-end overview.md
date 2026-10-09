# HeartCare AI: Comprehensive End-to-End System & Codebase Architecture

> **Project Name**: HeartCare AI - Clinical Heart Failure Risk Prediction & Cardiology Care Platform  
> **Backend Engine**: Python 3.11/3.14 + FastAPI + LightGBM + Scikit-Learn + PyMongo  
> **Database**: MongoDB Atlas (Cloud Cluster: `heartcare` database)  
> **Frontend Engine**: React 18 + Vite + Modern Vanilla CSS Glassmorphism Design System  
> **Geospatial Engine**: OpenStreetMap (OSM Overpass API) + Nominatim Geocoding + Geodesic Haversine Computation  
> **Deployment Infrastructure**: Render (Docker Backend) + Vercel (Frontend SPA)

---

## Table of Contents
1. [Executive Summary & System Architecture](#1-executive-summary--system-architecture)
2. [Data Layer & MongoDB Atlas Architecture](#2-data-layer--mongodb-atlas-architecture)
3. [Machine Learning & Clinical Intelligence Engine](#3-machine-learning--clinical-intelligence-engine)
4. [Backend API Architecture & Function Breakdown](#4-backend-api-architecture--function-breakdown)
5. [Geospatial & Proximity Services](#5-geospatial--proximity-services)
6. [Frontend UI/UX Architecture & Components](#6-frontend-uiux-architecture--components)
7. [API Client & Fallback Engine](#7-api-client--fallback-engine)
8. [Automated Testing & Quality Assurance](#8-automated-testing--quality-assurance)
9. [Security, Configuration & Cloud Deployment](#9-security-configuration--cloud-deployment)

---

## 1. Executive Summary & System Architecture

HeartCare AI is a full-stack clinical intelligence platform built to evaluate cardiovascular health, predict heart failure risk, provide what-if intervention simulations, track personalized longitudinal cardiac trends, generate clinical letterhead reports, and navigate patients to the nearest verified cardiology super-speciality centers.

```
+-----------------------------------------------------------------------------------+
|                                  USER INTERFACE                                    |
|              React 18 + Vite SPA (Vercel) with Glassmorphism Design                |
|  - Landing Page     - Authentication   - Clinical Dashboard   - Assessment Form   |
|  - What-If Engine   - History Table    - Hospital Locator     - Medical Reports   |
+-----------------------------------------+-----------------------------------------+
                                          | HTTPS / REST JSON
                                          v
+-----------------------------------------------------------------------------------+
|                                FASTAPI BACKEND                                    |
|                      Uvicorn ASGI Server (Render Docker)                          |
|  +-----------------------------------------------------------------------------+  |
|  | Routers: /auth, /predict, /simulate, /history, /analytics, /hospitals, /reports |
|  +-----------------------------------------------------------------------------+  |
|         |                                 |                             |         |
|         v                                 v                             v         |
|  +--------------+               +-------------------+           +--------------+  |
|  |  ML Service  |               |  MongoDB Atlas    |           | Geospatial   |  |
|  |  LightGBM    |               |  Singleton Driver |           | OSM Overpass |  |
|  |  Cleveland   |               |  users / history  |           | Haversine    |  |
|  |  Heuristics  |               |  hospitals / appt |           | Geocoding    |  |
|  +--------------+               +-------------------+           +--------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Data Layer & MongoDB Atlas Architecture

### 2.1 Connection Management (`backend/app/db/database.py`)
- **`get_mongo_client() -> MongoClient`**:
  - Implements a thread-safe singleton connection pool (`maxPoolSize=50`, `minPoolSize=5`, `serverSelectionTimeoutMS=8000`).
  - Reuses connections across concurrent requests to avoid connection thrashing and socket exhaustion.
- **`get_db() -> Database`**:
  - Accesses the active database instance configured by `MONGODB_DB_NAME` (default: `heartcare`).
- **`init_db() -> bool`**:
  - Executes during server startup.
  - Sends a `ping` command to verify connectivity.
  - Ensures necessary indexes across all collections.
  - Auto-seeds initial administrative/patient accounts and 23 Indian cardiology centers if collections are empty.
- **`hash_password(password: str) -> str`**:
  - Generates a SHA-256 salted hash (`heartcare_secure_salt_v1`) for secure authentication.

### 2.2 Collections & Schema Design

#### 1. `users` Collection
Stores clinical and patient accounts.
- **Fields**:
  - `id` *(String, Unique)*: e.g., `"USER-001"`, `"USER-E2FA531C"`
  - `email` *(String, Unique, Indexed)*: Lowercase user email.
  - `password_hash` *(String)*: Salted SHA-256 hash.
  - `name` *(String)*: Full name with credentials (e.g., `"Dr. Rajesh Sharma, MD, DM"`).
  - `role` *(String)*: `"Cardiologist / Physician"`, `"Patient / Individual User"`, etc.
  - `created_at` *(String)*: ISO formatted timestamp.
  - `last_login` *(String)*: Timestamp of the most recent authentication.

#### 2. `assessments` Collection
Stores historical evaluations, clinical biomarkers, ML probabilities, and explanation payloads.
- **Fields**:
  - `id` *(String, Unique, Indexed)*: e.g., `"PRED-A1B2C3D4"`
  - `user_email` *(String, Indexed)*: Owner of the record (enables strict user isolation).
  - `patient_name` *(String)*: Patient name.
  - `timestamp` *(String, Indexed)*: Assessment datetime.
  - `age` *(Integer)*, `gender` *(String)*
  - `risk_score` *(Integer, 0-100)*, `risk_level` *(String)*: Low, Moderate, High, Critical.
  - `probability_percentage` *(Float)*, `heart_health_score` *(Integer, 0-100)*
  - `systolic_bp` *(Integer)*, `diastolic_bp` *(Integer)*, `cholesterol` *(Integer)*
  - `ejection_fraction` *(Integer)*, `serum_creatinine` *(Float)*, `smoking` *(String)*, `chest_pain` *(String)*
  - `model_source` *(String)*: `"Trained LightGBM Classifier"` or `"AHA/Cleveland Clinical Engine"`
  - `summary_message` *(String)*: Clinical summary statement.
  - `input_data` *(Object)*: Full serialized patient input.
  - `response_data` *(Object)*: Comprehensive output including risk factors, protective factors, recommendations, and BMI metrics.

#### 3. `hospitals` Collection
Stores verified premier cardiology and rapid chest pain centers.
- **Fields**:
  - `id` *(String, Unique)*: e.g., `"IN-HOSP-01"`
  - `name` *(String, Indexed)*: Hospital name (e.g., `"AIIMS New Delhi"`).
  - `city` *(String, Indexed)*: City name.
  - `address` *(String)*, `phone` *(String)*
  - `rating` *(Float)*, `review_count` *(Integer)*
  - `emergency_available` *(Boolean)*: 24/7 cardiac ICU availability.
  - `specialties` *(String or Array)*: Key clinical procedures.
  - `latitude` *(Float)*, `longitude` *(Float)*: Verified GPS coordinates for Haversine distance.

#### 4. `appointments` Collection
Stores cardiology consultation appointments booked through the platform.
- **Fields**:
  - `booking_id` *(String, Unique, Indexed)*: e.g., `"APPT-9E3F8120"`
  - `hospital_id` *(String, Indexed)*: Target hospital ID.
  - `patient_name` *(String)*, `contact_phone` *(String)*
  - `preferred_date` *(String)*, `reason_for_visit` *(String)*
  - `created_at` *(String)*, `status` *(String: `"confirmed"`)*

### 2.3 Migration Engine (`backend/migrate_sqlite_to_mongodb.py`)
- Standalone pipeline that reads legacy SQLite database (`backend/data/heartcare.db`).
- Deserializes stored JSON strings into native MongoDB BSON subdocuments.
- Upserts all 19 Users, 35 Assessments, and 23 Hospitals to MongoDB Atlas.

---

## 3. Machine Learning & Clinical Intelligence Engine

### 3.1 Model Loader & Inference Service (`backend/app/ml/model_loader.py`)
- **Class**: `MLModelService`
  - **`_try_load_custom_model()`**: Automatically scans `backend/app/ml/saved_models/` for `best_lgbm_3m_model.joblib`.
  - **`predict(data: PatientInput) -> PredictionResponse`**:
    - Constructs a structured pandas DataFrame with 13 Cleveland clinical features:
      `[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]`
    - Categorical feature encoding mapping:
      - `sex`: 0 (Female), 1 (Male)
      - `cp`: 1 (Typical Angina), 2 (Atypical Angina), 3 (Non-anginal), 4 (Asymptomatic)
      - `fbs`: 0 ($\le 120$ mg/dL), 1 ($> 120$ mg/dL)
      - `restecg`: 0 (Normal), 1 (ST-T abnormality), 2 (LVH)
      - `exang`: 0 (No), 1 (Yes)
      - `slope`: 1 (Upsloping), 2 (Flat), 3 (Downsloping)
      - `ca`: 0.0 - 3.0 (Major vessels colored by fluoroscopy)
      - `thal`: 3.0 (Normal), 6.0 (Fixed defect), 7.0 (Reversible defect)
    - If LightGBM model is active, calls `model.predict_proba(df)` to obtain positive class risk probability.
    - If custom model is not present, falls back gracefully to the AHA/Cleveland heuristic engine.
    - Integrates extended clinical biomarkers (Ejection Fraction $< 40\%$, Serum Creatinine $> 1.4$ mg/dL, Active Smoking).
    - Computes `heart_health_score = max(5, min(98, 100 - risk_score + protective_bonus))`.
    - Generates personalized risk factor contributions, protective factors, and clinical recommendations.

### 3.2 Clinical Heuristic Engine (`backend/app/ml/clinical_engine.py`)
- **`run_clinical_heuristic_model(data: PatientInput)`**:
  - Implements an evidence-based risk scoring algorithm based on the Framingham & ACC/AHA cardiovascular guidelines.
  - Scores age, blood pressure stage, cholesterol thresholds, ST-segment depression, max heart rate deficit, ejection fraction impairment, and renal markers.
  - Returns risk category (`"Low Risk"`, `"Moderate Risk"`, `"High Risk"`, `"Critical Risk"`).

### 3.3 Recommendation Engine (`backend/app/ml/recommendations.py`)
- **`generate_recommendations(risk_level, top_factors, patient_data)`**:
  - Formulates actionable medical guidance across 4 pillars:
    1. **Emergency & Urgent Interventions** (e.g., immediate cardiology referral for Critical Risk).
    2. **Diagnostic Follow-ups** (e.g., 2D-Echocardiogram, Coronary Angiography, Holter monitoring).
    3. **Medication & Therapeutic Regimens** (e.g., ACE inhibitors/ARBs, Beta-blockers, Statins).
    4. **Lifestyle & Dietary Protocols** (e.g., Low-sodium DASH diet, smoking cessation, aerobic cardiac rehabilitation).

---

## 4. Backend API Architecture & Function Breakdown

### 4.1 Server Lifecycle & Base Routes (`backend/main.py`)
- **`lifespan(app: FastAPI)`**: Async context manager initializing the MongoDB Atlas connection pool and logging ML model status on startup.
- **`GET /`**: Returns API metadata, status (`"online"`), version, and ML model status.
- **`GET /api/health`**: Health diagnostic endpoint returning system status, timestamp, ML model loaded flag, and database connection state.

### 4.2 Authentication Router (`backend/app/api/endpoints/auth.py`)
- **`POST /api/auth/register` (`register_user`)**:
  - Validates email and password requirements.
  - Checks MongoDB `users` collection for existing accounts.
  - Creates salted SHA-256 password hash.
  - Inserts new user document into `users` collection.
  - Returns `AuthResponse` with JWT token simulation and sanitized `UserProfile`.
- **`POST /api/auth/login` (`login_user`)**:
  - Looks up user by email in MongoDB.
  - Rejects unregistered users with HTTP 404 (prompting sign up).
  - Validates password hash with HTTP 401 on mismatch.
  - Updates `last_login` timestamp in MongoDB.
  - Returns `AuthResponse` with `UserProfile`.

### 4.3 Prediction & Simulation Router (`backend/app/api/endpoints/predict.py`)
- **`POST /api/predict` (`run_prediction`)**:
  - Receives `PatientInput` with 13 Cleveland features + extended biomarkers.
  - Executes ML inference via `ml_service.predict(data)`.
  - Persists assessment document to MongoDB `assessments` collection scoped by `user_email`.
  - Returns `PredictionResponse` with risk score, probabilities, factor impacts, and recommendations.
- **`POST /api/simulate` (`run_what_if_simulation`)**:
  - Receives `SimulationInput` containing baseline parameters and modified intervention parameters.
  - Computes baseline risk vs. simulated risk after lifestyle/medication changes (e.g., reducing BP from 160 to 120 mmHg, quitting smoking).
  - Returns baseline metrics, simulated metrics, and score differences (`status: "improved" / "worsened"`).

### 4.4 History & Cohort Router (`backend/app/api/endpoints/history.py`)
- **`GET /api/history` (`get_assessment_history`)**:
  - Supports search query across patient name, summary message, and prediction ID (`$regex`).
  - Supports filtering by `risk_level` (`Low`, `Moderate`, `High`, `Critical`).
  - Enforces strict user isolation via `user_email` parameter.
  - Sorts by `timestamp` descending and applies pagination limit.
  - Returns `HistoryListResponse` with total matching count and item list.
- **`POST /api/history/generate-dynamic` (`generate_dynamic_history`)**:
  - Generates realistic synthetic clinical patients across healthy, moderate, high, and critical profiles.
  - Evaluates each with the LightGBM ML model.
  - Performs bulk insert into MongoDB `assessments` collection.
- **`GET /api/history/{id}` (`get_assessment_by_id`)**:
  - Queries MongoDB `assessments` collection for a specific assessment ID.
  - Returns full clinical breakdown and response payload.
- **`DELETE /api/history/{id}` (`delete_assessment`)**:
  - Deletes a specific assessment document from MongoDB.
- **`DELETE /api/history` (`clear_all_history`)**:
  - Clears all assessment documents from MongoDB.

### 4.5 Analytics & Dashboard Router (`backend/app/api/endpoints/analytics.py`)
- **`GET /api/analytics` (`get_analytics_overview`)**:
  - Accepts `user_email` to scope analytics strictly to the authenticated user.
  - Returns `has_assessments: False` with clean zero-state if user has 0 records.
  - Executes MongoDB aggregation pipeline to compute `average_risk_score` and `average_health_score`.
  - Groups assessments by `risk_level` to generate cohort distribution counts.
  - Fetches the user's latest assessment document for real-time dashboard cards.
  - Queries chronological timeline points for historical trajectory graphs.

### 4.6 Hospitals & Appointments Router (`backend/app/api/endpoints/hospitals.py`)
- **`GET /api/hospitals` (`list_hospitals`)**:
  - Accepts optional `city`, `emergency_only`, `user_lat`, `user_lon`, and `radius_km`.
  - **Live Dynamic Branch**: If user coordinates are provided, executes live query via `fetch_live_nearby_hospitals` (OSM Overpass API).
  - **City Geocoding Branch**: If city is provided without GPS, dynamically geocodes city and queries nearby facilities.
  - **Directory Fallback Branch**: Queries MongoDB `hospitals` collection.
  - Computes real-time Haversine distance, travel ETA minutes, and Google Maps direct navigation URLs.
  - Sorts hospitals by distance ascending (nearest first).
- **`POST /api/hospitals/book` (`book_consultation`)**:
  - Receives `AppointmentBookingRequest` (hospital ID, patient name, contact phone, date, notes).
  - Generates unique `booking_id` (`APPT-...`).
  - Persists booking document into MongoDB `appointments` collection.

### 4.7 Medical Reports Router (`backend/app/api/endpoints/reports.py`)
- **`GET /api/reports/{id}` (`generate_clinical_report`)**:
  - Queries MongoDB `assessments` collection by ID.
  - Formats patient vitals, clinical biomarker table, ML risk scores, and summary statements ready for printable hospital letterhead.

---

## 5. Geospatial & Proximity Services (`backend/app/services/live_hospitals.py`)

- **`calculate_haversine_distance(lat1, lon1, lat2, lon2) -> float`**:
  - Calculates the great-circle distance in kilometers between two GPS coordinates using the Haversine formula:
    $$d = 2r \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)$$
    where $r = 6371$ km (Earth radius).
- **`geocode_city(city_name: str) -> Optional[Dict]`**:
  - Interfaces with Nominatim OpenStreetMap geocoding API to resolve city and area names to latitude/longitude coordinates.
- **`fetch_live_nearby_hospitals(user_lat, user_lon, radius_km, emergency_only) -> List[Dict]`**:
  - Queries OpenStreetMap Overpass QL API with bounding box around user coordinates.
  - Filters for `amenity=hospital`, `amenity=clinic`, and `emergency=yes`.
  - Computes real-time distance and ETA for all discovered medical facilities.

---

## 6. Frontend UI/UX Architecture & Components

The frontend is an ultra-modern React SPA built with Vite, utilizing Glassmorphism design tokens, CSS custom properties, and smooth micro-animations.

```
src/
├── assets/             # Brand logos, cardiac icons, illustrations
├── components/
│   ├── EcgMonitor.jsx  # HTML5 Canvas real-time animated ECG cardiac wave visualizer
│   ├── Navbar.jsx      # Navigation bar with connection status & user profile dropdown
│   ├── RiskGauge.jsx   # SVG circular gauge with dynamic gradient risk coloring
│   ├── Sidebar.jsx     # Navigation sidebar with collapse support and role badge
│   └── StatCard.jsx    # Metric card with animated value updates and trend indicators
├── pages/
│   ├── Landing.jsx     # Public landing hero, platform feature cards, CTA
│   ├── Login.jsx       # Authentication page with login/signup toggle & role picker
│   ├── Dashboard.jsx   # Main clinical command center with risk gauges, charts, metrics
│   ├── NewPrediction.jsx # 13-feature clinical assessment input form with smart presets
│   ├── PredictionResult.jsx # Visual risk breakdown, SHAP explanations, recommendations
│   ├── History.jsx     # Longitudinal assessment history table with search & filters
│   ├── Hospitals.jsx   # Geospatial hospital radar, live GPS routing & appointment modal
│   ├── Reports.jsx     # Printable medical letterhead report viewer
│   └── Profile.jsx     # User account management, security credentials, logout
├── services/
│   └── api.js          # Unified API client with timeout handling & fallback calculation
├── utils/
│   └── geo.js          # Browser Geolocation API wrapper for live coordinate capture
├── App.jsx             # React Router v6 routing table
├── main.jsx            # React root entry point
└── styles.css          # Master design system (glassmorphism, typography, animations)
```

### 6.1 Key UI Components
1. **`RiskGauge.jsx`**:
   - Renders an SVG radial stroke gauge.
   - Dynamically interpolates stroke color from Green ($<25\%$) to Amber ($25-50\%$), Orange ($50-75\%$), and Crimson ($>75\%$).
2. **`EcgMonitor.jsx`**:
   - Uses an HTML5 `<canvas>` rendering loop with requestAnimationFrame.
   - Generates authentic P-Q-R-S-T cardiac rhythm waveform animations based on the patient's heart rate.
3. **`NewPrediction.jsx`**:
   - Interactive form supporting all 13 Cleveland clinical metrics (trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal).
   - Includes quick patient scenario presets:
     - *Healthy Athlete Profile*
     - *Moderate Hypertensive Profile*
     - *High-Risk Cardiac Patient*
     - *Critical Emergency Profile*
   - Interactive What-If intervention sliders allowing real-time biomarker adjustments.
4. **`Hospitals.jsx`**:
   - Live GPS locator button that captures browser coordinates (`navigator.geolocation`).
   - Filter by city, distance radius ($5$ km, $15$ km, $50$ km), and 24/7 emergency only.
   - Direct Google Maps routing integration (`maps_url`).
   - In-app modal for booking cardiology consultations.

---

## 7. API Client & Fallback Engine (`src/services/api.js`)

- **`fetchWithTimeout(resource, options)`**:
  - Wraps native `fetch` with an `AbortController` and 6-second timeout.
- **`localFallbackPrediction(input)`**:
  - Resilient client-side fallback heuristic engine.
  - If backend is temporarily unreachable or starting up, computes clinical risk estimates locally so the user experience is never interrupted.
- **Unified Methods**:
  - `authAPI.login()`, `authAPI.register()`, `authAPI.getCurrentUser()`, `authAPI.logout()`
  - `predictAPI.predict()`, `predictAPI.simulate()`
  - `historyAPI.getHistory()`, `historyAPI.generateDynamic()`, `historyAPI.getById()`, `historyAPI.delete()`
  - `analyticsAPI.getOverview()`
  - `hospitalsAPI.list()`, `hospitalsAPI.book()`
  - `reportsAPI.getReport()`

---

## 8. Automated Testing & Quality Assurance

HeartCare AI includes a comprehensive test suite across unit, isolation, and integration dimensions:

```
backend/tests/
├── test_auth_enforcement.py        # Validates registration, duplicate prevention, password validation, 404 rejection
├── test_user_dashboard_scores.py   # Validates User A vs User B data isolation and personalized score calculations
├── test_distance_calculation.py    # Validates Haversine distance accuracy across major Indian cities
├── test_hospitals_geo.py           # Validates proximity sorting, radius filters, and appointment booking
├── test_api_endpoints_direct.py    # Direct router execution suite testing all routes with MongoDB Atlas
└── test_full_suite.py              # End-to-end HTTP integration test suite
```

### Running Test Suites:
```bash
# Run all MongoDB endpoint unit tests
python -m unittest backend/tests/test_api_endpoints_direct.py

# Run auth enforcement, user isolation, and geospatial distance tests
python -m unittest backend/tests/test_auth_enforcement.py backend/tests/test_user_dashboard_scores.py backend/tests/test_distance_calculation.py backend/tests/test_hospitals_geo.py
```

---

## 9. Security, Configuration & Cloud Deployment

### 9.1 Environment Configuration (`.env`)
```ini
# Backend API Base URL for Frontend (React/Vite)
VITE_API_BASE_URL=http://127.0.0.1:8000/api

# Backend Server Configuration
PORT=8000
HOST=127.0.0.1
PROJECT_NAME=HeartCare AI Prediction Platform
VERSION=1.0.0
API_V1_STR=/api

# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://shivavadicherla1085_db_user:wQ37f83iqPwIqiLb@heart-failure.phsnwdd.mongodb.net/heartcare?retryWrites=true&w=majority&appName=heart-failure
MONGODB_DB_NAME=heartcare
```

### 9.2 `.gitignore` Protection
- Ensures sensitive files (`.env`, `.env.*`, `.env.local`) are excluded from Git commits.
- Excludes `node_modules/`, `dist/`, `__pycache__/`, `.venv/`, test coverage, and temporary files.
- Preserves `.env.example` as a public template.

### 9.3 Cloud Deployment Instructions
1. **Render (Backend API)**:
   - Built via Dockerfile (`python:3.11-slim` with `libgomp1` for LightGBM).
   - Set environment variables `MONGODB_URI` and `MONGODB_DB_NAME`.
   - Exposes port 8000.
2. **Vercel (Frontend SPA)**:
   - Configured with `vercel.json` rewrites for React Router client-side routing.
   - Set environment variable `VITE_API_BASE_URL=https://heartcare-ai-kcjl.onrender.com/api`.
   - Deploys static Vite build bundle.

---
*HeartCare AI Platform Architecture Document - Generated for Version 1.0.0*
