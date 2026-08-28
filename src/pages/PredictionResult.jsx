import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Heart,
  Activity,
  AlertTriangle,
  CheckCircle2,
  Sliders,
  Printer,
  FileText,
  ArrowLeft,
  Sparkles,
  ShieldCheck,
  Stethoscope,
  Utensils,
  Share2,
  TrendingDown,
  TrendingUp,
  Info,
  RefreshCw,
  Clock
} from "lucide-react";
import confetti from "canvas-confetti";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import RiskGauge from "../components/RiskGauge";
import { api } from "../services/api";

export default function PredictionResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);

  // Retrieve result passed from wizard or fallback to localStorage
  const initialResult =
    location.state?.result ||
    JSON.parse(localStorage.getItem("lastPredictionResult") || "null") ||
    {
      prediction_id: "PRED-SAMPLE",
      timestamp: "Today",
      patient_name: "Aarav Sharma",
      risk_score: 18,
      risk_level: "Low Risk",
      probability_percentage: 18.0,
      heart_health_score: 82,
      model_source: "AHA/Cleveland Clinical AI Heuristic Engine",
      bmi: 23.8,
      bmi_category: "Normal Weight",
      urgency_level: "low",
      summary_message: "Your cardiovascular profile exhibits strong protective indicators. Continue healthy maintenance habits.",
      confidence_interval: { lower: 13.0, upper: 23.0 },
      top_risk_factors: [
        { feature: "age", label: "Age 48", impact_score: 8, severity: "normal", explanation: "Baseline age monitoring." }
      ],
      protective_factors: [
        { feature: "ejection_fraction", label: "Ejection Fraction 60%", impact_score: -14, severity: "protective", explanation: "Strong left ventricular systolic performance." },
        { feature: "physical_activity", label: "Regular Cardio", impact_score: -12, severity: "protective", explanation: "Regular aerobic conditioning." }
      ],
      all_factor_impacts: [],
      recommendations: [
        { category: "Protective Strengths", title: "Maintain Active Regimen", description: "Keep up regular zone 2 exercise.", urgency: "maintenance", icon: "CheckCircle" },
        { category: "Dietary Strategy", title: "Heart-Healthy Balanced Nutrition", description: "Rich in antioxidants, lean proteins, and fiber.", urgency: "moderate", icon: "Utensils" }
      ]
    };

  const [result, setResult] = useState(initialResult);
  const baseInput = location.state?.input || {
    name: result.patient_name,
    age: 48,
    systolic_bp: 135,
    cholesterol: 205,
    smoking: "Never",
    exercise_days: "2-3 days",
    ejection_fraction: 55,
    serum_creatinine: 1.0
  };

  // What-If Dynamic Multi-Parameter State
  const [simBp, setSimBp] = useState(baseInput.systolic_bp || 135);
  const [simEf, setSimEf] = useState(baseInput.ejection_fraction || 55);
  const [simChol, setSimChol] = useState(baseInput.cholesterol || 205);
  const [simCr, setSimCr] = useState(baseInput.serum_creatinine || 1.0);
  const [simSmoking, setSimSmoking] = useState(baseInput.smoking || "Never");
  const [simExercise, setSimExercise] = useState(baseInput.exercise_days || "2-3 days");
  const [simComparison, setSimComparison] = useState(null);

  // Trigger celebration confetti if low risk
  useEffect(() => {
    if (result.risk_score < 25) {
      try {
        confetti({
          particleCount: 45,
          spread: 60,
          origin: { y: 0.6 }
        });
      } catch {}
    }
  }, [result.risk_score]);

  // Real-time continuous simulation on ANY parameter change
  useEffect(() => {
    const timer = setTimeout(async () => {
      try {
        const simData = await api.simulate(baseInput, {
          systolic_bp: simBp,
          ejection_fraction: simEf,
          cholesterol: simChol,
          serum_creatinine: simCr,
          smoking: simSmoking,
          exercise_days: simExercise
        });
        setSimComparison(simData);
      } catch (err) {
        console.error("Continuous simulation error:", err);
      }
    }, 150);
    return () => clearTimeout(timer);
  }, [simBp, simEf, simChol, simCr, simSmoking, simExercise]);

  return (
    <div className="dashboard-page-wrapper">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <div className="dashboard-main-area">
        <Navbar onMobileMenuClick={() => setMobileOpen(true)} />

        <main className="dashboard-content-scroll print-target">
          {/* TOP ACTION BAR */}
          <div className="result-topbar">
            <div>
              <span className="section-eyebrow">AI INFERENCE DIAGNOSTIC RESULT</span>
              <h1>Cardiovascular Assessment Report</h1>
              <p>
                Patient: <strong>{result.patient_name}</strong> | ID: <code>{result.prediction_id}</code> | Date: {result.timestamp}
              </p>
            </div>

            <div className="result-actions-group">
              <button
                className="secondary-action-btn"
                onClick={() => navigate("/history")}
                title="View in History"
              >
                <Clock size={16} />
                <span>View in History</span>
              </button>
              <button
                className="secondary-action-btn"
                onClick={() => navigate("/reports")}
                title="Formal Clinical Report"
              >
                <FileText size={16} />
                <span>Clinical Report</span>
              </button>
              <button
                className="secondary-action-btn"
                onClick={() => window.print()}
                title="Print Report"
              >
                <Printer size={16} />
                <span>Print PDF</span>
              </button>
              <button
                className="primary-action-btn"
                onClick={() => navigate("/new-prediction")}
              >
                <Activity size={16} />
                <span>New Evaluation</span>
              </button>
            </div>
          </div>

          {/* PRIMARY HERO CARD: GAUGE + HEALTH SCORE */}
          <div className="result-hero-grid">
            <div className="result-gauge-card">
              <div className="gauge-header">
                <h3>Overall Risk Probability</h3>
                <span className="model-source-tag">{result.model_source}</span>
              </div>

              <div className="gauge-center-wrapper">
                <RiskGauge score={result.risk_score} level={result.risk_level} size={200} />
              </div>

              <div className="confidence-interval-note">
                <span>95% Confidence Interval:</span>
                <strong>
                  {result.confidence_interval?.lower || Math.max(0, result.risk_score - 5)}% - {result.confidence_interval?.upper || Math.min(100, result.risk_score + 5)}%
                </strong>
              </div>
            </div>

            {/* CLINICAL SUMMARY & VITALITY SCORE */}
            <div className="result-summary-card">
              <div className="summary-card-header">
                <div className="vitality-badge">
                  <Heart size={18} className="text-rose" fill="#ef4444" />
                  <span>Heart Health Score: <strong>{result.heart_health_score}/100</strong></span>
                </div>
                <span className={`risk-status-pill ${result.risk_score < 30 ? "pill-low" : result.risk_score < 60 ? "pill-mod" : "pill-high"}`}>
                  {result.risk_level}
                </span>
              </div>

              <h2>Diagnostic Assessment Summary</h2>
              <p className="clinical-statement">{result.summary_message}</p>

              <div className="summary-biomarker-chips">
                <div className="biomarker-chip">
                  <span className="bio-label">Calculated BMI</span>
                  <strong>{result.bmi} kg/m² ({result.bmi_category})</strong>
                </div>
                <div className="biomarker-chip">
                  <span className="bio-label">Risk Category</span>
                  <strong>{result.risk_level}</strong>
                </div>
                <div className="biomarker-chip">
                  <span className="bio-label">Urgency Tier</span>
                  <strong className="text-capitalize">{result.urgency_level} Priority</strong>
                </div>
              </div>
            </div>
          </div>

          {/* EXPLAINABLE AI: FEATURE IMPACT BREAKDOWN */}
          <div className="explainability-section">
            <div className="section-title-row">
              <div className="section-title-icon bg-blue-light">
                <Sparkles size={20} className="text-blue" />
              </div>
              <div>
                <h2>Explainable AI: Key Factor Breakdown (SHAP-Style)</h2>
                <p>Understand which physiological biomarkers and lifestyle variables drove this prediction.</p>
              </div>
            </div>

            <div className="factors-dual-grid">
              {/* Risk Increasing Factors */}
              <div className="factor-box risk-increasing-box">
                <div className="factor-box-header">
                  <div className="factor-badge badge-elevated">
                    <TrendingUp size={16} />
                    <span>Factors Increasing Risk</span>
                  </div>
                </div>

                <div className="factor-items-list">
                  {result.top_risk_factors?.length > 0 ? (
                    result.top_risk_factors.map((f, idx) => (
                      <div key={idx} className="factor-item item-risk">
                        <div className="factor-item-top">
                          <strong>{f.label}</strong>
                          <span className="impact-weight-tag weight-danger">+{Math.abs(f.impact_score)}%</span>
                        </div>
                        <p>{f.explanation}</p>
                      </div>
                    ))
                  ) : (
                    <div className="factor-empty">No severe risk-increasing biomarkers detected.</div>
                  )}
                </div>
              </div>

              {/* Protective Factors */}
              <div className="factor-box protective-box">
                <div className="factor-box-header">
                  <div className="factor-badge badge-protective">
                    <TrendingDown size={16} />
                    <span>Protective Factors</span>
                  </div>
                </div>

                <div className="factor-items-list">
                  {result.protective_factors?.length > 0 ? (
                    result.protective_factors.map((f, idx) => (
                      <div key={idx} className="factor-item item-protective">
                        <div className="factor-item-top">
                          <strong>{f.label}</strong>
                          <span className="impact-weight-tag weight-success">-{Math.abs(f.impact_score)}%</span>
                        </div>
                        <p>{f.explanation}</p>
                      </div>
                    ))
                  ) : (
                    <div className="factor-empty">Incorporate cardiovascular exercise and balanced nutrition to build protective buffers.</div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* DYNAMIC REAL-TIME "WHAT-IF" RISK SIMULATOR */}
          <div className="simulator-card">
            <div className="simulator-header">
              <div className="sim-title-group">
                <div className="tool-icon bg-purple-light"><Sliders size={20} /></div>
                <div>
                  <h2>Live Dynamic "What-If" Health Simulator</h2>
                  <p>Drag any biomarker slider below to watch the projected cardiac risk update in real time.</p>
                </div>
              </div>

              <div className="live-pill status-online" style={{ padding: "4px 10px", fontSize: "11px" }}>
                <span className="status-indicator-dot online"></span>
                <span>Live Continuous Recalculation</span>
              </div>
            </div>

            <div className="simulator-body-grid">
              <div className="sim-controls">
                {/* Systolic BP Slider */}
                <div className="sim-group">
                  <div className="label-with-icon">
                    <label>Target Systolic BP: <strong>{simBp} mmHg</strong></label>
                    <small className={simBp < 125 ? "text-emerald" : simBp < 140 ? "text-amber" : "text-rose"}>
                      {simBp < 125 ? "Optimal" : simBp < 140 ? "Pre-HTN" : "Stage 2 HTN"}
                    </small>
                  </div>
                  <input
                    type="range"
                    min="100"
                    max="180"
                    value={simBp}
                    onChange={(e) => setSimBp(Number(e.target.value))}
                    className="range-slider"
                  />
                  <div className="slider-labels">
                    <span>100 (Optimal)</span>
                    <span>140 (Hypertension)</span>
                    <span>180 (Severe)</span>
                  </div>
                </div>

                {/* Ejection Fraction Slider */}
                <div className="sim-group">
                  <div className="label-with-icon">
                    <label>Ejection Fraction: <strong>{simEf}%</strong></label>
                    <small className={simEf >= 50 ? "text-emerald" : "text-rose"}>
                      {simEf >= 50 ? "Preserved Pump" : "Reduced Pump (HFrEF)"}
                    </small>
                  </div>
                  <input
                    type="range"
                    min="25"
                    max="70"
                    value={simEf}
                    onChange={(e) => setSimEf(Number(e.target.value))}
                    className="range-slider"
                  />
                  <div className="slider-labels">
                    <span>25% (Critical)</span>
                    <span>50% (Normal Baseline)</span>
                    <span>70% (Athlete)</span>
                  </div>
                </div>

                {/* Cholesterol Slider */}
                <div className="sim-group">
                  <div className="label-with-icon">
                    <label>Serum Cholesterol: <strong>{simChol} mg/dL</strong></label>
                    <small className={simChol < 200 ? "text-emerald" : "text-rose"}>
                      {simChol < 200 ? "Desirable" : "High LDL Risk"}
                    </small>
                  </div>
                  <input
                    type="range"
                    min="140"
                    max="320"
                    value={simChol}
                    onChange={(e) => setSimChol(Number(e.target.value))}
                    className="range-slider"
                  />
                </div>

                {/* Lifestyle Multi-Toggles */}
                <div className="sim-row-2col">
                  <div className="sim-group">
                    <label>Smoking Status</label>
                    <select
                      value={simSmoking}
                      onChange={(e) => setSimSmoking(e.target.value)}
                      className="sim-select"
                    >
                      <option>Never</option>
                      <option>Occasionally</option>
                      <option>Regularly</option>
                    </select>
                  </div>

                  <div className="sim-group">
                    <label>Weekly Exercise</label>
                    <select
                      value={simExercise}
                      onChange={(e) => setSimExercise(e.target.value)}
                      className="sim-select"
                    >
                      <option>0-1 days</option>
                      <option>2-3 days</option>
                      <option>4-5 days</option>
                      <option>6-7 days</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* DYNAMIC SIMULATION REAL-TIME OUTPUT */}
              <div className="sim-output-panel">
                <span className="sim-out-label">DYNAMIC HEALTH OUTCOME</span>

                <div className="sim-score-compare">
                  <div className="sim-score-col">
                    <small>Baseline Risk</small>
                    <strong>{result.risk_score}%</strong>
                  </div>

                  <div className="sim-arrow-divider">➔</div>

                  <div className="sim-score-col simulated-col">
                    <small>Projected Risk</small>
                    <strong className={simComparison?.simulated.risk_score < 30 ? "text-emerald" : "text-amber"}>
                      {simComparison ? `${simComparison.simulated.risk_score}%` : `${result.risk_score}%`}
                    </strong>
                  </div>
                </div>

                {simComparison && (
                  <div className={`sim-delta-badge ${simComparison.delta.risk_score_diff <= 0 ? "delta-good" : "delta-bad"}`}>
                    {simComparison.delta.risk_score_diff <= 0 ? (
                      <>
                        <TrendingDown size={16} />
                        <span>Risk Reduced by {Math.abs(simComparison.delta.risk_score_diff)} points ({Math.abs(simComparison.delta.probability_diff)}%)</span>
                      </>
                    ) : (
                      <>
                        <TrendingUp size={16} />
                        <span>Risk Increased by {simComparison.delta.risk_score_diff} points</span>
                      </>
                    )}
                  </div>
                )}

                <p className="sim-note">
                  *Simulated continuously via FastAPI ML inference engine with immediate feedback.
                </p>
              </div>
            </div>
          </div>

          {/* CLINICAL RECOMMENDATIONS SECTION */}
          <div className="recommendations-section">
            <div className="section-title-row">
              <div className="section-title-icon bg-emerald-light">
                <ShieldCheck size={20} className="text-emerald" />
              </div>
              <div>
                <h2>Evidence-Based Clinical Action Plan</h2>
                <p>Personalized dietary, lifestyle, and clinical monitoring recommendations tailored to your findings.</p>
              </div>
            </div>

            <div className="recommendations-grid">
              {result.recommendations?.map((rec, idx) => (
                <div key={idx} className="recommendation-card">
                  <div className="rec-card-top">
                    <span className="rec-category-tag">{rec.category}</span>
                    <span className={`rec-urgency-tag urgency-${rec.urgency}`}>{rec.urgency}</span>
                  </div>
                  <h3>{rec.title}</h3>
                  <p>{rec.description}</p>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}