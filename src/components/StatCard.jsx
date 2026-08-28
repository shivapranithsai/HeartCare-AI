import React from "react";
import { Heart, Activity, AlertTriangle, ShieldCheck, TrendingUp, TrendingDown } from "lucide-react";

export default function StatCard({
  title,
  value,
  description,
  iconType = "heart",
  variant = "blue",
  trend = null,
  trendDirection = "up"
}) {
  const renderIcon = () => {
    switch (iconType) {
      case "heart":
        return <Heart size={22} />;
      case "activity":
        return <Activity size={22} />;
      case "warning":
        return <AlertTriangle size={22} />;
      case "shield":
        return <ShieldCheck size={22} />;
      default:
        return <Activity size={22} />;
    }
  };

  return (
    <div className={`stat-card stat-card-${variant}`}>
      <div className="stat-card-header">
        <span className="stat-title">{title}</span>
        <div className={`stat-icon-wrapper icon-${variant}`}>
          {renderIcon()}
        </div>
      </div>
      <div className="stat-value-container">
        <h2 className="stat-value">{value}</h2>
        {trend && (
          <span className={`stat-trend-badge trend-${trendDirection}`}>
            {trendDirection === "up" ? <TrendingUp size={13} /> : <TrendingDown size={13} />}
            {trend}
          </span>
        )}
      </div>
      {description && <p className="stat-description">{description}</p>}
    </div>
  );
}