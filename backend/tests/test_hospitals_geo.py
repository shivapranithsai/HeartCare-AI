import unittest
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.db.database import init_db
from app.api.endpoints.hospitals import list_hospitals, book_consultation, calculate_haversine_distance, AppointmentBookingRequest

class TestHospitalsGeoProximity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_haversine_distance(self):
        # AIIMS (28.5672, 77.2100) to Fortis Escorts (28.5606, 77.2796) ~ 6.8 km
        dist = calculate_haversine_distance(28.5672, 77.2100, 28.5606, 77.2796)
        self.assertAlmostEqual(dist, 6.8, delta=0.5)

    def test_find_hospitals_delhi_gps(self):
        # New Delhi user coordinates
        res = list_hospitals(user_lat=28.5672, user_lon=77.2100, radius_km=15)
        self.assertGreater(res["count"], 0)
        self.assertIsNotNone(res["user_location"])
        
        # Nearest hospital should have low km distance and direct Google Maps route
        nearest = res["hospitals"][0]
        self.assertLessEqual(nearest["distance_km"], 5.0)
        self.assertTrue(nearest["is_live_dynamic"])
        self.assertIn("google.com/maps", nearest["maps_url"])

    def test_find_hospitals_bengaluru_gps(self):
        # Bengaluru user coordinates
        res = list_hospitals(user_lat=12.9716, user_lon=77.5946, radius_km=30)
        self.assertGreater(res["count"], 0)
        
        # Check that distances are sorted ascending
        distances = [h["distance_km"] for h in res["hospitals"]]
        self.assertEqual(distances, sorted(distances))

    def test_radius_filter(self):
        # Narrow 5 km radius in Delhi
        res_5km = list_hospitals(user_lat=28.5672, user_lon=77.2100, radius_km=5)
        self.assertGreater(res_5km["count"], 0)
        for h in res_5km["hospitals"]:
            self.assertLessEqual(h["distance_km"], 5.0)

    def test_booking_appointment(self):
        req = AppointmentBookingRequest(
            hospital_id="IN-HOSP-01",
            patient_name="Shiva Clinical Test",
            contact_phone="+91 99999 88888",
            preferred_date="2026-09-05",
            notes="Routine cardiovascular health checkup"
        )
        res = book_consultation(req)
        self.assertEqual(res["status"], "success")
        self.assertIn("APPT-", res["booking_id"])

if __name__ == "__main__":
    unittest.main()
