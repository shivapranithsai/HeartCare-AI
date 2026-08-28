# HeartCare.AI — Cardiovascular Risk Stratification & Clinical Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://react.dev/)
[![LightGBM](https://img.shields.io/badge/ML-LightGBM%20Classifier-brightgreen.svg)](https://lightgbm.readthedocs.io/)
[![Vite](https://img.shields.io/badge/Bundler-Vite%206-646CFF.svg)](https://vitejs.dev/)
[![Docker](https://img.shields.io/badge/Container-Docker%20Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**HeartCare.AI** is an evidence-based clinical decision support platform for multi-factorial cardiovascular risk prediction and longitudinal patient telemetry. It combines a 13-feature **LightGBM machine learning inference engine** calibrated against established Cleveland & UCI Clinical Heart Failure datasets with a modern, glassmorphic React dashboard, explainable AI (SHAP-style) attribution, interactive What-If simulation, hospital geo-routing, and automated clinical PDF reporting.

---

## Key Capabilities

### 1. Multi-Biomarker Predictive Modeling
- **13 Clinical Features**: Evaluates Age, Sex, Chest Pain Type (`cp`), Resting Blood Pressure (`trestbps`), Serum Cholesterol (`chol`), Fasting Blood Sugar (`fbs`), Resting ECG (`restecg`), Maximum Heart Rate (`thalach`), Exercise Induced Angina (`exang`), ST Depression (`oldpeak`), ST Slope (`slope`), Fluoroscopy Major Vessels (`ca`), and Thallium Stress Scintigraphy (`thal`).
- **High-Accuracy ML Model**: Powered by a trained and calibrated LightGBM model (`best_lgbm_3m_model.joblib`) with automatic fallback to AHA heuristic scoring.

### 2. Personalized Patient Dashboard & Longitudinal Telemetry
- **Individualized Health Scoring**: Computes genuine ML risk percentages (0–100%), Heart Health Scores, and clinical stages for each logged-in user.
- **Biomarker Telemetry Strip**: Displays live systolic/diastolic BP, serum cholesterol, fasting blood sugar, ejection fraction, serum creatinine, and smoking status.
- **Zero-Data State**: Clean, guided onboarding state for new users with one-click diagnostic assessment launch.

### 3. Explainable AI & "What-If" Interventions
- **Biomarker Attribution**: Identifies primary risk drivers (e.g. elevated ST depression, hypertension) alongside protective factors (e.g. optimal ejection fraction).
- **Interactive Simulation**: Allows clinicians and patients to simulate the immediate risk reduction impact of lifestyle and medication adjustments (e.g. lowering systolic BP by 15 mmHg).

### 4. Geo-Proximity Hospital Directory & Emergency Triage
- **Distance & GPS Calculation**: Haversine formula calculation for real-time proximity sorting.
- **Google Maps Navigation**: Verified turn-by-turn directions directly to emergency cardiac centers and specialized institutes across India.

### 5. Automated Clinical PDF Reporting
- **Printable Medical Summaries**: Generates high-resolution clinical PDF reports containing complete biomarker telemetry, risk gauge visualizations, physician review signatures, and QR verification codes.

### 6. Secure Authentication & Session Management
- **Role-Based Workspaces**: Supports physician/clinician and patient profiles with hashed credentials and strict database-level record isolation.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 19, Vite, Recharts, Lucide Icons, Canvas Confetti, Vanilla CSS Design System |
| **Backend API** | Python 3.11+, FastAPI, Uvicorn, Pydantic v2 |
| **Machine Learning** | LightGBM, Scikit-Learn, Pandas, NumPy, Joblib |
| **Persistence** | SQLite with automatic schema initialization (`heart_failure.db`) |
| **Deployment** | Docker, Docker Compose, Nginx, Vercel, Render |

---

## Project Structure

```
heart-failure-prediction/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── analytics.py       # Personalized user analytics & score telemetry
│   │   │   │   ├── auth.py            # User registration & login security
│   │   │   │   ├── history.py         # Assessment history & filtering
│   │   │   │   ├── hospitals.py       # Geo-proximity hospital directory & maps
│   │   │   │   ├── prediction.py      # ML inference pipeline
│   │   │   │   └── reports.py          # Clinical PDF report generator
│   │   │   └── router.py              # Main API router mounting
│   │   ├── core/
│   │   │   └── config.py              # App settings & CORS config
│   │   ├── db/
│   │   │   └── database.py            # SQLite schema & DB connection helpers
│   │   ├── ml/
│   │   │   ├── model_loader.py        # LightGBM model loader & feature engineering
│   │   │   └── saved_models/          # Trained model artifacts (.joblib)
│   │   └── schemas/                   # Pydantic validation schemas
│   ├── tests/                         # Automated test suites
│   ├── Dockerfile                     # Backend Docker container config
│   ├── main.py                        # FastAPI entrypoint
│   └── requirements.txt               # Python package dependencies
│
├── src/                               # React 19 Frontend
│   ├── components/                    # Reusable components (Navbar, Sidebar, RiskGauge, etc.)
│   ├── pages/                         # Core application views (Landing, Dashboard, Hospitals, etc.)
│   ├── services/                      # API client (Unified fetch handler)
│   ├── App.jsx                        # React Router configuration
│   └── main.jsx                       # React entry point
│
├── public/                            # Static public assets & Netlify redirects
├── Dockerfile                         # Frontend multi-stage Nginx Dockerfile
├── docker-compose.yml                 # Full-stack Docker orchestration
├── package.json                       # Frontend dependencies & build scripts
├── vercel.json                        # Vercel SPA routing configuration
└── vite.config.js                     # Vite build configuration
```

---

## Getting Started Locally

### Prerequisites
- **Node.js** (v18 or higher) & **npm**
- **Python** (v3.10 or higher)
- **Git**

---

### Step 1: Clone Repository
```bash
git clone https://github.com/shivapranithsai/HeartCare-AI.git
cd HeartCare-AI
```

---

### Step 2: Set Up Backend
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI backend server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
The backend will start at `http://127.0.0.1:8000`.
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/api/docs`
- **Health Endpoint**: `http://127.0.0.1:8000/api/health`

---

### Step 3: Set Up Frontend
In a new terminal window:
```bash
# Navigate to project root
cd ..

# Install npm packages
npm install

# Start Vite development server
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## Running Automated Tests

Run the backend unit and integration test suite:

```bash
# Test User Dashboard Scores & Scoping
python backend/tests/test_user_dashboard_scores.py

# Test Authentication & Registration Security
python backend/tests/test_auth_enforcement.py

# Test Hospital Haversine Distance & Geo Calculations
python backend/tests/test_distance_calculation.py
```

---

## Deployment

### Option A: Docker Compose (Single Command)
```bash
docker compose up --build -d
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

### Option B: Cloud Hosting (Vercel + Render)
1. **Backend (Render.com)**:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
2. **Frontend (Vercel)**:
   - Root Directory: `./`
   - Framework: `Vite`
   - Environment Variable: `VITE_API_BASE_URL=https://<your-render-app>.onrender.com/api`

---

## API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/predict` | Runs 13-biomarker ML inference and returns risk scores |
| `GET` | `/api/analytics` | Returns user-scoped cardiovascular scores and biomarker telemetry |
| `GET` | `/api/history` | Fetches historical patient assessment timeline |
| `GET` | `/api/hospitals` | Returns nearby hospitals sorted by GPS distance with Google Maps links |
| `POST` | `/api/auth/register` | Registers a new clinical/patient user account |
| `POST` | `/api/auth/login` | Authenticates existing user credentials |
| `GET` | `/api/health` | Service health status and ML model loaded check |

---

## Clinical Disclaimer

> [!WARNING]
> **HeartCare.AI** is designed as a clinical decision support and predictive analytics assistive tool. It is not a replacement for professional clinical judgment, laboratory diagnostic confirmation, or emergency medical response. Always consult a licensed healthcare practitioner for medical diagnosis and treatment planning.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
