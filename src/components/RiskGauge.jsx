import React from "react";

export default function RiskGauge({ score = 45, level = "Moderate Risk", size = 180 }) {
  const strokeWidth = 14;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  // Use 240 degrees arc for speedometer-style gauge
  const arcLength = circumference * 0.75;
  const progress = Math.min(100, Math.max(0, score));
  const strokeDashoffset = arcLength - (arcLength * progress) / 100;

  // Determine color theme
  let strokeColor = "#10b981"; // Green
  let badgeClass = "badge-low";
  if (score >= 75) {
    strokeColor = "#ef4444"; // Red
    badgeClass = "badge-critical";
  } else if (score >= 50) {
    strokeColor = "#f97316"; // Orange
    badgeClass = "badge-high";
  } else if (score >= 25) {
    strokeColor = "#f59e0b"; // Amber
    badgeClass = "badge-moderate";
  }

  return (
    <div className="risk-gauge-container" style={{ width: size, height: size }}>
      <svg className="risk-gauge-svg" width={size} height={size}>
        {/* Background Track Arc */}
        <circle
          className="risk-gauge-track"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          strokeDasharray={`${arcLength} ${circumference}`}
          transform={`rotate(135 ${size / 2} ${size / 2})`}
        />
        {/* Animated Progress Arc */}
        <circle
          className="risk-gauge-progress"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={strokeColor}
          strokeWidth={strokeWidth}
          strokeDasharray={`${arcLength} ${circumference}`}
          strokeDashoffset={strokeDashoffset}
          transform={`rotate(135 ${size / 2} ${size / 2})`}
        />
      </svg>
      <div className="risk-gauge-content">
        <div className="gauge-score-value">{score}</div>
        <div className="gauge-score-max">/100</div>
        <div className={`gauge-risk-badge ${badgeClass}`}>{level}</div>
      </div>
    </div>
  );
}
