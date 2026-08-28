import React, { useState, useEffect } from "react";
import { Search, Bell, Menu, CheckCircle2, AlertCircle, ChevronDown } from "lucide-react";
import { api } from "../services/api";

export default function Navbar({ onMobileMenuClick }) {
  const [backendOnline, setBackendOnline] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const userName = localStorage.getItem("userName") || "Aarav Sharma";
  const userInitials = userName.split(" ").map(n => n[0]).join("").toUpperCase().substring(0, 2);

  useEffect(() => {
    let isMounted = true;
    api.checkHealth().then((res) => {
      if (isMounted) {
        setBackendOnline(res.status === "healthy");
      }
    });
    const interval = setInterval(() => {
      api.checkHealth().then((res) => {
        if (isMounted) {
          setBackendOnline(res.status === "healthy");
        }
      });
    }, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <header className="topbar">
      {/* Left Area: Mobile Hamburger & Search */}
      <div className="topbar-left">
        <button
          className="mobile-hamburger-btn"
          onClick={onMobileMenuClick}
          aria-label="Toggle Menu"
        >
          <Menu size={22} />
        </button>

        <div className="search-bar-wrapper">
          <Search className="search-icon" size={17} />
          <input
            type="text"
            className="search-input"
            placeholder="Search vitals, assessments, reports... (Ctrl+K)"
          />
        </div>
      </div>

      {/* Right Area: Backend Status, Notifications, User */}
      <div className="topbar-right">
        {/* Backend Connectivity Status Pill */}
        <div className={`backend-status-pill ${backendOnline ? "status-online" : "status-offline"}`}>
          {backendOnline ? (
            <>
              <span className="status-indicator-dot online"></span>
              <span className="status-label">FastAPI Model Engine Online</span>
            </>
          ) : (
            <>
              <span className="status-indicator-dot offline"></span>
              <span className="status-label">Client Mode (Backend Standby)</span>
            </>
          )}
        </div>

        {/* Notifications */}
        <div className="notifications-dropdown-container">
          <button
            type="button"
            className="notification-icon-btn"
            onClick={() => setNotificationsOpen(!notificationsOpen)}
            aria-label="Notifications"
          >
            <Bell size={19} />
            <span className="notification-unread-dot"></span>
          </button>

          {notificationsOpen && (
            <div className="notifications-popover">
              <div className="popover-header">
                <strong>Notifications</strong>
                <span>Mark all as read</span>
              </div>
              <div className="popover-list">
                <div className="popover-item">
                  <CheckCircle2 size={16} className="text-success" />
                  <div>
                    <p>Cardiology baseline assessment ready for review.</p>
                    <small>10 mins ago</small>
                  </div>
                </div>
                <div className="popover-item">
                  <AlertCircle size={16} className="text-warning" />
                  <div>
                    <p>Reminder: Log evening resting blood pressure.</p>
                    <small>2 hours ago</small>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Profile Chip */}
        <div className="navbar-user-chip">
          <div className="chip-avatar">{userInitials}</div>
          <div className="chip-text">
            <strong>{userName}</strong>
            <span>Cardiology Patient</span>
          </div>
          <ChevronDown size={15} className="chip-arrow" />
        </div>
      </div>
    </header>
  );
}