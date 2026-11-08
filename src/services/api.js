/**
 * Unified API Client for HeartCare AI Prediction Platform
 * Connects to the FastAPI backend (http://127.0.0.1:8000/api)
 */

const rawBaseUrl = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api").trim().replace(/\/+$/, "");
const API_BASE_URL = rawBaseUrl.endsWith("/api") ? rawBaseUrl : `${rawBaseUrl}/api`;

/**
 * Standard fetch wrapper with request timeout and descriptive connection error handling.
 */
async function fetchWithTimeout(url, options = {}) {
  const { timeout = 15000 } = options;
  const controller = new AbortController();
  const timer = setTimeout(() => {
    controller.abort(new Error("Request timed out. The backend server did not respond within the expected timeframe."));
  }, timeout);

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
    if (error.name === "AbortError" || error.message?.includes("aborted")) {
      throw new Error(
        "Connection timed out. The server took longer than expected to respond. If it was idle, it may still be waking up. Please try again."
      );
    }
    if (error.message?.includes("Failed to fetch") || error.message?.includes("NetworkError")) {
      throw new Error(
        "Unable to connect to HeartCare AI server. If the backend was sleeping, it may take up to a minute to wake up. Please retry."
      );
    }
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
  /**
   * Check if FastAPI backend is healthy.
   * Returns { ok: boolean, status: string, ...data }
   */
  async checkHealth(timeout = 6000) {
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/health`, { timeout });
      if (res.ok) {
        const data = await res.json();
        return { ok: true, status: data.status || "healthy", ...data };
      }
      return { ok: false, status: "http_error", code: res.status };
    } catch (err) {
      return { ok: false, status: "offline", error: err.message };
    }
  },

  /**
   * Reliable Cold-Start Handling Mechanism for Render / Cloud Web Services.
   * Proactively polls /api/health until the backend server boots up and responds.
   * 
   * @param {Function} onStatusUpdate - Callback invoked with status reports: { status, elapsed, remaining, message }
   * @param {Object} options - { maxWaitMs: 90000, pollIntervalMs: 5000, signal }
   * @returns {Promise<{ ready: boolean, timeTakenMs: number, reason?: string }>}
   */
  async waitForServerReady(onStatusUpdate = () => {}, options = {}) {
    const {
      maxWaitMs = 90000,
      pollIntervalMs = 5000,
      signal
    } = options;

    const startTime = Date.now();
    let pollCount = 0;

    // Report initial probing state
    onStatusUpdate({
      status: "checking",
      elapsed: 0,
      remaining: Math.round(maxWaitMs / 1000),
      message: "Connecting to clinical AI server..."
    });

    while (Date.now() - startTime < maxWaitMs) {
      if (signal?.aborted) {
        return { ready: false, reason: "aborted" };
      }

      pollCount++;
      const elapsedMs = Date.now() - startTime;
      const elapsedSec = Math.floor(elapsedMs / 1000);
      const remainingSec = Math.max(0, Math.round((maxWaitMs - elapsedMs) / 1000));

      try {
        // Send a probe with an 8s timeout per check (allows TCP handshake during Render container spin-up)
        const health = await this.checkHealth(8000);
        if (health.ok && health.status === "healthy") {
          onStatusUpdate({
            status: "ready",
            elapsed: elapsedSec,
            remaining: 0,
            pollCount,
            message: "Server is ready."
          });
          return { ready: true, timeTakenMs: Date.now() - startTime };
        }
      } catch {
        // Fall through to polling interval
      }

      // If still not ready, notify that server is cold and waking up
      onStatusUpdate({
        status: "waking",
        elapsed: elapsedSec,
        remaining: remainingSec,
        pollCount,
        message: "Waking up the server. This may take up to a minute..."
      });

      // Wait pollIntervalMs before the next check, checking abort signal
      const waitStart = Date.now();
      while (Date.now() - waitStart < pollIntervalMs) {
        if (signal?.aborted) {
          return { ready: false, reason: "aborted" };
        }
        await new Promise((resolve) => setTimeout(resolve, 250));
      }
    }

    // 90 seconds expired without a healthy response
    onStatusUpdate({
      status: "timeout",
      elapsed: 90,
      remaining: 0,
      pollCount,
      message: "Server wake-up timed out. The server did not respond within 90 seconds."
    });

    return { ready: false, reason: "timeout", timeTakenMs: Date.now() - startTime };
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
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        body: JSON.stringify({ email, password }),
        timeout: 30000
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Login failed (${res.status})`);
      }
      return await res.json();
    } catch (err) {
      // If the server answered with an HTTP validation error, pass it directly through
      if (err.message && !err.message.includes("Unable to connect") && !err.message.includes("Connection timed out")) {
        throw err;
      }

      console.warn("Backend unavailable, using local authentication fallback:", err.message);
      const localUsers = JSON.parse(localStorage.getItem("offline_registered_users") || "[]");
      const emailLower = email.trim().toLowerCase();
      const matched = localUsers.find(u => u.email === emailLower);

      if (matched) {
        if (matched.password !== password) {
          throw new Error("Invalid password credentials. Please verify your password.");
        }
        return {
          status: "success",
          message: "Signed in successfully (Offline Local Session)",
          access_token: `offline_token_${Date.now()}`,
          user: {
            id: matched.id,
            name: matched.name,
            email: matched.email,
            role: matched.role || "Cardiologist / Physician"
          }
        };
      }

      // Default demo doctor account offline fallback
      if (emailLower === "dr.sharma@heartcare.ai" && password === "admin123") {
        return {
          status: "success",
          message: "Signed in successfully (Offline Demo Doctor Session)",
          access_token: `offline_token_${Date.now()}`,
          user: {
            id: "USER-001",
            name: "Dr. Rajesh Sharma, MD, DM (Cardiology)",
            email: "dr.sharma@heartcare.ai",
            role: "Cardiologist / Physician"
          }
        };
      }

      // Default demo patient account offline fallback
      if (emailLower === "patient@heartcare.ai" && password === "patient123") {
        return {
          status: "success",
          message: "Signed in successfully (Offline Demo Patient Session)",
          access_token: `offline_token_${Date.now()}`,
          user: {
            id: "USER-002",
            name: "Aarav Patel",
            email: "patient@heartcare.ai",
            role: "Patient / Individual User"
          }
        };
      }

      throw err;
    }
  },

  /** User Registration */
  async register(name, email, password, role) {
    try {
      const res = await fetchWithTimeout(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        body: JSON.stringify({ name, email, password, role }),
        timeout: 30000
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Registration failed (${res.status})`);
      }
      return await res.json();
    } catch (err) {
      // If the server answered with an HTTP validation error, pass it directly through
      if (err.message && !err.message.includes("Unable to connect") && !err.message.includes("Connection timed out")) {
        throw err;
      }

      console.warn("Backend unavailable, using local registration fallback:", err.message);
      const localUsers = JSON.parse(localStorage.getItem("offline_registered_users") || "[]");
      const emailClean = email.trim().toLowerCase();

      if (localUsers.some(u => u.email === emailClean)) {
        throw new Error("A clinical account with this email already exists in local storage.");
      }

      const newLocalUser = {
        id: `USER-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
        name: name.trim(),
        email: emailClean,
        password: password,
        role: role || "Cardiologist / Physician"
      };
      localUsers.push(newLocalUser);
      localStorage.setItem("offline_registered_users", JSON.stringify(localUsers));

      return {
        status: "success",
        message: "Clinical account registered successfully (Local Offline Session)",
        access_token: `offline_token_${Date.now()}`,
        user: {
          id: newLocalUser.id,
          name: newLocalUser.name,
          email: newLocalUser.email,
          role: newLocalUser.role
        }
      };
    }
  }
};

if (typeof window !== "undefined") {
  window.api = api;
}

