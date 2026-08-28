import React from "react";
import { useNavigate } from "react-router-dom";
import {
  Heart,
  ArrowRight
} from "lucide-react";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      {/* STICKY GLASS NAVBAR */}
      <nav className="landing-navbar">
        <div className="brand" onClick={() => navigate("/")}>
          <div className="brand-icon">
            <Heart size={20} fill="#ffffff" />
          </div>
          <span className="brand-title">HeartCare<span className="accent">.AI</span></span>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
        </div>

        <div className="nav-actions">
          <button className="nav-start-btn" onClick={() => navigate("/login")}>
            Sign In <ArrowRight size={16} />
          </button>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="hero-section" id="home">
        <div className="hero-content">
          <div className="ai-badge">
            <span className="pulse-dot"></span>
            <span>NEXT-GEN CLINICAL AI PLATFORM</span>
          </div>

          <h1 className="hero-heading">
            Predict Heart Failure Risk
            <br />
            <span className="gradient-text">Before Symptoms Escalate.</span>
          </h1>

          <p className="hero-description">
            Powered by advanced Machine Learning and validated clinical cardiovascular protocols.
            Analyze multi-factorial biomarker data, interpret explainable risk attributions, and simulate preventative interventions.
          </p>

          <div className="hero-buttons">
            <button className="primary-cta" onClick={() => navigate("/login")}>
              <span>Start Clinical Assessment</span>
              <ArrowRight size={18} />
            </button>
          </div>

          <div className="trust-row">
            <div className="trust-item">
              <strong className="trust-num">98.4%</strong>
              <span>Model Accuracy</span>
            </div>
            <div className="trust-divider"></div>
            <div className="trust-item">
              <strong className="trust-num">12+</strong>
              <span>Clinical Biomarkers</span>
            </div>
            <div className="trust-divider"></div>
            <div className="trust-item">
              <strong className="trust-num">Real-Time</strong>
              <span>SHAP Explainability</span>
            </div>
          </div>
        </div>

        {/* HERO VISUAL WITH ANIMATED PULSE */}
        <div className="hero-visual">
          <div className="hero-visual-card">
            <div className="visual-card-top">
              <div className="pulse-header-icon">
                <Heart size={28} className="beating-heart" />
              </div>
              <div>
                <small>REAL-TIME ANALYSIS</small>
                <h3>Ventricular Health Monitor</h3>
              </div>
            </div>

            <div className="mini-ecg-canvas">
              <svg viewBox="0 0 300 80" className="mini-ecg-svg">
                <path
                  d="M 0,40 L 40,40 L 50,35 L 60,40 L 80,40 L 90,40 L 95,15 L 105,70 L 115,5 L 125,45 L 135,40 L 170,40 L 180,35 L 190,40 L 210,40 L 215,15 L 225,70 L 235,5 L 245,45 L 255,40 L 300,40"
                  className="mini-ecg-line"
                />
              </svg>
            </div>

            <div className="floating-metric-row">
              <div className="metric-chip">
                <span className="metric-label">Systolic Output</span>
                <strong>Normal (62%)</strong>
              </div>
              <div className="metric-chip">
                <span className="metric-label">Arterial Resistance</span>
                <strong className="text-emerald">Optimal</strong>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="brand-icon">
              <Heart size={18} fill="#ffffff" />
            </div>
            <strong>HeartCare.AI</strong>
            <span>Cardiovascular Risk Stratification & Clinical AI Suite</span>
          </div>
          <div className="footer-links">
            <a href="#home">Home</a>
          </div>
          <p className="footer-disclaimer">
            Disclaimer: HeartCare AI is an assistive decision support platform. Always consult certified medical practitioners for diagnostic clinical decisions.
          </p>
        </div>
      </footer>
    </div>
  );
}