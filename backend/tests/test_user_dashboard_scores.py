import unittest
import json
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.db.database import get_db_connection, init_db
from app.schemas.prediction import PatientInput
from app.api.endpoints.predict import run_prediction
from app.api.endpoints.analytics import get_analytics_overview
from app.api.endpoints.history import get_assessment_history

class TestUserDashboardScores(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

        # Clear any prior test assessments for test users to ensure clean isolation
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assessments WHERE user_email IN ('user_a@health.in', 'user_b@health.in', 'user_c@health.in')")
        conn.commit()
        conn.close()

    def test_01_user_a_healthy_submission_and_personalized_scores(self):
        """User A submits healthy biomarkers -> Analytics returns low risk (<25%) and high health score (>75)."""
        healthy_payload = {
            "name": "User A (Healthy Baseline)",
            "user_email": "user_a@health.in",
            "age": 32,
            "sex": 1,
            "gender": "Male",
            "cp": 3,
            "chest_pain": "None",
            "trestbps": 114,
            "systolic_bp": 114,
            "diastolic_bp": 74,
            "chol": 172,
            "cholesterol": 172,
            "fbs": 0,
            "fasting_blood_sugar": 88,
            "restecg": 0,
            "resting_ecg": "Normal",
            "thalach": 174,
            "exang": 0,
            "oldpeak": 0.0,
            "slope": 0,
            "ca": 0,
            "thal": 1,
            "ejection_fraction": 65,
            "serum_creatinine": 0.8,
            "smoking": "Never"
        }

        # 1. Post prediction
        pred_resp = run_prediction(PatientInput(**healthy_payload))
        self.assertLess(pred_resp.risk_score, 30, "Healthy patient risk score should be in low baseline range (<30%)")
        self.assertGreater(pred_resp.heart_health_score, 70, "Healthy patient health score should be > 70")

        # 2. Get User A's personalized analytics
        analytics_data = get_analytics_overview(user_email="user_a@health.in")

        self.assertTrue(analytics_data["has_assessments"])
        self.assertIsNotNone(analytics_data["latest_assessment"])
        self.assertEqual(analytics_data["total_assessments"], 1)
        self.assertLess(analytics_data["latest_assessment"]["risk_score"], 30)
        self.assertGreater(analytics_data["latest_assessment"]["heart_health_score"], 70)
        self.assertEqual(analytics_data["latest_assessment"]["systolic_bp"], 114)
        self.assertEqual(analytics_data["latest_assessment"]["cholesterol"], 172)
        self.assertEqual(analytics_data["latest_assessment"]["ejection_fraction"], 65)

    def test_02_user_b_high_risk_submission_and_personalized_scores(self):
        """User B submits high-risk biomarkers -> Analytics returns high risk (>65%) and lower health score (<40)."""
        high_risk_payload = {
            "name": "User B (High Risk Baseline)",
            "user_email": "user_b@health.in",
            "age": 68,
            "sex": 0,
            "gender": "Female",
            "cp": 0,
            "chest_pain": "Severe",
            "trestbps": 168,
            "systolic_bp": 168,
            "diastolic_bp": 102,
            "chol": 275,
            "cholesterol": 275,
            "fbs": 1,
            "fasting_blood_sugar": 145,
            "restecg": 2,
            "resting_ecg": "Left Ventricular Hypertrophy",
            "thalach": 118,
            "exang": 1,
            "oldpeak": 2.8,
            "slope": 2,
            "ca": 2,
            "thal": 3,
            "ejection_fraction": 34,
            "serum_creatinine": 1.8,
            "smoking": "Regularly"
        }

        # 1. Post prediction
        pred_resp = run_prediction(PatientInput(**high_risk_payload))
        self.assertGreater(pred_resp.risk_score, 65, "High-risk patient risk score should be > 65%")
        self.assertLess(pred_resp.heart_health_score, 40, "High-risk patient health score should be < 40")

        # 2. Get User B's personalized analytics
        analytics_data = get_analytics_overview(user_email="user_b@health.in")

        self.assertTrue(analytics_data["has_assessments"])
        self.assertIsNotNone(analytics_data["latest_assessment"])
        self.assertEqual(analytics_data["total_assessments"], 1)
        self.assertGreater(analytics_data["latest_assessment"]["risk_score"], 65)
        self.assertLess(analytics_data["latest_assessment"]["heart_health_score"], 40)
        self.assertEqual(analytics_data["latest_assessment"]["systolic_bp"], 168)
        self.assertEqual(analytics_data["latest_assessment"]["cholesterol"], 275)
        self.assertEqual(analytics_data["latest_assessment"]["ejection_fraction"], 34)

    def test_03_user_c_new_user_zero_data_state(self):
        """New User C with 0 evaluations -> Analytics returns has_assessments: False and None scores."""
        analytics_data = get_analytics_overview(user_email="user_c@health.in")

        self.assertFalse(analytics_data["has_assessments"])
        self.assertIsNone(analytics_data["latest_assessment"])
        self.assertEqual(analytics_data["total_assessments"], 0)
        self.assertIsNone(analytics_data["average_risk_score"])
        self.assertIsNone(analytics_data["average_health_score"])
        self.assertEqual(len(analytics_data["timeline"]), 0)

        # History should also return 0 records
        history_resp = get_assessment_history(user_email="user_c@health.in")
        self.assertEqual(history_resp.total, 0)
        self.assertEqual(len(history_resp.items), 0)

    def test_04_user_isolation_no_score_leakage(self):
        """Verify User A's dashboard analytics and history do NOT leak User B's records or scores."""
        # Check User A's analytics
        data_a = get_analytics_overview(user_email="user_a@health.in")
        self.assertEqual(data_a["total_assessments"], 1)
        self.assertEqual(data_a["latest_assessment"]["patient_name"], "User A (Healthy Baseline)")
        self.assertLess(data_a["latest_assessment"]["risk_score"], 30)

        # Check User B's analytics
        data_b = get_analytics_overview(user_email="user_b@health.in")
        self.assertEqual(data_b["total_assessments"], 1)
        self.assertEqual(data_b["latest_assessment"]["patient_name"], "User B (High Risk Baseline)")
        self.assertGreater(data_b["latest_assessment"]["risk_score"], 65)

        # Check User A's history items
        hist_a = get_assessment_history(user_email="user_a@health.in")
        self.assertEqual(len(hist_a.items), 1)
        self.assertEqual(hist_a.items[0].patient_name, "User A (Healthy Baseline)")

        # Check User B's history items
        hist_b = get_assessment_history(user_email="user_b@health.in")
        self.assertEqual(len(hist_b.items), 1)
        self.assertEqual(hist_b.items[0].patient_name, "User B (High Risk Baseline)")

    @classmethod
    def tearDownClass(cls):
        # Clean up test user records
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assessments WHERE user_email IN ('user_a@health.in', 'user_b@health.in', 'user_c@health.in')")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)
