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
