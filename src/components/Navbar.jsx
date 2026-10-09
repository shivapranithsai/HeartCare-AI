import React, { useState, useEffect } from "react";
import { Search, Bell, Menu, CheckCircle2, AlertCircle, ChevronDown } from "lucide-react";
import { api } from "../services/api";

export default function Navbar({ onMobileMenuClick }) {
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const userName = localStorage.getItem("userName") || "Patient";
  const userInitials = userName.split(" ").map(n => n[0]).join("").toUpperCase().substring(0, 2);

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