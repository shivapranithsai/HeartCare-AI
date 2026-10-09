from report_generator.styles import (
    add_chapter_title, add_section_heading, add_subsection_heading,
    add_paragraph, add_bullet, add_styled_table
)

def add_chapter_2(doc):
    """Generates Chapter 2 – Literature Survey."""
    add_chapter_title(doc, "2", "LITERATURE SURVEY")

    # 2.1 Introduction
    add_section_heading(doc, "2.1", "Introduction")
    add_paragraph(
        doc,
        "The application of machine learning, statistical pattern recognition, and clinical decision support systems (CDSS) to cardiovascular risk assessment has "
        "been an active domain of multidisciplinary investigation for over four decades. Beginning with early Bayesian diagnostic networks and linear discriminant "
        "analyses in the 1980s, the field has evolved through support vector machines, neural networks, and decision tree ensembles to modern gradient-boosted architectures. "
        "This chapter presents a rigorous review of foundational and contemporary academic research literature, examines existing commercial and open-source clinical systems, "
        "articulates the critical research gaps in current implementations, and situates the proposed HeartCare AI architecture within the contemporary state of the art."
    )

    # 2.2 Review of Existing Research Papers
    add_section_heading(doc, "2.2", "Review of Existing Research Papers")
    add_paragraph(
        doc,
        "A systematic analysis of peer-reviewed publications was conducted, focusing on clinical cardiology datasets, algorithmic architectures, feature importance methodologies, "
        "and empirical validation metrics. Six landmark academic contributions were evaluated in detail:"
    )

    # Paper 1: Detrano et al. (1989)
    add_subsection_heading(doc, "2.2.1", "Foundational Multi-Center Clinical Dataset Creation (Detrano et al., 1989)")
    add_paragraph(
        doc,
        "Detrano et al. (1989) established the seminal international benchmark for computational cardiology by compiling the multi-center Heart Disease Database across four institutions: "
        "the Cleveland Clinic Foundation (USA), the Hungarian Institute of Cardiology (Budapest), the University Hospital Zurich (Switzerland), and the V.A. Medical Center (Long Beach, CA). "
        "The authors evaluated a logistic regression probability algorithm across 303 consecutive patients undergoing coronary arteriography at the Cleveland Clinic."
    )
    add_bullet(
        doc,
        "Methodology & Dataset: ",
        "Evaluated 13 non-invasive clinical and fluoroscopic parameters against the gold standard of coronary arteriography (>50% diameter stenosis in at least one major coronary artery). The dataset captured resting ECG, exercise thallium scintigraphy, and fluoroscopic vessel counts."
    )
    add_bullet(
        doc,
        "Findings: ",
        "Demonstrated that non-invasive clinical features could predict significant coronary stenosis with an accuracy of approximately 77% and an area under the ROC curve of 0.86, establishing that exercise-induced ST depression and fluoroscopic major vessel calcification were the strongest independent discriminators."
    )
    add_bullet(
        doc,
        "Limitations: ",
        "The original model was constrained by linear logistic modeling and did not provide granular disease severity staging or automated software integration for clinical bedside use."
    )

    # Paper 2: Chicco & Jurman (2020)
    add_subsection_heading(doc, "2.2.2", "Cardiorenal Biomarker Superiority in Heart Failure (Chicco & Jurman, 2020)")
    add_paragraph(
        doc,
        "Chicco and Jurman (2020) conducted a critical machine learning investigation into survival prediction among patients suffering from heart failure, analyzing the UCI Heart Failure "
        "Clinical Records dataset comprising 299 patients evaluated at the Faisalabad Institute of Cardiology. Their research challenged the prevailing paradigm of utilizing exhaustive, "
        "high-dimensional feature sets by demonstrating the decisive prognostic superiority of two cardiorenal biomarkers."
    )
    add_bullet(
        doc,
        "Methodology & Algorithms: ",
        "Employed Random Forests, Support Vector Machines (SVM), AdaBoost, and Decision Trees, paired with Matthew Correlation Coefficient (MCC) optimization to avoid accuracy paradoxes on imbalanced survival data."
    )
    add_bullet(
        doc,
        "Findings: ",
        "Demonstrated that utilizing only Left Ventricular Ejection Fraction (EF) and Serum Creatinine achieved survival prediction accuracy (74.0% accuracy, MCC of 0.44) equivalent to or exceeding models trained on all 12 clinical attributes combined. This substantiated the pathophysiological primacy of cardiorenal syndrome in progressive heart failure."
    )
    add_bullet(
        doc,
        "Limitations: ",
        "The study was limited to retrospective mortality prediction during hospital follow-up and did not provide an interactive clinical decision support interface for ambulatory preventative care."
    )

    # Paper 3: Ke et al. (2017)
    add_subsection_heading(doc, "2.2.3", "LightGBM Gradient Boosted Decision Trees (Ke et al., 2017)")
    add_paragraph(
        doc,
        "Ke et al. (2017) introduced LightGBM, a novel Gradient Boosting Decision Tree (GBDT) framework specifically engineered to overcome the computational and memory bottlenecks "
        "of traditional implementations (such as XGBoost and standard Scikit-Learn GradientBoosting). The authors introduced two pioneering algorithmic innovations: Gradient-based "
        "One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB)."
    )
    add_bullet(
        doc,
        "Methodology: ",
        "GOSS retains data instances with large gradients (which contribute more to information gain) while randomly sub-sampling instances with small gradients, maintaining theoretical accuracy while substantially accelerating training speed. EFB groups mutually exclusive sparse features into dense bundles. Furthermore, LightGBM adopts a leaf-wise (best-first) tree growth strategy rather than the standard level-wise approach."
    )
    add_bullet(
        doc,
        "Findings: ",
        "Experimental evaluations proved LightGBM accelerates training speeds up to 20 times over conventional GBDTs while achieving superior generalization on high-dimensional clinical and tabular datasets."
    )
    add_bullet(
        doc,
        "Relevance to HeartCare AI: ",
        "Directly justifies the selection of LightGBM as the core predictive engine for HeartCare AI, allowing multi-class probability estimation with native booster categorical encoding in sub-millisecond inference times."
    )

    # Paper 4: Lundberg & Lee (2017)
    add_subsection_heading(doc, "2.2.4", "Unified Explainable AI through SHAP Framework (Lundberg & Lee, 2017)")
    add_paragraph(
        doc,
        "Lundberg and Lee (2017) addressed the foundational challenge of model interpretability in artificial intelligence by formulating SHAP (SHapley Additive exPlanations). "
        "Drawing upon cooperative game theory, SHAP unifies six existing feature attribution methods (including LIME, DeepLIFT, and TreeInterpreter) under an axiomatic framework "
        "satisfying three essential properties: Local Accuracy, Missingness, and Consistency."
    )
    add_bullet(
        doc,
        "Methodology: ",
        "Calculates the marginal contribution of each input feature across all possible feature subsets, computing exact Shapley values that represent the magnitude and direction by which each biomarker drives an individual prediction away from the baseline expected value."
    )
    add_bullet(
        doc,
        "Findings: ",
        "Proved that tree-specific optimizations (TreeSHAP) could compute exact polynomial-time feature explanations for ensemble models, resolving the opacity of gradient-boosted decision trees in high-stakes clinical decision-making."
    )
    add_bullet(
        doc,
        "Limitations: ",
        "Computing full Shapley permutations across large feature spaces in low-latency web request cycles can introduce runtime overhead, necessitating streamlined clinical heuristic attribution for rapid web user interfaces."
    )

    # Paper 5: Benjamin et al. (2019)
    add_subsection_heading(doc, "2.2.5", "American Heart Association Clinical Guidelines (Benjamin et al., 2019)")
    add_paragraph(
        doc,
        "Benjamin et al. (2019), representing the American Heart Association (AHA) and National Institutes of Health (NIH), compiled the definitive epidemiological and clinical guidelines "
        "for heart disease and stroke statistics. The report establishes validated physiological thresholds for staging hypertension (ACC/AHA 2017 guidelines: Stage 1 = 130–139/80–89 mmHg; "
        "Stage 2 >= 140/90 mmHg), hypercholesterolemia (>200 mg/dL), impaired fasting glucose (>100 mg/dL; diabetes >126 mg/dL), and left ventricular ejection fraction impairment (<40% defining HFrEF)."
    )
    add_paragraph(
        doc,
        "These clinical guidelines provide the foundational physiological basis for HeartCare AI's clinical heuristic scoring engine (`clinical_engine.py`) and recommendation generator (`recommendations.py`)."
    )

    # Paper 6: Mohan et al. (2019)
    add_subsection_heading(doc, "2.2.6", "Hybrid Machine Learning Techniques on Cleveland Dataset (Mohan et al., 2019)")
    add_paragraph(
        doc,
        "Mohan, Thirumalai and Srivastava (2019) explored hybrid machine learning architectures for heart disease prediction on the UCI Cleveland dataset. The authors combined Random Forest "
        "and Linear Model classifiers into a hybrid framework (HRFLM), achieving a binary classification accuracy of 88.7% by optimizing split points and feature correlation matrices. "
        "However, their research focused purely on algorithmic benchmarking without developing software APIs, longitudinal tracking, or emergency triage integrations."
    )

    # 2.3 Existing Systems
    add_section_heading(doc, "2.3", "Existing Systems")
    add_paragraph(
        doc,
        "A critical review of existing commercial and academic cardiovascular risk assessment platforms reveals several prominent categories:"
    )
    add_bullet(
        doc,
        "1. Static Online Clinical Calculators (e.g., MDCalc Framingham Score, ASCVD Risk Estimator Plus): ",
        "These web tools provide point-based 10-year risk estimations based on linear Cox proportional hazard models. While widely accepted in outpatient clinics, they evaluate only a limited subset of biomarkers (age, sex, total cholesterol, HDL, SBP, smoking, diabetes) and fail to incorporate acute diagnostic features such as ST-segment depression, ECG abnormalities, or ejection fraction. Furthermore, they offer no user session persistence or longitudinal tracking."
    )
    add_bullet(
        doc,
        "2. General Consumer Wellness Applications (e.g., Apple Health, Google Fit): ",
        "These applications excel at ingesting real-time wearable telemetry (heart rate, step counts, sleep cycles). However, they lack clinical diagnostic modeling, laboratory biomarker ingestion, or oncology/cardiorenal integration, restricting their outputs to general lifestyle coaching."
    )
    add_bullet(
        doc,
        "3. Academic Machine Learning Prototypes (e.g., Streamlit / Gradio Demos): ",
        "Numerous open-source machine learning demonstrations exist on GitHub. While functionally demonstrating trained Scikit-Learn models, they are typically implemented as single-file scripts without database persistence, user authentication, security isolation, geospatial mapping, or automated medical letterhead reporting."
    )

    # 2.4 Comparison of Existing Systems
    add_section_heading(doc, "2.4", "Comparison of Existing Systems")
    add_paragraph(
        doc,
        "To clearly delineate the technological positioning of HeartCare AI, Table 2.1 provides a detailed comparative matrix benchmarking HeartCare AI against existing "
        "clinical calculators, consumer health platforms, and academic prototypes across ten critical clinical and architectural dimensions."
    )

    headers_comp = ["Dimension / Capability", "MDCalc ASCVD", "Apple Health", "Academic Prototypes", "HeartCare AI (Proposed)"]
    data_comp = [
        ["Predictive ML Architecture", "Linear Cox / FRS", "Basic Thresholds", "RF / SVM / XGBoost", "LightGBM + Heuristic Fallback"],
        ["Biomarker Features Evaluated", "7 Epidemiological", "Wearable Vitals", "13 Cleveland", "13 Cleveland + EF + Creatinine"],
        ["Disease Severity Staging", "No (10-Yr % Only)", "No", "Binary Only (0/1)", "5-Class (Stages 0 to 4) + Binary"],
        ["Explainable AI Attribution", "None", "None", "SHAP Plots (Static)", "Categorized Risk & Protective Drivers"],
        ["Interactive 'What-If' Simulator", "No", "No", "Rarely Implemented", "Yes (Real-Time Biomarker Sliders)"],
        ["Longitudinal Patient Telemetry", "No (Stateless)", "Yes (Device Sync)", "No (Stateless)", "Yes (User-Scoped MongoDB Cloud)"],
        ["Printable Clinical Reports", "No", "Summary PDF", "No", "Yes (Hospital Letterhead Ready)"],
        ["Geospatial Emergency Routing", "No", "Emergency SOS", "No", "Yes (Live OSM + Haversine + Maps)"],
        ["Cardiology Appointment Booking", "No", "No", "No", "Yes (Integrated Hospital Modal)"],
        ["Fail-Safe Resilient Architecture", "Static Calculator", "Device Dependent", "Single Script", "Dual-Engine (LGBM + Fallback)"]
    ]
    col_widths_comp = [1.8, 1.1, 1.1, 1.1, 1.15]
    add_styled_table(doc, headers_comp, data_comp, col_widths_comp, "Table 2.1: Comparison Matrix of Existing Cardiovascular Prediction Systems")

    # 2.5 Research Gap
    add_section_heading(doc, "2.5", "Research Gap")
    add_paragraph(
        doc,
        "Based on the systematic review of academic literature and existing digital solutions, four fundamental research and engineering gaps were identified:"
    )
    add_bullet(
        doc,
        "Research Gap 1 — The Disconnect Between High-Accuracy ML and Clinical Explainability: ",
        "While non-linear gradient-boosted decision trees deliver superior diagnostic accuracy over linear risk scores, their black-box nature inhibits clinical adoption. Existing literature largely generates post-hoc global feature importance plots rather than personalized, patient-centric risk and protective factor breakdowns ready for point-of-care interpretation."
    )
    add_bullet(
        doc,
        "Research Gap 2 — Lack of Interactive Counterfactual ('What-If') Clinical Simulation: ",
        "Current systems provide static risk probabilities. There is a marked absence of dynamic simulation frameworks where clinicians can interactively manipulate physiological dials (e.g., simulating a 20 mmHg systolic BP reduction or smoking cessation) to quantitatively show patients their projected risk reduction."
    )
    add_bullet(
        doc,
        "Research Gap 3 — Absence of High-Availability Fallback Architectures in Medical AI: ",
        "Machine learning web applications frequently suffer complete operational failure if the pickled model artifact fails to load, incurs memory corruption, or encounters out-of-distribution feature dimensions. Literature lacks resilient dual-engine designs combining high-accuracy ML with deterministic heuristic fallbacks."
    )
    add_bullet(
        doc,
        "Research Gap 4 — Fragmented Emergency Care and Geospatial Triage: ",
        "Medical predictive models operate in clinical isolation. No existing open platform links acute high-risk machine learning predictions directly to live geospatial emergency routing, calculating geodesic Haversine distances to verified regional cardiac catheterization facilities."
    )

    # 2.6 Proposed System
    add_section_heading(doc, "2.6", "Proposed System")
    add_paragraph(
        doc,
        "To directly address and resolve the aforementioned research gaps, this project proposes HeartCare AI—an integrated, cloud-native cardiovascular risk stratification "
        "and clinical decision support platform. HeartCare AI introduces four key innovations:"
    )
    add_bullet(
        doc,
        "1. Calibrated Multi-Class LightGBM Classifier with Automatic Heuristic Fallback: ",
        "Implements a high-efficiency LightGBM model trained on 13 Cleveland clinical features (`best_lgbm_3m_model.joblib`), paired with an automatic, fail-safe AHA/Framingham clinical heuristic engine (`clinical_engine.py`) to guarantee 100% service uptime."
    )
    add_bullet(
        doc,
        "2. Explainable AI and Interactive Counterfactual Simulation: ",
        "Decomposes complex model probabilities into actionable biomarker attributions (categorized into vital, clinical, demographic, and lifestyle factors) and provides real-time What-If simulation sliders to project immediate therapeutic risk reduction."
    )
    add_bullet(
        doc,
        "3. User-Scoped Longitudinal Telemetry & Clinical Documentation: ",
        "Enforces strict database-level record isolation on MongoDB Atlas, allowing patients and attending physicians to monitor longitudinal biomarker trajectories and generate printable hospital-grade letterhead reports."
    )
    add_bullet(
        doc,
        "4. Live Geospatial Emergency Radar: ",
        "Integrates OpenStreetMap Overpass and Nominatim APIs with geodetic Haversine calculations to sort nearby verified cardiology centers by real-time distance and ETA, providing direct Google Maps turn-by-turn navigation."
    )

    # 2.7 Summary
    add_section_heading(doc, "2.7", "Summary")
    add_paragraph(
        doc,
        "This chapter surveyed the historical and contemporary scientific literature in machine learning for cardiovascular risk prediction. Foundational datasets "
        "(Detrano et al., 1989; Chicco & Jurman, 2020), advanced boosting algorithms (Ke et al., 2017), and explainable AI frameworks (Lundberg & Lee, 2017) were critically "
        "examined. A comparative analysis against existing clinical calculators and wellness apps established four critical research gaps, directly motivating the "
        "development of the proposed HeartCare AI architecture. The subsequent chapter details the comprehensive project flow and technical methodology."
    )
