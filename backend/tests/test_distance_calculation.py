import unittest
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.db.database import init_db, get_db_connection
from app.api.endpoints.hospitals import list_hospitals, calculate_haversine_distance

class TestHospitalDistanceCalculation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_haversine_formula_accuracy(self):
        """Test Haversine distance between well-known GPS points across India."""
        # Hyderabad (17.3850, 78.4867) to New Delhi (28.6139, 77.2090) ~ 1253 km
        dist_hyd_del = calculate_haversine_distance(17.3850, 78.4867, 28.6139, 77.2090)
        self.assertAlmostEqual(dist_hyd_del, 1253.0, delta=20.0)

        # Mumbai (19.0760, 72.8777) to Chennai (13.0827, 80.2707) ~ 1030 km
        dist_mum_chn = calculate_haversine_distance(19.0760, 72.8777, 13.0827, 80.2707)
        self.assertAlmostEqual(dist_mum_chn, 1030.0, delta=20.0)

        # Same point should be 0.0 km
        self.assertEqual(calculate_haversine_distance(28.5672, 77.2100, 28.5672, 77.2100), 0.0)

    def test_user_in_hyderabad_differentiates_cities(self):
        """
        Verify that a user in Hyderabad gets:
        - Local Hyderabad hospitals < 20 km
        - Bengaluru ~ 516 km
        - Mumbai ~ 625 km
        - Delhi ~ 1253 km
        - Thiruvananthapuram ~ 1000 km
        """
        user_lat, user_lon = 17.3850, 78.4867
        conn = get_db_connection()
        rows = conn.cursor().execute("SELECT name, city, latitude, longitude FROM hospitals").fetchall()
        conn.close()

        by_name = {r["name"]: calculate_haversine_distance(user_lat, user_lon, r["latitude"], r["longitude"]) for r in rows}

        # Hyderabad hospitals
        apollo_hyd = by_name.get("Apollo Health City")
        self.assertIsNotNone(apollo_hyd)
        self.assertLess(apollo_hyd, 15.0, "Apollo Hyderabad should be < 15 km from Hyderabad center")

        care_hyd = by_name.get("CARE Hospitals (Institute of Cardiac Sciences)")
        self.assertIsNotNone(care_hyd)
        self.assertLess(care_hyd, 10.0, "CARE Hyderabad should be < 10 km from Hyderabad center")

        # Mumbai hospital
        ahi_mumbai = by_name.get("Asian Heart Institute (AHI)")
        self.assertIsNotNone(ahi_mumbai)
        self.assertGreater(ahi_mumbai, 550.0, "Asian Heart Mumbai should be > 550 km from Hyderabad")
        self.assertLess(ahi_mumbai, 750.0, "Asian Heart Mumbai should be < 750 km from Hyderabad")

        # Delhi hospital
        aiims_delhi = by_name.get("All India Institute of Medical Sciences (AIIMS)")
        self.assertIsNotNone(aiims_delhi)
        self.assertGreater(aiims_delhi, 1150.0, "AIIMS Delhi should be > 1150 km from Hyderabad")
        self.assertLess(aiims_delhi, 1350.0, "AIIMS Delhi should be < 1350 km from Hyderabad")

        # Kerala hospital
        sctimst = by_name.get("Sree Chitra Tirunal Institute for Medical Sciences")
        self.assertIsNotNone(sctimst)
        self.assertGreater(sctimst, 900.0, "SCTIMST Kerala should be > 900 km from Hyderabad")
        self.assertLess(sctimst, 1100.0, "SCTIMST Kerala should be < 1100 km from Hyderabad")

    def test_user_in_delhi_differentiates_cities(self):
        """
        Verify that a user in Delhi gets:
        - Local Delhi hospitals < 15 km
        - Jaipur ~ 240 km
        - Mumbai ~ 1150 km
        - Thiruvananthapuram > 2200 km
        """
        user_lat, user_lon = 28.6139, 77.2090
        conn = get_db_connection()
        rows = conn.cursor().execute("SELECT name, city, latitude, longitude FROM hospitals").fetchall()
        conn.close()

        by_name = {r["name"]: calculate_haversine_distance(user_lat, user_lon, r["latitude"], r["longitude"]) for r in rows}

        aiims = by_name.get("All India Institute of Medical Sciences (AIIMS)")
        self.assertIsNotNone(aiims)
        self.assertLess(aiims, 15.0)

        ahi_mumbai = by_name.get("Asian Heart Institute (AHI)")
        self.assertIsNotNone(ahi_mumbai)
        self.assertGreater(ahi_mumbai, 1100.0, "Mumbai should be > 1100 km from Delhi")

        sctimst = by_name.get("Sree Chitra Tirunal Institute for Medical Sciences")
        self.assertIsNotNone(sctimst)
        self.assertGreater(sctimst, 2100.0, "Kerala should be > 2100 km from Delhi")

    def test_no_gps_coordinates_returns_none_distances(self):
        """
        When user coordinates are NOT passed, distance_km MUST be None and not fake numbers (1.8, 2.5, 4.0).
        """
        res = list_hospitals(user_lat=None, user_lon=None)
        self.assertIsNone(res["user_location"])
        self.assertFalse(res["is_live_dynamic"])

        for h in res["hospitals"]:
            self.assertIsNone(h["distance_km"], f"Expected None distance for {h['name']} without GPS, got {h['distance_km']}")
            self.assertIsNone(h["eta_minutes"])

    def test_hospital_coordinates_validity(self):
        """Verify all seeded hospitals have valid latitude and longitude within Indian bounds."""
        res = list_hospitals()
        for h in res["hospitals"]:
            lat = h["latitude"]
            lon = h["longitude"]
            self.assertIsNotNone(lat, f"Missing latitude for {h['name']}")
            self.assertIsNotNone(lon, f"Missing longitude for {h['name']}")
            self.assertTrue(8.0 <= lat <= 36.0, f"Invalid latitude {lat} for {h['name']}")
            self.assertTrue(68.0 <= lon <= 98.0, f"Invalid longitude {lon} for {h['name']}")

if __name__ == "__main__":
    unittest.main()
