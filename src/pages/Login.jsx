import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Heart,
  Shield,
  ArrowRight,
  CheckCircle2,
  Lock,
  Mail,
  User,
  Eye,
  EyeOff,
  AlertCircle,
  AlertTriangle,
  RefreshCw,
  Loader2
} from "lucide-react";
import { api } from "../services/api";

export default function Login() {
  const navigate = useNavigate();
  const [isSignUp, setIsSignUp] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  // Cloud Backend Cold-Start Lifecycle States (for Render / Vercel deployment)
  const [serverState, setServerState] = useState({
    status: "checking", // "checking" | "waking" | "ready" | "timeout" | "error"
    message: "Connecting to server...",
    elapsed: 0,
    remaining: 90
  });
  const [wakeAttempt, setWakeAttempt] = useState(0);

  // Proactively wake up backend as soon as the login screen mounts or on manual retry
  useEffect(() => {
    let isCancelled = false;
    const abortController = new AbortController();

    const initiateWakeUp = async () => {
      try {
        await api.waitForServerReady(
          (update) => {
            if (!isCancelled && !abortController.signal.aborted) {
              setServerState(update);
            }
          },
          {
            maxWaitMs: 90000,
            pollIntervalMs: 5000,
            signal: abortController.signal
          }
        );
      } catch (err) {
        if (!isCancelled && !abortController.signal.aborted) {
          setServerState({
            status: "error",
            message: "Unable to reach the server. Please verify your connection.",
            elapsed: 0,
            remaining: 0
          });
        }
      }
    };

    initiateWakeUp();

    return () => {
      isCancelled = true;
      abortController.abort();
    };
  }, [wakeAttempt]);

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg(null);

    // Only allow submission when serverState.status is "ready"
    if (serverState.status !== "ready") {
      if (serverState.status === "waking") {
        setErrorMsg("The cloud server is currently waking up. Please wait until the server is ready before submitting.");
      } else if (serverState.status === "checking") {
        setErrorMsg("Checking server status. Please wait a moment until the connection is established.");
      } else if (serverState.status === "timeout") {
        setErrorMsg("The server took too long to wake up. Please click 'Retry Waking Server' above.");
      } else if (serverState.status === "error") {
        setErrorMsg("Unable to connect to the server. Please click 'Retry Waking Server' above.");
      } else {
        setErrorMsg("Server is not ready yet. Please wait.");
      }
      return;
    }

    const emailTrimmed = email.trim();
    if (!emailTrimmed) {
      setErrorMsg("Please enter your email address.");
      return;
    }
    if (!password) {
      setErrorMsg("Please enter your password.");
      return;
    }

    setLoading(true);

    try {
      let authResponse;
      if (isSignUp) {
        if (!name.trim()) {
          setErrorMsg("Please enter your full name.");
          setLoading(false);
          return;
        }
        authResponse = await api.register(name.trim(), emailTrimmed, password, "Cardiologist / Physician");
      } else {
        authResponse = await api.login(emailTrimmed, password);
      }

      if (authResponse && authResponse.user) {
        const u = authResponse.user;
        localStorage.setItem("userName", u.name || "Clinician");
        localStorage.setItem("userEmail", u.email || emailTrimmed);
        localStorage.setItem("userRole", u.role || "Cardiologist / Physician");
        localStorage.setItem("authToken", authResponse.access_token || "auth_valid");
        localStorage.setItem("isAuthenticated", "true");

        navigate("/dashboard", { replace: true });
      } else {
        setErrorMsg("Authentication failed. Please check your credentials.");
      }
    } catch (err) {
      const msg = (err && err.message) ? String(err.message) : "An error occurred during authentication.";
      if (
        msg.includes("aborted without reason") ||
        msg.includes("AbortError") ||
        msg.includes("timed out") ||
        msg.includes("timeout")
      ) {
        setErrorMsg("Connection timed out. The server may still be warming up from an idle state. Please try again.");
      } else {
        setErrorMsg(msg);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page-container">
      {/* LEFT SHOWCASE BANNER */}
      <div className="login-left-banner">
        <div className="banner-overlay">
          <div className="banner-brand" onClick={() => navigate("/")} style={{ cursor: "pointer" }}>
            <div className="banner-logo">
              <Heart size={24} fill="#ffffff" />
            </div>
            <div>
              <h2>HeartCare<span>.AI</span></h2>
              <span>Cardiovascular Health Intelligence</span>
            </div>
          </div>

          <div className="banner-hero-text">
            <span className="banner-tag">SECURE CLINICAL PORTAL</span>
            <h1>Optimized Machine Learning System for Heart Failure Prediction</h1>
            <p>
              The heart disease prediction system uses machine learning models to predict the likelihood of heart disease in a patient based on various clinical features. It provides insights into the patient's risk factors and helps in decision for treatment
            </p>

            <div className="banner-checkmarks">
              <div className="check-item">
                <CheckCircle2 size={18} className="text-emerald" />
                <span>13-feature Cleveland UCI machine learning engine</span>
              </div>
              <div className="check-item">
                <CheckCircle2 size={18} className="text-emerald" />
                <span>Feature impact attribution & risk explainability</span>
              </div>
              <div className="check-item">
                <CheckCircle2 size={18} className="text-emerald" />
                <span>Interactive What-If clinical intervention simulation</span>
              </div>
            </div>
          </div>

          <div className="banner-footer-security">
            <Shield size={16} className="text-emerald" />
            <span>Secure Role-Based Authentication & SHA-256 Hashing</span>
          </div>
        </div>
      </div>

      {/* RIGHT AUTHENTICATION FORM */}
      <div className="login-right-form-area">
        <div className="form-card-wrapper">
          <div className="form-header">
            <h2>{isSignUp ? "Create Clinical Account" : "Sign In to HeartCare AI"}</h2>
            <p>
              {isSignUp
                ? "Register your credentials to access the diagnostic portal."
                : "Enter your registered email and password to access your dashboard."}
            </p>
          </div>

          {/* RENDER CLOUD SERVER COLD-START STATUS BANNER */}
          {serverState.status === "waking" && (
            <div className="server-wake-card waking">
              <Loader2 size={18} className="spin-icon text-amber" style={{ flexShrink: 0, marginTop: "2px" }} />
              <div className="wake-info">
                <strong>Waking up the server. This may take up to a minute...</strong>
                <p>
                  Render free-tier hosting spins down when idle. Starting cloud instance ({serverState.elapsed}s / 90s)...
                </p>
                <div className="wake-progress-bar">
                  <div
                    className="wake-progress-fill"
                    style={{ width: `${Math.min(100, Math.max(8, Math.round((serverState.elapsed / 90) * 100)))}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {serverState.status === "ready" && serverState.elapsed > 2 && (
            <div className="server-wake-card ready">
              <CheckCircle2 size={18} className="text-emerald" style={{ flexShrink: 0, marginTop: "1px" }} />
              <div className="wake-info">
                <strong>Server is online and ready.</strong>
                <p>Clinical diagnostic backend is connected. You can now sign in.</p>
              </div>
            </div>
          )}

          {(serverState.status === "timeout" || serverState.status === "error") && (
            <div className={`server-wake-card ${serverState.status === "timeout" ? "timeout" : "error"}`}>
              <AlertTriangle size={18} className="text-rose" style={{ flexShrink: 0, marginTop: "2px" }} />
              <div className="wake-info">
                <strong>
                  {serverState.status === "timeout"
                    ? "Server wake-up timed out (90s)"
                    : "Server connection failed"}
                </strong>
                <p>
                  {serverState.status === "timeout"
                    ? "The cloud backend took longer than 90 seconds to start. Free-tier servers occasionally experience delayed boot times."
                    : serverState.message || "Unable to reach the server. Please verify your connection or try waking it again."}
                </p>
                <button
                  type="button"
                  className="wake-retry-action-btn"
                  onClick={() => {
                    setErrorMsg(null);
                    setServerState({
                      status: "checking",
                      message: "Reconnecting to server...",
                      elapsed: 0,
                      remaining: 90
                    });
                    setWakeAttempt((prev) => prev + 1);
                  }}
                >
                  <RefreshCw size={13} />
                  <span>Retry Waking Server</span>
                </button>
              </div>
            </div>
          )}

          {errorMsg && (
            <div
              style={{
                background: "#fef2f2",
                border: "1px solid #fca5a5",
                color: "#b91c1c",
                padding: "12px 14px",
                borderRadius: "8px",
                fontSize: "13px",
                marginBottom: "16px",
                display: "flex",
                alignItems: "flex-start",
                gap: "10px",
                lineHeight: "1.4"
              }}
            >
              <AlertCircle size={18} style={{ flexShrink: 0, marginTop: "1px" }} />
              <div>
                <span>{errorMsg}</span>
                {!isSignUp && errorMsg.toLowerCase().includes("sign up") && (
                  <div style={{ marginTop: "6px" }}>
                    <button
                      type="button"
                      onClick={() => {
                        setIsSignUp(true);
                        setErrorMsg(null);
                      }}
                      style={{
                        background: "#b91c1c",
                        color: "#ffffff",
                        border: "none",
                        padding: "4px 10px",
                        borderRadius: "6px",
                        fontSize: "12px",
                        fontWeight: "700",
                        cursor: "pointer"
                      }}
                    >
                      Switch to Sign Up →
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          <form onSubmit={handleAuthSubmit} className="custom-login-form">
            {isSignUp && (
              <div className="input-group">
                <label>Full Name</label>
                <div className="input-with-icon-wrapper">
                  <User size={18} className="input-icon text-muted" />
                  <input
                    type="text"
                    placeholder="Enter your full name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
              </div>
            )}

            <div className="input-group">
              <label>Email Address</label>
              <div className="input-with-icon-wrapper">
                <Mail size={18} className="input-icon text-muted" />
                <input
                  type="email"
                  placeholder=" "
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="input-group">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <label>Password</label>
                {!isSignUp && (
                  <span
                    onClick={() => alert("Password reset: Please contact your system administrator.")}
                    style={{ fontSize: "12px", color: "var(--primary)", cursor: "pointer", fontWeight: "600" }}
                  >
                    Forgot Password?
                  </span>
                )}
              </div>
              <div className="input-with-icon-wrapper">
                <Lock size={18} className="input-icon text-muted" />
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder=" "
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="password-toggle-btn"
                  onClick={() => setShowPassword(!showPassword)}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", margin: "4px 0" }}>
              <label style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "13px", cursor: "pointer", userSelect: "none" }}>
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  style={{ width: "16px", height: "16px", accentColor: "var(--primary)" }}
                />
                <span>Remember this workstation</span>
              </label>
            </div>

            <button
              type="submit"
              className="login-submit-btn"
              disabled={loading || serverState.status !== "ready"}
            >
              {loading ? (
                <>
                  <Loader2 size={18} className="spin-icon" />
                  <span>Authenticating...</span>
                </>
              ) : serverState.status === "checking" ? (
                <>
                  <Loader2 size={18} className="spin-icon" />
                  <span>Connecting to Server...</span>
                </>
              ) : serverState.status === "waking" ? (
                <>
                  <Loader2 size={18} className="spin-icon" />
                  <span>Waking Server ({serverState.elapsed}s)...</span>
                </>
              ) : serverState.status === "timeout" ? (
                <>
                  <RefreshCw size={18} />
                  <span>Server Offline – Click Retry Above</span>
                </>
              ) : serverState.status === "error" ? (
                <>
                  <AlertCircle size={18} />
                  <span>Connection Error – Click Retry Above</span>
                </>
              ) : (
                <>
                  <span>{isSignUp ? "Register Account" : "Sign In to Workspace"}</span>
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          {/* TOGGLE SIGN IN / SIGN UP */}
          <div style={{ marginTop: "24px", textAlign: "center", fontSize: "14px", color: "#64748b" }}>
            {isSignUp ? (
              <span>
                Already have an account?{" "}
                <button
                  type="button"
                  onClick={() => {
                    setIsSignUp(false);
                    setErrorMsg(null);
                  }}
                  style={{ background: "none", border: "none", color: "var(--primary)", fontWeight: "700", cursor: "pointer", padding: 0 }}
                >
                  Sign In
                </button>
              </span>
            ) : (
              <span>
                Don't have an account?{" "}
                <button
                  type="button"
                  onClick={() => {
                    setIsSignUp(true);
                    setErrorMsg(null);
                  }}
                  style={{ background: "none", border: "none", color: "var(--primary)", fontWeight: "700", cursor: "pointer", padding: 0 }}
                >
                  Create Account
                </button>
              </span>
            )}
          </div>

          <div style={{ marginTop: "20px", textAlign: "center" }}>
            <span
              onClick={() => navigate("/")}
              style={{ fontSize: "13px", color: "#94a3b8", cursor: "pointer", fontWeight: "600" }}
            >
              ← Return to Homepage
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}