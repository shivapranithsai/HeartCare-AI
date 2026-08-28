import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Sparkles,
  ArrowRight,
  ArrowLeft,
  Activity,
  Heart,
  HelpCircle,
  FileSpreadsheet,
  CheckCircle2,
  Cpu,
  Layers,
  Info
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function NewPrediction() {
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [step, setStep] = useState(1);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStage, setAnalysisStage] = useState("Extracting 13 Clinical Biomarkers...");

  // Default patient form state matching exact 13 Cleveland Features:
  // [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
  const [form, setForm] = useState({
    user_email: localStorage.getItem("userEmail") || "",
    name: localStorage.getItem("userName") || "Aarav Sharma",
    
    // 1. age
    age: 54,
    
    // 2. sex (1 = Male, 0 = Female)
    sex: 1,
    gender: "Male",
    
    // 3. cp (0: Typical Angina, 1: Atypical Angina, 2: Non-anginal, 3: Asymptomatic)
    cp: 0,
    chest_pain: "Typical Angina",
    
    // 4. trestbps (Resting Blood Pressure in mmHg)
    trestbps: 130,
    systolic_bp: 130,
    diastolic_bp: 84,
    
    // 5. chol (Serum Cholesterol in mg/dL)
    chol: 210,
    cholesterol: 210,
    
    // 6. fbs (Fasting Blood Sugar > 120 mg/dL: 1 = True, 0 = False)
    fbs: 0,
    fasting_blood_sugar: 98,
    
    // 7. restecg (0: Normal, 1: ST-T wave abnormality, 2: Left ventricular hypertrophy)
    restecg: 0,
    resting_ecg: "Normal",
    
    // 8. thalach (Maximum Heart Rate achieved in BPM)
    thalach: 150,
    heart_rate: 75,
    
    // 9. exang (Exercise Induced Angina: 1 = Yes, 0 = No)
    exang: 0,
    exercise_angina: "No",
    
    // 10. oldpeak (ST depression induced by exercise relative to rest)
    oldpeak: 1.0,
    st_depression: 1.0,
    
    // 11. slope (0: Upsloping, 1: Flat, 2: Downsloping)
    slope: 1,
    st_slope: "Flat",
    
    // 12. ca (Number of major vessels (0-3) colored by fluoroscopy)
    ca: 0,
    
    // 13. thal (1: Normal, 2: Fixed defect, 3: Reversible defect)
    thal: 1,
    
    // Complementary biomarkers
    ejection_fraction: 55,
    serum_creatinine: 1.0,
    height: 175,
    weight: 76,
    smoking: "Never",
    exercise_days: "2-3 days",
    sleep_hours: "7-9 hours",
    stress_level: "Medium"
  });

  const updateForm = (field, val) => {
    setForm((prev) => ({ ...prev, [field]: val }));
  };

  // Presets mapping to 13 Cleveland Features with authentic Indian clinical profiles
  const loadPreset = (type) => {
    if (type === "healthy") {
      setForm({
        name: "Aarav Sharma",
        age: 32,
        sex: 1,
        gender: "Male",
        cp: 3, // asymptomatic
        chest_pain: "None",
        trestbps: 114,
        systolic_bp: 114,
        diastolic_bp: 74,
        chol: 172,
        cholesterol: 172,
        fbs: 0,
        fasting_blood_sugar: 88,
        restecg: 0,
        resting_ecg: "Normal",
        thalach: 174,
        heart_rate: 68,
        exang: 0,
        exercise_angina: "No",
        oldpeak: 0.0,
        st_depression: 0.0,
        slope: 0, // upsloping
        st_slope: "Upsloping",
        ca: 0,
        thal: 1, // normal
        ejection_fraction: 65,
        serum_creatinine: 0.8,
        height: 178,
        weight: 72,
        smoking: "Never",
        exercise_days: "4-5 days",
        sleep_hours: "7-9 hours",
        stress_level: "Low"
      });
    } else if (type === "moderate") {
      setForm({
        name: "Rajesh Patel",
        age: 56,
        sex: 1,
        gender: "Male",
        cp: 1, // atypical angina
        chest_pain: "Mild",
        trestbps: 138,
        systolic_bp: 138,
        diastolic_bp: 88,
        chol: 228,
        cholesterol: 228,
        fbs: 0,
        fasting_blood_sugar: 110,
        restecg: 1, // ST-T wave
        resting_ecg: "ST-T Abnormality",
        thalach: 142,
        heart_rate: 80,
        exang: 0,
        exercise_angina: "No",
        oldpeak: 1.4,
        st_depression: 1.4,
        slope: 1, // flat
        st_slope: "Flat",
        ca: 1,
        thal: 2, // fixed defect
        ejection_fraction: 48,
        serum_creatinine: 1.2,
        height: 172,
        weight: 82,
        smoking: "Occasionally",
        exercise_days: "1-2 days",
        sleep_hours: "5-7 hours",
        stress_level: "High"
      });
    } else if (type === "high") {
      setForm({
        name: "Sunita Deshmukh",
        age: 68,
        sex: 0,
        gender: "Female",
        cp: 0, // typical angina
        chest_pain: "Severe",
        trestbps: 168,
        systolic_bp: 168,
        diastolic_bp: 102,
        chol: 275,
        cholesterol: 275,
        fbs: 1,
        fasting_blood_sugar: 145,
        restecg: 2, // LV hypertrophy
        resting_ecg: "Left Ventricular Hypertrophy",
        thalach: 118,
        heart_rate: 90,
        exang: 1,
        exercise_angina: "Yes",
        oldpeak: 2.8,
        st_depression: 2.8,
        slope: 2, // downsloping
        st_slope: "Downsloping",
        ca: 2,
        thal: 3, // reversible defect
        ejection_fraction: 34,
        serum_creatinine: 1.8,
        height: 162,
        weight: 86,
        smoking: "Regularly",
        exercise_days: "0-1 days",
        sleep_hours: "Less than 5 hours",
        stress_level: "High"
      });
    }
  };

  // Handle final submission
  const handleSubmitPrediction = async () => {
    setIsAnalyzing(true);
    setAnalysisStage("Extracting 13 Cleveland ML Feature Vectors...");

    setTimeout(() => {
      setAnalysisStage("Mapping [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]...");
    }, 600);

    setTimeout(() => {
      setAnalysisStage("Computing Risk Probability & SHAP Factor Weights...");
    }, 1200);

    setTimeout(async () => {
      try {
        const userEmail = localStorage.getItem("userEmail") || "";
        const userName = localStorage.getItem("userName") || form.name || "Patient";
        const submissionPayload = {
          ...form,
          user_email: userEmail,
          name: form.name && form.name.trim() ? form.name.trim() : userName
        };
        const result = await api.predict(submissionPayload);
        setIsAnalyzing(false);
        navigate("/prediction-result", { state: { result, input: submissionPayload } });
      } catch (err) {
        console.error("Submission error:", err);
        setIsAnalyzing(false);
        navigate("/prediction-result", { state: { input: form } });
      }
    }, 1800);
  };

  return (
    <div className="dashboard-page-wrapper">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <div className="dashboard-main-area">
        <Navbar onMobileMenuClick={() => setMobileOpen(true)} />

        {/* SCANNING & NEURAL ANALYSIS MODAL OVERLAY */}
        {isAnalyzing && (
          <div className="analyzing-overlay">
            <div className="analyzing-modal">
              <div className="analyzing-spinner">
                <Cpu size={42} className="spin-icon text-cyan" />
              </div>
              <h3>ML Model Inference Engine Running</h3>
              <p className="analyzing-stage-text">{analysisStage}</p>
              <div className="analyzing-progress-track">
                <div className="analyzing-progress-fill"></div>
              </div>
              <small>Calibrated to 13 Cleveland / UCI Clinical Features (Target: `num`)</small>
            </div>
          </div>
        )}

        <main className="dashboard-content-scroll">
          {/* HEADER */}
          <div className="prediction-wizard-header">
            <div>
              <span className="section-eyebrow">13-FEATURE ML DIAGNOSTIC PROTOCOL</span>
              <h1>Cleveland Cardiovascular ML Assessment</h1>
              <p>Direct mapping for <code>[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]</code>.</p>
            </div>

            {/* QUICK PRESET BUTTONS */}
            <div className="preset-quick-pills">
              <span className="preset-label">Load Sample Patient:</span>
              <button
                type="button"
                className="preset-pill pill-low"
                onClick={() => loadPreset("healthy")}
              >
                Healthy Athlete
              </button>
              <button
                type="button"
                className="preset-pill pill-mod"
                onClick={() => loadPreset("moderate")}
              >
                Moderate Risk
              </button>
              <button
                type="button"
                className="preset-pill pill-high"
                onClick={() => loadPreset("high")}
              >
                High Risk Alert
              </button>
            </div>
          </div>

          {/* 4-STEP PROGRESS BAR */}
          <div className="wizard-stepper">
            {[
              { num: 1, title: "1. Vitals & Lipids (age, sex, trestbps, chol)" },
              { num: 2, title: "2. Cardiac Stress & ECG (cp, restecg, thalach)" },
              { num: 3, title: "3. Ischemia & ST Segment (exang, oldpeak, slope)" },
              { num: 4, title: "4. Vessels & Defect (ca, thal, lifestyle)" }
            ].map((s) => (
              <div
                key={s.num}
                className={`stepper-item ${step === s.num ? "current" : step > s.num ? "completed" : ""}`}
                onClick={() => setStep(s.num)}
              >
                <div className="stepper-bubble">
                  {step > s.num ? <CheckCircle2 size={16} /> : s.num}
                </div>
                <span className="stepper-title">{s.title}</span>
              </div>
            ))}
          </div>

          {/* WIZARD CARD */}
          <div className="wizard-form-card">
            {/* STEP 1: DEMOGRAPHICS, BP & CHOLESTEROL */}
            {step === 1 && (
              <div className="wizard-step-content">
                <div className="step-section-intro">
                  <h2>Step 1: Patient Baseline, Blood Pressure & Lipids</h2>
                  <p>Covers <code>age</code>, <code>sex</code>, <code>trestbps</code> (resting BP), and <code>chol</code> (cholesterol).</p>
                </div>

                <div className="form-grid-3col">
                  <div className="form-group">
                    <label>Patient Full Name</label>
                    <input
                      type="text"
                      value={form.name}
                      onChange={(e) => updateForm("name", e.target.value)}
                    />
                  </div>

                  <div className="form-group">
                    <label><code>age</code>: Age (years)</label>
                    <input
                      type="number"
                      min="18"
                      max="100"
                      value={form.age}
                      onChange={(e) => updateForm("age", Number(e.target.value))}
                    />
                    <small className="field-hint">Range: 29 - 77 years</small>
                  </div>

                  <div className="form-group">
                    <label><code>sex</code>: Biological Sex</label>
                    <select
                      value={form.sex}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("sex", val);
                        updateForm("gender", val === 1 ? "Male" : "Female");
                      }}
                    >
                      <option value={1}>1: Male</option>
                      <option value={0}>0: Female</option>
                    </select>
                  </div>

                  <div className="form-group highlight-group">
                    <label><code>trestbps</code>: Resting Blood Pressure (mmHg)</label>
                    <input
                      type="number"
                      min="80"
                      max="220"
                      value={form.trestbps}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("trestbps", val);
                        updateForm("systolic_bp", val);
                      }}
                    />
                    <small className="field-hint">Target: &lt;120 mmHg (on hospital admission)</small>
                  </div>

                  <div className="form-group highlight-group">
                    <label><code>chol</code>: Total Serum Cholesterol (mg/dL)</label>
                    <input
                      type="number"
                      min="100"
                      max="600"
                      value={form.chol}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("chol", val);
                        updateForm("cholesterol", val);
                      }}
                    />
                    <small className="field-hint">Desirable: &lt;200 mg/dL</small>
                  </div>

                  <div className="form-group">
                    <label><code>fbs</code>: Fasting Blood Sugar &gt; 120 mg/dL</label>
                    <select
                      value={form.fbs}
                      onChange={(e) => updateForm("fbs", Number(e.target.value))}
                    >
                      <option value={0}>0: False (&le; 120 mg/dL)</option>
                      <option value={1}>1: True (&gt; 120 mg/dL - Diabetic/Pre-diabetic)</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* STEP 2: CHEST PAIN, ECG & MAX HEART RATE */}
            {step === 2 && (
              <div className="wizard-step-content">
                <div className="step-section-intro">
                  <h2>Step 2: Chest Pain, Resting ECG & Maximum Heart Rate</h2>
                  <p>Covers <code>cp</code> (Chest pain type), <code>restecg</code> (Resting ECG), and <code>thalach</code> (Max HR).</p>
                </div>

                <div className="form-grid-3col">
                  <div className="form-group highlight-group">
                    <label><code>cp</code>: Chest Pain Type (0 - 3)</label>
                    <select
                      value={form.cp}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("cp", val);
                        updateForm("chest_pain", val === 0 ? "Typical Angina" : val === 1 ? "Atypical Angina" : val === 2 ? "Non-anginal" : "Asymptomatic");
                      }}
                    >
                      <option value={0}>0: Typical Angina (Substernal pressure)</option>
                      <option value={1}>1: Atypical Angina (Discomfort)</option>
                      <option value={2}>2: Non-anginal Pain</option>
                      <option value={3}>3: Asymptomatic</option>
                    </select>
                  </div>

                  <div className="form-group highlight-group">
                    <label><code>restecg</code>: Resting Electrocardiographic Results</label>
                    <select
                      value={form.restecg}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("restecg", val);
                        updateForm("resting_ecg", val === 0 ? "Normal" : val === 1 ? "ST-T Abnormality" : "Left Ventricular Hypertrophy");
                      }}
                    >
                      <option value={0}>0: Normal</option>
                      <option value={1}>1: ST-T wave abnormality (T-wave inversion)</option>
                      <option value={2}>2: Left Ventricular Hypertrophy (Estes' criteria)</option>
                    </select>
                  </div>

                  <div className="form-group highlight-group">
                    <label><code>thalach</code>: Max Heart Rate Achieved (BPM)</label>
                    <input
                      type="number"
                      min="60"
                      max="220"
                      value={form.thalach}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("thalach", val);
                        updateForm("heart_rate", val);
                      }}
                    />
                    <small className="field-hint">During exercise treadmill test (Range: 71 - 202 BPM)</small>
                  </div>

                  <div className="form-group">
                    <label>Left Ventricular Ejection Fraction (%)</label>
                    <input
                      type="number"
                      min="15"
                      max="80"
                      value={form.ejection_fraction}
                      onChange={(e) => updateForm("ejection_fraction", Number(e.target.value))}
                    />
                    <small className="field-hint">Normal: 50 - 70%</small>
                  </div>

                  <div className="form-group">
                    <label>Serum Creatinine (mg/dL)</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0.4"
                      max="10.0"
                      value={form.serum_creatinine}
                      onChange={(e) => updateForm("serum_creatinine", Number(e.target.value))}
                    />
                    <small className="field-hint">Renal function: 0.7 - 1.2 mg/dL</small>
                  </div>
                </div>
              </div>
            )}

            {/* STEP 3: EXERCISE ANGINA & ST SEGMENT DEPRESSION */}
            {step === 3 && (
              <div className="wizard-step-content">
                <div className="step-section-intro">
                  <h2>Step 3: Exercise Induced Ischemia & ST Segment Depression</h2>
                  <p>Covers <code>exang</code> (Exercise Angina), <code>oldpeak</code> (ST Depression), and <code>slope</code> (ST Slope).</p>
                </div>

                <div className="form-grid-3col">
                  <div className="form-group highlight-group">
                    <label><code>exang</code>: Exercise Induced Angina (1 / 0)</label>
                    <select
                      value={form.exang}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("exang", val);
                        updateForm("exercise_angina", val === 1 ? "Yes" : "No");
                      }}
                    >
                      <option value={0}>0: No (No angina during stress test)</option>
                      <option value={1}>1: Yes (Angina induced by exercise)</option>
                    </select>
                  </div>

                  <div className="form-group highlight-group">
                    <label><code>oldpeak</code>: ST Depression (Exercise relative to rest)</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0.0"
                      max="7.0"
                      value={form.oldpeak}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("oldpeak", val);
                        updateForm("st_depression", val);
                      }}
                    />
                    <small className="field-hint">ECG ST segment depression (e.g. 0.0 - 6.2 mV)</small>
                  </div>

                  <div className="form-group highlight-group">
                    <label><code>slope</code>: Slope of Peak Exercise ST Segment</label>
                    <select
                      value={form.slope}
                      onChange={(e) => {
                        const val = Number(e.target.value);
                        updateForm("slope", val);
                        updateForm("st_slope", val === 0 ? "Upsloping" : val === 1 ? "Flat" : "Downsloping");
                      }}
                    >
                      <option value={0}>0: Upsloping (Healthy response)</option>
                      <option value={1}>1: Flat (Ischemic sign)</option>
                      <option value={2}>2: Downsloping (Severe myocardial ischemia)</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* STEP 4: MAJOR VESSELS, THALASSEMIA & LIFESTYLE */}
            {step === 4 && (
              <div className="wizard-step-content">
                <div className="step-section-intro">
                  <h2>Step 4: Major Vessels Fluoroscopy, Thalassemia & Lifestyle</h2>
                  <p>Covers <code>ca</code> (Vessels 0-3), <code>thal</code> (Thalassemia defect), and lifestyle habits.</p>
                </div>

                <div className="form-grid-3col">
                  <div className="form-group highlight-group">
                    <label><code>ca</code>: Major Vessels (0 - 3) Colored by Fluoroscopy</label>
                    <select
                      value={form.ca}
                      onChange={(e) => updateForm("ca", Number(e.target.value))}
                    >
                      <option value={0}>0: Zero major vessels occluded</option>
                      <option value={1}>1: One major vessel occluded</option>
                      <option value={2}>2: Two major vessels occluded</option>
                      <option value={3}>3: Three major vessels occluded</option>
                    </select>
                    <small className="field-hint">Count of major coronaries with &gt;50% stenosis</small>
                  </div>

                  <div className="form-group highlight-group">
                    <label><code>thal</code>: Thalassemia Heart Defect</label>
                    <select
                      value={form.thal}
                      onChange={(e) => updateForm("thal", Number(e.target.value))}
                    >
                      <option value={1}>1: Normal blood flow</option>
                      <option value={2}>2: Fixed defect (No blood flow in part of heart)</option>
                      <option value={3}>3: Reversible defect (Blood flow observed during rest)</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Tobacco / Smoking Habit</label>
                    <select
                      value={form.smoking}
                      onChange={(e) => updateForm("smoking", e.target.value)}
                    >
                      <option>Never</option>
                      <option>Occasionally</option>
                      <option>Regularly</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Weekly Exercise Activity</label>
                    <select
                      value={form.exercise_days}
                      onChange={(e) => updateForm("exercise_days", e.target.value)}
                    >
                      <option>0-1 days</option>
                      <option>2-3 days</option>
                      <option>4-5 days</option>
                      <option>6-7 days</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Daily Stress Level</label>
                    <select
                      value={form.stress_level}
                      onChange={(e) => updateForm("stress_level", e.target.value)}
                    >
                      <option>Low</option>
                      <option>Medium</option>
                      <option>High</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Average Sleep Duration</label>
                    <select
                      value={form.sleep_hours}
                      onChange={(e) => updateForm("sleep_hours", e.target.value)}
                    >
                      <option>Less than 5 hours</option>
                      <option>5-7 hours</option>
                      <option>7-9 hours</option>
                      <option>More than 9 hours</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* WIZARD ACTIONS */}
            <div className="wizard-actions-bar">
              {step > 1 ? (
                <button
                  type="button"
                  className="wizard-back-btn"
                  onClick={() => setStep(step - 1)}
                >
                  <ArrowLeft size={16} />
                  <span>Previous Step</span>
                </button>
              ) : (
                <div></div>
              )}

              {step < 4 ? (
                <button
                  type="button"
                  className="wizard-next-btn"
                  onClick={() => setStep(step + 1)}
                >
                  <span>Next Step</span>
                  <ArrowRight size={16} />
                </button>
              ) : (
                <button
                  type="button"
                  className="wizard-submit-btn"
                  onClick={handleSubmitPrediction}
                >
                  <Sparkles size={18} />
                  <span>Run 13-Feature AI Diagnostic Assessment →</span>
                </button>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}