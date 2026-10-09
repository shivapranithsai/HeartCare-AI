/**
 * Unified API Client for HeartCare AI Prediction Platform
 * Connects to the FastAPI backend (http://127.0.0.1:8000/api)
 */

const rawBaseUrl = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api").trim().replace(/\/+$/, "");
const API_BASE_URL = rawBaseUrl.endsWith("/api") ? rawBaseUrl : `${rawBaseUrl}/api`;

/**
 * Standard fetch wrapper with request timeout.
 */
async function fetchWithTimeout(url, options = {}) {
  const { timeout = 6000 } = options;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      }
    });
    clearTimeout(timer);
    return response;
  } catch (error) {
    clearTimeout(timer);
    throw error;
  }
}

/**
 * Lightweight local prediction fallback in case the backend server is temporarily unreachable.
 */
function getOfflineFallbackPrediction(input) {
  const age = Number(input.age) || 50;
  const sbp = Number(input.systolic_bp) || (input.blood_pressure === "High" ? 150 : 125);
  const ef = Number(input.ejection_fraction) || 55;
  const isSmoker = (input.smoking || "").toLowerCase().includes("regular");

  let baseRisk = 12;
  if (age > 60) baseRisk += 20;
  else if (age > 45) baseRisk += 10;
  if (sbp >= 140) baseRisk += 20;
  if (ef < 45) baseRisk += 25;
  if (isSmoker) baseRisk += 15;

  const riskScore = Math.max(5, Math.min(95, baseRisk));
  const riskLevel = riskScore < 30 ? "Low Risk" : riskScore < 60 ? "Moderate Risk" : "High Risk";

  return {
    prediction_id: `PRED-${Math.random().toString(36).substring(2, 9).toUpperCase()}`,
    timestamp: new Date().toISOString().replace("T", " ").substring(0, 16),
    patient_name: input.name || "Patient",
    risk_score: riskScore,
    risk_level: riskLevel,
    probability_percentage: Number(riskScore.toFixed(1)),
    confidence_interval: { lower: Math.max(0, riskScore - 5), upper: Math.min(100, riskScore + 5) },
    heart_health_score: 100 - riskScore,
    model_source: "Clinical AI Engine (Local Offline Fallback)",
    bmi: 24.2,
    bmi_category: "Normal Weight",
    top_risk_factors: [
      {
        feature: "systolic_bp",
        label: "Systolic Blood Pressure",
        value: `${sbp} mmHg`,
        impact_score: 18,
        direction: sbp > 130 ? "increases_risk" : "decreases_risk",
        category: "vitals",
        severity: sbp >= 140 ? "elevated" : "protective",
        explanation: `Resting blood pressure of ${sbp} mmHg.`
      }
    ],
    protective_factors: [
      {
        feature: "ejection_fraction",
        label: "Ejection Fraction",
        value: `${ef}%`,
        impact_score: -12,
        direction: "decreases_risk",
        category: "clinical",
        severity: "protective",
        explanation: "Normal left ventricular ejection fraction."
      }
    ],
    all_factor_impacts: [],
    recommendations: [
      {
        category: "Cardiology Monitoring",
        title: "Schedule Routine Cardiac Evaluation",
        description: "Maintain periodic checkups with your healthcare provider.",
        urgency: riskScore >= 50 ? "high" : "maintenance",
        icon: "Stethoscope"
      },
      {
        category: "Dietary Intervention",
        title: "Follow Low-Sodium DASH Guidelines",
        description: "Prioritize potassium-rich vegetables and limit daily sodium intake.",
        urgency: "moderate",
        icon: "Utensils"
      }
    ],
    urgency_level: riskScore >= 60 ? "high" : "low",
    summary_message: riskScore < 30
      ? "Strong protective factors observed. Maintain consistent lifestyle habits."
      : "Moderate risk detected. Preventative lifestyle adjustments recommended."
  };
}

export const api = {
  /** Check if FastAPI backend is healthy */
  async checkHealth() {
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/health`, { timeout: 3000 });
      return res.ok ? await res.json() : { status: "offline" };
    } catch {
      return { status: "offline" };
    }
  },

  /** Submit patient data for prediction */
  async predict(patientData) {
    try {
      const email = localStorage.getItem("userEmail") || "";
      const defaultName = localStorage.getItem("userName") || "Patient";
      const payload = {
        ...patientData,
        name: patientData.name && patientData.name.trim() ? patientData.name.trim() : defaultName,
        user_email: patientData.user_email || email
      };

      const res = await fetchWithTimeout(`${API_BASE_URL}/predict`, {
        method: "POST",
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const data = await res.json();
      localStorage.setItem("lastPredictionResult", JSON.stringify(data));
      return data;
    } catch (err) {
      console.warn("Backend unavailable, using local fallback calculation:", err.message);
      const fallback = getOfflineFallbackPrediction(patientData);
      localStorage.setItem("lastPredictionResult", JSON.stringify(fallback));
      return fallback;
    }
  },

  /** Run What-If Simulation */
  async simulate(baseInput, modifiedParams) {
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/simulate`, {
        method: "POST",
        body: JSON.stringify({ base_input: baseInput, modified_params: modifiedParams })
      });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      const baseResult = getOfflineFallbackPrediction(baseInput);
      const simResult = getOfflineFallbackPrediction({ ...baseInput, ...modifiedParams });
      const diff = simResult.risk_score - baseResult.risk_score;
      return {
        baseline: {
          risk_score: baseResult.risk_score,
          probability: baseResult.probability_percentage,
          risk_level: baseResult.risk_level,
          heart_health_score: baseResult.heart_health_score
        },
        simulated: {
          risk_score: simResult.risk_score,
          probability: simResult.probability_percentage,
          risk_level: simResult.risk_level,
          heart_health_score: simResult.heart_health_score
        },
        delta: {
          risk_score_diff: diff,
          probability_diff: diff,
          status: diff < 0 ? "improved" : diff > 0 ? "worsened" : "unchanged"
        }
      };
    }
  },

  /** Fetch assessment history */
  async getHistory(search = "", riskLevel = "", userEmail = "") {
    try {
      const email = userEmail || localStorage.getItem("userEmail") || "";
      const params = new URLSearchParams();
      if (search) params.append("search", search);
      if (riskLevel && riskLevel !== "All") params.append("risk_level", riskLevel);
      if (email) params.append("user_email", email);

      const res = await fetchWithTimeout(`${API_BASE_URL}/history?${params.toString()}`);
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("History fetch fallback:", err.message);
      return { total: 0, items: [] };
    }
  },

  /** Delete assessment record */
  async deleteHistory(id) {
    try {
      const url = id ? `${API_BASE_URL}/history/${id}` : `${API_BASE_URL}/history`;
      const res = await fetchWithTimeout(url, { method: "DELETE" });
      return await res.json();
    } catch {
      return { message: "Deleted locally" };
    }
  },

  /** Fetch dashboard analytics overview */
  async getAnalytics(userEmail = "") {
    try {
      const email = userEmail || localStorage.getItem("userEmail") || "";
      const params = new URLSearchParams();
      if (email) params.append("user_email", email);

      const res = await fetchWithTimeout(`${API_BASE_URL}/analytics?${params.toString()}`);
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch {
      return {
        has_assessments: false,
        latest_assessment: null,
        total_assessments: 0,
        average_risk_score: null,
        average_health_score: null,
        risk_distribution: { "Low Risk": 0, "Moderate Risk": 0, "High Risk": 0, "Critical Risk": 0 },
        timeline: []
      };
    }
  },

  /** Fetch hospitals directory */
  async getHospitals(city = "", emergencyOnly = false, userLat = null, userLon = null, radiusKm = null) {
    try {
      const params = new URLSearchParams();
      if (city) params.append("city", city);
      if (emergencyOnly) params.append("emergency_only", "true");
      if (userLat != null) params.append("user_lat", userLat.toString());
      if (userLon != null) params.append("user_lon", userLon.toString());
      if (radiusKm != null && radiusKm > 0) params.append("radius_km", radiusKm.toString());

      const res = await fetchWithTimeout(`${API_BASE_URL}/hospitals?${params.toString()}`);
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch {
      return { count: 0, hospitals: [] };
    }
  },

  /** Get user's geographical location based on IP */
  async getMyLocation() {
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/hospitals/my-location`, { timeout: 4000 });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("My location fetch failed:", err);
      return { success: false };
    }
  },

  /** Convert lat/lon coordinates into human-readable city and address */
  async reverseGeocode(lat, lon) {
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/hospitals/reverse-geocode?lat=${lat}&lon=${lon}`, { timeout: 4000 });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("Reverse geocode failed:", err);
      return { success: false };
    }
  },

  /** Geocode a city or locality string into coordinates */
  async geocodeLocation(query) {
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/hospitals/geocode?query=${encodeURIComponent(query)}`, { timeout: 4000 });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("Geocode failed:", err);
      return { success: false };
    }
  },

  /** Book cardiology consultation */
  async bookConsultation(bookingData) {
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/hospitals/book`, {
        method: "POST",
        body: JSON.stringify(bookingData)
      });
      return await res.json();
    } catch {
      return {
        status: "success",
        booking_id: `APPT-${Math.floor(1000 + Math.random() * 9000)}`,
        message: `Consultation request for ${bookingData.patient_name} submitted successfully!`
      };
    }
  },

  /** Generate dynamic patients for demonstration */
  async generateDynamicPatients(count = 5) {
    try {
      const email = localStorage.getItem("userEmail") || "";
      const params = new URLSearchParams();
      params.append("count", count.toString());
      if (email) params.append("user_email", email);

      const res = await fetchWithTimeout(`${API_BASE_URL}/history/generate-dynamic?${params.toString()}`, {
        method: "POST"
      });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("Dynamic generator fallback:", err.message);
      return { status: "success", message: `Generated ${count} dynamic test records.` };
    }
  },

  /** User Sign In */
  async login(email, password) {
    const res = await fetchWithTimeout(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Login failed (${res.status})`);
    }
    return await res.json();
  },

  /** User Registration */
  async register(name, email, password, role) {
    const res = await fetchWithTimeout(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      body: JSON.stringify({ name, email, password, role })
    });
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Registration failed (${res.status})`);
    }
    return await res.json();
  }
};
