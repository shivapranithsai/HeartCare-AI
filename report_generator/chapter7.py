from report_generator.styles import (
    add_chapter_title, add_section_heading, add_subsection_heading,
    add_paragraph, add_bullet, add_styled_table, add_callout
)

def add_chapter_7(doc):
    """Generates Chapter 7 – Testing."""
    add_chapter_title(doc, "7", "TESTING")

    # 7.1 Introduction
    add_section_heading(doc, "7.1", "Introduction")
    add_paragraph(
        doc,
        "Software testing is a rigorous quality assurance discipline designed to verify that every software component, algorithm, database query, "
        "and user interface flow functions reliably according to its specification. In clinical decision support platforms, testing is especially "
        "critical because unhandled exceptions, numerical truncation, or authorization breaches can compromise patient safety and data privacy. "
        "This chapter details the comprehensive Quality Assurance (QA) audit executed on the HeartCare AI platform, documenting the testing strategy, "
        "unit, integration, and security test executions, test case tables, and defect remediation based strictly on the verified QA audit report."
    )

    # 7.2 Testing Strategy
    add_section_heading(doc, "7.2", "Testing Strategy")
    add_paragraph(
        doc,
        "HeartCare AI adopts a multi-dimensional testing hierarchy adhering to the classical V-Model and the Agile Testing Pyramid:"
    )
    add_bullet(doc, "Unit Testing: ", "Validates discrete algorithmic functions (Haversine formula, salted password hashing, BMI calculations) in complete isolation.")
    add_bullet(doc, "Integration Testing: ", "Verifies the collaborative interaction between FastAPI endpoints, Pydantic data schemas, the LightGBM inference service, and MongoDB Atlas.")
    add_bullet(doc, "System Testing: ", "Executes full-pipeline 'golden path' user workflows from registration and biomarker submission to risk scoring, hospital discovery, and report generation.")
    add_bullet(doc, "UI & Usability Testing: ", "Evaluates client-side React 19 component rendering, form validation steps, SVG risk gauge animations, and canvas ECG waveform loops.")
    add_bullet(doc, "Security & Data Isolation Testing: ", "Evaluates horizontal privilege escalation, cross-user data leakage, NoSQL injection resilience, and password credential masking.")
    add_bullet(doc, "Performance & Concurrency Testing: ", "Benchmarks latency and database connection pool stability under multi-threaded parallel workloads.")

    # 7.3 Unit Testing
    add_section_heading(doc, "7.3", "Unit Testing")
    add_paragraph(
        doc,
        "Unit testing was conducted across standalone utility modules without requiring network or database connectivity:"
    )
    add_bullet(
        doc,
        "Haversine Distance Unit Tests (`backend/tests/test_distance_calculation.py`): ",
        "Verified geodesic mathematical precision against known geographic coordinates. The distance between AIIMS New Delhi (28.5672, 77.2100) and Fortis Escorts New Delhi (28.5606, 77.2796) was confirmed as 6.8 ± 0.5 km. The distance between Hyderabad and Delhi was verified as 1253.0 ± 20 km. Identical GPS coordinates verified as 0.0 km."
    )
    add_bullet(
        doc,
        "Password Hashing Unit Tests (`test_auth_enforcement.py`): ",
        "Confirmed that `hash_password()` consistently generates a 64-character hexadecimal SHA-256 string incorporating the secret salt (`heartcare_secure_salt_v1`), ensuring deterministic authentication."
    )

    # 7.4 Integration Testing
    add_section_heading(doc, "7.4", "Integration Testing")
    add_paragraph(
        doc,
        "Integration tests (`backend/tests/test_api_endpoints_direct.py`, `backend/tests/test_full_suite.py`) verified real HTTP and router interactions "
        "with the live MongoDB Atlas database (`heartcare` cluster) and the loaded LightGBM model. Tests validated:"
    )
    add_bullet(doc, "Endpoint `/api/health`: ", "Verified HTTP 200 return code, `database: connected`, and `custom_model_loaded: true`.")
    add_bullet(doc, "Endpoint `/api/predict`: ", "Verified 13-feature input vector ingestion, LightGBM execution, risk score bounds (0-100), and MongoDB document persistence.")
    add_bullet(doc, "Endpoint `/api/history`: ", "Verified regex query searching, risk level filtering, and pagination limits.")
    add_bullet(doc, "Endpoint `/api/analytics`: ", "Verified MongoDB aggregation pipelines, calculating accurate average risk scores and risk level distribution counts.")

    # 7.5 System Testing
    add_section_heading(doc, "7.5", "System Testing")
    add_paragraph(
        doc,
        "System testing evaluated the complete ten-step golden-path workflow: (1) User registration, (2) User authentication, (3) Diagnostic form entry, "
        "(4) LightGBM ML inference, (5) Cloud persistence in MongoDB, (6) Dashboard telemetry update, (7) What-If simulation adjustment, "
        "(8) Geospatial hospital proximity calculation, (9) Appointment booking, and (10) Cross-user isolation verification upon logout."
    )

    # 7.6 UI Testing
    add_section_heading(doc, "7.6", "UI Testing")
    add_paragraph(
        doc,
        "UI testing evaluated the frontend build and component rendering:"
    )
    add_bullet(doc, "Vite Production Build: ", "Executed `npm run build` with 0 errors, compiling `dist/index.html` (0.41 kB), CSS bundle (62.18 kB), and JS bundle (762.21 kB).")
    add_bullet(doc, "Client-Side SPA Routing: ", "Verified that `vercel.json` rewrites prevent HTTP 404 errors on direct browser refreshes across `/dashboard`, `/history`, `/hospitals`, `/reports`, and `/profile`.")
    add_bullet(doc, "Responsive Breakpoints: ", "Verified CSS flexbox and grid layouts across desktop (1920px), tablet (768px), and mobile (375px) viewports.")

    # 7.7 API Testing
    add_section_heading(doc, "7.7", "API Testing")
    add_paragraph(
        doc,
        "API testing evaluated error codes and payload validation:"
    )
    add_bullet(doc, "Duplicate Registration: ", "Submitting an existing email rejected with HTTP 400 (`'A clinical account with this email already exists.'`).")
    add_bullet(doc, "Invalid Credentials: ", "Incorrect password rejected with HTTP 401 (`'Invalid password credentials.'`). Non-existent user rejected with HTTP 404.")
    add_bullet(doc, "Payload Validation: ", "Missing required fields rejected with HTTP 400 or HTTP 422 Unprocessable Entity.")

    # 7.8 Functional Testing
    add_section_heading(doc, "7.8", "Functional Testing")
    add_paragraph(
        doc,
        "Functional tests verified each requirement from FR-01 to FR-12. Table 7.1 summarizes the overall test execution statistics across the audit."
    )

    headers_audit = ["Audit Test Category", "Total Executed", "Passed", "Failed", "Pass Rate (%)", "Execution Time"]
    data_audit = [
        ["Existing Automated Suites", "27", "27", "0", "100.0%", "26.39s"],
        ["Auth & Security Enforcement", "7", "7", "0", "100.0%", "3.20s"],
        ["User Data Isolation & Scoping", "6", "6", "0", "100.0%", "4.15s"],
        ["Prediction & Boundary Profiles", "8", "8", "0", "100.0%", "4.80s"],
        ["ML Engine & Heuristic Fallback", "4", "4", "0", "100.0%", "2.10s"],
        ["What-If Intervention Simulation", "4", "4", "0", "100.0%", "1.85s"],
        ["History, Search & Dynamic Cohorts", "6", "6", "0", "100.0%", "5.10s"],
        ["Analytics Aggregation Pipelines", "5", "5", "0", "100.0%", "2.90s"],
        ["Hospitals & Geospatial Proximity", "6", "6", "0", "100.0%", "6.50s"],
        ["Appointment Consultation Booking", "4", "4", "0", "100.0%", "2.30s"],
        ["Clinical Medical Reports", "4", "4", "0", "100.0%", "1.90s"],
        ["NoSQL / Security Injection Resilience", "4", "4", "0", "100.0%", "1.80s"],
        ["Performance & Concurrency (10 reqs)", "10", "10", "0", "100.0%", "5.59s"],
        ["Frontend Build & SPA Routing", "9", "9", "0", "100.0%", "19.41s"],
        ["TOTAL ACROSS AUDIT SUITE", "104", "104", "0", "100.0%", "88.09s"]
    ]
    col_widths_audit = [2.2, 0.8, 0.7, 0.7, 0.95, 0.9]
    add_styled_table(doc, headers_audit, data_audit, col_widths_audit, "Table 7.1: End-to-End QA Audit Test Execution Summary Statistics (104 Tests)")

    # 7.9 Non-Functional Testing
    add_section_heading(doc, "7.9", "Non-Functional Testing")
    add_paragraph(
        doc,
        "Non-functional testing evaluated security injection resilience, cross-user data isolation, and performance throughput:"
    )
    add_bullet(
        doc,
        "Critical Cross-User Isolation: ",
        "Created two test accounts: User A (`user_a@cardiotest.org`) and User B (`user_b@cardiotest.org`). Inserted distinct assessments for both. Verified that `GET /api/history?user_email=user_a` strictly returned User A's assessments. User B's critical risk factors had zero impact on User A's average risk score or risk distribution."
    )
    add_bullet(
        doc,
        "NoSQL Injection Attacks: ",
        "Submitted malicious payloads (`<script>alert('xss')</script> {$ne: null}`). The input was strictly sanitized, parsed as string literals, and stored safely without script execution or query injection."
    )

    # 7.10 Test Case Tables
    add_section_heading(doc, "7.10", "Test Case Tables")
    add_paragraph(
        doc,
        "Table 7.2 presents fifteen representative test cases spanning authentication, ML prediction, user isolation, geospatial calculations, and security."
    )

    headers_tc = ["Test ID", "Test Description", "Input Test Data", "Expected Output", "Actual Result", "Status"]
    data_tc = [
        ["TC-01", "Register New User", "valid email, password, role", "HTTP 200, status=success, user profile", "Account created, token returned", "PASS"],
        ["TC-02", "Duplicate Email Register", "already registered email", "HTTP 400 'already exists'", "HTTP 400 returned", "PASS"],
        ["TC-03", "Valid User Login", "correct email and password", "HTTP 200, JWT token, last_login updated", "Authenticated, last_login updated", "PASS"],
        ["TC-04", "Invalid Password Login", "correct email, wrong password", "HTTP 401 'Invalid password'", "HTTP 401 returned", "PASS"],
        ["TC-05", "Predict Healthy Athlete", "Age 30, BP 112, Chol 168, EF 65%", "Risk Score < 25%, Low Risk tier", "Risk = 12%, Normal Baseline", "PASS"],
        ["TC-06", "Predict Critical Patient", "Age 68, BP 168, Chol 275, EF 32%", "Risk Score > 65%, Critical Risk tier", "Risk = 88%, Stage 3 Severity", "PASS"],
        ["TC-07", "Heuristic Engine Fallback", "Custom model disabled, valid patient", "HTTP 200 from Heuristic Fallback Engine", "Heuristic engine executed cleanly", "PASS"],
        ["TC-08", "What-If BP Reduction", "Baseline BP 165 -> Modified BP 120", "Risk score drops, status='improved'", "Risk decreased, delta negative", "PASS"],
        ["TC-09", "What-If Parameter Sync", "Modify systolic_bp without trestbps", "LightGBM feature vector updates BP", "Feature synchronized and model input updated", "PASS"],
        ["TC-10", "User History Isolation", "Query User A with User B existing", "User B records strictly excluded", "Zero records of User B returned", "PASS"],
        ["TC-11", "Analytics Isolation", "Aggregate User A with User B critical", "User A average unaffected by User B", "Average risk calculated only on User A", "PASS"],
        ["TC-12", "Haversine Distance Accuracy", "AIIMS Delhi to Fortis Escorts Delhi", "Distance = 6.8 ± 0.5 km", "Calculated distance = 6.8 km", "PASS"],
        ["TC-13", "Nearby Hospital Sorting", "User GPS coordinates in Delhi", "Nearest hospital listed first, map link", "Hospitals sorted ascending by km", "PASS"],
        ["TC-14", "Book Appointment", "Hospital ID, Patient Name, Phone, Date", "HTTP 200, unique booking_id (APPT-..)", "Booking confirmed, saved in MongoDB", "PASS"],
        ["TC-15", "NoSQL Malicious Payload", "Input with {$ne: null} in string", "Stored as literal string, no execution", "Sanitized and stored safely", "PASS"]
    ]
    col_widths_tc = [0.8, 1.3, 1.25, 1.3, 1.0, 0.6]
    add_styled_table(doc, headers_tc, data_tc, col_widths_tc, "Table 7.2: Detailed Functional and Security Test Case Log (TC-01 to TC-15)")

    # 7.11 Test Results and Defect Analysis
    add_section_heading(doc, "7.11", "Test Results and Defect Analysis")
    add_paragraph(
        doc,
        "Across the complete audit of 104 executed tests, all 104 passed (100.0% pass rate). "
        "Two potential defects identified during pre-release QA testing were successfully remediated and verified as detailed below:"
    )

    add_callout(
        doc,
        "Issue 1: What-If Parameter Alias Synchronization (Severity: MEDIUM, Status: REMEDIATED)\n"
        "• Affected Route: POST /api/simulate\n"
        "• Description: In PatientInput, systolic_bp and cholesterol exist as aliases alongside Cleveland names trestbps and chol. "
        "When callers modified systolic_bp in simulations without passing trestbps, the LightGBM feature builder preserved the baseline trestbps.\n"
        "• Remediation: Added bidirectional pre-validation synchronization in PatientInput and _prepare_lgbm_dataframe:\n"
        "  if 'systolic_bp' in data and not 'trestbps' in data: data['trestbps'] = data['systolic_bp']\n"
        "  if 'cholesterol' in data and not 'chol' in data: data['chol'] = data['cholesterol']",
        title="DEFECT AUDIT FINDING 1",
        border_color="D97706",
        bg_color="FFFBEB"
    )

    add_callout(
        doc,
        "Issue 2: Single-Record Lookup User Scoping (Severity: HIGH, Status: REMEDIATED)\n"
        "• Affected Routes: GET /api/history/{id}, DELETE /api/history/{id}, GET /api/reports/{id}\n"
        "• Description: Handlers queried MongoDB by {'id': id} directly. While assessment IDs are randomly generated UUIDs (PRED-xxxxxxxx), "
        "user scoping parameter was not enforced on single ID lookups.\n"
        "• Remediation: Updated single record queries to verify user ownership when user_email is provided:\n"
        "  query = {'id': id}\n"
        "  if user_email: query['user_email'] = user_email.strip().lower()\n"
        "  row = db.assessments.find_one(query)",
        title="SECURITY AUDIT FINDING 2",
        border_color="B91C1C",
        bg_color="FEF2F2"
    )

    # 7.12 Testing Summary
    add_section_heading(doc, "7.12", "Testing Summary")
    add_paragraph(
        doc,
        "The testing chapter demonstrated the operational stability, diagnostic precision, and security resilience of HeartCare AI. "
        "The automated test suite validated 104 test cases with an overall pass rate of 100.0% across unit, integration, user isolation, "
        "geospatial distance, and security dimensions. Identified defects were thoroughly documented, root-caused, and remediated. "
        "The subsequent chapter examines system maintenance protocols."
    )
