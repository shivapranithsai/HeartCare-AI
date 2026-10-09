from report_generator.styles import (
    add_chapter_title, add_section_heading, add_subsection_heading,
    add_paragraph, add_bullet
)

def add_chapter_8(doc):
    """Generates Chapter 8 – Maintenance of the System."""
    add_chapter_title(doc, "8", "MAINTENANCE OF THE SYSTEM")

    # 8.1 Introduction
    add_section_heading(doc, "8.1", "Introduction")
    add_paragraph(
        doc,
        "Software maintenance constitutes the longest and most critical phase of the software engineering lifecycle, accounting for an estimated "
        "60% to 80% of total lifecycle expenditure. In clinical decision support platforms, maintenance transcends conventional bug fixing; it involves "
        "continuous surveillance of predictive accuracy, mitigation of machine learning model drift, adaptation to evolving clinical guidelines, "
        "hardening of database security, and disaster recovery readiness. This chapter formulates a comprehensive maintenance plan for HeartCare AI, "
        "categorized across corrective, adaptive, perfective, and preventive dimensions."
    )

    # 8.2 Types of Maintenance
    add_section_heading(doc, "8.2", "Types of Maintenance")
    add_paragraph(
        doc,
        "Following ISO/IEC 14764 international software engineering standards, maintenance activities for HeartCare AI are partitioned into four distinct categories:"
    )
    add_bullet(doc, "1. Corrective Maintenance: ", "Reactive modifications executed to rectify discovered faults, defects, and logical anomalies.")
    add_bullet(doc, "2. Adaptive Maintenance: ", "Proactive modifications to keep the software operational in changing environmental, platform, and operating system contexts.")
    add_bullet(doc, "3. Perfective Maintenance: ", "Enhancements undertaken to improve user experience, execution performance, algorithmic explainability, and feature richness.")
    add_bullet(doc, "4. Preventive Maintenance: ", "Interventions designed to detect and correct latent faults before they manifest as operational failures.")

    # 8.3 Corrective Maintenance
    add_section_heading(doc, "8.3", "Corrective Maintenance")
    add_paragraph(
        doc,
        "Corrective maintenance protocols address defects discovered during production usage or QA audits. In HeartCare AI, corrective actions include:"
    )
    add_bullet(
        doc,
        "Parameter Alias Synchronization: ",
        "Remediated the discrepancy in `POST /api/simulate` where modifying `systolic_bp` or `cholesterol` without passing raw Cleveland names (`trestbps`, `chol`) failed to alter the feature vector. Pre-validation bidirectional synchronization was integrated into `PatientInput` to guarantee parameter consistency."
    )
    add_bullet(
        doc,
        "Single-Record Authorization Enforcement: ",
        "Corrected single-record lookup endpoints (`/api/history/{id}`, `/api/reports/{id}`) by enforcing `user_email` validation filters to prevent unauthorized access across patient IDs."
    )
    add_bullet(
        doc,
        "Transient Database Disconnect Recovery: ",
        "Configured PyMongo with `serverSelectionTimeoutMS=8000` and automatic retry writes (`retryWrites=true`) to handle transient cloud networking hiccups without application crashes."
    )

    # 8.4 Adaptive Maintenance
    add_section_heading(doc, "8.4", "Adaptive Maintenance")
    add_paragraph(
        doc,
        "Adaptive maintenance ensures HeartCare AI remains fully compatible with external cloud platforms, APIs, and evolving runtimes:"
    )
    add_bullet(
        doc,
        "OpenStreetMap API Adaptation: ",
        "The external Nominatim and Overpass APIs occasionally modify rate limits or HTTP user-agent header policies. Adaptive maintenance includes rotating user-agent strings, implementing local caching for frequent city coordinates, and maintaining the 23-hospital internal database fallback."
    )
    add_bullet(
        doc,
        "Browser Geolocation Permission Policies: ",
        "Modern web browsers frequently update security policies regarding HTML5 Geolocation API access over HTTPS. The frontend gracefully adapts by offering manual city dropdown selection whenever GPS permissions are restricted or denied."
    )
    add_bullet(
        doc,
        "Runtime Upgrades: ",
        "Continual monitoring and adaptation of Python runtime dependencies (Python 3.11 to 3.14), Node.js LTS releases (Node 20 to 22), and LightGBM booster categorical compatibility across major version increments."
    )

    # 8.5 Perfective Maintenance
    add_section_heading(doc, "8.5", "Perfective Maintenance")
    add_paragraph(
        doc,
        "Perfective maintenance incorporates enhancements that improve clinical utility, computational efficiency, and visual engagement:"
    )
    add_bullet(
        doc,
        "Full SHAP TreeExplainer Integration: ",
        "While the current platform employs a clinical heuristic attribution engine for sub-millisecond web responsiveness, future releases will integrate a background TreeSHAP worker to compute exact game-theoretic Shapley force plots for advanced cardiological review."
    )
    add_bullet(
        doc,
        "WebSockets Real-Time ECG Streaming: ",
        "Upgrading the current HTML5 canvas simulator to ingest live telemetry streams from Bluetooth Low Energy (BLE) ECG monitoring hardware via WebSockets."
    )
    add_bullet(
        doc,
        "Multi-Language Localization: ",
        "Translating the patient dashboard and printable medical reports into major Indian regional languages (Hindi, Telugu, Tamil, Marathi, Bengali) to widen accessibility across rural healthcare centers."
    )

    # 8.6 Preventive Maintenance
    add_section_heading(doc, "8.6", "Preventive Maintenance")
    add_paragraph(
        doc,
        "Preventive maintenance anticipates potential vulnerabilities and performance bottlenecks:"
    )
    add_bullet(doc, "Automated Dependency Auditing: ", "Running `pip-audit` and `npm audit` monthly to identify and patch vulnerable sub-dependencies.")
    add_bullet(doc, "Database Index Optimization: ", "Analyzing MongoDB query execution plans via `.explain('executionStats')` to ensure queries utilize compound indexes (`user_email`, `timestamp`).")
    add_bullet(doc, "Log Rotation & Disk Hygiene: ", "Configuring log rotation on production Docker containers to prevent disk exhaustion from unmanaged Uvicorn access logs.")

    # 8.7 Database Maintenance
    add_section_heading(doc, "8.7", "Database Maintenance")
    add_paragraph(
        doc,
        "Database maintenance on MongoDB Atlas (`heartcare` database) involves:"
    )
    add_bullet(doc, "Index Defragmentation: ", "Periodic rebuilding of indexes across `users`, `assessments`, `hospitals`, and `appointments` to maintain optimal B-tree depths.")
    add_bullet(doc, "Connection Pool Hygiene: ", "Monitoring active connections against the 50-connection ceiling to detect socket leakage.")
    add_bullet(doc, "TTL Indexing for Temporary Sessions: ", "Configuring Time-To-Live (TTL) expiration indexes on transient token collections to prevent unneeded storage accumulation.")

    # 8.8 Security Maintenance
    add_section_heading(doc, "8.8", "Security Maintenance")
    add_paragraph(
        doc,
        "Security maintenance focuses on sustaining a hardened defensive posture:"
    )
    add_bullet(doc, "Cryptographic Salt Rotation: ", "Maintaining versioned salt schemes (e.g., `heartcare_secure_salt_v1` transitioning to `v2`) with backward-compatible re-hashing upon user login.")
    add_bullet(doc, "CORS Whitelisting Review: ", "Periodically auditing allowed origin headers to restrict API consumption exclusively to verified frontend production domains.")
    add_bullet(doc, "Continuous Credential Scanning: ", "Automated scanning of Git repositories using secret detection tools to prevent accidental commit of `.env` files.")

    # 8.9 Machine Learning Model Maintenance
    add_section_heading(doc, "8.9", "Machine Learning Model Maintenance")
    add_paragraph(
        doc,
        "In healthcare applications, machine learning models are inherently susceptible to two forms of degradation over time:"
    )
    add_bullet(
        doc,
        "Data Drift: ",
        "Shifts in input biomarker distributions (e.g., a patient cohort presenting with significantly higher mean BMI or earlier onset hypertension compared to the 1989 Cleveland dataset)."
    )
    add_bullet(
        doc,
        "Concept Drift: ",
        "Shifts in the underlying statistical relationship between biomarkers and heart failure outcomes (e.g., novel cardioprotective medications altering the mortality risk associated with reduced ejection fraction)."
    )
    add_paragraph(
        doc,
        "To mitigate drift, HeartCare AI implements an active learning surveillance protocol: historical predictions with verified hospital outcomes "
        "are flagged in MongoDB. When drift metrics exceed a 5% threshold, an automated re-training pipeline fine-tunes LightGBM hyperparameters on the expanded cohort."
    )

    # 8.10 Backup and Recovery
    add_section_heading(doc, "8.10", "Backup and Disaster Recovery")
    add_paragraph(
        doc,
        "A formal disaster recovery plan is established with defined recovery metrics:"
    )
    add_bullet(doc, "Recovery Point Objective (RPO): ", "Target RPO of < 1 hour, achieved through MongoDB Atlas automated continuous cloud snapshots.")
    add_bullet(doc, "Recovery Time Objective (RTO): ", "Target RTO of < 15 minutes, enabled by containerized Docker deployments capable of rapid redeployment on alternative cloud infrastructure.")
    add_bullet(doc, "Point-in-Time Restore (PITR): ", "Enabled on production MongoDB Atlas clusters to restore database state to any specific minute within a 7-day retention window.")

    # 8.11 Future Maintenance Requirements
    add_section_heading(doc, "8.11", "Future Maintenance Requirements")
    add_paragraph(
        doc,
        "Future maintenance roadmaps include transitioning from single-node container hosting to Kubernetes cluster orchestration, establishing automated "
        "CI/CD deployment pipelines on GitHub Actions, integrating OAuth2 federated login (Google / Apple Health), and implementing end-to-end encryption "
        "for stored patient records in compliance with HIPAA and ISO 27001 data protection standards."
    )
