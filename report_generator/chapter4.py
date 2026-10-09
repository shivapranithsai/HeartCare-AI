from report_generator.styles import (
    add_chapter_title, add_section_heading, add_subsection_heading,
    add_paragraph, add_bullet, add_styled_table, add_diagram_box
)

def add_chapter_4(doc):
    """Generates Chapter 4 – System Design."""
    add_chapter_title(doc, "4", "SYSTEM DESIGN")

    # 4.1 Introduction
    add_section_heading(doc, "4.1", "Introduction")
    add_paragraph(
        doc,
        "System design establishes the architectural blueprint, data relationships, component interactions, and interface boundaries required to transform "
        "HeartCare AI's clinical and machine learning objectives into a robust, high-performance software system. A resilient clinical intelligence platform "
        "must satisfy rigorous non-functional constraints regarding data privacy, low-latency inference, fail-safe availability, and intuitive user experience. "
        "This chapter articulates the multi-tier architectural design, functional and non-functional specifications, Use Case and Data Flow models, system flowcharts, "
        "NoSQL database schema structures, and security controls governing the platform."
    )

    # 4.2 System Architecture
    add_section_heading(doc, "4.2", "System Architecture")
    add_paragraph(
        doc,
        "HeartCare AI is architected as a modular, decoupled, multi-tier cloud system consisting of five core architectural layers: the Presentation Tier, "
        "the Application & API Gateway Tier, the Machine Learning Inference Tier, the Cloud Persistence Tier, and the Geospatial Services Tier. "
        "Figure 4.1 illustrates this multi-tier architecture and the communication protocols binding each layer."
    )

    ascii_arch = """
+---------------------------------------------------------------------------------------------------+
|                                      PRESENTATION TIER (SPA)                                      |
|                            React 19 + Vite 6 + Vanilla CSS Glassmorphism                          |
|  [Landing Page]    [Auth View]    [Clinical Dashboard]    [Assessment Form]    [What-If Simulator]|
|  [EcgMonitor (Canvas)]  [RiskGauge (SVG)]  [History Explorer]  [Hospital Radar]  [Medical Reports]|
+-------------------------------------------------+-------------------------------------------------+
                                                  | HTTPS / REST JSON (Timeout: 6000ms)
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                  APPLICATION & API GATEWAY TIER                                   |
|                                 FastAPI (Python 3.11/3.14) + Uvicorn                              |
|   +--------------------------------------------------------------------------------------------+  |
|   |   CORS Middleware  •  Pydantic v2 Validation  •  Salted SHA-256 Authentication  •  Router  |  |
|   |   Endpoints: /auth  •  /predict  •  /simulate  •  /history  •  /analytics  •  /hospitals   |  |
|   +--------------------------------------------------------------------------------------------+  |
|         |                                      |                                    |             |
|         v                                      v                                    v             |
|  +--------------------+             +--------------------+                +--------------------+  |
|  | ML INFERENCE TIER  |             |  PERSISTENCE TIER  |                |  GEOSPATIAL TIER   |  |
|  | LightGBM Classifier|             | MongoDB Atlas      |                | OpenStreetMap      |  |
|  | (best_lgbm_3m.joblib)             | (heartcare cluster)|                | Overpass API       |  |
|  | Heuristic Engine   |             | Singleton Pool     |                | Nominatim Geocoding|  |
|  | Recommendations    |             | users, assessments |                | Haversine Geodesic |  |
|  | What-If Engine     |             | hospitals, appts   |                | Google Maps Routing|  |
|  +--------------------+             +--------------------+                +--------------------+  |
+---------------------------------------------------------------------------------------------------+
"""
    add_diagram_box(doc, ascii_arch, "Multi-Tier Cloud Microservices System Architecture Diagram")

    # 4.3 Architecture Components
    add_section_heading(doc, "4.3", "Architecture Components")
    add_paragraph(
        doc,
        "The system's modular architecture is subdivided into discrete functional subsystems:"
    )
    add_bullet(
        doc,
        "1. Presentation Subsystem (Client UI): ",
        "Engineered as a modern Single-Page Application (SPA) utilizing React 19. It manages local view states, form step wizards, dynamic SVG risk gauge rendering, requestAnimationFrame HTML5 canvas ECG animations, and client-side fallback inference."
    )
    add_bullet(
        doc,
        "2. API Gateway Subsystem (FastAPI): ",
        "Acts as the central orchestrator, executing strict request deserialization via Pydantic v2 schemas, verifying salted password hashes, isolating tenant records via `user_email` query filters, and returning standardized HTTP response envelopes."
    )
    add_bullet(
        doc,
        "3. Machine Learning Subsystem (`MLModelService`): ",
        "Encapsulates model deserialization, categorical feature encoding, multi-class probability scoring, disease risk probability formulation, confidence interval calculation, and dynamic recommendation generation."
    )
    add_bullet(
        doc,
        "4. Persistence Subsystem (`database.py`): ",
        "Implements a thread-safe connection-pooled singleton driver to MongoDB Atlas (`maxPoolSize=50`), guaranteeing transactional safety, index enforcement, and low-latency JSON BSON storage."
    )
    add_bullet(
        doc,
        "5. Geospatial Subsystem (`live_hospitals.py`): ",
        "Interfaces with external OpenStreetMap APIs, computes spherical great-circle distances via the Haversine equation, calculates estimated travel times, and constructs direct turn-by-turn navigation URLs."
    )

    # 4.4 Functional Requirements
    add_section_heading(doc, "4.4", "Functional Requirements")
    add_paragraph(
        doc,
        "Functional requirements define the core operational capabilities and behaviors that HeartCare AI must execute. "
        "Table 4.1 details the twelve functional requirements (FR1 through FR12) implemented in the platform."
    )

    headers_fr = ["Requirement ID", "Functional Requirement Name", "Detailed Operational Description"]
    data_fr = [
        ["FR-01", "User Authentication", "System shall authenticate clinical and patient users with salted SHA-256 password hashing and role assignments."],
        ["FR-02", "13-Biomarker Ingestion", "System shall accept 13 Cleveland clinical features along with cardiorenal markers (EF, Creatinine) via an intuitive form wizard."],
        ["FR-03", "LightGBM ML Inference", "System shall execute trained LightGBM inference, computing multi-class probabilities and overall cardiovascular risk percentages."],
        ["FR-04", "Heuristic Fail-Safe Fallback", "System shall seamlessly execute AHA/Framingham clinical heuristic scoring if custom ML model artifact loading is interrupted."],
        ["FR-05", "Explainable AI Attribution", "System shall decompose predictions into specific risk-increasing drivers and protective factors with clinical explanations."],
        ["FR-06", "What-If Simulation", "System shall allow real-time interactive manipulation of physiological biomarkers (BP, EF, Cholesterol) to project risk score changes."],
        ["FR-07", "Longitudinal Telemetry", "System shall record and display chronological historical assessments and biomarker trends scoped strictly to the authenticated user."],
        ["FR-08", "Dynamic Cohort Generation", "System shall support clinical bulk creation of realistic synthetic patient cohorts across healthy, moderate, and critical profiles."],
        ["FR-09", "Geospatial Hospital Discovery", "System shall dynamically discover nearby cardiac hospitals using browser GPS or city geocoding via OpenStreetMap."],
        ["FR-10", "Haversine Proximity Sorting", "System shall compute exact geodetic distance in kilometers, estimated travel ETA, and sort medical centers nearest-first."],
        ["FR-11", "Consultation Appointment Booking", "System shall accept in-app appointment consultation requests, generate unique booking IDs, and persist records in MongoDB."],
        ["FR-12", "Printable Clinical Reporting", "System shall compile patient vitals, risk gauges, biomarker tables, and physician sign-offs into printable hospital letterhead summaries."]
    ]
    col_widths_fr = [1.2, 1.8, 3.25]
    add_styled_table(doc, headers_fr, data_fr, col_widths_fr, "Table 4.1: Functional Requirements Specification (FR1 to FR12)")

    # 4.5 Non-Functional Requirements
    add_section_heading(doc, "4.5", "Non-Functional Requirements")
    add_paragraph(
        doc,
        "Non-functional requirements define the architectural quality attributes, operational constraints, and performance baselines of the system. "
        "Table 4.2 presents the eight non-functional requirements (NFR1 through NFR8)."
    )

    headers_nfr = ["Requirement ID", "Quality Dimension", "Design Target & Verification Criteria"]
    data_nfr = [
        ["NFR-01", "Inference Latency", "ML prediction endpoint response time shall not exceed 1000ms for 95% of requests (Verified: 559ms concurrent average)."],
        ["NFR-02", "Service Availability", "System shall maintain 99.9% uptime by pairing cloud container hosting with an automatic local heuristic fallback engine."],
        ["NFR-03", "Data Privacy & Isolation", "Assessments and analytics shall be strictly scoped by user email; User A shall never access or view User B's clinical data."],
        ["NFR-04", "Credential Security", "Passwords shall be securely hashed using salted SHA-256 before database insertion; plaintext passwords shall never be persisted or logged."],
        ["NFR-05", "Responsive Usability", "User interface shall maintain responsive layouts across desktop displays (1920x1080), laptops (1366x768), and mobile devices (375x667)."],
        ["NFR-06", "Client-Side Resilience", "Frontend shall enforce a 6000ms API timeout; if backend is unreachable, client-side fallback shall calculate instant local estimates."],
        ["NFR-07", "Input Validation", "All API payloads shall be validated against Pydantic schemas; out-of-range physiological values shall reject with HTTP 400/422."],
        ["NFR-08", "NoSQL Injection Resilience", "System shall sanitize and cast all query parameters; NoSQL operator injection payloads shall be stored as harmless string literals."]
    ]
    col_widths_nfr = [1.2, 1.6, 3.45]
    add_styled_table(doc, headers_nfr, data_nfr, col_widths_nfr, "Table 4.2: Non-Functional Requirements Specification (NFR1 to NFR8)")

    # 4.6 Use Case Diagram
    add_section_heading(doc, "4.6", "Use Case Diagram and Specifications")
    add_paragraph(
        doc,
        "The platform mediates interactions between two primary actors: Attending Clinicians/Cardiologists and Patients/Individual Users, alongside "
        "the System Administrator. Figure 4.2 illustrates the core Use Case interactions."
    )

    ascii_usecase = """
+---------------------------------------------------------------------------------------------------+
|                               HEARTCARE AI SYSTEM BOUNDARY                                        |
|                                                                                                   |
|    +----------------------+                                    +----------------------+           |
|    |      PATIENT         |                                    |      CLINICIAN       |           |
|    +----------+-----------+                                    +----------+-----------+           |
|               |                                                           |                       |
|               |---> (UC-01: Register / Login Account) <-------------------|                       |
|               |                                                           |                       |
|               |---> (UC-02: Input 13 Biomarkers via Form) <---------------|                       |
|               |                                                           |                       |
|               |---> (UC-03: View ML Risk Score & Health Score) <----------|                       |
|               |                                                           |                       |
|               |---> (UC-04: Review Biomarker Impact & Protective Drivers)-|                       |
|               |                                                           |                       |
|               |---> (UC-05: Run Interactive What-If Simulation) <---------|                       |
|               |                                                           |                       |
|               |---> (UC-06: View Longitudinal Dashboard Telemetry) <------|                       |
|               |                                                           |                       |
|               |---> (UC-07: Search & Filter Assessment History) <---------|                       |
|               |                                                           |                       |
|               |---> (UC-08: Locate Nearby Hospitals via GPS Haversine) <--|                       |
|               |                                                           |                       |
|               |---> (UC-09: Book Cardiology Consultation Appointment)     |                       |
|               |                                                           |                       |
|               |---> (UC-10: Generate Printable Medical Letterhead Report) |                       |
|                                                                           |                       |
|                                                   +-----------------------+                       |
|                                                   |---> (UC-11: Generate Dynamic Patient Cohorts) |
|                                                   |---> (UC-12: Delete / Manage Historical Records)|
+---------------------------------------------------------------------------------------------------+
"""
    add_diagram_box(doc, ascii_usecase, "System Use Case Diagram for Clinicians and Patients")

    # 4.7 Data Flow Diagrams
    add_section_heading(doc, "4.7", "Data Flow Diagrams (DFD Level 0 and Level 1)")
    add_paragraph(
        doc,
        "Data Flow Diagrams depict how clinical information flows through the system, undergoes transformation, and persists within datastores. "
        "Figure 4.3 presents the DFD Level 0 Context Diagram, showing high-level information exchanges between external entities and HeartCare AI."
    )

    ascii_dfd0 = """
+-----------------------+                                                       +-----------------------+
|                       | ---------- 1. Credentials (Login/Register) ---------> |                       |
|                       | <--------- 2. Auth Session & Profile ---------------- |                       |
|                       |                                                       |                       |
|                       | ---------- 3. 13 Biomarkers + Cardiorenal Vitals ---> |                       |
|                       | <--------- 4. Risk Score, Impacts & Recommendations - |                       |
|        PATIENT        |                                                       |     HEARTCARE AI      |
|          OR           | ---------- 5. Modified Parameters (What-If) --------> |     CORE SYSTEM       |
|       CLINICIAN       | <--------- 6. Simulated Risk Delta & Status --------- |                       |
|                       |                                                       |                       |
|                       | ---------- 7. GPS Coordinates / City ----------------> |                       |
|                       | <--------- 8. Nearby Hospitals Sorted by Distance --- |                       |
|                       |                                                       |                       |
|                       | ---------- 9. Appointment Booking Request ----------> |                       |
|                       | <--------- 10. Booking Confirmation (APPT-ID) ------- |                       |
+-----------------------+                                                       +-----------+-----------+
                                                                                            |
                                         External Services Communication                    |
                                         11. GPS / Nominatim Overpass Query ----------------+
                                         12. Verified Facilities Geo JSON <-----------------+
                                                                                            |
                                                                                +-----------v-----------+
                                                                                |      OPENSTREETMAP    |
                                                                                |    GEOSPATIAL SERVER  |
                                                                                +-----------------------+
"""
    add_diagram_box(doc, ascii_dfd0, "Data Flow Diagram (DFD Level 0 Context Diagram)")

    add_paragraph(
        doc,
        "Figure 4.4 illustrates the DFD Level 1 Detailed Functional Flow, decomposing the system into distinct internal processing modules: "
        "Authentication Handler (1.0), ML Prediction Engine (2.0), What-If Simulation Engine (3.0), Analytics & Telemetry Aggregator (4.0), "
        "Geospatial Hospital Radar (5.0), and Medical Report Generator (6.0)."
    )

    ascii_dfd1 = """
   +---------------+                     +--------------------+
   |   USER /      |                     |   D1: users        |
   |   CLINICIAN   |                     +---------+----------+
   +---+-------+---+                               ^
       |       |                                   | (Verify / Upsert)
       |       +========> [ 1.0 Auth Handler ] ====+
       |
       +================> [ 2.0 ML Prediction Engine ] =========+===> [ D2: assessments ]
       |                         |                              |
       |                         | (Inference Feature Vector)   | (Persist Telemetry)
       |                         v                              v
       |                  [ LightGBM Model ]           [ 4.0 Analytics & Trends ]
       |                  [ Heuristic Fallback ]                |
       |                                                        v
       +================> [ 3.0 What-If Simulator ]    [ D2: Aggregation Pipeline ]
       |                         |
       |                         v
       |                  [ Delta Calculation ]
       |
       +================> [ 5.0 Hospital Radar ] ====> [ D3: hospitals ]
       |                         |
       |                         +-------------------> [ OpenStreetMap Overpass ]
       |
       +================> [ 6.0 Report Generator ] ==> [ Formatted Letterhead ]
"""
    add_diagram_box(doc, ascii_dfd1, "Data Flow Diagram (DFD Level 1 Detailed Functional Flow)")

    # 4.8 System Flowchart
    add_section_heading(doc, "4.8", "System Flowchart")
    add_paragraph(
        doc,
        "The system flowchart (Figure 4.5) charts the decision-making logic executed when a patient or clinician submits diagnostic data."
    )

    ascii_flowchart = """
                            +-----------------------------------+
                            |           START SESSION           |
                            +-----------------+-----------------+
                                              |
                                              v
                            +-----------------------------------+
                            |   Authenticate User Credentials   |
                            +-----------------+-----------------+
                                              |
                                              v
                            +-----------------------------------+
                            |  Input 13 Cleveland Biomarkers    |
                            |  + EF, Creatinine, Vitals, Smoke  |
                            +-----------------+-----------------+
                                              |
                                              v
                                      /---------------\\
                                     /  Is Custom LGBM \\----- NO -----> [ Run AHA/Framingham Heuristic ]
                                     \\  Model Loaded?  /                 [ Fallback Engine             ]
                                      \\---------------/                                 |
                                              | YES                                     |
                                              v                                         |
                            +-----------------------------------+                       |
                            | Format Pandas DataFrame with      |                       |
                            | Exact Booster Categoricals        |                       |
                            +-----------------+-----------------+                       |
                                              |                                         |
                                              v                                         |
                            +-----------------------------------+                       |
                            | LightGBM predict_proba(df)        |                       |
                            | P(Risk) = 1.0 - P(Stage 0 Healthy)|                       |
                            +-----------------+-----------------+                       |
                                              |                                         |
                                              |<----------------------------------------+
                                              v
                            +-----------------------------------+
                            | Calculate Heart Health Score,     |
                            | Biomarker Impacts & Recommendations|
                            +-----------------+-----------------+
                                              |
                                              v
                            +-----------------------------------+
                            | Persist to MongoDB 'assessments'  |
                            | Scoped by user_email              |
                            +-----------------+-----------------+
                                              |
                                              v
                            +-----------------------------------+
                            | Render Risk Gauge, Waveform ECG,  |
                            | Interactive What-If Simulation    |
                            +-----------------+-----------------+
                                              |
                                      /---------------\\
                                     /   Risk Level    \\----- CRITICAL -> [ Alert Emergency Red Flag ]
                                     \\    Critical?    /                  [ Auto-Trigger Hospital Radar]
                                      \\---------------/                                 |
                                              | LOW / MOD / HIGH                        |
                                              v                                         |
                            +-----------------------------------+                       |
                            | Display Preventative Lifestyle &  |<----------------------+
                            | Outpatient Cardiology Booking     |
                            +-----------------+-----------------+
                                              |
                                              v
                            +-----------------------------------+
                            |            END SESSION            |
                            +-----------------------------------+
"""
    add_diagram_box(doc, ascii_flowchart, "End-to-End Clinical Diagnostic System Flowchart")

    # 4.9 Database Design / ER Diagram
    add_section_heading(doc, "4.9", "Database Design and Entity-Relationship (ER) Schema")
    add_paragraph(
        doc,
        "The data tier is deployed on MongoDB Atlas (`heartcare` database). While MongoDB is document-oriented (NoSQL), the data model enforces "
        "structured schemas, strict typing, and relational foreign references across four core collections: `users`, `assessments`, `hospitals`, "
        "and `appointments`. Figure 4.6 presents the Entity-Relationship architectural model."
    )

    ascii_er = """
+-----------------------------+                 +-----------------------------------+
|            USERS            |                 |            ASSESSMENTS            |
+-----------------------------+                 +-----------------------------------+
| PK  id: String (Unique)     | 1               | PK  id: String (Unique, Indexed)  |
|     email: String (Indexed) +---+           N | FK  user_email: String (Indexed)  |
|     password_hash: String   |   +============>|     patient_name: String          |
|     name: String            |                 |     timestamp: String (Indexed)   |
|     role: String            |                 |     age: Integer, gender: String  |
|     created_at: String      |                 |     risk_score: Integer (0-100)   |
|     last_login: String      |                 |     risk_level: String            |
+-----------------------------+                 |     probability_percentage: Float |
                                                |     heart_health_score: Integer   |
                                                |     systolic_bp: Integer          |
                                                |     cholesterol: Integer          |
                                                |     ejection_fraction: Integer    |
                                                |     serum_creatinine: Float       |
                                                |     model_source: String          |
                                                |     input_data: BSON Object       |
                                                |     response_data: BSON Object    |
                                                +-----------------------------------+

+-----------------------------+                 +-----------------------------------+
|          HOSPITALS          |                 |           APPOINTMENTS            |
+-----------------------------+                 +-----------------------------------+
| PK  id: String (Unique)     | 1             N | PK  booking_id: String (Unique)   |
|     name: String (Indexed)  +---+           +-+ FK  hospital_id: String (Indexed) |
|     city: String (Indexed)  |   +==========>  |     patient_name: String          |
|     address: String         |                 |     contact_phone: String         |
|     phone: String           |                 |     preferred_date: String        |
|     rating: Float           |                 |     reason_for_visit: String      |
|     review_count: Integer   |                 |     created_at: String            |
|     emergency_available: Bool|                |     status: String ('confirmed')  |
|     specialties: Array      |                 +-----------------------------------+
|     latitude: Float (GPS)   |
|     longitude: Float (GPS)  |
+-----------------------------+
"""
    add_diagram_box(doc, ascii_er, "MongoDB Atlas Entity-Relationship (ER) Schema Design")

    # 4.10 Module Design
    add_section_heading(doc, "4.10", "Module Design")
    add_paragraph(
        doc,
        "HeartCare AI enforces high internal cohesion and loose coupling through modular software decomposition:"
    )
    add_bullet(
        doc,
        "Module 1: Authentication Engine (`app/api/endpoints/auth.py`): ",
        "Handles user registration, duplicate email rejection (HTTP 400), password hashing via salted SHA-256, login credential verification, and last-login tracking."
    )
    add_bullet(
        doc,
        "Module 2: Prediction & Simulation Engine (`app/api/endpoints/predict.py`): ",
        "Exposes `/api/predict` for 13-feature ML inference and `/api/simulate` for What-If counterfactual analysis, persisting output payloads to MongoDB."
    )
    add_bullet(
        doc,
        "Module 3: Longitudinal History Engine (`app/api/endpoints/history.py`): ",
        "Implements paginated retrieval, substring regex search across patient names and IDs, risk level filtering, single-record lookup, and dynamic cohort generation."
    )
    add_bullet(
        doc,
        "Module 4: Analytics Aggregation Engine (`app/api/endpoints/analytics.py`): ",
        "Executes MongoDB multi-stage aggregation pipelines to calculate average risk scores, cohort risk distributions, latest biomarker cards, and historical trajectory plots."
    )
    add_bullet(
        doc,
        "Module 5: Geospatial Hospital Directory (`app/api/endpoints/hospitals.py`): ",
        "Resolves user coordinates via OpenStreetMap Nominatim/Overpass or searches the 23-hospital database, computing Haversine distances and managing appointment bookings."
    )
    add_bullet(
        doc,
        "Module 6: Medical Report Generator (`app/api/endpoints/reports.py`): ",
        "Compiles structured patient vitals, clinical summaries, and biomarker tables formatted for printable medical letterheads."
    )

    # 4.11 API Design
    add_section_heading(doc, "4.11", "API Design and Contracts")
    add_paragraph(
        doc,
        "The RESTful API adheres to OpenAPI 3.0 specifications, exposing interactive Swagger documentation at `/api/docs`. "
        "Table 4.3 details the core API endpoints, HTTP methods, and payload structures."
    )

    headers_api = ["HTTP Method", "Endpoint Path", "Request Body / Query Params", "Response Schema", "HTTP Status Codes"]
    data_api = [
        ["POST", "/api/auth/register", "UserRegister (email, name, pwd, role)", "AuthResponse (token, user)", "200 OK, 400 Bad Request"],
        ["POST", "/api/auth/login", "UserLogin (email, password)", "AuthResponse (token, user)", "200 OK, 401 Unauthorized, 404 Not Found"],
        ["POST", "/api/predict", "PatientInput (13 Cleveland + EF, Cr)", "PredictionResponse (score, factors, recs)", "200 OK, 422 Unprocessable"],
        ["POST", "/api/simulate", "SimulationInput (base, modified)", "SimulationResponse (base, sim, delta)", "200 OK, 422 Unprocessable"],
        ["GET", "/api/history", "query, risk_level, user_email, limit", "HistoryListResponse (total, items)", "200 OK"],
        ["POST", "/api/history/generate-dynamic", "count (default: 5), user_email", "Dict (message, generated_count)", "200 OK"],
        ["GET", "/api/history/{id}", "id: String (PRED-xxxxxxxx)", "HistoryItem / Full Analysis", "200 OK, 404 Not Found"],
        ["DELETE", "/api/history/{id}", "id: String (PRED-xxxxxxxx)", "Dict (status: success)", "200 OK, 404 Not Found"],
        ["GET", "/api/analytics", "user_email: String", "AnalyticsOverviewResponse (averages, trends)", "200 OK"],
        ["GET", "/api/hospitals", "city, emergency_only, user_lat, user_lon", "HospitalListResponse (sorted list)", "200 OK"],
        ["POST", "/api/hospitals/book", "AppointmentBookingRequest", "Dict (status, booking_id)", "200 OK, 422 Unprocessable"],
        ["GET", "/api/reports/{id}", "id: String (PRED-xxxxxxxx)", "ClinicalReportResponse (letterhead)", "200 OK, 404 Not Found"],
        ["GET", "/api/health", "None", "HealthResponse (status, db, model)", "200 OK"]
    ]
    col_widths_api = [0.85, 1.6, 1.45, 1.35, 1.0]
    add_styled_table(doc, headers_api, data_api, col_widths_api, "Table 4.3: RESTful API Endpoints and Schema Definitions")

    # 4.12 Security Considerations
    add_section_heading(doc, "4.12", "Security Architecture and Threat Mitigation")
    add_paragraph(
        doc,
        "Given the sensitive nature of clinical telemetry and personal health information (PHI), HeartCare AI incorporates a multi-layer security model:"
    )
    add_bullet(
        doc,
        "Salted Cryptographic Hashing: ",
        "Passwords are never stored in plaintext. Passwords are concatenated with a dedicated system salt (`heartcare_secure_salt_v1`) and hashed using SHA-256 (`hashlib.sha256`). When returning user profiles in JSON payloads, the `password_hash` attribute is stripped."
    )
    add_bullet(
        doc,
        "Strict Cross-User Isolation: ",
        "All historical queries (`/api/history`) and analytics aggregation pipelines (`/api/analytics`) mandate `user_email` scoping. An authenticated user can only view, search, and aggregate their own medical records, preventing horizontal privilege escalation."
    )
    add_bullet(
        doc,
        "NoSQL Injection Mitigation: ",
        "Client inputs are parsed through Pydantic v2 type validators. In MongoDB queries, user inputs are passed as literal parameter values in BSON dictionaries rather than dynamically evaluated strings, neutralising `$ne` or `$gt` operator injection attempts."
    )
    add_bullet(
        doc,
        "Environment Secret Isolation: ",
        "Sensitive cloud credentials (`MONGODB_URI`, `MONGODB_DB_NAME`) are stored in `.env` files protected by `.gitignore` rules. The public repository contains only `.env.example` with sanitized placeholder strings, preventing accidental secret leakage to source control."
    )
