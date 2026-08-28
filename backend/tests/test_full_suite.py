import unittest
import json
import urllib.request
import urllib.error
import numpy as np
import pandas as pd
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000/api"

class TestFullPlatformIntegration(unittest.TestCase):

    def _post(self, endpoint, data):
        req = urllib.request.Request(
            f"{BASE_URL}{endpoint}",
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8")), resp.getcode()

    def _get(self, endpoint):
        req = urllib.request.Request(f"{BASE_URL}{endpoint}")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8")), resp.getcode()

    def _delete(self, endpoint):
        req = urllib.request.Request(f"{BASE_URL}{endpoint}", method="DELETE")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8")), resp.getcode()

    # --------------------------------------------------------------------------
    # 1. HEALTH & SYSTEM DIAGNOSTICS
    # --------------------------------------------------------------------------
    def test_01_backend_health_and_model_status(self):
        """Verify API health, SQLite connectivity, and LightGBM model status."""
        data, code = self._get("/health")
        self.assertEqual(code, 200)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")
        self.assertTrue(data["custom_model_loaded"], "Uploaded custom model should be active!")

    # --------------------------------------------------------------------------
    # 2. ML INFERENCE WITH 13 CLEVELAND FEATURES
    # --------------------------------------------------------------------------
    def test_02_predict_high_risk_patient(self):
        """Verify LightGBM inference on a high-risk cardiac patient."""
        payload = {
            "name": "Sunita Deshmukh (Integration Test)",
            "age": 68,
            "sex": 0,
            "gender": "Female",
            "cp": 0, # Typical Angina
            "trestbps": 168,
            "chol": 275,
            "fbs": 1,
            "restecg": 2,
            "thalach": 118,
            "exang": 1,
            "oldpeak": 2.8,
            "slope": 2,
            "ca": 2,
            "thal": 3,
            "ejection_fraction": 32,
            "serum_creatinine": 2.1,
            "smoking": "Regularly"
        }
        data, code = self._post("/predict", payload)
        self.assertEqual(code, 200)
        self.assertIn("PRED-", data["prediction_id"])
        self.assertGreater(data["risk_score"], 60, "Expected high risk score for Stage 2-4 profile")
        self.assertIn("LightGBM", data["model_source"])
        self.assertGreater(len(data["top_risk_factors"]), 0)
        self.assertGreater(len(data["recommendations"]), 0)
        self.__class__.created_prediction_id = data["prediction_id"]

    def test_03_predict_low_risk_athlete(self):
        """Verify LightGBM inference on a low-risk athlete."""
        payload = {
            "name": "Aarav Sharma (Integration Test)",
            "age": 30,
            "sex": 1,
            "gender": "Male",
            "cp": 3, # Asymptomatic
            "trestbps": 112,
            "chol": 168,
            "fbs": 0,
            "restecg": 0,
            "thalach": 178,
            "exang": 0,
            "oldpeak": 0.0,
            "slope": 0,
            "ca": 0,
            "thal": 1,
            "ejection_fraction": 65,
            "serum_creatinine": 0.8,
            "smoking": "Never"
        }
        data, code = self._post("/predict", payload)
        self.assertEqual(code, 200)
        self.assertLess(data["risk_score"], 35, "Expected low risk score for healthy athlete")
        self.assertGreater(data["heart_health_score"], 65)

    # --------------------------------------------------------------------------
    # 3. WHAT-IF REAL-TIME SIMULATOR
    # --------------------------------------------------------------------------
    def test_04_what_if_simulation(self):
        """Verify dynamic what-if biomarker delta calculations."""
        payload = {
            "base_input": {
                "name": "Robert Chen",
                "age": 56,
                "sex": 1,
                "cp": 1,
                "trestbps": 155,
                "chol": 240,
                "fbs": 0,
                "restecg": 1,
                "thalach": 140,
                "exang": 1,
                "oldpeak": 1.6,
                "slope": 1,
                "ca": 1,
                "thal": 2,
                "smoking": "Regularly"
            },
            "modified_params": {
                "systolic_bp": 120,
                "cholesterol": 180,
                "smoking": "Never",
                "exercise_days": "4-5 days"
            }
        }
        data, code = self._post("/simulate", payload)
        self.assertEqual(code, 200)
        self.assertIn("baseline", data)
        self.assertIn("simulated", data)
        self.assertIn("delta", data)
        self.assertIn("risk_score_diff", data["delta"])

    # --------------------------------------------------------------------------
    # 4. HISTORY, PERSISTENCE & DYNAMIC COHORTS
    # --------------------------------------------------------------------------
    def test_05_history_retrieval_and_search(self):
        """Verify SQLite history querying and search filtering."""
        data, code = self._get("/history?limit=10")
        self.assertEqual(code, 200)
        self.assertIsInstance(data["items"], list)
        self.assertGreater(data["total"], 0)

    def test_06_dynamic_cohort_generation(self):
        """Verify bulk dynamic patient simulation into SQLite DB."""
        data, code = self._post("/history/generate-dynamic?count=3", {})
        self.assertEqual(code, 200)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["generated"]), 3)

    def test_07_analytics_aggregation(self):
        """Verify population cohort distribution and timeline analytics."""
        data, code = self._get("/analytics")
        self.assertEqual(code, 200)
        self.assertIn("total_assessments", data)
        self.assertIn("average_risk_score", data)
        self.assertIn("risk_distribution", data)
        self.assertIn("Low Risk", data["risk_distribution"])

    # --------------------------------------------------------------------------
    # 5. HOSPITALS & REPORTS
    # --------------------------------------------------------------------------
    def test_08_hospitals_directory_and_booking(self):
        """Verify hospital listing and appointment booking."""
        hosp_data, code = self._get("/hospitals")
        self.assertEqual(code, 200)
        self.assertGreater(hosp_data["count"], 0)

        # Test booking
        booking_payload = {
            "hospital_id": hosp_data["hospitals"][0]["id"],
            "patient_name": "Integration Test Patient",
            "contact_phone": "+1 555-0199",
            "preferred_date": "2026-09-01",
            "reason_for_visit": "Cardiology evaluation and echo"
        }
        book_resp, b_code = self._post("/hospitals/book", booking_payload)
        self.assertEqual(b_code, 200)
        self.assertEqual(book_resp["status"], "success")
        self.assertIn("APPT-", book_resp["booking_id"])

    def test_09_medical_report_generation(self):
        """Verify formatted medical report generation for letterhead."""
        pred_id = getattr(self.__class__, "created_prediction_id", None)
        if pred_id:
            report_data, code = self._get(f"/reports/{pred_id}")
            self.assertEqual(code, 200)
            self.assertEqual(report_data["report_id"], f"REP-{pred_id}")
            self.assertIn("clinical_summary", report_data)
            self.assertIn("full_analysis", report_data)

    def test_10_cleanup_created_record(self):
        """Verify record deletion."""
        pred_id = getattr(self.__class__, "created_prediction_id", None)
        if pred_id:
            del_resp, code = self._delete(f"/history/{pred_id}")
            self.assertEqual(code, 200)
            self.assertEqual(del_resp["id"], pred_id)

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFullPlatformIntegration)
    result = runner.run(suite)
    if not result.wasSuccessful():
        exit(1)
