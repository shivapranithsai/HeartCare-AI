import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Heart,
  Activity,
  AlertTriangle,
  ShieldCheck,
  PlusCircle,
  TrendingUp,
  FileText,
  Calendar,
  ChevronRight,
  Sparkles,
  RefreshCw,
  Radio,
  ArrowRight,
  ClipboardList,
  Clock,
  Droplets,
  Gauge,
  Zap,
  Stethoscope
} from "lucide-react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, PieChart, Pie, Cell } from "recharts";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import StatCard from "../components/StatCard";
import EcgMonitor from "../components/EcgMonitor";
import { api } from "../services/api";

const PIE_COLORS = ["#10b981", "#f59e0b", "#f97316", "#ef4444"];

export default function Dashboard() {
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [analytics, setAnalytics] = useState(null);
  const [historyItems, setHistoryItems] = useState([]);
  const [liveBpm, setLiveBpm] = useState(72);
  const [liveStreamActive, setLiveStreamActive] = useState(true);

  const userName = localStorage.getItem("userName") || "Clinician";
  const userRole = localStorage.getItem("userRole") || "Cardiologist / Physician";
  const userEmail = localStorage.getItem("userEmail") || "";

  const loadData = async () => {
    setLoading(true);
    try {
      const [analyticsData, historyData] = await Promise.all([
        api.getAnalytics(userEmail),
        api.getHistory("", "", userEmail)
      ]);
      setAnalytics(analyticsData);
      const items = historyData.items || [];
      setHistoryItems(items);

      const latest = analyticsData?.latest_assessment || (items.length > 0 ? items[0] : null);

      if (latest) {
        if (latest.risk_score >= 60) setLiveBpm(88);
        else if (latest.risk_score >= 40) setLiveBpm(78);
        else setLiveBpm(68);
      } else {
        setLiveBpm(72);
      }
    } catch (err) {
      console.error("Dashboard data load error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [userEmail]);

  // Dynamic live BPM fluctuation simulator
  useEffect(() => {
    if (!liveStreamActive) return;
    const interval = setInterval(() => {
      setLiveBpm((prev) => {
        const delta = Math.floor(Math.random() * 5) - 2;
        return Math.max(58, Math.min(105, prev + delta));
      });
    }, 3000);
    return () => clearInterval(interval);
  }, [liveStreamActive]);

  const latestAssessment = analytics?.latest_assessment || (historyItems.length > 0 ? historyItems[0] : null);
  const isNewUser = !latestAssessment;

  // Prepare Pie Chart data
  const pieData = analytics?.risk_distribution
    ? Object.entries(analytics.risk_distribution)
        .filter(([_, val]) => val > 0)
        .map(([name, value]) => ({ name, value }))
    : [];

  return (
    <div className="dashboard-page-wrapper">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <div className="dashboard-main-area">
        <Navbar onMobileMenuClick={() => setMobileOpen(true)} />

        <main className="dashboard-content-scroll">
          {/* WELCOME HEADER */}
          <div className="dashboard-welcome-header">
            <div>
              <span className="section-eyebrow">CLINICAL COMMAND CENTER • {userRole.toUpperCase()}</span>
              <h1>Welcome back, {userName}!</h1>
              <p>
                {isNewUser
                  ? "Complete your health profile to calculate your risk score."
                  : "Live personalized cardiac telemetry and biomarker intelligence."}
              </p>
            </div>

            <div className="header-action-group">
              <button
                type="button"
                className={`secondary-action-btn ${liveStreamActive ? "status-online" : ""}`}
                onClick={() => setLiveStreamActive(!liveStreamActive)}
                title="Toggle live telemetry"
              >
                <Radio size={16} className={liveStreamActive ? "spin-pulse text-emerald" : ""} />
                <span>{liveStreamActive ? "Telemetry Active" : "Stream Paused"}</span>
              </button>

              <button className="secondary-action-btn" onClick={loadData} title="Sync latest data">
                <RefreshCw size={16} className={loading ? "spin-icon" : ""} />
                <span>Sync Data</span>
              </button>

              <button
                className="primary-action-btn"
                onClick={() => navigate("/new-prediction")}
              >
                <PlusCircle size={18} />
                <span>{isNewUser ? "Launch Diagnostic Assessment" : "Run New AI Prediction"}</span>
              </button>
            </div>
          </div>

          {/* NEW USER ONBOARDING ZERO-DATA BANNER */}
          {isNewUser && (
            <div
              style={{
                background: "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
                color: "white",
                padding: "24px 28px",
                borderRadius: "16px",
                marginBottom: "24px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                boxShadow: "0 10px 25px rgba(2, 132, 199, 0.25)",
                gap: "20px",
                flexWrap: "wrap"
              }}
            >
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px" }}>
                  <Sparkles size={18} className="text-amber" />
                  <strong style={{ fontSize: "16px", letterSpacing: "0.3px" }}>
                    Complete your health profile to calculate your risk score.
                  </strong>
                </div>
                <p style={{ margin: 0, fontSize: "14px", color: "#e0f2fe", maxWidth: "680px", lineHeight: "1.5" }}>
                  Evaluate 13 key physiological biomarkers including resting blood pressure, cholesterol, ST segment slope, and ejection fraction using our trained LightGBM ML model.
                </p>
              </div>

              <button
                type="button"
                onClick={() => navigate("/new-prediction")}
                style={{
                  background: "white",
                  color: "#0369a1",
                  border: "none",
                  padding: "12px 20px",
                  borderRadius: "10px",
                  fontWeight: "700",
                  fontSize: "14px",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  whiteSpace: "nowrap",
                  boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)"
                }}
              >
                <span>Launch Diagnostic Assessment</span>
                <ArrowRight size={16} />
              </button>
            </div>
          )}

          {/* 4 PRIMARY STAT CARDS */}
          <div className="dashboard-stats-grid">
            <StatCard
              title="Heart Health Score"
              value={latestAssessment ? `${latestAssessment.heart_health_score}/100` : "—"}
              description={latestAssessment ? `Clinical Status: ${latestAssessment.risk_level}` : "Complete your health profile to calculate your risk score."}
              iconType="heart"
              variant="blue"
              trend={latestAssessment ? `${latestAssessment.probability_percentage}% Prob` : null}
              trendDirection={latestAssessment?.risk_score >= 50 ? "down" : "up"}
            />
            <StatCard
              title="Cardiovascular Risk Index"
              value={latestAssessment ? `${latestAssessment.risk_score}%` : "—"}
              description={latestAssessment ? "Calculated 10-year risk" : "Complete your health profile to calculate your risk score."}
              iconType="activity"
              variant={latestAssessment?.risk_score >= 50 ? "orange" : "emerald"}
              trend={latestAssessment ? (latestAssessment.risk_score < 30 ? "Optimal Low" : latestAssessment.risk_score < 60 ? "Moderate Risk" : "High Alert") : null}
              trendDirection={latestAssessment?.risk_score >= 50 ? "down" : "up"}
            />
            <StatCard
              title="Total Assessments"
              value={(analytics?.total_assessments !== undefined ? analytics.total_assessments : historyItems.length).toString()}
              description={isNewUser ? "No evaluations recorded" : "Evaluations in your account"}
              iconType="shield"
              variant="purple"
            />
            <StatCard
              title="Clinical Status"
              value={latestAssessment?.risk_level || "Not Evaluated"}
              description={latestAssessment ? `Updated: ${latestAssessment.timestamp ? latestAssessment.timestamp.split(" ")[0] : "Recent"}` : "Complete your health profile to calculate your risk score."}
              iconType="warning"
              variant={latestAssessment?.risk_score >= 60 ? "rose" : "cyan"}
            />
          </div>

          {/* BIOMARKER TELEMETRY STRIP (RENDERED WHEN EVALUATION EXISTS) */}
          {latestAssessment && (
            <div
              style={{
                background: "#ffffff",
                borderRadius: "16px",
                border: "1px solid #e2e8f0",
                padding: "20px 24px",
                marginBottom: "24px",
                boxShadow: "0 1px 3px rgba(0,0,0,0.05)"
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", flexWrap: "wrap", gap: "10px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <Activity size={18} className="text-primary" />
                  <h3 style={{ fontSize: "15px", fontWeight: "700", color: "#0f172a", margin: 0 }}>
                    Personalized Biomarker Telemetry
                  </h3>
                </div>
                <span style={{ fontSize: "12px", color: "#64748b", fontWeight: "600" }}>
                  Patient: {latestAssessment.patient_name} • Evaluated {latestAssessment.timestamp}
                </span>
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                  gap: "14px"
                }}
              >
                <div style={{ background: "#f8fafc", padding: "14px 16px", borderRadius: "12px", border: "1px solid #edf2f7" }}>
                  <div style={{ fontSize: "11px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", marginBottom: "4px" }}>
                    Blood Pressure
                  </div>
                  <div style={{ fontSize: "18px", fontWeight: "800", color: "#0f172a" }}>
                    {latestAssessment.systolic_bp ? `${latestAssessment.systolic_bp}/${latestAssessment.diastolic_bp || 80}` : "120/80"} <span style={{ fontSize: "12px", fontWeight: "500", color: "#64748b" }}>mmHg</span>
                  </div>
                </div>

                <div style={{ background: "#f8fafc", padding: "14px 16px", borderRadius: "12px", border: "1px solid #edf2f7" }}>
                  <div style={{ fontSize: "11px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", marginBottom: "4px" }}>
                    Serum Cholesterol
                  </div>
                  <div style={{ fontSize: "18px", fontWeight: "800", color: "#0f172a" }}>
                    {latestAssessment.cholesterol || 195} <span style={{ fontSize: "12px", fontWeight: "500", color: "#64748b" }}>mg/dL</span>
                  </div>
                </div>

                <div style={{ background: "#f8fafc", padding: "14px 16px", borderRadius: "12px", border: "1px solid #edf2f7" }}>
                  <div style={{ fontSize: "11px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", marginBottom: "4px" }}>
                    Fasting Blood Sugar
                  </div>
                  <div style={{ fontSize: "18px", fontWeight: "800", color: "#0f172a" }}>
                    {latestAssessment.fasting_blood_sugar ? `${latestAssessment.fasting_blood_sugar}` : "95"} <span style={{ fontSize: "12px", fontWeight: "500", color: "#64748b" }}>mg/dL</span>
                  </div>
                </div>

                <div style={{ background: "#f8fafc", padding: "14px 16px", borderRadius: "12px", border: "1px solid #edf2f7" }}>
                  <div style={{ fontSize: "11px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", marginBottom: "4px" }}>
                    Ejection Fraction
                  </div>
                  <div style={{ fontSize: "18px", fontWeight: "800", color: "#0f172a" }}>
                    {latestAssessment.ejection_fraction || 55}<span style={{ fontSize: "12px", fontWeight: "500", color: "#64748b" }}>%</span>
                  </div>
                </div>

                <div style={{ background: "#f8fafc", padding: "14px 16px", borderRadius: "12px", border: "1px solid #edf2f7" }}>
                  <div style={{ fontSize: "11px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", marginBottom: "4px" }}>
                    Serum Creatinine
                  </div>
                  <div style={{ fontSize: "18px", fontWeight: "800", color: "#0f172a" }}>
                    {latestAssessment.serum_creatinine || 1.0} <span style={{ fontSize: "12px", fontWeight: "500", color: "#64748b" }}>mg/dL</span>
                  </div>
                </div>

                <div style={{ background: "#f8fafc", padding: "14px 16px", borderRadius: "12px", border: "1px solid #edf2f7" }}>
                  <div style={{ fontSize: "11px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", marginBottom: "4px" }}>
                    Smoking / Tobacco
                  </div>
                  <div style={{ fontSize: "16px", fontWeight: "800", color: latestAssessment.smoking === "Regularly" ? "#ef4444" : "#0f172a" }}>
                    {latestAssessment.smoking || "Never"}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* MIDDLE SECTION: ECG TELEMETRY + RISK DISTRIBUTION */}
          <div className="dashboard-telemetry-grid">
            {/* Real-Time Cardiac Rhythm */}
            <div className="telemetry-col-left">
              <EcgMonitor
                bpm={liveBpm}
                status={liveBpm >= 90 ? "Sinus Tachycardia" : liveBpm <= 60 ? "Sinus Bradycardia" : "Normal Sinus Rhythm"}
              />
            </div>

            {/* Risk Distribution Breakdown */}
            <div className="telemetry-col-right chart-card">
              <div className="chart-card-header">
                <div>
                  <span className="chart-eyebrow">RISK STRATIFICATION</span>
                  <h3>Risk Category Breakdown</h3>
                </div>
                <Sparkles size={18} className="text-amber" />
              </div>

              {pieData.length > 0 ? (
                <div className="pie-chart-container">
                  <ResponsiveContainer width="100%" height={160}>
                    <PieChart>
                      <Pie
                        data={pieData}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        innerRadius={42}
                        outerRadius={68}
                        paddingAngle={4}
                      >
                        {pieData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>

                  <div className="pie-legend">
                    {pieData.map((item, idx) => (
                      <div key={item.name} className="legend-row">
                        <span className="legend-dot" style={{ background: PIE_COLORS[idx % PIE_COLORS.length] }}></span>
                        <span className="legend-label">{item.name}</span>
                        <strong>{item.value}</strong>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div style={{ textAlign: "center", padding: "32px 16px", color: "#64748b" }}>
                  <Clock size={32} style={{ color: "#94a3b8", marginBottom: "8px" }} />
                  <p style={{ fontSize: "13px", margin: 0, fontWeight: "600" }}>
                    Complete your health profile to calculate your risk score.
                  </p>
                  <small style={{ color: "#94a3b8" }}>Run an evaluation to populate your cohort breakdown.</small>
                </div>
              )}
            </div>
          </div>

          {/* BOTTOM SECTION: RECENT ASSESSMENTS TABLE & QUICK ACTIONS */}
          <div className="dashboard-bottom-grid">
            <div className="recent-table-card">
              <div className="table-card-header">
                <div>
                  <span className="chart-eyebrow">PERSONAL LOG</span>
                  <h3>Recent Assessment Telemetry</h3>
                </div>
                {historyItems.length > 0 && (
                  <button
                    className="table-view-all-btn"
                    onClick={() => navigate("/history")}
                  >
                    View All ({historyItems.length}) <ChevronRight size={15} />
                  </button>
                )}
              </div>

              <div className="table-responsive">
                {historyItems.length === 0 ? (
                  <div style={{ textAlign: "center", padding: "40px 20px" }}>
                    <ClipboardList size={36} style={{ color: "#94a3b8", marginBottom: "10px" }} />
                    <h4 style={{ fontSize: "16px", fontWeight: "700", color: "#334155", marginBottom: "4px" }}>
                      Complete your health profile to calculate your risk score.
                    </h4>
                    <p style={{ fontSize: "13px", color: "#64748b", maxWidth: "420px", margin: "0 auto 16px" }}>
                      No evaluations recorded yet for this account. Launch your first assessment to calculate your clinical risk index.
                    </p>
                    <button
                      type="button"
                      className="primary-action-btn"
                      style={{ margin: "0 auto", display: "inline-flex" }}
                      onClick={() => navigate("/new-prediction")}
                    >
                      <PlusCircle size={16} />
                      <span>Launch Diagnostic Assessment</span>
                    </button>
                  </div>
                ) : (
                  <table className="clinical-table">
                    <thead>
                      <tr>
                        <th>Patient</th>
                        <th>Date</th>
                        <th>BP (mmHg)</th>
                        <th>Ejection Fraction</th>
                        <th>Risk Score</th>
                        <th>Classification</th>
                      </tr>
                    </thead>
                    <tbody>
                      {historyItems.slice(0, 5).map((item) => (
                        <tr key={item.id} style={{ cursor: "pointer" }} onClick={() => navigate("/prediction-result", { state: { result: item } })}>
                          <td>
                            <strong>{item.patient_name}</strong>
                            <span className="patient-sub-age">{item.age}y / {item.gender}</span>
                          </td>
                          <td>{item.timestamp}</td>
                          <td>{item.systolic_bp ? `${item.systolic_bp}/${item.diastolic_bp}` : "Normal"}</td>
                          <td>{item.ejection_fraction ? `${item.ejection_fraction}%` : "55%"}</td>
                          <td>
                            <span className="score-pill">{item.risk_score}/100</span>
                          </td>
                          <td>
                            <span className={`risk-tag ${item.risk_score < 25 ? "tag-low" : item.risk_score < 50 ? "tag-mod" : "tag-high"}`}>
                              {item.risk_level}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>

            {/* QUICK ACTIONS & EMERGENCY PORTAL */}
            <div className="quick-actions-card">
              <h3>Clinical Tool Suite</h3>
              <div className="tool-links-list">
                <div
                  className="tool-link-item"
                  onClick={() => navigate("/new-prediction")}
                >
                  <div className="tool-icon bg-blue-light"><Sparkles size={18} /></div>
                  <div>
                    <strong>Run 13-Feature Assessment</strong>
                    <span>Evaluate BP, ST slope, and vessels</span>
                  </div>
                  <ChevronRight size={16} />
                </div>

                <div
                  className="tool-link-item"
                  onClick={() => navigate("/history")}
                >
                  <div className="tool-icon bg-amber-light"><Activity size={18} /></div>
                  <div>
                    <strong>Longitudinal Trends & History</strong>
                    <span>Track progress curves over time</span>
                  </div>
                  <ChevronRight size={16} />
                </div>

                <div
                  className="tool-link-item"
                  onClick={() => navigate("/hospitals")}
                >
                  <div className="tool-icon bg-emerald-light"><Activity size={18} /></div>
                  <div>
                    <strong>Nearby Cardiology Centers</strong>
                    <span>Find urgent 24/7 cardiac triage</span>
                  </div>
                  <ChevronRight size={16} />
                </div>

                <div
                  className="tool-link-item"
                  onClick={() => navigate("/reports")}
                >
                  <div className="tool-icon bg-purple-light"><FileText size={18} /></div>
                  <div>
                    <strong>Export Clinical PDF Report</strong>
                    <span>Generate physician letterhead summary</span>
                  </div>
                  <ChevronRight size={16} />
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}