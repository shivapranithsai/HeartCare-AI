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
  ArrowUpRight,
  Edit2,
  Globe
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { api } from "../services/api";
import {
  calculateHaversineDistance,
  formatDistance,
  INDIAN_CITY_COORDINATES
} from "../utils/geo";

const INDIAN_CITIES = [
  "All",
  "Vadodara",
  "Ahmedabad",
  "Mumbai",
  "New Delhi",
  "Bengaluru",
  "Chennai",
  "Hyderabad",
  "Kolkata",
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

  // User Location & GPS States
  const [userCoords, setUserCoords] = useState(null); // { lat, lon, accuracy, source: "gps" | "ip" | "city_chip" | "custom" }
  const [locationLabel, setLocationLabel] = useState(null); // Human-readable locality / city name
  const [locatingGPS, setLocatingGPS] = useState(false);
  const [gpsError, setGpsError] = useState(null);
  const [showLocationInput, setShowLocationInput] = useState(false);
  const [customLocationText, setCustomLocationText] = useState("");
  const [isGeocodingLocation, setIsGeocodingLocation] = useState(false);

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
      let list = [...(data.hospitals || [])];

      // Seamlessly integrate Parul Sevashram Hospital if user is near Vadodara / Parul campus
      const lat = userLat != null ? userLat : userCoords?.lat;
      const lon = userLon != null ? userLon : userCoords?.lon;
      const PARUL_COORDS = { lat: 22.2882187, lon: 73.3652789 };

      const distToParul = (lat != null && lon != null)
        ? calculateHaversineDistance(lat, lon, PARUL_COORDS.lat, PARUL_COORDS.lon)
        : null;

      // Only include Parul if user is within 80km OR specifically browsing Vadodara
      const isNearVadodara = distToParul != null && distToParul <= 80;
      const isSearchingVadodara = city && /vadodara|parul|limda|waghodia/i.test(city);
      const shouldShowParul = isNearVadodara || isSearchingVadodara;

      const hasParul = list.some(h => /parul|sevashram/i.test(h.name || ""));

      if (shouldShowParul && !hasParul) {
        list.push({
          id: "IN-HOSP-24",
          name: "Parul Sevashram Hospital",
          city: "Vadodara",
          address: "Parul University Campus, Post Limda, Waghodia Road, Vadodara, Gujarat 391760",
          phone: "+91 2668 260232 / 1800 889 0088 / 108",
          rating: 4.9,
          review_count: 1480,
          emergency_available: true,
          specialties: [
            "24/7 Cardiac Emergency & Cath Lab",
            "Interventional Cardiology",
            "Critical Care CCU/ICU",
            "Heart Failure Clinic",
            "Cardiothoracic Surgery",
            "Echocardiography"
          ],
          distance_km: distToParul,
          eta_minutes: distToParul != null ? Math.max(4, Math.round(distToParul * 2.2)) : null,
          latitude: PARUL_COORDS.lat,
          longitude: PARUL_COORDS.lon,
          is_live_dynamic: true,
          data_source: "Verified Indian Cardiology Network",
          maps_url: "https://www.google.com/maps/dir/?api=1&destination=22.2882187,73.3652789"
        });
      }

      // If 24/7 Cardiac ER Only is selected, filter strictly to emergency cardiac facilities
      if (emergency) {
        list = list.filter(h => {
          if (!h.emergency_available) return false;
          const n = (h.name || "").toLowerCase();
          const nonCardiac = [
            "orthopedic", "orthopaedic", "eye hospital", "netralaya", "dental",
            "maternity", "infertility", "skin", "laser", "children", "pediatric",
            "laparoscopy", "homeopathy", "ayurveda", "physiotherapy", "ent hospital"
          ];
          return !nonCardiac.some(term => n.includes(term));
        });
      }

      // Sort: closest distance first, then by highest rating
      list.sort((a, b) => {
        const distA = a.distance_km != null ? a.distance_km : 999999;
        const distB = b.distance_km != null ? b.distance_km : 999999;
        if (distA !== distB) return distA - distB;
        return (b.rating || 0) - (a.rating || 0);
      });

      setHospitals(list);
      setDataSource(data.data_source || (userCoords ? "Live OpenStreetMap & Verified Cardiology Network" : "Verified Cardiology Directory"));
      setIsLiveDynamic(data.is_live_dynamic || Boolean(userCoords));
    } catch (err) {
      console.error("Error loading hospitals:", err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Applies given coordinates and sets a human-readable location label
   */
  const applyCoordinates = async (coords, explicitLabel = null) => {
    setUserCoords(coords);
    let resolvedLabel = explicitLabel;

    if (!resolvedLabel) {
      try {
        const rev = await api.reverseGeocode(coords.lat, coords.lon);
        if (rev?.success && rev.formatted_address) {
          resolvedLabel = rev.formatted_address;
        } else {
          resolvedLabel = `${coords.lat.toFixed(4)}° N, ${coords.lon.toFixed(4)}° E`;
        }
      } catch {
        resolvedLabel = `${coords.lat.toFixed(4)}° N, ${coords.lon.toFixed(4)}° E`;
      }
    }

    setLocationLabel(resolvedLabel);

    loadHospitals({
      city: activeCityTab,
      emergency: emergencyOnly,
      userLat: coords.lat,
      userLon: coords.lon
    });
  };

  /**
   * Fallback to IP-based location if browser GPS fails or permission is denied
   */
  const fallbackToIPLocation = async () => {
    try {
      const ipData = await api.getMyLocation();
      if (ipData?.success && ipData.lat && ipData.lon) {
        const label = ipData.formatted_address || `${ipData.city || "Vadodara"}, ${ipData.state || "Gujarat"}`;
        await applyCoordinates({
          lat: ipData.lat,
          lon: ipData.lon,
          source: "ip"
        }, label);
        return true;
      }
    } catch (err) {
      console.warn("IP location fallback failed:", err);
    }

    // Default fallback to first city in case no coordinates obtained
    loadHospitals({
      city: activeCityTab,
      emergency: emergencyOnly,
      userLat: null,
      userLon: null
    });
    return false;
  };

  /**
   * High-accuracy GPS detection
   */
  const handleDetectLocation = () => {
    if (!navigator.geolocation) {
      setGpsError("Browser GPS not supported. Detected location via network instead.");
      fallbackToIPLocation();
      return;
    }

    setLocatingGPS(true);
    setGpsError(null);

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const coords = {
          lat: pos.coords.latitude,
          lon: pos.coords.longitude,
          accuracy: Math.round(pos.coords.accuracy),
          source: "gps"
        };
        setLocatingGPS(false);
        setActiveCityTab("All");
        setCityFilter("");
        await applyCoordinates(coords);
      },
      async (err) => {
        console.warn("Browser GPS prompt error:", err.message);
        setLocatingGPS(false);
        setGpsError("Browser GPS was unavailable or blocked. Auto-detected approximate location via network.");
        await fallbackToIPLocation();
      },
      { enableHighAccuracy: true, timeout: 8000, maximumAge: 60000 }
    );
  };

  /**
   * Manual custom location search
   */
  const handleSetCustomLocation = async (e) => {
    if (e) e.preventDefault();
    const q = customLocationText.trim();
    if (!q) return;

    setIsGeocodingLocation(true);
    setGpsError(null);

    try {
      const res = await api.geocodeLocation(q);
      if (res?.success && res.lat && res.lon) {
        const coords = {
          lat: res.lat,
          lon: res.lon,
          source: "custom"
        };
        const label = res.formatted_address || res.city || q;
        setActiveCityTab("All");
        setCityFilter("");
        await applyCoordinates(coords, label);
        setShowLocationInput(false);
        setCustomLocationText("");
      } else {
        setGpsError(`Could not pinpoint "${q}". Please enter a recognized city name, area, or PIN code.`);
      }
    } catch (err) {
      setGpsError(`Location search failed: ${err.message}`);
    } finally {
      setIsGeocodingLocation(false);
    }
  };

  // Attempt initial GPS discovery or fall back to IP location on mount
  useEffect(() => {
    let isMounted = true;

    const init = async () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          async (pos) => {
            if (!isMounted) return;
            const coords = {
              lat: pos.coords.latitude,
              lon: pos.coords.longitude,
              accuracy: Math.round(pos.coords.accuracy),
              source: "gps"
            };
            await applyCoordinates(coords);
          },
          async (err) => {
            if (!isMounted) return;
            console.log("Initial GPS prompt note:", err.message);
            await fallbackToIPLocation();
          },
          { enableHighAccuracy: true, timeout: 7000, maximumAge: 60000 }
        );
      } else {
        await fallbackToIPLocation();
      }
    };

    init();

    return () => {
      isMounted = false;
    };
  }, []);

  // Reload when emergency filter changes
  useEffect(() => {
    loadHospitals({
      city: activeCityTab,
      emergency: emergencyOnly,
      userLat: userCoords?.lat || null,
      userLon: userCoords?.lon || null
    });
  }, [emergencyOnly]);

  const handleCityTabClick = async (city) => {
    setActiveCityTab(city);
    setCityFilter(city === "All" ? "" : city);

    if (city === "All") {
      // Re-center around user's active coordinates if known, else live detect
      if (userCoords?.lat && userCoords?.lon) {
        loadHospitals({
          city: "All",
          emergency: emergencyOnly,
          userLat: userCoords.lat,
          userLon: userCoords.lon
        });
      } else {
        handleDetectLocation();
      }
      return;
    }

    // If an Indian city chip was chosen, center coordinates on that city
    const cityInfo = INDIAN_CITY_COORDINATES[city];
    if (cityInfo) {
      const coords = {
        lat: cityInfo.lat,
        lon: cityInfo.lon,
        source: "city_chip"
      };
      const label = `${city}, ${cityInfo.state}`;
      setUserCoords(coords);
      setLocationLabel(label);
      loadHospitals({
        city: city,
        emergency: emergencyOnly,
        userLat: cityInfo.lat,
        userLon: cityInfo.lon
      });
    } else {
      loadHospitals({
        city: city,
        emergency: emergencyOnly,
        userLat: userCoords?.lat || null,
        userLon: userCoords?.lon || null
      });
    }
  };

  const handleClearLocation = () => {
    setUserCoords(null);
    setLocationLabel(null);
    setGpsError(null);
    setActiveCityTab("All");
    setCityFilter("");
    loadHospitals({
      city: "All",
      emergency: emergencyOnly,
      userLat: null,
      userLon: null
    });
  };

  // Generate turn-by-turn navigation URL starting from user's current coordinates
  const getNavigationUrl = (hosp) => {
    if (!hosp) return "#";
    if (userCoords?.lat && userCoords?.lon && hosp.latitude && hosp.longitude) {
      return `https://www.google.com/maps/dir/?api=1&origin=${userCoords.lat},${userCoords.lon}&destination=${hosp.latitude},${hosp.longitude}`;
    }
    return hosp.maps_url || `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent((hosp.name || "") + ", " + (hosp.city || "India"))}`;
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
                Real-time geospatial proximity triage, 24/7 cardiac emergency centers, live distance calculations, and turn-by-turn navigation across India.
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
                <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap", marginBottom: "4px" }}>
                  <h3 style={{ margin: 0, fontSize: "17px", fontWeight: "700" }}>
                    {locationLabel ? `📍 Current Location: ${locationLabel}` : "Find Cardiac Centers Near Your Location"}
                  </h3>
                  {userCoords && (
                    <span
                      style={{
                        fontSize: "11px",
                        fontWeight: "700",
                        padding: "2px 8px",
                        borderRadius: "12px",
                        background: userCoords.source === "gps" ? "rgba(16, 185, 129, 0.2)" : userCoords.source === "ip" ? "rgba(14, 165, 233, 0.2)" : "rgba(245, 158, 11, 0.2)",
                        color: userCoords.source === "gps" ? "#34d399" : userCoords.source === "ip" ? "#38bdf8" : "#fbbf24",
                        border: `1px solid ${userCoords.source === "gps" ? "rgba(16, 185, 129, 0.4)" : userCoords.source === "ip" ? "rgba(14, 165, 233, 0.4)" : "rgba(245, 158, 11, 0.4)"}`
                      }}
                    >
                      {userCoords.source === "gps" ? "⚡ Live GPS" : userCoords.source === "ip" ? "🌐 Network / IP" : userCoords.source === "city_chip" ? "🏙️ Selected City" : "📌 Custom Location"}
                    </span>
                  )}
                </div>
                <p style={{ margin: 0, fontSize: "13px", color: "#94a3b8" }}>
                  {userCoords
                    ? `Coordinates: ${userCoords.lat.toFixed(4)}° N, ${userCoords.lon.toFixed(4)}° E • Live distances calculated & closest cardiac centers ranked first.`
                    : "Detect your live GPS or search any city to calculate transit ETA, drive distance, and find the closest 24/7 cardiac emergency room."}
                </p>
              </div>
            </div>

            <div className="gps-actions-right">
              {userCoords ? (
                <>
                  <button
                    type="button"
                    onClick={() => setShowLocationInput(!showLocationInput)}
                    title="Change location or search custom city/area"
                    style={{
                      background: "rgba(255, 255, 255, 0.12)",
                      color: "#ffffff",
                      border: "1px solid rgba(255, 255, 255, 0.25)",
                      padding: "8px 14px",
                      borderRadius: "8px",
                      fontSize: "13px",
                      fontWeight: "600",
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: "6px",
                      transition: "all 0.15s"
                    }}
                  >
                    <Edit2 size={13} />
                    <span>{showLocationInput ? "Close" : "Change Location"}</span>
                  </button>

                  <button
                    type="button"
                    onClick={handleDetectLocation}
                    disabled={locatingGPS}
                    title="Refresh high-accuracy GPS coordinates"
                    style={{
                      background: "rgba(14, 165, 233, 0.2)",
                      color: "#38bdf8",
                      border: "1px solid rgba(14, 165, 233, 0.4)",
                      padding: "8px 14px",
                      borderRadius: "8px",
                      fontSize: "13px",
                      fontWeight: "600",
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: "6px"
                    }}
                  >
                    <Crosshair size={14} className={locatingGPS ? "spin-pulse" : ""} />
                    <span>{locatingGPS ? "Locating..." : "Use Live GPS"}</span>
                  </button>

                  <button type="button" className="gps-clear-btn" onClick={handleClearLocation}>
                    Reset
                  </button>
                </>
              ) : (
                <>
                  <button
                    type="button"
                    className="gps-detect-btn"
                    onClick={handleDetectLocation}
                    disabled={locatingGPS}
                  >
                    <Crosshair size={18} className={locatingGPS ? "spin-pulse" : ""} />
                    <span>{locatingGPS ? "Acquiring Coordinates..." : "📍 Find Near Me (Detect GPS)"}</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setShowLocationInput(!showLocationInput)}
                    style={{
                      background: "rgba(255, 255, 255, 0.12)",
                      color: "#ffffff",
                      border: "1px solid rgba(255, 255, 255, 0.25)",
                      padding: "10px 16px",
                      borderRadius: "10px",
                      fontSize: "13px",
                      fontWeight: "600",
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: "6px"
                    }}
                  >
                    <MapPin size={15} />
                    <span>Enter City / Area</span>
                  </button>
                </>
              )}
            </div>
          </div>

          {/* INLINE LOCATION SEARCH & PINPOINT FORM */}
          {showLocationInput && (
            <form
              onSubmit={handleSetCustomLocation}
              style={{
                background: "#ffffff",
                border: "1.5px solid #0284c7",
                borderRadius: "14px",
                padding: "14px 18px",
                marginBottom: "20px",
                display: "flex",
                alignItems: "center",
                gap: "12px",
                boxShadow: "0 6px 20px rgba(2, 132, 199, 0.12)",
                animation: "fadeIn 0.2s ease"
              }}
            >
              <MapPin size={20} className="text-primary" style={{ flexShrink: 0 }} />
              <input
                type="text"
                placeholder="Type your city, locality, landmark, or PIN code (e.g. Vadodara, Alkapuri, Hyderabad, Banjara Hills, 500034)..."
                value={customLocationText}
                onChange={(e) => setCustomLocationText(e.target.value)}
                style={{
                  flex: 1,
                  border: "none",
                  outline: "none",
                  fontSize: "14px",
                  color: "#0f172a",
                  background: "transparent"
                }}
                autoFocus
              />
              <button
                type="submit"
                disabled={isGeocodingLocation || !customLocationText.trim()}
                style={{
                  background: "linear-gradient(135deg, #0284c7, #0369a1)",
                  color: "white",
                  border: "none",
                  padding: "9px 20px",
                  borderRadius: "8px",
                  fontSize: "13px",
                  fontWeight: "700",
                  cursor: isGeocodingLocation || !customLocationText.trim() ? "not-allowed" : "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "6px",
                  boxShadow: "0 2px 8px rgba(2, 132, 199, 0.3)"
                }}
              >
                <Search size={14} />
                <span>{isGeocodingLocation ? "Pinpointing..." : "Set Location"}</span>
              </button>
              <button
                type="button"
                onClick={() => setShowLocationInput(false)}
                style={{
                  background: "transparent",
                  border: "none",
                  color: "#64748b",
                  cursor: "pointer",
                  fontSize: "14px",
                  padding: "4px"
                }}
              >
                ✕
              </button>
            </form>
          )}

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
                <AlertCircle size={18} style={{ flexShrink: 0 }} />
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
                  {userCoords ? `⚡ CLOSEST EMERGENCY CARDIAC CENTER ${locationLabel ? `TO ${locationLabel.toUpperCase()}` : ""}` : "⭐ TOP-RATED CARDIOLOGY INSTITUTE"}
                </span>
                <h2 className="nearest-er-title">{nearestHospital.name}</h2>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#475569", fontSize: "14px", margin: "4px 0" }}>
                  <MapPin size={16} className="text-rose" style={{ flexShrink: 0 }} />
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
                  href={getNavigationUrl(nearestHospital)}
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
                placeholder="Search AIIMS, Fortis, Bankers, Apollo, city or specialty..."
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

          {/* PROXIMITY RADAR STRIP - Rendered when coordinates are active */}
          {userCoords && hospitals.length > 0 && (
            <div className="proximity-radar-card">
              <div className="radar-header">
                <h3>
                  <Compass size={16} style={{ display: "inline", verticalAlign: "middle", marginRight: "6px", color: "#0284c7" }} />
                  Proximity Radar ({hospitals.length} centers ranked by distance from {locationLabel || "you"})
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
                      href={getNavigationUrl(hosp)}
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
                {userCoords ? `Hospitals Near ${locationLabel || "Your Location"}` : activeCityTab !== "All" ? `Hospitals in ${activeCityTab}` : "Verified Cardiac Care Centers"}
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
                          {(hosp.specialties || []).map((s, idx) => (
                            <span key={idx} className="spec-tag">{s}</span>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className="hospital-footer">
                      <a
                        href={getNavigationUrl(hosp)}
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
