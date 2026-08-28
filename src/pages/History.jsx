import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  History as HistoryIcon,
  Search,
  Filter,
  Trash2,
  Eye,
  Download,
  PlusCircle,
  TrendingDown,
  TrendingUp,
  Sparkles,
  RefreshCw,
  FileSpreadsheet,
  CheckCircle2,
  X
} from "lucide-react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function History() {
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState("");
  const [riskFilter, setRiskFilter] = useState("All");
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [toastMsg, setToastMsg] = useState(null);

  const showToast = (msg) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(null), 3000);
  };

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await api.getHistory(search, riskFilter);
      setItems(data.items || []);
    } catch (err) {
      console.error("Error loading history:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [riskFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchHistory();
  };

  const handleGenerateDynamic = async () => {
    setGenerating(true);
    try {
      const res = await api.generateDynamicPatients(5);
      showToast("Generated 5 dynamic clinical assessments!");
      await fetchHistory();
    } catch (err) {
      console.error("Dynamic generator error:", err);
    } finally {
      setGenerating(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this assessment record?")) {
      await api.deleteHistory(id);
      setItems(items.filter((item) => item.id !== id));
      if (selectedRecord?.id === id) setSelectedRecord(null);
      showToast("Record deleted.");
    }
  };

  const handleClearAll = async () => {
    if (window.confirm("Are you sure you want to clear all history records?")) {
      await api.deleteHistory("");
      setItems([]);
      showToast("All history records cleared.");
    }
  };

  const handleExportCSV = () => {
    if (items.length === 0) {
      alert("No records to export.");
      return;
    }
    const headers = ["ID", "Patient Name", "Age", "Gender", "Date", "Risk Score", "Risk Level", "BP Systolic", "BP Diastolic", "Ejection Fraction", "Creatinine", "Smoking", "Chest Pain"];
    const csvRows = [
      headers.join(","),
      ...items.map((i) =>
        [
          i.id,
          `"${i.patient_name}"`,
          i.age,
          i.gender,
          `"${i.timestamp}"`,
          i.risk_score,
          `"${i.risk_level}"`,
          i.systolic_bp || "N/A",
          i.diastolic_bp || "N/A",
          i.ejection_fraction || "N/A",
          i.serum_creatinine || "N/A",
          `"${i.smoking || "N/A"}"`,
          `"${i.chest_pain || "N/A"}"`
        ].join(",")
      )
    ];

    const blob = new Blob([csvRows.join("\n")], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `HeartCare_Assessments_${new Date().toISOString().split("T")[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("CSV dataset exported successfully!");
  };

  // Dynamic quick statistics
  const totalCount = items.length;
  const avgRisk = totalCount > 0 ? (items.reduce((acc, i) => acc + i.risk_score, 0) / totalCount).toFixed(1) : 0;
  const highRiskCount = items.filter((i) => i.risk_score >= 50).length;

  // Prepare chronological line chart data
  const chartData = [...items]
    .reverse()
    .map((item) => ({
      date: item.timestamp.split(" ")[0],
      riskScore: item.risk_score,
      healthScore: item.heart_health_score,
      patient: item.patient_name
    }));

  return (
    <div className="dashboard-page-wrapper">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <div className="dashboard-main-area">
        <Navbar onMobileMenuClick={() => setMobileOpen(true)} />

        <main className="dashboard-content-scroll">
          {/* HEADER WITH DYNAMIC CONTROLS */}
          <div className="page-header-row">
            <div>
              <span className="section-eyebrow">LONGITUDINAL TELEMETRY & DATASETS</span>
              <h1>Assessment History & Trend Analytics</h1>
              <p>Review dynamically persisted patient runs, generate live cohorts, or export datasets.</p>
            </div>

            <div className="header-action-group">
              <button
                type="button"
                className="secondary-action-btn"
                onClick={handleGenerateDynamic}
                disabled={generating}
                title="Generate 5 dynamic patient assessments"
              >
                <Sparkles size={16} className={generating ? "spin-icon text-amber" : "text-amber"} />
                <span>{generating ? "Simulating..." : "⚡ Generate Dynamic Cohort"}</span>
              </button>

              <button
                type="button"
                className="secondary-action-btn"
                onClick={handleExportCSV}
                title="Download CSV dataset"
              >
                <Download size={16} />
                <span>Export CSV</span>
              </button>

              <button
                className="primary-action-btn"
                onClick={() => navigate("/new-prediction")}
              >
                <PlusCircle size={18} />
                <span>New Assessment</span>
              </button>
            </div>
          </div>

          {/* DYNAMIC TOAST NOTIFICATION */}
          {toastMsg && (
            <div className="saved-toast" style={{ marginBottom: "16px" }}>
              <CheckCircle2 size={16} className="text-emerald" />
              <span>{toastMsg}</span>
            </div>
          )}

          {/* DYNAMIC KPI SUMMARY STRIP */}
          <div className="dashboard-stats-grid" style={{ marginBottom: "20px" }}>
            <div className="stat-card">
              <span className="stat-title">Total Dynamic Records</span>
              <h2 className="stat-value">{totalCount}</h2>
              <span className="stat-description">Persisted in SQLite DB</span>
            </div>
            <div className="stat-card">
              <span className="stat-title">Cohort Mean Risk</span>
              <h2 className="stat-value">{avgRisk}%</h2>
              <span className="stat-description">Average 10-year risk</span>
            </div>
            <div className="stat-card">
              <span className="stat-title">Elevated Risk Cases</span>
              <h2 className="stat-value text-rose">{highRiskCount}</h2>
              <span className="stat-description">Requires clinical review</span>
            </div>
          </div>

          {/* HISTORICAL TREND LINE CHART */}
          {chartData.length > 0 && (
            <div className="chart-card history-chart-card">
              <div className="chart-card-header">
                <div>
                  <span className="chart-eyebrow">DYNAMIC TIME-SERIES CURVE</span>
                  <h3>Cardiovascular Risk Score Progression Over Time</h3>
                </div>
                <button className="table-view-all-btn" onClick={fetchHistory}>
                  <RefreshCw size={14} className={loading ? "spin-icon" : ""} /> Refresh
                </button>
              </div>

              <div className="line-chart-wrapper">
                <ResponsiveContainer width="100%" height={220}>
                  <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="date" stroke="#64748b" />
                    <YAxis domain={[0, 100]} stroke="#64748b" />
                    <Tooltip
                      formatter={(val, name) => [
                        `${val}/100`,
                        name === "riskScore" ? "Risk Score" : "Health Score"
                      ]}
                      labelFormatter={(label, payload) => {
                        const item = payload?.[0]?.payload;
                        return item ? `${item.patient} (${label})` : label;
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="riskScore"
                      stroke="#ef4444"
                      strokeWidth={3}
                      dot={{ r: 5 }}
                      name="riskScore"
                    />
                    <Line
                      type="monotone"
                      dataKey="healthScore"
                      stroke="#10b981"
                      strokeWidth={2}
                      strokeDasharray="4 4"
                      dot={{ r: 4 }}
                      name="healthScore"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* FILTER & SEARCH CONTROLS */}
          <div className="history-filter-bar">
            <form onSubmit={handleSearchSubmit} className="history-search-form">
              <Search className="search-icon" size={17} />
              <input
                type="text"
                placeholder="Search patient name, ID, or keywords..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <button type="submit" className="search-btn">Search</button>
            </form>

            <div className="filter-pill-group">
              <Filter size={16} className="filter-icon" />
              {["All", "Low Risk", "Moderate Risk", "High Risk"].map((lvl) => (
                <button
                  key={lvl}
                  type="button"
                  className={`filter-pill ${riskFilter === lvl ? "active" : ""}`}
                  onClick={() => setRiskFilter(lvl)}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>

          {/* TABLE OF ASSESSMENTS */}
          <div className="history-table-card">
            <div className="table-responsive">
              <table className="clinical-table">
                <thead>
                  <tr>
                    <th>Record ID</th>
                    <th>Patient</th>
                    <th>Assessment Date</th>
                    <th>Vitals (BP / EF)</th>
                    <th>Risk Score</th>
                    <th>Risk Category</th>
                    <th style={{ textAlign: "right" }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {items.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="table-empty-row" style={{ textAlign: "center", padding: "32px" }}>
                        <p>No assessment records found.</p>
                        <button
                          type="button"
                          className="primary-action-btn"
                          style={{ margin: "12px auto 0", display: "inline-flex" }}
                          onClick={handleGenerateDynamic}
                        >
                          <Sparkles size={16} />
                          <span>Generate Dynamic Test Cohort Now</span>
                        </button>
                      </td>
                    </tr>
                  ) : (
                    items.map((item) => (
                      <tr key={item.id}>
                        <td>
                          <code>{item.id}</code>
                        </td>
                        <td>
                          <strong>{item.patient_name}</strong>
                          <span className="patient-sub-age">{item.age}y • {item.gender}</span>
                        </td>
                        <td>{item.timestamp}</td>
                        <td>
                          <span>{item.systolic_bp ? `${item.systolic_bp}/${item.diastolic_bp} mmHg` : "120/80"}</span>
                          <span className="patient-sub-age">EF: {item.ejection_fraction || 55}%</span>
                        </td>
                        <td>
                          <span className="score-pill">{item.risk_score}/100</span>
                        </td>
                        <td>
                          <span className={`risk-tag ${item.risk_score < 25 ? "tag-low" : item.risk_score < 50 ? "tag-mod" : "tag-high"}`}>
                            {item.risk_level}
                          </span>
                        </td>
                        <td style={{ textAlign: "right" }}>
                          <div className="row-actions">
                            <button
                              type="button"
                              className="action-icon-btn view-btn"
                              title="View Details"
                              onClick={() => setSelectedRecord(item)}
                            >
                              <Eye size={16} />
                            </button>
                            <button
                              type="button"
                              className="action-icon-btn delete-btn"
                              title="Delete Record"
                              onClick={() => handleDelete(item.id)}
                            >
                              <Trash2 size={16} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>

      {/* DETAIL MODAL */}
      {selectedRecord && (
        <div className="modal-backdrop" onClick={() => setSelectedRecord(null)}>
          <div className="detail-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div>
                <span className="section-eyebrow">ASSESSMENT RECORD</span>
                <h2>{selectedRecord.patient_name}</h2>
                <small>ID: {selectedRecord.id} • {selectedRecord.timestamp}</small>
              </div>
              <button
                type="button"
                className="modal-close-btn"
                onClick={() => setSelectedRecord(null)}
              >
                <X size={20} />
              </button>
            </div>

            <div className="modal-body">
              <div className="modal-stat-grid">
                <div className="modal-stat-box">
                  <small>Risk Score</small>
                  <strong>{selectedRecord.risk_score}/100</strong>
                </div>
                <div className="modal-stat-box">
                  <small>Risk Classification</small>
                  <strong className="text-rose">{selectedRecord.risk_level}</strong>
                </div>
                <div className="modal-stat-box">
                  <small>Ejection Fraction</small>
                  <strong>{selectedRecord.ejection_fraction || 55}%</strong>
                </div>
                <div className="modal-stat-box">
                  <small>Blood Pressure</small>
                  <strong>{selectedRecord.systolic_bp}/{selectedRecord.diastolic_bp} mmHg</strong>
                </div>
              </div>

              <div className="modal-summary-box">
                <h4>Clinical Summary Statement</h4>
                <p>{selectedRecord.summary_message}</p>
              </div>
            </div>

            <div className="modal-footer">
              <button
                type="button"
                className="secondary-action-btn"
                onClick={() => setSelectedRecord(null)}
              >
                Close
              </button>
              <button
                type="button"
                className="primary-action-btn"
                onClick={() => {
                  navigate("/prediction-result", { state: { result: selectedRecord } });
                }}
              >
                Open in Diagnostic Studio →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
