import React, { useState } from "react";
import { Save, CheckCircle2, Trash2 } from "lucide-react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function Profile() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [savedAlert, setSavedAlert] = useState(false);

  const currentEmail = localStorage.getItem("userEmail") || "";
  const currentName = localStorage.getItem("userName") || "";

  // Retrieve user-specific saved profile from localStorage or initialize with empty fields
  const storageKey = currentEmail ? `user_profile_${currentEmail}` : "user_profile";
  const savedData = JSON.parse(localStorage.getItem(storageKey) || "{}");

  const [profile, setProfile] = useState({
    name: savedData.name || currentName || "",
    email: savedData.email || currentEmail || "",
    phone: savedData.phone || "",
    emergencyContact: savedData.emergencyContact || "",
    bloodGroup: savedData.bloodGroup || "",
    emailNotifications: savedData.emailNotifications || false,
    smsAlerts: savedData.smsAlerts || false
  });

  const handleSave = (e) => {
    e.preventDefault();
    if (profile.name.trim()) {
      localStorage.setItem("userName", profile.name.trim());
    }
    localStorage.setItem(storageKey, JSON.stringify(profile));
    setSavedAlert(true);
    setTimeout(() => setSavedAlert(false), 2500);
  };

  return (
    <div className="dashboard-page-wrapper">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <div className="dashboard-main-area">
        <Navbar onMobileMenuClick={() => setMobileOpen(true)} />

        <main className="dashboard-content-scroll">
          <div className="page-header-row">
            <div>
              <span className="section-eyebrow">PATIENT PREFERENCES</span>
              <h1>Account Settings & Medical Baseline</h1>
              <p>Manage personal credentials, emergency contacts, and cardiovascular baseline data.</p>
            </div>

            {savedAlert && (
              <div className="saved-toast">
                <CheckCircle2 size={16} className="text-emerald" />
                <span>Profile updated successfully!</span>
              </div>
            )}
          </div>

          <form onSubmit={handleSave} className="profile-form-card">
            {/* PERSONAL IDENTITY */}
            <div className="form-section-block">
              <h3>Personal Information</h3>
              <div className="form-grid-2col">
                <div className="form-group">
                  <label>Full Legal Name</label>
                  <input
                    type="text"
                    value={profile.name}
                    onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                    placeholder="Enter your full name"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email Address</label>
                  <input
                    type="email"
                    value={profile.email}
                    onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                    placeholder=" "
                    disabled
                  />
                </div>
                <div className="form-group">
                  <label>Primary Phone Number</label>
                  <input
                    type="tel"
                    value={profile.phone}
                    onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                    placeholder=" "
                  />
                </div>
                <div className="form-group">
                  <label>Emergency Contact Person & Phone</label>
                  <input
                    type="text"
                    value={profile.emergencyContact}
                    onChange={(e) =>
                      setProfile({ ...profile, emergencyContact: e.target.value })
                    }
                    placeholder=" "
                  />
                </div>
              </div>
            </div>

            {/* CLINICAL BASELINE */}
            <div className="form-section-block">
              <h3>Cardiovascular Baseline & Medical Notes</h3>
              <div className="form-grid-2col">
                <div className="form-group">
                  <label>Blood Group Type</label>
                  <select
                    value={profile.bloodGroup}
                    onChange={(e) => setProfile({ ...profile, bloodGroup: e.target.value })}
                  >
                    <option value="">Select Blood Group (Optional)</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                  </select>
                </div>
              </div>
            </div>

            {/* NOTIFICATIONS & TELEMETRY PREFERENCES */}
            <div className="form-section-block">
              <h3>Notification & Triage Settings</h3>
              <div className="checkbox-list">
                <label className="checkbox-row">
                  <input
                    type="checkbox"
                    checked={profile.emailNotifications}
                    onChange={(e) =>
                      setProfile({ ...profile, emailNotifications: e.target.checked })
                    }
                  />
                  <span>Receive monthly cardiovascular risk trend reports via email</span>
                </label>

                <label className="checkbox-row">
                  <input
                    type="checkbox"
                    checked={profile.smsAlerts}
                    onChange={(e) =>
                      setProfile({ ...profile, smsAlerts: e.target.checked })
                    }
                  />
                  <span>Enable SMS emergency telemetry alerts if high risk biomarkers are detected</span>
                </label>
              </div>
            </div>

            {/* ACTIONS */}
            <div className="wizard-actions-bar" style={{ marginTop: "24px" }}>
              <button
                type="button"
                className="wizard-back-btn text-danger"
                onClick={() => {
                  if (window.confirm("Clear local cache and sign out?")) {
                    localStorage.clear();
                    window.location.href = "/login";
                  }
                }}
              >
                <Trash2 size={16} />
                <span>Reset Local Session</span>
              </button>

              <button type="submit" className="primary-action-btn">
                <Save size={16} />
                <span>Save Profile Preferences</span>
              </button>
            </div>
          </form>
        </main>
      </div>
    </div>
  );
}
