import unittest
import sys
import uuid
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.db.database import get_db, init_db
from app.schemas.auth import UserRegister, UserLogin
from app.schemas.prediction import PatientInput, SimulationInput
from app.schemas.history import HistoryListResponse
from app.api.endpoints.auth import register_user, login_user
from app.api.endpoints.predict import run_prediction, run_what_if_simulation
from app.api.endpoints.history import get_assessment_history, generate_dynamic_history, get_assessment_by_id, delete_assessment
from app.api.endpoints.analytics import get_analytics_overview
from app.api.endpoints.hospitals import list_hospitals, book_consultation, AppointmentBookingRequest
from app.api.endpoints.reports import generate_clinical_report

class TestApiEndpointsDirect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.db = get_db()
        cls.test_email = f"test_user_{uuid.uuid4().hex[:6]}@cardio.ai"

    def test_01_auth_flow(self):
        """Test registration and login with MongoDB persistence."""
        reg_req = UserRegister(
            email=self.test_email,
            name="Dr. Direct Test",
            password="testPassword123!",
            role="Cardiologist / Physician"
        )
        reg_res = register_user(reg_req)
        self.assertEqual(reg_res.status, "success")
        self.assertEqual(reg_res.user.email, self.test_email)

        # Verify MongoDB document exists
        user_in_db = self.db.users.find_one({"email": self.test_email})
        self.assertIsNotNone(user_in_db)
        self.assertEqual(user_in_db["name"], "Dr. Direct Test")

        # Test login
        login_req = UserLogin(email=self.test_email, password="testPassword123!")
        login_res = login_user(login_req)
        self.assertEqual(login_res.status, "success")
        self.assertIsNotNone(login_res.access_token)

    def test_02_predict_and_persistence(self):
        """Test ML prediction and MongoDB persistence."""
        patient_data = PatientInput(
            name="Direct Test Patient",
            user_email=self.test_email,
            age=58,
            sex=1,
            gender="Male",
            cp=2,
            chest_pain="Moderate",
            trestbps=145,
            systolic_bp=145,
            diastolic_bp=90,
            chol=235,
            cholesterol=235,
            fbs=0,
            fasting_blood_sugar=95,
            restecg=1,
            thalach=135,
            exang=0,
            oldpeak=1.2,
            slope=1,
            ca=1,
            thal=2,
            ejection_fraction=48,
            serum_creatinine=1.2,
            smoking="Occasionally"
        )

        pred_res = run_prediction(patient_data)
        self.assertIsNotNone(pred_res.prediction_id)
        self.assertTrue(0 <= pred_res.risk_score <= 100)

        self.__class__.created_pred_id = pred_res.prediction_id

        # Verify persisted in MongoDB
        doc = self.db.assessments.find_one({"id": pred_res.prediction_id})
        self.assertIsNotNone(doc)
        self.assertEqual(doc["user_email"], self.test_email)
        self.assertEqual(doc["patient_name"], "Direct Test Patient")
        self.assertEqual(doc["systolic_bp"], 145)

    def test_03_what_if_simulation(self):
        """Test what-if simulation calculations."""
        base_input = PatientInput(
            name="Sim Patient",
            age=55,
            sex=1,
            trestbps=160,
            chol=260,
            smoking="Regularly"
        )
        sim_input = SimulationInput(
            base_input=base_input,
            modified_params={"systolic_bp": 120, "cholesterol": 180, "smoking": "Never"}
        )
        sim_res = run_what_if_simulation(sim_input)
        self.assertIn("baseline", sim_res)
        self.assertIn("simulated", sim_res)
        self.assertIn("delta", sim_res)
        self.assertLessEqual(sim_res["simulated"]["risk_score"], sim_res["baseline"]["risk_score"])

    def test_04_history_and_analytics_isolation(self):
        """Test assessment history and analytics scoped to user."""
        # Query history for test user
        history = get_assessment_history(user_email=self.test_email)
        self.assertGreaterEqual(history.total, 1)
        self.assertTrue(any(item.id == self.created_pred_id for item in history.items))

        # Query analytics for test user
        analytics = get_analytics_overview(user_email=self.test_email)
        self.assertTrue(analytics["has_assessments"])
        self.assertGreaterEqual(analytics["total_assessments"], 1)
        self.assertIsNotNone(analytics["latest_assessment"])
        self.assertEqual(analytics["latest_assessment"]["id"], self.created_pred_id)

    def test_05_dynamic_cohort_generation(self):
        """Test dynamic batch generation in MongoDB."""
        gen_res = generate_dynamic_history(count=3, user_email=self.test_email)
        self.assertEqual(gen_res["status"], "success")
        self.assertEqual(len(gen_res["generated"]), 3)

        # Verify added to user's history
        history = get_assessment_history(user_email=self.test_email)
        self.assertGreaterEqual(history.total, 4)

    def test_06_reports_generation(self):
        """Test clinical report generation from MongoDB data."""
        report = generate_clinical_report(self.created_pred_id)
        self.assertEqual(report["assessment_id"], self.created_pred_id)
        self.assertEqual(report["patient"]["name"], "Direct Test Patient")
        self.assertIn("clinical_summary", report)

    def test_07_hospitals_directory_and_booking(self):
        """Test hospitals query from MongoDB and appointment booking."""
        hosp_res = list_hospitals(city="Mumbai")
        self.assertGreater(hosp_res["count"], 0)
        first_hosp = hosp_res["hospitals"][0]

        booking_req = AppointmentBookingRequest(
            hospital_id=first_hosp["id"],
            patient_name="Direct Booking Patient",
            contact_phone="+91 98765 43210",
            preferred_date="2026-09-10",
            notes="Routine checkup"
        )
        book_res = book_consultation(booking_req)
        self.assertEqual(book_res["status"], "success")
        self.assertIn("APPT-", book_res["booking_id"])

        # Verify booking in MongoDB
        booking_doc = self.db.appointments.find_one({"booking_id": book_res["booking_id"]})
        self.assertIsNotNone(booking_doc)
        self.assertEqual(booking_doc["hospital_id"], first_hosp["id"])

    def test_08_cleanup(self):
        """Test deleting individual test assessment and cleaning up."""
        del_res = delete_assessment(self.created_pred_id)
        self.assertEqual(del_res["status"], "success")

        # Cleanup test user documents
        self.db.users.delete_many({"email": self.test_email})
        self.db.assessments.delete_many({"user_email": self.test_email})

if __name__ == "__main__":
    unittest.main(verbosity=2)
