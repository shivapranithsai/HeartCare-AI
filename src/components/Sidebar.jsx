import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Sparkles,
  History,
  Building2,
  FileText,
  User,
  LogOut,
  Heart,
  HelpCircle,
  X
} from "lucide-react";

export default function Sidebar({ mobileOpen, setMobileOpen }) {
  const navigate = useNavigate();
  const userName = localStorage.getItem("userName") || "Aarav Sharma";
  const userInitials = userName.split(" ").map(n => n[0]).join("").toUpperCase().substring(0, 2);

  const handleLogout = () => {
    localStorage.removeItem("userName");
    navigate("/login");
  };

  const closeMobile = () => {
    if (setMobileOpen) setMobileOpen(false);
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {mobileOpen && (
        <div className="sidebar-backdrop" onClick={closeMobile}></div>
      )}

      <aside className={`sidebar ${mobileOpen ? "mobile-open" : ""}`}>
        {/* BRAND */}
        <div className="sidebar-brand">
          <div className="brand-logo-glow">
            <Heart className="brand-heart-icon" size={22} />
          </div>
          <div className="sidebar-brand-text">
            <h2>HeartCare<span>.AI</span></h2>
            <span>Clinical Cardiology Suite</span>
          </div>
          {setMobileOpen && (
            <button className="mobile-close-btn" onClick={closeMobile}>
              <X size={20} />
            </button>
          )}
        </div>

        {/* NAVIGATION LINKS */}
        <nav className="sidebar-menu">
          <div className="menu-group-label">CLINICAL SUITE</div>

          <NavLink
            to="/dashboard"
            onClick={closeMobile}
            className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
          >
            <LayoutDashboard className="sidebar-icon" size={19} />
            <span>Dashboard</span>
          </NavLink>

          <NavLink
            to="/new-prediction"
            onClick={closeMobile}
            className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
          >
            <Sparkles className="sidebar-icon" size={19} />
            <span>New Prediction</span>
            <span className="sidebar-badge-new">AI</span>
          </NavLink>

          <NavLink
            to="/history"
            onClick={closeMobile}
            className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
          >
            <History className="sidebar-icon" size={19} />
            <span>Prediction History</span>
          </NavLink>

          <NavLink
            to="/hospitals"
            onClick={closeMobile}
            className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
          >
            <Building2 className="sidebar-icon" size={19} />
            <span>Hospitals & Centers</span>
          </NavLink>

          <NavLink
            to="/reports"
            onClick={closeMobile}
            className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
          >
            <FileText className="sidebar-icon" size={19} />
            <span>Clinical Reports</span>
          </NavLink>

          <div className="menu-group-label" style={{ marginTop: "18px" }}>ACCOUNT & PREFERENCES</div>

          <NavLink
            to="/profile"
            onClick={closeMobile}
            className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
          >
            <User className="sidebar-icon" size={19} />
            <span>Patient Profile</span>
          </NavLink>
        </nav>

        {/* BOTTOM SECTION */}
        <div className="sidebar-bottom">
          {/* Emergency Assistance card */}
          <div className="help-box" onClick={() => navigate("/hospitals")}>
            <div className="help-box-header">
              <HelpCircle size={16} />
              <span>Cardiology Hotline</span>
            </div>
            <p>24/7 Rapid Triage Direct line available</p>
          </div>

          {/* User Profile Info & Logout */}
          <div className="sidebar-user-card">
            <div className="user-avatar-circle">{userInitials}</div>
            <div className="user-info">
              <strong>{userName}</strong>
              <span>Verified Patient</span>
            </div>
            <button
              type="button"
              className="logout-btn"
              onClick={handleLogout}
              title="Sign Out"
            >
              <LogOut size={17} />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}