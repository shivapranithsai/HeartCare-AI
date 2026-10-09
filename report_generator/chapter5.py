from report_generator.styles import (
    add_chapter_title, add_section_heading, add_subsection_heading,
    add_paragraph, add_bullet, add_styled_table, add_code_block
)

def add_chapter_5(doc):
    """Generates Chapter 5 – Implementation."""
    add_chapter_title(doc, "5", "IMPLEMENTATION")

    # 5.1 Introduction
    add_section_heading(doc, "5.1", "Introduction")
    add_paragraph(
        doc,
        "Implementation translates the architectural diagrams, mathematical formulations, and clinical requirements established in previous chapters "
        "into executable, production-grade software code. The HeartCare AI codebase is organized into a modular full-stack repository comprising an asynchronous "
        "FastAPI backend, a React 19 single-page frontend, a serialized LightGBM machine learning service, a PyMongo connection-pooled database layer, and "
        "geospatial OpenStreetMap services. This chapter examines the concrete implementation details of each subsystem, highlighting key algorithms, code "
        "structures, and architectural patterns."
    )

    # 5.2 Development Environment
    add_section_heading(doc, "5.2", "Development Environment")
    add_paragraph(
        doc,
        "The development and local benchmarking environment was configured using the following software and operating system specifications:"
    )
    add_bullet(doc, "Operating System: ", "Microsoft Windows 11 Enterprise (64-bit) / Linux Ubuntu 22.04 LTS container runtime.")
    add_bullet(doc, "Backend Language Runtime: ", "Python 3.11.8 / Python 3.14.0 with isolated virtual environment (`venv`).")
    add_bullet(doc, "Frontend Language Runtime: ", "Node.js v20.12.0 LTS with Node Package Manager (`npm` v10.5.0).")
    add_bullet(doc, "Integrated Development Environment (IDE): ", "Visual Studio Code with Python, Pylance, ESLint, and Docker extensions.")
    add_bullet(doc, "Version Control System: ", "Git 2.44 with GitHub remote repository (`shivapranithsai/HeartCare-AI`).")

    # 5.3 Technology Stack
    add_section_heading(doc, "5.3", "Technology Stack")
    add_paragraph(
        doc,
        "Table 5.1 enumerates the complete technology stack across all tiers of the HeartCare AI platform."
    )

    headers_tech = ["System Layer", "Technology / Framework", "Version", "Role & Justification"]
    data_tech = [
        ["Frontend Core", "React", "^19.1.0", "Component-based reactive UI rendering, state management with Hooks."],
        ["Frontend Bundler", "Vite", "^6.3.5", "Next-generation ESM development server and optimized rollup production build."],
        ["Client Routing", "React Router DOM", "^7.18.2", "Client-side declarative routing for seamless SPA view navigation."],
        ["Data Visualization", "Recharts", "^3.10.1", "Declarative SVG charting for historical risk trajectories and distributions."],
        ["Iconography", "Lucide React", "^1.34.0", "High-performance medical and UI iconography."],
        ["Backend API Core", "FastAPI", ">=0.110.0", "High-throughput asynchronous ASGI web framework with automatic OpenAPI docs."],
        ["ASGI Server", "Uvicorn", ">=0.28.0", "Lightning-fast ASGI server implementation using `uvloop` and `httptools`."],
        ["Data Validation", "Pydantic", ">=2.6.0", "Fast, runtime data parsing and schema validation using Python type hints."],
        ["ML Ensemble", "LightGBM", ">=4.3.0", "Fast gradient boosting framework with native booster categorical encoding."],
        ["Scientific Computing", "Scikit-Learn / NumPy / Pandas", ">=1.4.0 / >=1.26.0", "Model evaluation metrics, matrix transformations, and tabular manipulation."],
        ["Model Serialization", "Joblib", ">=1.3.2", "Optimized persistence for NumPy-heavy machine learning estimators."],
        ["Cloud Persistence", "MongoDB Atlas / PyMongo", ">=4.6.0", "Scalable cloud NoSQL document store with connection pooling."],
        ["Geospatial Services", "OpenStreetMap / Nominatim", "REST API", "Real-world medical facility discovery, bounding box geocoding."],
        ["Containerization", "Docker & Docker Compose", "v24+", "Multi-stage isolated container orchestration across frontend and backend."]
    ]
    col_widths_tech = [1.2, 1.6, 0.9, 2.55]
    add_styled_table(doc, headers_tech, data_tech, col_widths_tech, "Table 5.1: Complete Development and Deployment Technology Stack")

    # 5.4 Frontend Implementation
    add_section_heading(doc, "5.4", "Frontend Implementation")
    add_paragraph(
        doc,
        "The frontend application (`src/`) is structured around reusable, modular components and dedicated page views styled with a custom "
        "Glassmorphism design system (`src/styles.css`):"
    )
    add_bullet(
        doc,
        "1. Dynamic Animated ECG Waveform Monitor (`src/components/EcgMonitor.jsx`): ",
        "Implements an HTML5 `<canvas>` rendering loop utilizing `window.requestAnimationFrame()`. It calculates authentic cardiac P-Q-R-S-T wave morphology, dynamically adjusting animation sweep speed and cycle frequency to match the patient's current heart rate (BPM)."
    )
    add_bullet(
        doc,
        "2. Radial Risk Gauge Component (`src/components/RiskGauge.jsx`): ",
        "Renders a dynamic SVG circular stroke gauge that computes `strokeDashoffset` based on the 0–100% risk score. The stroke color smoothly interpolates across four risk gradients: Emerald Green (<25%), Amber Yellow (25–50%), Orange (50–75%), and Crimson Red (>75%)."
    )
    add_bullet(
        doc,
        "3. Step-by-Step Diagnostic Form Wizard (`src/pages/NewPrediction.jsx`): ",
        "Organizes 13 clinical biomarkers into intuitive thematic tabs (Vitals, Laboratory Diagnostics, and Lifestyle Indicators). It includes one-click scenario presets (Healthy Athlete, Hypertensive, High-Risk Cardiac, Critical Emergency) allowing instant population of authentic clinical profiles."
    )
    add_bullet(
        doc,
        "4. Master Design System (`src/styles.css`): ",
        "Comprises 80KB of curated Vanilla CSS defining CSS custom property tokens (`--bg-primary`, `--accent-cyan`, `--glass-border`), smooth micro-transitions, responsive flex/grid layouts, and glassmorphic translucent panels with `backdrop-filter: blur(16px)`."
    )

    # 5.5 Backend Implementation
    add_section_heading(doc, "5.5", "Backend Implementation")
    add_paragraph(
        doc,
        "The backend API entry point (`backend/main.py`) initializes the FastAPI application using an asynchronous lifespan context manager. "
        "Listing 5.1 illustrates the application lifecycle initialization and database pool startup."
    )

    code_main = """@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MongoDB Atlas connection pool & verify ML model
    print("[Server Startup] Connecting to MongoDB Atlas cluster...")
    db_ok = init_db()
    if db_ok:
        print("[Server Startup] MongoDB Atlas successfully connected & indexed.")
    else:
        print("[Server Startup] Warning: MongoDB connection deferred.")
    
    print(f"[Server Startup] ML Engine Status: {ml_service.loaded_model_name}")
    yield
    # Shutdown: Close connection pool cleanly
    print("[Server Shutdown] Closing MongoDB connections.")

app = FastAPI(
    title="HeartCare AI Prediction Platform",
    version="1.0.0",
    lifespan=lifespan
)"""
    add_code_block(doc, code_main, "FastAPI Lifespan Startup and Shutdown Context Manager (backend/main.py)")

    add_paragraph(
        doc,
        "Individual route controllers are grouped within `backend/app/api/endpoints/` and registered through the master API router (`backend/app/api/router.py`), "
        "mounting `/auth`, `/predict`, `/simulate`, `/history`, `/analytics`, `/hospitals`, and `/reports` under the `/api` prefix."
    )

    # 5.6 Database Implementation
    add_section_heading(doc, "5.6", "Database Implementation")
    add_paragraph(
        doc,
        "The database layer (`backend/app/db/database.py`) manages connectivity to MongoDB Atlas using PyMongo's connection pooling. "
        "Listing 5.2 displays the singleton connection pool implementation and index creation logic."
    )

    code_db = """def get_mongo_client() -> MongoClient:
    global _mongo_client
    if _mongo_client is None:
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI missing in .env")
        _mongo_client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=8000,
            connectTimeoutMS=8000,
            maxPoolSize=50,
            minPoolSize=5
        )
    return _mongo_client

def init_db():
    db = get_db()
    db.command("ping")
    # Ensure unique indexes
    db.users.create_index("email", unique=True)
    db.users.create_index("id", unique=True)
    db.assessments.create_index("id", unique=True)
    db.assessments.create_index("user_email")
    db.assessments.create_index([("user_email", pymongo.ASCENDING), 
                                 ("timestamp", pymongo.DESCENDING)])
    db.hospitals.create_index("id", unique=True)
    db.hospitals.create_index("city")
    db.appointments.create_index("booking_id", unique=True)
    return True"""
    add_code_block(doc, code_db, "Thread-Safe MongoDB Atlas Connection Pool & Index Initialization (database.py)")

    # 5.7 Machine Learning Implementation
    add_section_heading(doc, "5.7", "Machine Learning Implementation")
    add_paragraph(
        doc,
        "The machine learning inference service (`backend/app/ml/model_loader.py`) implements the `MLModelService` class. "
        "Upon initialization, the service scans `backend/app/ml/saved_models/` for `best_lgbm_3m_model.joblib`. "
        "When detected, Joblib deserializes the model into memory and inspects the booster's categorical encoding parameters:"
    )

    code_ml_load = """# Inspect LightGBM Booster for exact pandas categorical codes
if hasattr(self.model, "_Booster") and hasattr(self.model._Booster, "pandas_categorical"):
    self.cat_categories = self.model._Booster.pandas_categorical
    self.is_custom_loaded = True
    self.loaded_model_name = "Trained LightGBM Classifier (best_lgbm_3m_model.joblib)"
    print(f"[ML Service] Successfully loaded LightGBM model with {len(self.cat_categories)} categoricals.")"""
    add_code_block(doc, code_ml_load, "Booster Categorical Inspection and Initialization (model_loader.py)")

    # 5.8 Model Prediction Process
    add_section_heading(doc, "5.8", "Model Prediction Process")
    add_paragraph(
        doc,
        "When executing predictions (`predict()`), input data is converted into a single-row pandas DataFrame matching the exact categorical types "
        "expected by the booster. Listing 5.3 shows the feature vector preparation and probability inference pipeline."
    )

    code_pred = """def predict(self, data: PatientInput) -> PredictionResponse:
    # 1. Baseline explainability from clinical heuristic engine
    analysis = run_clinical_heuristic_model(data)

    if self.is_custom_loaded and self.model is not None:
        try:
            df = self._prepare_lgbm_dataframe(data)
            # Multi-class probability distribution: [P(Stage 0), P(Stage 1), ..., P(Stage 4)]
            prob_dist = self.model.predict_proba(df)[0]
            pred_class = int(self.model.predict(df)[0])
            
            # Disease probability = 1.0 - P(Stage 0: Healthy)
            disease_prob = float(1.0 - prob_dist[0])
            disease_prob = max(0.02, min(0.98, disease_prob))
            
            risk_score = int(round(disease_prob * 100))
            analysis["risk_score"] = risk_score
            analysis["probability_percentage"] = round(disease_prob * 100, 1)
            analysis["heart_health_score"] = max(0, 100 - risk_score)
            analysis["model_source"] = self.loaded_model_name
        except Exception as e:
            print(f"[ML Inference Error] {e}. Falling back to Clinical AI Engine.")
            analysis["model_source"] = "AHA/Cleveland Clinical AI Heuristic Engine"

    recommendations = generate_recommendations(data, analysis)
    return PredictionResponse(...)"""
    add_code_block(doc, code_pred, "LightGBM Probability Extraction and Fallback Handling (model_loader.py)")

    # 5.9 Explainable AI Implementation
    add_section_heading(doc, "5.9", "Explainable AI Implementation")
    add_paragraph(
        doc,
        "Explainable AI is implemented through deterministic clinical heuristic scoring in `backend/app/ml/clinical_engine.py`. "
        "The engine calculates baseline log-odds (-2.8) and systematically evaluates biomarker deviations, appending `FeatureImpact` objects. "
        "For example, an ejection fraction below 35% triggers a critical risk impact of +35 points with an explanation of severe systolic dysfunction, "
        "while an ejection fraction >= 55% appends a protective impact of -12 points."
    )

    # 5.10 Feature Implementation
    add_section_heading(doc, "5.10", "Feature Implementation")
    add_paragraph(
        doc,
        "Key user-facing features implemented across the application include:"
    )
    add_bullet(
        doc,
        "What-If Dynamic Intervention Simulator (`/api/simulate`): ",
        "Allows users to adjust physiological sliders (e.g., lowering systolic blood pressure from 165 to 125 mmHg, increasing ejection fraction, or toggling smoking status). The backend evaluates both baseline and modified inputs, calculating the net risk score difference and improvement status ('improved' or 'worsened')."
    )
    add_bullet(
        doc,
        "Live Geospatial Proximity Radar (`backend/app/services/live_hospitals.py`): ",
        "Calculates geodetic distances using the spherical Haversine formula and queries OpenStreetMap Nominatim/Overpass within a dynamic bounding box. If GPS is unavailable, it queries the 23 pre-seeded Indian super-speciality centers."
    )
    add_bullet(
        doc,
        "Official Medical Report Viewer (`src/pages/Reports.jsx`): ",
        "Compiles complete patient assessment history into an official hospital letterhead layout ready for browser printing or PDF saving, containing physician review signature blocks and QR verification badges."
    )

    # 5.11 API Integration
    add_section_heading(doc, "5.11", "API Integration")
    add_paragraph(
        doc,
        "On the frontend, all API interactions are centralized within `src/services/api.js`. The client enforces an `AbortController` timeout "
        "of 6000ms. If network transit times out or fails, the client automatically executes `localFallbackPrediction()`, calculating immediate "
        "heuristic risk scores so the user interface never freezes."
    )

    # 5.12 Frontend-Backend Integration
    add_section_heading(doc, "5.12", "Frontend-Backend Integration")
    add_paragraph(
        doc,
        "Frontend-backend communication is bound through Cross-Origin Resource Sharing (CORS) middleware configured in FastAPI: "
        "`allow_origins=['*']`, `allow_credentials=True`, `allow_methods=['*']`, `allow_headers=['*']`. "
        "The frontend dynamically retrieves the API base URL from the `VITE_API_BASE_URL` environment variable, defaulting to `http://127.0.0.1:8000/api` "
        "in local development and pointing to the production Render URL (`https://heartcare-ai-kcjl.onrender.com/api`) in cloud deployment."
    )

    # 5.13 Implementation Summary
    add_section_heading(doc, "5.13", "Implementation Summary")
    add_paragraph(
        doc,
        "This chapter reviewed the comprehensive implementation of the HeartCare AI codebase. The architecture achieves tight synergy between "
        "modern reactive web design (React 19), high-performance asynchronous API services (FastAPI), resilient machine learning inference (LightGBM with "
        "clinical fallback), scalable cloud persistence (MongoDB Atlas), and live geospatial navigation (OpenStreetMap). The following chapter presents "
        "the empirical result analysis and model evaluation metrics."
    )
