import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  FileText,
  Printer,
  Download,
  CheckCircle2,
  AlertTriangle,
  Stethoscope,
  Heart,
  Calendar,
  Building,
  User,
  PlusCircle,
  Clock
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Reports() {
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null);
  const [historyItems, setHistoryItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const userName = localStorage.getItem("userName") || "Aarav Sharma";
  const userEmail = localStorage.getItem("userEmail") || "";

  useEffect(() => {
    const loadReports = async () => {
      setLoading(true);
      try {
        const data = await api.getHistory("", "", userEmail);
        let items = data.items || [];

        // Fallback to last prediction in localStorage if list is empty
        if (items.length === 0) {
          const cached = localStorage.getItem("lastPredictionResult");
          if (cached) {
            try {
              const parsed = JSON.parse(cached);
              items = [{
                id: parsed.prediction_id || "PRED-LAST",
                patient_name: parsed.patient_name || userName,
                timestamp: parsed.timestamp || new Date().toISOString().replace("T", " ").substring(0, 16),
                risk_score: parsed.risk_score || 0,
                risk_level: parsed.risk_level || "Low Risk",
                probability_percentage: parsed.probability_percentage || 0,
                heart_health_score: parsed.heart_health_score || 100,
                systolic_bp: parsed.input_data?.systolic_bp || parsed.input_data?.trestbps || 120,
                diastolic_bp: parsed.input_data?.diastolic_bp || 80,
                cholesterol: parsed.input_data?.chol || parsed.input_data?.cholesterol || 190,
                ejection_fraction: parsed.input_data?.ejection_fraction || 60,
                serum_creatinine: parsed.input_data?.serum_creatinine || 0.9,
                smoking: parsed.input_data?.smoking || "Never",
                chest_pain: parsed.input_data?.chest_pain || "None",
                model_source: parsed.model_source || "LightGBM ML Classifier",
                summary_message: parsed.summary_message || "Clinical assessment completed."
              }];
            } catch (e) {
              console.warn("Cached prediction parse error:", e);
            }
          }
        }

        setHistoryItems(items);
        if (items.length > 0) {
          setSelectedReport(items[0]);
        }
      } catch (err) {
        console.error("Reports loading error:", err);
      } finally {
        setLoading(false);
      }
    };

    loadReports();
  }, [userEmail, userName]);

  return (
    <div className="dashboard-page-wrapper">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <div className="dashboard-main-area">
        <Navbar onMobileMenuClick={() => setMobileOpen(true)} />

        <main className="dashboard-content-scroll">
          {/* HEADER */}
          <div className="page-header-row">
            <div>
              <span className="section-eyebrow">FORMAL CLINICAL DOCUMENTATION</span>
              <h1>Medical Health Reports & Diagnostic Summaries</h1>
              <p>Download or print official structured clinical summaries formatted for cardiologist reviews.</p>
            </div>

            <div className="header-action-group">
              <button
                type="button"
                className="primary-action-btn"
                onClick={() => window.print()}
                disabled={!selectedReport}
              >
                <Printer size={16} />
                <span>Print Official PDF</span>
              </button>
            </div>
          </div>

          {/* REPORT SELECTOR CHIPS */}
          {historyItems.length > 0 && (
            <div className="report-selector-bar">
              <span>Select Assessment Run:</span>
              {historyItems.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  className={`report-select-chip ${selectedReport?.id === item.id ? "active" : ""}`}
                  onClick={() => setSelectedReport(item)}
                >
                  <strong>{item.patient_name}</strong>
                  <small>{item.timestamp.split(" ")[0]} ({item.risk_score}%)</small>
                </button>
              ))}
            </div>
          )}

          {/* EMPTY STATE IF NO REPORTS */}
          {!loading && historyItems.length === 0 && (
            <div style={{ background: "var(--card-bg, white)", padding: "60px 20px", textAlign: "center", borderRadius: "16px", border: "1px solid var(--border-color, #e2e8f0)", marginTop: "20px" }}>
              <Clock size={48} style={{ color: "#94a3b8", marginBottom: "12px" }} />
              <h3 style={{ fontSize: "18px", color: "#1e293b", marginBottom: "8px", fontWeight: "700" }}>No Clinical Reports Generated Yet</h3>
              <p style={{ color: "#64748b", maxWidth: "460px", margin: "0 auto 20px", fontSize: "14px" }}>
                Run an evidence-based 13-biomarker AI cardiovascular evaluation to generate and print your formal clinical summary.
              </p>
              <button
                type="button"
                className="primary-action-btn"
                style={{ display: "inline-flex", margin: "0 auto" }}
                onClick={() => navigate("/new-prediction")}
              >
                <PlusCircle size={16} />
                <span>Run New Assessment</span>
              </button>
            </div>
          )}

          {/* FORMAL CLINICAL REPORT SHEET */}
          {selectedReport && (
            <div className="formal-report-sheet print-target">
              {/* LETTERHEAD */}
              <div className="report-letterhead">
                <div className="letterhead-brand">
                  <div className="letterhead-icon">
                    <Heart size={26} fill="#2563eb" color="#2563eb" />
                  </div>
                  <div>
                    <h2>HEARTCARE CLINICAL AI INSTITUTE</h2>
                    <span>Cardiovascular Risk Assessment & Telemetry Service</span>
                  </div>
                </div>

                <div className="letterhead-meta">
                  <p><strong>REPORT ID:</strong> REP-{selectedReport.id}</p>
                  <p><strong>DATE:</strong> {selectedReport.timestamp}</p>
                  <p><strong>ALGORITHM:</strong> {selectedReport.model_source || "LightGBM Multi-Class ML Model"}</p>
                </div>
              </div>

              <div className="report-divider"></div>

              {/* PATIENT INFO BANNER */}
              <div className="report-patient-banner">
                <div className="patient-grid-4col">
                  <div>
                    <label>PATIENT NAME</label>
                    <strong>{selectedReport.patient_name}</strong>
                  </div>
                  <div>
                    <label>AGE / GENDER</label>
                    <strong>{selectedReport.age || 50} Years / {selectedReport.gender || "Unspecified"}</strong>
                  </div>
                  <div>
                    <label>EVALUATION DATE</label>
                    <strong>{selectedReport.timestamp}</strong>
                  </div>
                  <div>
                    <label>CLINICAL STATUS</label>
                    <span className={`status-badge-inline ${selectedReport.risk_score < 25 ? "badge-low" : selectedReport.risk_score < 50 ? "badge-mod" : "badge-high"}`}>
                      {selectedReport.risk_level}
                    </span>
                  </div>
                </div>
              </div>

              {/* PRIMARY RISK SCORE SUMMARY */}
              <div className="report-risk-summary-card">
                <div className="risk-score-display">
                  <span className="risk-score-num">{selectedReport.risk_score}</span>
                  <span className="risk-score-denom">/100</span>
                </div>
                <div className="risk-score-explanation">
                  <h3>{selectedReport.risk_level} Classification</h3>
                  <p>{selectedReport.summary_message || "Predicted multi-factor cardiovascular risk profile computed using trained LightGBM algorithm."}</p>
                  <div className="risk-probability-bar">
                    <div
                      className="risk-probability-fill"
                      style={{
                        width: `${Math.min(100, Math.max(5, selectedReport.probability_percentage || selectedReport.risk_score))}%`,
                        background: selectedReport.risk_score < 25 ? "#10b981" : selectedReport.risk_score < 50 ? "#f59e0b" : "#ef4444"
                      }}
                    ></div>
                  </div>
                  <small>Calculated Probability: <strong>{selectedReport.probability_percentage || selectedReport.risk_score}%</strong></small>
                </div>
              </div>

              {/* MEASURED BIOMARKERS TABLE */}
              <div className="report-biomarkers-section">
                <h3>Measured Clinical Biomarkers & Diagnostic Features</h3>
                <table className="report-biomarker-table">
                  <thead>
                    <tr>
                      <th>Biomarker / Clinical Factor</th>
                      <th>Observed Value</th>
                      <th>Reference / Target Range</th>
                      <th>Status Evaluation</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Resting Blood Pressure (Systolic / Diastolic)</td>
                      <td>{selectedReport.systolic_bp || 120} / {selectedReport.diastolic_bp || 80} mmHg</td>
                      <td>&lt;120 / &lt;80 mmHg</td>
                      <td>
                        <span className={`status-pill ${selectedReport.systolic_bp >= 140 ? "pill-danger" : selectedReport.systolic_bp >= 125 ? "pill-warning" : "pill-normal"}`}>
                          {selectedReport.systolic_bp >= 140 ? "Stage 2 Hypertension" : selectedReport.systolic_bp >= 125 ? "Elevated" : "Optimal"}
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <td>Left Ventricular Ejection Fraction (LVEF)</td>
                      <td>{selectedReport.ejection_fraction || 55}%</td>
                      <td>55% – 70%</td>
                      <td>
                        <span className={`status-pill ${selectedReport.ejection_fraction < 40 ? "pill-danger" : selectedReport.ejection_fraction < 50 ? "pill-warning" : "pill-normal"}`}>
                          {selectedReport.ejection_fraction < 40 ? "Severely Reduced" : selectedReport.ejection_fraction < 50 ? "Mildly Reduced" : "Normal"}
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <td>Serum Creatinine</td>
                      <td>{selectedReport.serum_creatinine || 0.9} mg/dL</td>
                      <td>0.6 – 1.2 mg/dL</td>
                      <td>
                        <span className={`status-pill ${selectedReport.serum_creatinine > 1.3 ? "pill-warning" : "pill-normal"}`}>
                          {selectedReport.serum_creatinine > 1.3 ? "Elevated" : "Normal Renal Function"}
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <td>Total Serum Cholesterol</td>
                      <td>{selectedReport.cholesterol || 195} mg/dL</td>
                      <td>&lt;200 mg/dL</td>
                      <td>
                        <span className={`status-pill ${selectedReport.cholesterol >= 200 ? "pill-warning" : "pill-normal"}`}>
                          {selectedReport.cholesterol >= 200 ? "Borderline High" : "Desirable"}
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <td>Tobacco / Smoking Status</td>
                      <td>{selectedReport.smoking || "Never"}</td>
                      <td>Non-Smoker</td>
                      <td>
                        <span className={`status-pill ${selectedReport.smoking === "Regularly" ? "pill-danger" : "pill-normal"}`}>
                          {selectedReport.smoking === "Regularly" ? "High Risk" : "Controlled"}
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <td>Chest Pain Experience</td>
                      <td>{selectedReport.chest_pain || "None"}</td>
                      <td>Asymptomatic / None</td>
                      <td>
                        <span className={`status-pill ${selectedReport.chest_pain === "Severe" || selectedReport.chest_pain === "Moderate" ? "pill-danger" : "pill-normal"}`}>
                          {selectedReport.chest_pain || "None"}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* PHYSICIAN SIGN-OFF BLOCK */}
              <div className="report-signoff-grid">
                <div className="signoff-col">
                  <h4>Clinical Recommendations & Action Plan</h4>
                  <ul>
                    <li>Initiate daily home arterial blood pressure logs morning and evening.</li>
                    <li>Follow DASH dietary protocol with dietary sodium &lt;1,500mg/day.</li>
                    <li>Schedule comprehensive 12-lead resting ECG and echocardiography review.</li>
                    <li>Review regular exercise routine with cardiologist before intense exertion.</li>
                  </ul>
                </div>
                <div className="signoff-signature-box">
                  <div className="signature-line">
                    <em>HeartCare Automated Clinical AI Validator</em>
                  </div>
                  <small>Authorized Clinical Decision Support System</small>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
