import uuid
import datetime
import urllib.parse
from typing import Optional, Annotated
from fastapi import APIRouter, Query, Request
from pydantic import BaseModel

from app.db.database import get_db
from app.services.live_hospitals import (
    calculate_haversine_distance,
    fetch_live_nearby_hospitals,
    geocode_city,
    geocode_location,
    reverse_geocode,
    fetch_ip_location
)

router = APIRouter()

class AppointmentBookingRequest(BaseModel):
    hospital_id: str
    patient_name: str
    contact_phone: str
    preferred_date: str
    reason_for_visit: Optional[str] = None
    notes: Optional[str] = None

@router.get("/my-location")
def get_current_location(request: Request):
    """
    Detects user's geographic location based on their client IP address.
    Provides instant location fallback when browser GPS is blocked, denied, or unavailable.
    """
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else None)
    return fetch_ip_location(client_ip=client_ip)

@router.get("/reverse-geocode")
def get_reverse_geocode(
    lat: Annotated[float, Query(description="Latitude")],
    lon: Annotated[float, Query(description="Longitude")]
):
    """
    Converts GPS latitude & longitude coordinates into a human-readable city, locality, and state.
    """
    return reverse_geocode(lat, lon)

@router.get("/geocode")
def search_location(
    query: Annotated[str, Query(description="City, area, locality, or PIN code")]
):
    """
    Geocodes a user-entered location query into exact GPS coordinates and city metadata.
    """
    res = geocode_location(query)
    if not res:
        return {"success": False, "message": f"Could not find coordinates for '{query}'"}
    return {"success": True, **res}

@router.get("")
def list_hospitals(
    city: Annotated[Optional[str], Query()] = None,
    emergency_only: Annotated[bool, Query()] = False,
    user_lat: Annotated[Optional[float], Query(description="User GPS Latitude")] = None,
    user_lon: Annotated[Optional[float], Query(description="User GPS Longitude")] = None,
    radius_km: Annotated[Optional[float], Query(description="Distance filter in km")] = None
):
    """
    Returns cardiology centers and emergency hospitals.
    1. If GPS coordinates are provided, queries live OpenStreetMap nearby nodes and merges verified database centers.
    2. If a specific city or hospital keyword is queried, searches live geocoding and database records.
    3. Seamlessly integrates hyper-local centers like Parul Sevashram Hospital right next to the user.
    """
    has_coords = (
        user_lat is not None and isinstance(user_lat, (int, float))
        and user_lon is not None and isinstance(user_lon, (int, float))
    )
    is_emergency = emergency_only is True
    effective_radius = radius_km if (radius_km is not None and isinstance(radius_km, (int, float)) and radius_km > 0) else 50.0
    clean_city = city.strip() if isinstance(city, str) and city.strip() and city.strip().lower() != "all" else None

    db = get_db()
    combined_hospitals = []
    seen_names = set()

    # 1. Fetch live geospatial hospitals if user GPS coordinates are provided
    if has_coords:
        live_results = fetch_live_nearby_hospitals(
            user_lat=user_lat,
            user_lon=user_lon,
            radius_km=effective_radius,
            emergency_only=is_emergency,
            query=clean_city
        )
        for h in live_results:
            norm = h["name"].lower().strip()
            if norm not in seen_names:
                seen_names.add(norm)
                combined_hospitals.append(h)

    # 2. If a specific city or hospital name is searched without GPS, try live geocoding & nearby query
    elif clean_city:
        geocoded = geocode_city(clean_city)
        if geocoded:
            city_live = fetch_live_nearby_hospitals(
                user_lat=geocoded["lat"],
                user_lon=geocoded["lon"],
                radius_km=effective_radius,
                emergency_only=is_emergency,
                query=clean_city
            )
            for h in city_live:
                norm = h["name"].lower().strip()
                if norm not in seen_names:
                    seen_names.add(norm)
                    combined_hospitals.append(h)

    # 3. Always merge matching verified cardiology centers stored in MongoDB
    db_query = {}
    if clean_city:
        term = clean_city
        db_query["$or"] = [
            {"city": {"$regex": term, "$options": "i"}},
            {"name": {"$regex": term, "$options": "i"}},
            {"address": {"$regex": term, "$options": "i"}},
            {"specialties": {"$regex": term, "$options": "i"}}
        ]

    if is_emergency:
        db_query["emergency_available"] = True

    db_rows = list(db.hospitals.find(db_query))
    for r in db_rows:
        h_name = r.get("name", "")
        norm = h_name.lower().strip()

        lat = r.get("latitude")
        lon = r.get("longitude")

        # Compute spherical distance via Haversine formula if user GPS available
        if has_coords and lat is not None and lon is not None:
            dist = calculate_haversine_distance(user_lat, user_lon, lat, lon)
            calculated_live = True
            eta_minutes = max(4, int(dist * 2.2))
            if not clean_city and radius_km is not None and isinstance(radius_km, (int, float)) and dist > radius_km:
                continue
            if not clean_city and dist > effective_radius:
                continue
        else:
            dist = None
            calculated_live = False
            eta_minutes = None

        if lat and lon:
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
        else:
            dest_query = urllib.parse.quote(f"{r.get('name')}, {r.get('city')}")
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={dest_query}"

        specialties_raw = r.get("specialties")
        if isinstance(specialties_raw, str):
            specialties_list = [s.strip() for s in specialties_raw.split(",") if s.strip()]
        elif isinstance(specialties_raw, list):
            specialties_list = specialties_raw
        else:
            specialties_list = []

        db_hosp = {
            "id": r.get("id"),
            "name": h_name,
            "city": r.get("city"),
            "address": r.get("address"),
            "phone": r.get("phone"),
            "rating": r.get("rating", 4.8),
            "review_count": r.get("review_count", 120),
            "emergency_available": bool(r.get("emergency_available")),
            "specialties": specialties_list,
            "distance_km": dist,
            "eta_minutes": eta_minutes,
            "latitude": lat,
            "longitude": lon,
            "is_live_dynamic": calculated_live,
            "data_source": "Verified Indian Cardiology Network",
            "maps_url": maps_url
        }

        # If already in combined_hospitals from OSM, upgrade it with verified DB details
        matched_idx = next((i for i, ch in enumerate(combined_hospitals) if norm in ch["name"].lower() or ch["name"].lower() in norm), None)
        if matched_idx is not None:
            if dist is not None:
                matched_dist = combined_hospitals[matched_idx].get("distance_km")
                db_hosp["distance_km"] = min(dist, matched_dist) if matched_dist is not None else dist
            combined_hospitals[matched_idx] = db_hosp
        else:
            seen_names.add(norm)
            combined_hospitals.append(db_hosp)

    # Sort all hospitals ascending by distance if coordinates are available, then by rating
    if has_coords:
        combined_hospitals.sort(
            key=lambda h: (
                h["distance_km"] is None,
                h["distance_km"] if h["distance_km"] is not None else 999999,
                -h.get("rating", 0)
            )
        )
    else:
        combined_hospitals.sort(key=lambda h: (-h.get("rating", 0), h.get("name", "")))

    return {
        "count": len(combined_hospitals),
        "is_live_dynamic": has_coords or bool(clean_city),
        "data_source": "Live OpenStreetMap & Verified Cardiology Network" if has_coords else "Verified Indian Cardiology Centers",
        "user_location": {"lat": user_lat, "lon": user_lon} if has_coords else None,
        "hospitals": combined_hospitals
    }

@router.post("/book")
def book_consultation(req: AppointmentBookingRequest):
    """
    Saves a cardiology consultation appointment request in MongoDB.
    """
    db = get_db()
    booking_id = f"APPT-{uuid.uuid4().hex[:8].upper()}"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    booking_doc = {
        "booking_id": booking_id,
        "hospital_id": req.hospital_id,
        "patient_name": req.patient_name,
        "contact_phone": req.contact_phone,
        "preferred_date": req.preferred_date,
        "reason_for_visit": req.reason_for_visit or req.notes or "Cardiology Consultation",
        "created_at": now_str,
        "status": "confirmed"
    }

    db.appointments.insert_one(booking_doc)

    return {
        "status": "success",
        "message": "Cardiology consultation appointment booked successfully!",
        "booking_id": booking_id,
        "booking": {
            "booking_id": booking_id,
            "hospital_id": req.hospital_id,
            "patient_name": req.patient_name,
            "preferred_date": req.preferred_date,
            "status": "confirmed"
        }
    }
