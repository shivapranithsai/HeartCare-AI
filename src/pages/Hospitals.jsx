import React, { useState, useEffect } from "react";
import {
  Building2,
  MapPin,
  Star,
  ShieldAlert,
  CheckCircle2,
  Search,
  Clock,
  Navigation,
  Crosshair,
  Compass,
  AlertCircle,
  Zap,
  ArrowUpRight
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { api } from "../services/api";
import { calculateHaversineDistance, formatDistance } from "../utils/geo";

const INDIAN_CITIES = [
  "All",
  "New Delhi",
  "Mumbai",
  "Bengaluru",
  "Chennai",
  "Hyderabad",
  "Kolkata",
  "Ahmedabad",
  "Pune",
  "Chandigarh",
  "Thiruvananthapuram",
  "Jaipur",
  "Lucknow",
  "Bhubaneswar"
];

export default function Hospitals() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cityFilter, setCityFilter] = useState("");
  const [activeCityTab, setActiveCityTab] = useState("All");
  const [emergencyOnly, setEmergencyOnly] = useState(false);
  const [dataSource, setDataSource] = useState("Live Geospatial Discovery");
  const [isLiveDynamic, setIsLiveDynamic] = useState(false);

  // GPS Geolocation States
  const [userCoords, setUserCoords] = useState(null);
  const [locatingGPS, setLocatingGPS] = useState(false);
  const [gpsError, setGpsError] = useState(null);

  const loadHospitals = async ({
    city = activeCityTab,
    emergency = emergencyOnly,
    userLat = userCoords?.lat || null,
    userLon = userCoords?.lon || null
  } = {}) => {
    setLoading(true);
    try {
      const data = await api.getHospitals(
        city === "All" ? "" : city,
        emergency,
        userLat,
        userLon
      );
      setHospitals(data.hospitals || []);
      setDataSource(data.data_source || "Live Geospatial Network");
      setIsLiveDynamic(data.is_live_dynamic || false);
    } catch (err) {
      console.error("Error loading hospitals:", err);
    } finally {
      setLoading(false);
    }
  };

  // Attempt initial GPS discovery or load city directory on mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const coords = {
            lat: pos.coords.latitude,
            lon: pos.coords.longitude,
            accuracy: Math.round(pos.coords.accuracy)
          };
          setUserCoords(coords);
          loadHospitals({
            city: "All",
            emergency: emergencyOnly,
            userLat: coords.lat,
            userLon: coords.lon
          });
        },
        (err) => {
          console.log("Initial geolocation prompt note:", err.message);
          loadHospitals({
            city: activeCityTab,
            emergency: emergencyOnly,
            userLat: null,
            userLon: null
          });
        },
        { enableHighAccuracy: true, timeout: 6000, maximumAge: 60000 }
      );
    } else {
      loadHospitals({
        city: activeCityTab,
        emergency: emergencyOnly,
        userLat: null,
        userLon: null
      });
    }
  }, []);

  // Reload when filters change
  useEffect(() => {
    loadHospitals({
      city: activeCityTab,
      emergency: emergencyOnly,
      userLat: userCoords?.lat || null,
      userLon: userCoords?.lon || null
    });
  }, [emergencyOnly, activeCityTab]);

  const handleCityTabClick = (city) => {
    setActiveCityTab(city);
    setCityFilter(city === "All" ? "" : city);
    loadHospitals({
      city: city,
      emergency: emergencyOnly,
      userLat: userCoords?.lat || null,
      userLon: userCoords?.lon || null
    });
  };

  const handleDetectLocation = () => {
    if (!navigator.geolocation) {
      setGpsError("Geolocation is not supported by your browser.");
      return;
    }

    setLocatingGPS(true);
    setGpsError(null);

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const coords = {
          lat: pos.coords.latitude,
          lon: pos.coords.longitude,
          accuracy: Math.round(pos.coords.accuracy)
        };
        setUserCoords(coords);
        setActiveCityTab("All");
        setCityFilter("");
        setLocatingGPS(false);
        loadHospitals({
          city: "All",
          emergency: emergencyOnly,
          userLat: coords.lat,
          userLon: coords.lon
        });
      },
      (err) => {
        console.warn("GPS detection error:", err);
        setLocatingGPS(false);
        if (err.code === 1) {
          setGpsError("Location permission denied. Please allow location access in your browser or select a city below.");
        } else {
          setGpsError("Unable to retrieve precise GPS coordinates. Please select your nearest city below.");
        }
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  };

  const handleClearLocation = () => {
    setUserCoords(null);
    setGpsError(null);
    loadHospitals({
      city: activeCityTab,
      emergency: emergencyOnly,
      userLat: null,
      userLon: null
    });
  };

  // Identify closest hospital and its dynamic distance
  const nearestHospital = hospitals.length > 0 ? hospitals[0] : null;
  const nearestDistValue = nearestHospital
    ? (nearestHospital.distance_km !== null && nearestHospital.distance_km !== undefined
        ? nearestHospital.distance_km
        : (userCoords && nearestHospital.latitude && nearestHospital.longitude)
          ? calculateHaversineDistance(userCoords.lat, userCoords.lon, nearestHospital.latitude, nearestHospital.longitude)
          : null)
    : null;
  const nearestDistLabel = formatDistance(nearestDistValue);

  return (
    <div className="dashboard-page-wrapper">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <div className="dashboard-main-area">
        <Navbar onMobileMenuClick={() => setMobileOpen(true)} />

        <main className="dashboard-content-scroll">
          {/* HEADER ROW */}
          <div className="page-header-row">
            <div>
              <span className="section-eyebrow">INDIA CARDIOLOGY NETWORK</span>
              <h1>Find Cardiac Hospitals Near You</h1>
              <p>
                Instant GPS proximity triage, 24/7 cardiac emergency centers, live distance calculations, and turn-by-turn navigation across India.
              </p>
            </div>

            <div className="emergency-hotline-pill">
              <span className="text-rose spin-pulse" style={{ fontSize: "18px" }}>🚨</span>
              <div>
                <small>National Cardiac & Ambulance Emergency</small>
                <strong>112 / 108 / 102 (India)</strong>
              </div>
            </div>
          </div>

          {/* GPS FIND NEAR ME TOOLBAR */}
          <div className="gps-finder-banner">
            <div className="gps-info-left">
              <div className="gps-icon-orb">
                <Crosshair size={24} className={locatingGPS ? "spin-pulse" : ""} />
              </div>
              <div>
                <h3>{userCoords ? "GPS Location Active" : "Find Cardiac Centers Near Your Location"}</h3>
                <p>
                  {userCoords
                    ? `Live coordinates: ${userCoords.lat.toFixed(4)}° N, ${userCoords.lon.toFixed(4)}° E (Sorted by closest first)`
                    : "Detect your live GPS coordinates to calculate exact distance, drive ETA, and the closest 24/7 cardiac emergency room."}
                </p>
              </div>
            </div>

            <div className="gps-actions-right">
              {userCoords ? (
                <>
                  <div className="gps-active-badge">
                    <CheckCircle2 size={16} />
                    <span>Location Locked</span>
                  </div>
                  <button type="button" className="gps-clear-btn" onClick={handleClearLocation}>
                    Reset GPS
                  </button>
                </>
              ) : (
                <button
                  type="button"
                  className="gps-detect-btn"
                  onClick={handleDetectLocation}
                  disabled={locatingGPS}
                >
                  <Crosshair size={18} />
                  <span>{locatingGPS ? "Acquiring Coordinates..." : "📍 Find Near Me (Detect GPS)"}</span>
                </button>
              )}
            </div>
          </div>

          {/* GPS ERROR NOTIFICATION */}
          {gpsError && (
            <div
              style={{
                background: "#fef2f2",
                border: "1px solid #fca5a5",
                color: "#b91c1c",
                padding: "12px 16px",
                borderRadius: "12px",
                fontSize: "13px",
                marginBottom: "20px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "10px"
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <AlertCircle size={18} />
                <span>{gpsError}</span>
              </div>
              <button
                type="button"
                onClick={() => setGpsError(null)}
                style={{ background: "none", border: "none", cursor: "pointer", color: "#b91c1c", fontWeight: "700" }}
              >
                ✕
              </button>
            </div>
          )}

          {/* NEAREST EMERGENCY SPOTLIGHT HERO */}
          {nearestHospital && (
            <div className="nearest-er-spotlight">
              <div className="nearest-er-content">
                <span className="nearest-er-tag">
                  <Zap size={13} fill="#ffffff" />
                  {userCoords ? "⚡ CLOSEST EMERGENCY CARDIAC CENTER" : "⭐ TOP-RATED CARDIOLOGY INSTITUTE"}
                </span>
                <h2 className="nearest-er-title">{nearestHospital.name}</h2>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#475569", fontSize: "14px", margin: "4px 0" }}>
                  <MapPin size={16} className="text-rose" />
                  <span>{nearestHospital.address}</span>
                </div>
                <div className="nearest-er-meta">
                  {nearestDistLabel ? (
                    <span className="nearest-er-distance-pill">
                      <Navigation size={14} />
                      {nearestDistLabel}
                    </span>
                  ) : (
                    <button
                      type="button"
                      onClick={handleDetectLocation}
                      className="nearest-er-distance-pill"
                      style={{ cursor: "pointer", border: "1px dashed #cbd5e1", background: "#f8fafc", color: "#475569" }}
                    >
                      <Navigation size={14} />
                      <span>Enable location to calculate distance</span>
                    </button>
                  )}
                  {nearestDistLabel && (
                    <span style={{ display: "flex", alignItems: "center", gap: "4px", fontWeight: "600", color: "#0f172a" }}>
                      <Clock size={15} className="text-muted" />
                      Est. Transit ETA: ~{nearestHospital.eta_minutes || Math.max(4, Math.round(nearestDistValue * 2.2))} mins
                    </span>
                  )}
                  <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                    <Star size={15} fill="#f59e0b" color="#f59e0b" />
                    <strong>{nearestHospital.rating}</strong> ({nearestHospital.review_count} reviews)
                  </span>
                </div>
              </div>

              <div className="nearest-er-actions">
                <a
                  href={nearestHospital.maps_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="emergency-nav-btn"
                  title="Open direct turn-by-turn route on Google Maps"
                >
                  <Navigation size={16} />
                  <span>Navigate Now</span>
                  <ArrowUpRight size={15} />
                </a>
              </div>
            </div>
          )}

          {/* SEARCH & FILTER CONTROLS */}
          <div className="hospitals-filter-bar">
            <div className="hospitals-search-box">
              <Search size={18} className="search-icon" />
              <input
                type="text"
                placeholder="Search AIIMS, Fortis, Narayana, Apollo, city or specialty..."
                value={cityFilter}
                onChange={(e) => setCityFilter(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    loadHospitals({
                      city: cityFilter,
                      emergency: emergencyOnly,
                      userLat: userCoords?.lat || null,
                      userLon: userCoords?.lon || null
                    });
                  }
                }}
              />
              <button
                type="button"
                className="search-btn"
                onClick={() =>
                  loadHospitals({
                    city: cityFilter,
                    emergency: emergencyOnly,
                    userLat: userCoords?.lat || null,
                    userLon: userCoords?.lon || null
                  })
                }
              >
                Search
              </button>
            </div>

            <label className="emergency-filter-toggle">
              <input
                type="checkbox"
                checked={emergencyOnly}
                onChange={(e) => setEmergencyOnly(e.target.checked)}
              />
              <ShieldAlert size={16} className={emergencyOnly ? "text-rose" : ""} />
              <span>24/7 Cardiac ER Only</span>
            </label>
          </div>

          {/* QUICK CITY SELECTOR CHIPS */}
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "24px" }}>
            {INDIAN_CITIES.map((city) => (
              <button
                key={city}
                type="button"
                onClick={() => handleCityTabClick(city)}
                style={{
                  padding: "6px 14px",
                  borderRadius: "20px",
                  fontSize: "13px",
                  fontWeight: "600",
                  cursor: "pointer",
                  border: activeCityTab === city ? "1px solid var(--primary, #0284c7)" : "1px solid #e2e8f0",
                  background: activeCityTab === city ? "var(--primary, #0284c7)" : "#ffffff",
                  color: activeCityTab === city ? "#ffffff" : "#475569",
                  transition: "all 0.15s ease",
                  boxShadow: activeCityTab === city ? "0 2px 8px rgba(2, 132, 199, 0.25)" : "none"
                }}
              >
                {city}
              </button>
            ))}
          </div>

          {/* PROXIMITY RADAR STRIP - Rendered only when GPS location is locked */}
          {userCoords && hospitals.length > 0 && (
            <div className="proximity-radar-card">
              <div className="radar-header">
                <h3>
                  <Compass size={16} style={{ display: "inline", verticalAlign: "middle", marginRight: "6px", color: "#0284c7" }} />
                  Proximity Radar ({hospitals.length} centers found near you)
                </h3>
                <span style={{ fontSize: "12px", color: "#64748b" }}>Click card for turn-by-turn map directions</span>
              </div>
              <div className="radar-items-row">
                {hospitals.slice(0, 8).map((hosp, idx) => {
                  const dVal = hosp.distance_km !== null && hosp.distance_km !== undefined
                    ? hosp.distance_km
                    : (userCoords && hosp.latitude && hosp.longitude)
                      ? calculateHaversineDistance(userCoords.lat, userCoords.lon, hosp.latitude, hosp.longitude)
                      : null;
                  const dText = formatDistance(dVal);
                  return (
                    <a
                      key={hosp.id}
                      href={hosp.maps_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="radar-hospital-chip"
                    >
                      <span className="radar-chip-name">{idx + 1}. {hosp.name}</span>
                      {dText && (
                        <span className="radar-chip-dist">
                          <Navigation size={12} />
                          {dText} • {hosp.city}
                        </span>
                      )}
                    </a>
                  );
                })}
              </div>
            </div>
          )}

          {/* DYNAMIC RESULTS HEADER & DATA SOURCE BADGE */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px", marginBottom: "16px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <h3 style={{ fontSize: "16px", fontWeight: "700", color: "#1e293b", margin: 0 }}>
                {userCoords ? "Hospitals Nearest to You" : activeCityTab !== "All" ? `Hospitals in ${activeCityTab}` : "Verified Cardiac Care Centers"}
              </h3>
              <span style={{ background: "#f1f5f9", color: "#475569", padding: "2px 8px", borderRadius: "12px", fontSize: "12px", fontWeight: "600" }}>
                {hospitals.length} centers found
              </span>
            </div>

            <div style={{ display: "inline-flex", alignItems: "center", gap: "6px", background: isLiveDynamic ? "#ecfdf5" : "#f8fafc", border: isLiveDynamic ? "1px solid #a7f3d0" : "1px solid #e2e8f0", padding: "4px 10px", borderRadius: "16px", fontSize: "12px", color: isLiveDynamic ? "#065f46" : "#64748b", fontWeight: "600" }}>
              <span style={{ width: "7px", height: "7px", borderRadius: "50%", background: isLiveDynamic ? "#10b981" : "#94a3b8" }}></span>
              <span>{dataSource}</span>
            </div>
          </div>

          {/* HOSPITALS GRID */}
          {loading ? (
            <div style={{ textAlign: "center", padding: "40px", color: "#64748b" }}>
              <div className="spin-pulse" style={{ fontSize: "24px", marginBottom: "8px" }}>🩺</div>
              <p>Locating verified cardiac centers & calculating travel routes...</p>
            </div>
          ) : hospitals.length === 0 ? (
            <div style={{ textAlign: "center", padding: "48px 24px", background: "white", borderRadius: "16px", border: "1.5px dashed #cbd5e1" }}>
              <Building2 size={40} className="text-muted" style={{ margin: "0 auto 12px" }} />
              <h3>No cardiac centers match your criteria</h3>
              <p style={{ color: "#64748b", fontSize: "14px", maxWidth: "400px", margin: "0 auto 16px" }}>
                Try clearing search terms or selecting another city to discover verified cardiac institutes.
              </p>
              <button
                type="button"
                onClick={() => {
                  setActiveCityTab("All");
                  setEmergencyOnly(false);
                }}
                className="primary-action-btn"
                style={{ padding: "8px 18px", fontSize: "13px" }}
              >
                Reset All Filters
              </button>
            </div>
          ) : (
            <div className="hospitals-grid">
              {hospitals.map((hosp) => {
                const calculatedDist = hosp.distance_km !== null && hosp.distance_km !== undefined
                  ? hosp.distance_km
                  : (userCoords && hosp.latitude && hosp.longitude)
                    ? calculateHaversineDistance(userCoords.lat, userCoords.lon, hosp.latitude, hosp.longitude)
                    : null;
                const distanceLabel = formatDistance(calculatedDist);

                return (
                  <div key={hosp.id} className="hospital-card">
                    <div className="hospital-card-header">
                      <div className="hospital-title-row">
                        <h3>{hosp.name}</h3>
                        {hosp.emergency_available && (
                          <span className="emergency-badge">
                            <ShieldAlert size={12} /> 24/7 ER
                          </span>
                        )}
                      </div>
                      <div className="hospital-rating-row">
                        <div className="star-rating">
                          <Star size={14} fill="#f59e0b" color="#f59e0b" />
                          <strong>{hosp.rating}</strong>
                          <span>({hosp.review_count} reviews)</span>
                        </div>
                        {distanceLabel ? (
                          <span className={`distance-tag ${calculatedDist > 50 ? "distance-far" : ""}`}>
                            <Navigation size={12} />
                            {distanceLabel}
                          </span>
                        ) : (
                          <button
                            type="button"
                            onClick={handleDetectLocation}
                            className="distance-tag distance-prompt-btn"
                            title="Click to calculate distance using your GPS location"
                            style={{
                              background: "#f8fafc",
                              color: "#64748b",
                              border: "1px dashed #cbd5e1",
                              cursor: "pointer",
                              padding: "3px 8px",
                              borderRadius: "12px",
                              fontSize: "11px",
                              display: "inline-flex",
                              alignItems: "center",
                              gap: "4px",
                              fontWeight: "600"
                            }}
                          >
                            <Navigation size={11} />
                            <span>Enable location to calculate distance</span>
                          </button>
                        )}
                      </div>
                    </div>

                    <div className="hospital-body">
                      <p className="hospital-address">
                        <MapPin size={15} className="text-muted" style={{ flexShrink: 0, marginTop: "2px" }} />
                        <span>{hosp.address}</span>
                      </p>

                      <div className="hospital-specialties">
                        <label>Key Specialties & Advanced Care:</label>
                        <div className="specialties-tags">
                          {hosp.specialties.map((s, idx) => (
                            <span key={idx} className="spec-tag">{s}</span>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className="hospital-footer">
                      <a
                        href={hosp.maps_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="nav-maps-btn"
                        style={{ width: "100%", justifyContent: "center" }}
                        title="Open turn-by-turn route on Google Maps"
                      >
                        <Navigation size={14} />
                        <span>Directions</span>
                        <ArrowUpRight size={14} />
                      </a>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
