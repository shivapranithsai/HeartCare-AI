import React, { useState } from "react";
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
  KeyRound,
  AlertCircle,
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

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg(null);

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
        authResponse = await api.register(name.trim(), emailTrimmed, password, "Clinician / Practitioner");
      } else {
        authResponse = await api.login(emailTrimmed, password);
      }

      if (authResponse && authResponse.user) {
        const u = authResponse.user;
        localStorage.setItem("userName", u.name || "Clinician");
        localStorage.setItem("userEmail", u.email || emailTrimmed);
        localStorage.setItem("userRole", u.role || "Clinician / Practitioner");
        localStorage.setItem("authToken", authResponse.access_token || "auth_valid");
        localStorage.setItem("isAuthenticated", "true");

        // Immediate robust redirect to Dashboard
        navigate("/dashboard", { replace: true });
      } else {
        setErrorMsg("Authentication failed. Please check your credentials.");
      }
    } catch (err) {
      console.error("Auth error:", err);
      setErrorMsg(err.message || "An error occurred during authentication.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page-container">
      {/* LEFT SHOWCASE BANNER */}
      <div className="login-left-banner">
        <div className="banner-overlay">
          <div className="banner-brand" onClick={() => navigate("/")}>
            <div className="banner-logo">
              <Heart size={24} fill="#ffffff" />
            </div>
            <div>
              <h2>HeartCare<span>.AI</span></h2>
              <span>Clinical Health Intelligence</span>
            </div>
          </div>

          <div className="banner-hero-text">
            <span className="banner-tag">SECURE CLINICAL WORKSPACE</span>
            <h1>Cardiovascular Machine Learning Platform</h1>
            <p>
              Evidence-based 13-biomarker risk stratification, LightGBM multi-class predictive modeling, and continuous longitudinal telemetry.
            </p>

            <div className="banner-checkmarks">
              <div className="check-item">
                <CheckCircle2 size={18} className="text-emerald" />
                <span>Active 13-feature Cleveland ML inference engine</span>
              </div>
              <div className="check-item">
                <CheckCircle2 size={18} className="text-emerald" />
                <span>Explainable AI with SHAP-style biomarker attribution</span>
              </div>
              <div className="check-item">
                <CheckCircle2 size={18} className="text-emerald" />
                <span>Real-time What-If intervention simulation</span>
              </div>
            </div>
          </div>

          <div className="banner-footer-security">
            <Shield size={16} className="text-emerald" />
            <span>End-to-End HIPAA & GDPR Privacy Compliant Architecture</span>
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
                ? "Register your credentials to access the AI diagnostic portal."
                : "Enter your clinical credentials to access your diagnostic workspace."}
            </p>
          </div>

          {/* ERROR NOTIFICATION ALERT */}
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
                    placeholder="e.g. Dr. Sarah Jenkins, MD"
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
                  placeholder="name@hospital.org"
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
                    onClick={() => alert("Password reset instructions sent to your registered email.")}
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
                  placeholder="••••••••••••"
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

            <button type="submit" className="login-submit-btn" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 size={18} className="spin-icon" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>{isSignUp ? "Register Clinical Account" : "Sign In to Workspace"}</span>
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          {/* TOGGLE SIGN IN / SIGN UP */}
          <div style={{ marginTop: "24px", textAlign: "center", fontSize: "14px", color: "#64748b" }}>
            {isSignUp ? (
              <span>
                Already have a clinical account?{" "}
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