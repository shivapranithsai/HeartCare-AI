import React, { useEffect, useState } from "react";
import { Activity, Heart } from "lucide-react";

export default function EcgMonitor({ bpm = 72, status = "Normal Sinus Rhythm" }) {
  const [pulse, setPulse] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulse((prev) => !prev);
    }, (60 / bpm) * 1000);
    return () => clearInterval(interval);
  }, [bpm]);

  return (
    <div className="ecg-monitor-card">
      <div className="ecg-header">
        <div className="ecg-title">
          <Activity className="ecg-icon" size={18} />
          <span>REAL-TIME CARDIAC RHYTHM</span>
        </div>
        <div className="ecg-live-badge">
          <span className="ecg-live-dot"></span> LIVE TELEMETRY
        </div>
      </div>

      <div className="ecg-display-area">
        {/* Animated ECG grid and wave */}
        <div className="ecg-grid-overlay"></div>
        <svg className="ecg-svg" viewBox="0 0 500 100" preserveAspectRatio="none">
          <path
            className="ecg-wave-path"
            d="M 0,50 L 40,50 L 50,45 L 60,50 L 80,50 L 90,50 L 95,20 L 105,85 L 115,10 L 125,55 L 135,50 L 160,50 L 175,40 L 190,50 L 250,50 L 260,45 L 270,50 L 290,50 L 300,50 L 305,20 L 315,85 L 325,10 L 335,55 L 345,50 L 370,50 L 385,40 L 400,50 L 500,50"
          />
        </svg>
      </div>

      <div className="ecg-footer">
        <div className="ecg-bpm-readout">
          <Heart className={`ecg-heart-icon ${pulse ? "pulse-active" : ""}`} size={20} />
          <div>
            <span className="bpm-number">{bpm}</span>
            <span className="bpm-unit">BPM</span>
          </div>
        </div>
        <div className="ecg-status-text">
          <span className="status-label">Status</span>
          <span className="status-val">{status}</span>
        </div>
      </div>
    </div>
  );
}
