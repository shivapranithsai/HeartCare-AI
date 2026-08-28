import math
import uuid
import datetime
import urllib.parse
from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel
from app.db.database import get_db

router = APIRouter()

from app.services.live_hospitals import (
    calculate_haversine_distance,
    fetch_live_nearby_hospitals,
    geocode_city
)

class AppointmentBookingRequest(BaseModel):
    hospital_id: str
    patient_name: str
    contact_phone: str
    preferred_date: str
    reason_for_visit: Optional[str] = None
    notes: Optional[str] = None

@router.get("")
def list_hospitals(
    city: Optional[str] = Query(default=None),
    emergency_only: bool = Query(default=False),
    user_lat: Optional[float] = Query(default=None, description="User live GPS Latitude"),
    user_lon: Optional[float] = Query(default=None, description="User live GPS Longitude"),
    radius_km: Optional[float] = Query(default=None, description="Optional distance filter in km")
):
    # Clean input parameters
    city_val = city if isinstance(city, str) else None
    emergency_val = bool(emergency_only) if not hasattr(emergency_only, "default") else False
    user_lat_val = float(user_lat) if isinstance(user_lat, (int, float)) else None
    user_lon_val = float(user_lon) if isinstance(user_lon, (int, float)) else None
    radius_km_val = float(radius_km) if isinstance(radius_km, (int, float)) and radius_km > 0 else None

    has_user_coords = (user_lat_val is not None and user_lon_val is not None)

    # 1. If live user GPS coordinates are provided, dynamically fetch real-world hospitals
    if has_user_coords:
        live_results = fetch_live_nearby_hospitals(
            user_lat=user_lat_val,
            user_lon=user_lon_val,
            radius_km=radius_km_val or 50.0,
            emergency_only=emergency_val
        )
        if live_results and len(live_results) > 0:
            return {
                "count": len(live_results),
                "is_live_dynamic": True,
                "data_source": "Live OpenStreetMap Geospatial Network",
                "user_location": {"lat": user_lat_val, "lon": user_lon_val},
                "hospitals": live_results
            }

    # 2. If a specific city or area search is requested, attempt dynamic geocoding & live query
    if city_val and city_val.strip() and city_val.lower() != "all" and not has_user_coords:
        geocoded = geocode_city(city_val)
        if geocoded:
            city_live = fetch_live_nearby_hospitals(
                user_lat=geocoded["lat"],
                user_lon=geocoded["lon"],
                radius_km=radius_km_val or 50.0,
                emergency_only=emergency_val
            )
            if city_live and len(city_live) > 0:
                return {
                    "count": len(city_live),
                    "is_live_dynamic": True,
                    "data_source": "Live OpenStreetMap Geospatial Network",
                    "user_location": {"lat": geocoded["lat"], "lon": geocoded["lon"]},
                    "hospitals": city_live
                }

    # 3. Fallback: Query MongoDB hospital database
    db = get_db()
    query = {}

    if city_val and city_val.strip() and city_val.lower() != "all":
        term = city_val.strip()
        query["$or"] = [
            {"city": {"$regex": term, "$options": "i"}},
            {"name": {"$regex": term, "$options": "i"}},
            {"address": {"$regex": term, "$options": "i"}},
            {"specialties": {"$regex": term, "$options": "i"}}
        ]

    if emergency_val:
        query["emergency_available"] = True

    rows = list(db.hospitals.find(query))

    hospitals = []

    for r in rows:
        lat = r.get("latitude")
        lon = r.get("longitude")
        
        # Calculate real-time geodetic distance only if user GPS coordinates are provided
        if has_user_coords and lat is not None and lon is not None:
            dist = calculate_haversine_distance(user_lat_val, user_lon_val, lat, lon)
            calculated_live = True
            eta_minutes = max(4, int(dist * 2.2))
            if radius_km_val is not None and radius_km_val > 0 and dist > radius_km_val:
                continue
        else:
            dist = None
            calculated_live = False
            eta_minutes = None

        # Direct Google Maps Navigation URL
        if lat and lon:
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
        else:
            dest_query = urllib.parse.quote(f"{r.get('name')}, {r.get('city')}")
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={dest_query}"

        specialties_raw = r.get("specialties")
        specialties_list = [s.strip() for s in specialties_raw.split(",")] if isinstance(specialties_raw, str) and specialties_raw else specialties_raw if isinstance(specialties_raw, list) else []

        hospitals.append({
            "id": r.get("id"),
            "name": r.get("name"),
            "city": r.get("city"),
            "address": r.get("address"),
            "phone": r.get("phone"),
            "rating": r.get("rating"),
            "review_count": r.get("review_count"),
            "emergency_available": bool(r.get("emergency_available")),
            "specialties": specialties_list,
            "distance_km": dist,
            "eta_minutes": eta_minutes,
            "latitude": lat,
            "longitude": lon,
            "is_live_dynamic": calculated_live,
            "data_source": "Verified Cardiology Directory",
            "maps_url": maps_url
        })

    # Sort hospitals by distance ascending if user coordinates are provided, otherwise by rating
    if has_user_coords:
        hospitals.sort(key=lambda h: (h["distance_km"] if h["distance_km"] is not None else float("inf"), -h["rating"]))
    else:
        hospitals.sort(key=lambda h: (-h["rating"], h["name"]))

    return {
        "count": len(hospitals),
        "is_live_dynamic": has_user_coords,
        "data_source": "Verified Cardiology Directory",
        "user_location": {"lat": user_lat_val, "lon": user_lon_val} if has_user_coords else None,
        "hospitals": hospitals
    }

@router.post("/book")
def book_consultation(req: AppointmentBookingRequest):
    """
    Persists cardiology appointment consultations to MongoDB.
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
