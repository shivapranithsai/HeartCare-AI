from report_generator.styles import (
    add_chapter_title, add_section_heading, add_subsection_heading,
    add_paragraph, add_bullet, add_callout
)

def add_chapter_1(doc):
    """Generates Chapter 1 – Introduction."""
    add_chapter_title(doc, "1", "INTRODUCTION")

    # 1.1 Introduction
    add_section_heading(doc, "1.1", "Introduction")
    add_paragraph(
        doc,
        "Cardiovascular diseases (CVDs) remain the predominant etiology of premature mortality, clinical morbidity, and escalating healthcare expenditures worldwide. "
        "According to the World Health Organization (WHO), ischemic heart disease and heart failure account for approximately 17.9 million annual fatalities, representing "
        "nearly 32% of all global deaths. In clinical cardiology, heart failure is not an isolated pathological diagnosis but rather a complex, debilitating clinical syndrome "
        "resulting from structural or functional cardiac abnormalities that impair the ventricular ejection or diastolic filling of blood. Early diagnosis and accurate risk "
        "stratification are pivotal in curbing progressive myocardial remodeling, preventing lethal arrhythmic episodes, and mitigating emergency hospital re-admissions."
    )
    add_paragraph(
        doc,
        "In recent years, the convergence of high-performance computing, advanced data analytics, and Artificial Intelligence (AI) has sparked a transformative paradigm shift "
        "within clinical informatics. Modern Machine Learning (ML) algorithms possess the unique capability to uncover intricate, non-linear relationships across high-dimensional "
        "biomarker arrays—patterns that frequently elude traditional, linear clinical risk scores such as the Framingham Risk Score (FRS) or the Systematic Coronary Risk Evaluation (SCORE). "
        "However, translating cutting-edge ML models into everyday clinical practice demands far more than isolated predictive accuracy. Clinicians and patients require transparent, "
        "interpretable predictions, interactive counterfactual simulations, longitudinal patient monitoring, and rapid emergency triage mechanisms."
    )
    add_paragraph(
        doc,
        "This project introduces HeartCare AI, an evidence-based clinical intelligence platform designed to operationalize modern predictive modeling, explainable AI, "
        "and geospatial emergency triage within a cohesive, production-grade cloud application. Centered around a calibrated 13-feature LightGBM (Light Gradient Boosting Machine) "
        "classification engine, HeartCare AI integrates multi-biomarker risk scoring, real-time longitudinal telemetry tracking, interactive 'What-If' clinical simulation, "
        "automated printable medical report generation, and dynamic Haversine-based hospital routing. By combining algorithmic rigor with clinical usability, HeartCare AI aims "
        "to empower healthcare practitioners with actionable decision support while simultaneously promoting proactive self-management among cardiac patients."
    )

    # 1.2 Background of the Project
    add_section_heading(doc, "1.2", "Background of the Project")
    add_paragraph(
        doc,
        "The historical trajectory of cardiovascular risk stratification has traditionally relied on point-based epidemiological tables formulated from longitudinal cohort studies. "
        "The landmark Framingham Heart Study, initiated in 1948, pioneered the conceptual identification of key cardiovascular risk factors, including systemic arterial hypertension, "
        "hypercholesterolemia, cigarette smoking, and advancing age. While these classical heuristic models provided foundational epidemiological benchmarks, their clinical utility "
        "in modern acute and sub-acute care is increasingly constrained by three fundamental limitations:"
    )
    add_bullet(
        doc,
        "Linearity Assumptions: ",
        "Conventional scores predominantly apply generalized linear regression or proportional hazard models that presuppose linear or monotonic relationships between biomarkers and clinical outcomes, thereby obscuring complex biological non-linearities and epistatic interactions."
    )
    add_bullet(
        doc,
        "Narrow Biomarker Inclusion: ",
        "Traditional scores frequently omit acute physiological markers—such as peak exercise ST-segment depression (oldpeak), fluoroscopic major vessel calcification (ca), thallium scintigraphy defects (thal), and critical cardiorenal markers like left ventricular ejection fraction (EF) and serum creatinine."
    )
    add_bullet(
        doc,
        "Static and Disconnected Nature: ",
        "Existing risk assessments are typically conducted as one-off evaluations. They lack dynamic integration with real-time patient telemetry, interactive lifestyle counterfactual modeling, or automated routing to emergency care facilities during acute decompensation."
    )
    add_paragraph(
        doc,
        "With the digitalization of medical records and the availability of open, well-curated clinical research datasets—notably the Cleveland Heart Disease Database from the "
        "University of California Irvine (UCI) Machine Learning Repository—computational researchers have demonstrated the efficacy of ensemble learning techniques in detecting "
        "occult coronary artery disease. HeartCare AI builds upon this extensive scientific foundation by translating validated machine learning algorithms from static Jupyter notebooks "
        "into an end-to-end, full-stack, cloud-hosted software ecosystem."
    )

    # 1.3 Problem Statement
    add_section_heading(doc, "1.3", "Problem Statement")
    add_paragraph(
        doc,
        "Despite significant advancements in cardiovascular pharmacological interventions and surgical care, heart failure diagnosis and risk stratification continue to face critical systemic bottlenecks:"
    )
    add_bullet(
        doc,
        "Diagnostic Delay in Early-Stage Myocardial Impairment: ",
        "Patients presenting with atypical angina or non-specific symptoms are frequently misdiagnosed or diagnosed at advanced disease stages (Stages 2 to 4), where irreversible ventricular remodeling has already occurred."
    )
    add_bullet(
        doc,
        "The 'Black-Box' Interpretability Dilemma: ",
        "Complex ensemble ML algorithms (such as Random Forests, Gradient Boosted Trees, and Neural Networks) often operate as opaque decision systems, providing risk probabilities without articulating the underlying physiological drivers or protective factors, leading to widespread clinical distrust."
    )
    add_bullet(
        doc,
        "Absence of Dynamic 'What-If' Prognostic Modeling: ",
        "Existing systems fail to provide patients and attending physicians with interactive simulation tools to quantitatively project how specific clinical modifications (e.g., reducing systolic blood pressure from 165 to 125 mmHg, or smoking cessation) would alter their cardiovascular risk trajectory."
    )
    add_bullet(
        doc,
        "Fragmented Emergency Care Navigation: ",
        "When an assessment identifies high or critical cardiac risk, prevailing digital health applications provide generic disclaimers rather than instantly connecting the patient to verified, geo-proximate cardiology super-speciality centers equipped with 24/7 cardiac catheterization labs and emergency ICUs."
    )

    # 1.4 Motivation
    add_section_heading(doc, "1.4", "Motivation")
    add_paragraph(
        doc,
        "The driving motivation behind HeartCare AI originates from the urgent clinical imperative to bridge the divide between theoretical artificial intelligence research "
        "and practical point-of-care utility. While thousands of academic research papers report high classification accuracies on medical datasets, a negligible fraction are ever "
        "packaged into production-ready software capable of serving clinicians, medical students, and at-risk individuals in low-resource or emergency environments."
    )
    add_paragraph(
        doc,
        "Furthermore, India and developing nations face a rapidly growing cardiovascular disease epidemic, with cardiac mortality occurring on average a decade earlier than in Western "
        "populations. In such healthcare landscapes, access to senior cardiologists is often concentrated in metropolitan hubs. An accessible, highly responsive, cloud-hosted platform "
        "that accepts standard clinical and laboratory parameters, produces instant probability stratification backed by transparent clinical explanations, and routes critical cases "
        "to verified regional super-speciality facilities holds immense potential to reduce avoidable mortality and optimize intensive care resource utilization."
    )

    # 1.5 Objectives
    add_section_heading(doc, "1.5", "Objectives")
    add_paragraph(
        doc,
        "The primary objective of this project is to research, design, develop, test, and deploy HeartCare AI—a full-stack clinical intelligence and cardiovascular risk stratification platform. "
        "The specific technical and research objectives are delineated as follows:"
    )
    add_bullet(
        doc,
        "Objective 1 — Predictive Model Engineering: ",
        "Train, calibrate, and validate a high-accuracy, multi-class LightGBM machine learning classifier using 13 clinical biomarkers from the benchmark Cleveland and UCI Heart Disease repositories, achieving benchmark-competitive accuracy, precision, recall, and ROC-AUC."
    )
    add_bullet(
        doc,
        "Objective 2 — High-Availability Heuristic Fallback Engine: ",
        "Design and implement a deterministic clinical heuristic fallback engine operationalizing Framingham and ACC/AHA cardiovascular guidelines, ensuring fail-safe continuity of care if the custom ML model artifact is unavailable."
    )
    add_bullet(
        doc,
        "Objective 3 — Explainable AI & Counterfactual Simulation: ",
        "Implement a transparent biomarker attribution mechanism that decomposes overall risk into categorized risk drivers and protective factors, coupled with an interactive What-If simulation engine to evaluate therapeutic interventions in real time."
    )
    add_bullet(
        doc,
        "Objective 4 — Asynchronous RESTful API Backend: ",
        "Develop an enterprise-grade, asynchronous backend using Python 3.11/3.14 and FastAPI, implementing structured Pydantic v2 data validation schemas, salted SHA-256 authentication, and sub-second endpoint response times."
    )
    add_bullet(
        doc,
        "Objective 5 — Secure Cloud Persistence & User Isolation: ",
        "Architect a thread-safe connection-pooled database layer using MongoDB Atlas with unique indexing across users, assessments, hospitals, and appointments, enforcing strict data isolation between patients."
    )
    add_bullet(
        doc,
        "Objective 6 — Modern Glassmorphic Frontend & Telemetry UI: ",
        "Build a responsive single-page web interface using React 19 and Vite featuring an HTML5 canvas real-time ECG rhythm visualizer, SVG dynamic radial risk gauges, and printable hospital-grade diagnostic letterhead reports."
    )
    add_bullet(
        doc,
        "Objective 7 — Live Geospatial Emergency Radar: ",
        "Incorporate a geodetic Haversine calculation service integrated with OpenStreetMap Overpass and Nominatim APIs to discover nearby hospitals, sort them by distance, and provide turn-by-turn Google Maps navigation."
    )
    add_bullet(
        doc,
        "Objective 8 — Rigorous Quality Assurance & Containerized Deployment: ",
        "Execute an exhaustive end-to-end testing audit across unit, integration, and security domains, and orchestrate automated multi-cloud deployment via Docker, Render, and Vercel."
    )

    # 1.6 Scope of the Project
    add_section_heading(doc, "1.6", "Scope of the Project")
    add_paragraph(
        doc,
        "The operational scope of HeartCare AI encompasses the complete clinical workflow from patient onboarding to emergency referral. Specifically, the system scope includes:"
    )
    add_bullet(
        doc,
        "Clinical Feature Domain: ",
        "Evaluation of 13 primary Cleveland features: Age, Sex, Chest Pain Type (cp), Resting Blood Pressure (trestbps), Serum Cholesterol (chol), Fasting Blood Sugar (fbs), Resting ECG (restecg), Maximum Heart Rate Achieved (thalach), Exercise Induced Angina (exang), ST Depression (oldpeak), ST Slope (slope), Number of Major Vessels Colored by Fluoroscopy (ca), and Thallium Scintigraphy Defect (thal). Extended biomarkers include Left Ventricular Ejection Fraction (EF), Serum Creatinine, and Smoking Status."
    )
    add_bullet(
        doc,
        "User Personas Supported: ",
        "Primary support for two distinct user profiles: Attending Clinicians/Cardiologists (accessing deep diagnostic matrices, dynamic synthetic cohort generation, and batch telemetry) and Patients/Individual Users (accessing self-assessment forms, personalized dashboards, What-If simulation, and hospital locators)."
    )
    add_bullet(
        doc,
        "Geospatial Coverage: ",
        "Comprehensive directory seeding of 23 premier super-speciality cardiology institutes across major Indian metropolitan centers (Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata, Pune, Ahmedabad, Chandigarh, Jaipur, Lucknow, Bhubaneswar, Thiruvananthapuram), augmented with real-time global OpenStreetMap discovery."
    )
    add_bullet(
        doc,
        "Deployment Boundary: ",
        "Containerized Linux backend deployment on Render PaaS, static Single-Page Application (SPA) hosting on Vercel Edge CDN, and managed NoSQL persistence on MongoDB Atlas."
    )

    # 1.7 Significance of the Project
    add_section_heading(doc, "1.7", "Significance of the Project")
    add_paragraph(
        doc,
        "The significance of HeartCare AI spans clinical, technological, and societal dimensions:"
    )
    add_bullet(
        doc,
        "Clinical Significance: ",
        "By achieving an empirical Sensitivity (Recall) of 86.86% and an ROC-AUC of 91.70%, the platform provides a highly sensitive early-warning screening tool that effectively minimizes false-negative classifications. This early detection capability allows clinicians to initiate preventative ACE inhibitors, statin therapies, or lifestyle modifications before symptomatic heart failure ensues."
    )
    add_bullet(
        doc,
        "Technological Significance: ",
        "HeartCare AI illustrates how state-of-the-art tree-based gradient boosting (LightGBM) can be seamlessly integrated into modern asynchronous web frameworks (FastAPI) and reactive frontends (React 19) without incurring significant computational latency (average concurrent prediction latency of 559ms). It provides a concrete architecture for handling booster categorical types and multi-stage classification."
    )
    add_bullet(
        doc,
        "Societal Significance: ",
        "By delivering clear, jargon-free biomarker explanations and What-If scenarios, the application empowers individuals to understand the direct physiological consequence of lifestyle choices. In acute emergencies, its instant geospatial navigation reduces the critical 'door-to-balloon' transit time for myocardial infarction patients."
    )

    # 1.8 Limitations
    add_section_heading(doc, "1.8", "Limitations")
    add_paragraph(
        doc,
        "In adherence to strict academic honesty and clinical governance, the following project limitations must be formally recognized:"
    )
    add_bullet(
        doc,
        "Dataset Sample Size: ",
        "The supervised machine learning engine is trained and evaluated on 297 clean patient records from the UCI Cleveland benchmark dataset. While this dataset remains a globally recognized gold standard for algorithmic comparison, clinical validation across larger, contemporary multi-ethnic cohorts (exceeding tens of thousands of electronic health records) is necessary prior to formal hospital deployment."
    )
    add_bullet(
        doc,
        "Multi-Class Imbalance: ",
        "While binary classification (Healthy vs. Disease) demonstrates robust performance (81.82% accuracy, 91.70% ROC-AUC), multi-class discrimination across individual disease stages (Stages 0 through 4) achieves a lower accuracy of 53.87% due to small sample counts in severe sub-classes (e.g., only 13 Stage 4 records in the benchmark). As a result, the platform uses multi-stage outputs primarily as directional severity indicators rather than definitive staging."
    )
    add_bullet(
        doc,
        "Absence of Prospective Clinical Trials: ",
        "HeartCare AI is engineered as an academic software engineering and clinical decision support demonstration. It has not been subjected to prospective randomized clinical trials and holds no formal medical device regulatory certification (such as US FDA 510(k) or CE mark approval)."
    )
    add_bullet(
        doc,
        "Hardware IoT Sensor Telemetry: ",
        "While the system features an animated HTML5 canvas ECG waveform and real-time biomarker telemetry cards, these currently ingest structured user inputs and synthetic streams rather than direct hardware Bluetooth/BLE feeds from wearable electrocardiogram sensors."
    )

    # 1.9 Organization of the Report
    add_section_heading(doc, "1.9", "Organization of the Report")
    add_paragraph(
        doc,
        "This project report is systematically organized into nine comprehensive chapters, structured as follows:"
    )
    add_bullet(
        doc,
        "Chapter 1 – Introduction: ",
        "Establishes the clinical problem, historical background, core motivation, project objectives, operational scope, significance, and intrinsic limitations."
    )
    add_bullet(
        doc,
        "Chapter 2 – Literature Survey: ",
        "Reviews authentic peer-reviewed literature in cardiovascular machine learning, evaluates existing digital cardiac systems, identifies key research gaps, and presents the proposed system."
    )
    add_bullet(
        doc,
        "Chapter 3 – Project Flow and Methodology: ",
        "Details the complete technical workflow, dataset ingestion, preprocessing, categorical encoding, LightGBM mathematical formulation, explainable AI heuristics, and database pipeline."
    )
    add_bullet(
        doc,
        "Chapter 4 – System Design: ",
        "Presents the multi-tier architectural blueprint, functional and non-functional specifications, Use Case specifications, DFD Level 0/1 diagrams, system flowcharts, and MongoDB ER schemas."
    )
    add_bullet(
        doc,
        "Chapter 5 – Implementation: ",
        "Thoroughly examines the codebase implementation across React 19 frontend components, FastAPI asynchronous routers, PyMongo persistence, ML model loading, and geospatial calculations."
    )
    add_bullet(
        doc,
        "Chapter 6 – Result Analysis: ",
        "Reports empirical evaluation metrics, binary and 5-class confusion matrices, baseline algorithmic comparisons, SHAP-style attribution results, and system performance benchmarks."
    )
    add_bullet(
        doc,
        "Chapter 7 – Testing: ",
        "Documents the comprehensive QA audit across 104 executed test cases, covering unit, integration, security, and performance testing, detailing test case tables and defect remediation."
    )
    add_bullet(
        doc,
        "Chapter 8 – Maintenance of the System: ",
        "Formulates corrective, adaptive, perfective, and preventive maintenance protocols, addressing model drift, security patching, and disaster recovery strategies."
    )
    add_bullet(
        doc,
        "Chapter 9 – Deployment: ",
        "Details multi-cloud production deployment across Vercel, Render, and MongoDB Atlas, Docker containerization, environment configuration, and post-deployment monitoring."
    )

    add_callout(
        doc,
        "Clinical Disclaimer: HeartCare AI is developed strictly as a clinical decision support and predictive analytics assistive tool. "
        "It does not constitute definitive medical advice, diagnostic confirmation, or emergency medical dispatch. All clinical determinations "
        "must be verified by qualified medical professionals in conjunction with formal clinical laboratory protocols.",
        title="CLINICAL GOVERNANCE NOTICE",
        border_color="B91C1C",
        bg_color="FEF2F2"
    )
