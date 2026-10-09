/**
 * Geographic calculation and formatting utilities for HeartCare Hospital Finder
 */

/**
 * Calculates geodetic distance in kilometers between two GPS coordinates using the Haversine formula.
 * @param {number} lat1 - Latitude of point 1 in degrees
 * @param {number} lon1 - Longitude of point 1 in degrees
 * @param {number} lat2 - Latitude of point 2 in degrees
 * @param {number} lon2 - Longitude of point 2 in degrees
 * @returns {number} Distance in kilometers
 */
export function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
  if (
    lat1 === null || lat1 === undefined ||
    lon1 === null || lon1 === undefined ||
    lat2 === null || lat2 === undefined ||
    lon2 === null || lon2 === undefined ||
    isNaN(lat1) || isNaN(lon1) || isNaN(lat2) || isNaN(lon2)
  ) {
    return null;
  }

  const R = 6371.0; // Earth's mean radius in km
  const toRad = (deg) => (deg * Math.PI) / 180.0;

  const phi1 = toRad(lat1);
  const phi2 = toRad(lat2);
  const deltaPhi = toRad(lat2 - lat1);
  const deltaLambda = toRad(lon2 - lon1);

  const a =
    Math.sin(deltaPhi / 2.0) ** 2 +
    Math.cos(phi1) * Math.cos(phi2) * (Math.sin(deltaLambda / 2.0) ** 2);
  
  const c = 2.0 * Math.atan2(Math.sqrt(a), Math.sqrt(1.0 - a));
  const dist = R * c;
  return Math.round(dist * 10) / 10;
}

/**
 * Formats a distance in kilometers into a human-readable string.
 * e.g., "2.4 km away", "156 km away", "1,520 km away".
 * Returns null if distance is invalid.
 * @param {number|null} distKm - Distance in km
 * @returns {string|null}
 */
export function formatDistance(distKm) {
  if (distKm === null || distKm === undefined || isNaN(distKm)) {
    return null;
  }

  const num = Number(distKm);
  if (num < 0) return null;

  if (num < 1.0) {
    return `${num.toFixed(1)} km away`;
  }
  if (num < 100) {
    return `${num.toFixed(1)} km away`;
  }
  // Large inter-city / inter-state distances with comma separators
  return `${Math.round(num).toLocaleString()} km away`;
}

/**
 * Standard GPS coordinate reference points for major Indian metropolitan and tier-1/tier-2 healthcare hubs.
 */
export const INDIAN_CITY_COORDINATES = {
  "Vadodara": { lat: 22.3072, lon: 73.1812, state: "Gujarat" },
  "Ahmedabad": { lat: 23.0225, lon: 72.5714, state: "Gujarat" },
  "Mumbai": { lat: 19.0760, lon: 72.8777, state: "Maharashtra" },
  "New Delhi": { lat: 28.6139, lon: 77.2090, state: "Delhi" },
  "Bengaluru": { lat: 12.9716, lon: 77.5946, state: "Karnataka" },
  "Chennai": { lat: 13.0827, lon: 80.2707, state: "Tamil Nadu" },
  "Hyderabad": { lat: 17.3850, lon: 78.4867, state: "Telangana" },
  "Kolkata": { lat: 22.5726, lon: 88.3639, state: "West Bengal" },
  "Pune": { lat: 18.5204, lon: 73.8567, state: "Maharashtra" },
  "Chandigarh": { lat: 30.7333, lon: 76.7794, state: "Punjab/Haryana" },
  "Thiruvananthapuram": { lat: 8.5241, lon: 76.9366, state: "Kerala" },
  "Jaipur": { lat: 26.9124, lon: 75.7873, state: "Rajasthan" },
  "Lucknow": { lat: 26.8467, lon: 80.9462, state: "Uttar Pradesh" },
  "Bhubaneswar": { lat: 20.2961, lon: 85.8245, state: "Odisha" }
};

