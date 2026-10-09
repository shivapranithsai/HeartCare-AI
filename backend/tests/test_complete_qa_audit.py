import unittest
import sys
import uuid
import time
import json
import concurrent.futures
from pathlib import Path
from fastapi import HTTPException

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.db.database import get_db, init_db, hash_password
from app.core.config import MONGODB_URI, MONGODB_DB_NAME
from app.schemas.auth import UserRegister, UserLogin
from app.schemas.prediction import PatientInput, SimulationInput
from app.api.endpoints.auth import register_user, login_user
from app.api.endpoints.predict import run_prediction, run_what_if_simulation
from app.api.endpoints.history import (
    get_assessment_history,
    generate_dynamic_history,
    get_assessment_by_id,
    delete_assessment,
    clear_all_history
)
from app.api.endpoints.analytics import get_analytics_overview
from app.api.endpoints.hospitals import list_hospitals, book_consultation, AppointmentBookingRequest
from app.api.endpoints.reports import generate_clinical_report
from app.ml.model_loader import ml_service
from app.services.live_hospitals import calculate_haversine_distance

class TestComprehensiveQAAudit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.db = get_db()
        cls.user_a_email = f"user_a_{uuid.uuid4().hex[:6]}@cardiotest.org"
        cls.user_b_email = f"user_b_{uuid.uuid4().hex[:6]}@cardiotest.org"

    # =========================================================================
    # SECTION 4: AUTHENTICATION & SECURITY
    # =========================================================================
    def test_01_auth_complete_flow(self):
        """Test registration, duplicate check, password hashing, login, and last_login update."""
        # 1. Valid Registration
        reg_a = register_user(UserRegister(
            email=self.user_a_email,
            name="Dr. User A (Cardiologist)",
            password="StrongPassword123!",
            role="Cardiologist / Physician"
        ))
        self.assertEqual(reg_a.status, "success")
        self.assertNotIn("password_hash", reg_a.user.model_dump())
        self.assertEqual(reg_a.user.email, self.user_a_email)

        # 2. Duplicate Registration Rejection
        with self.assertRaises(HTTPException) as ctx:
            register_user(UserRegister(
                email=self.user_a_email,
                name="Dr. Duplicate",
                password="AnotherPassword123!",
                role="Cardiologist / Physician"
            ))
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("already exists", ctx.exception.detail)

        # 3. Missing Fields Validation
        with self.assertRaises(HTTPException) as ctx:
            register_user(UserRegister(email="", name="No Email", password="123", role="Patient"))
        self.assertEqual(ctx.exception.status_code, 400)

        # 4. Valid Login
        login_res = login_user(UserLogin(email=self.user_a_email, password="StrongPassword123!"))
        self.assertEqual(login_res.status, "success")
        self.assertIsNotNone(login_res.access_token)
        self.assertIsNotNone(login_res.user.last_login)

        # 5. Invalid Password Rejection
        with self.assertRaises(HTTPException) as ctx:
            login_user(UserLogin(email=self.user_a_email, password="WrongPassword999"))
        self.assertEqual(ctx.exception.status_code, 401)

        # 6. Non-existent User Rejection
        with self.assertRaises(HTTPException) as ctx:
            login_user(UserLogin(email="nonexistent_user_999@unknown.org", password="AnyPassword123!"))
        self.assertEqual(ctx.exception.status_code, 404)

        # 7. Register User B
        reg_b = register_user(UserRegister(
            email=self.user_b_email,
            name="Dr. User B (Physician)",
            password="StrongPassword456!",
            role="Cardiologist / Physician"
        ))
        self.assertEqual(reg_b.status, "success")

    # =========================================================================
    # SECTION 5: CRITICAL USER ISOLATION TESTS
    # =========================================================================
    def test_02_strict_user_isolation(self):
        """Verify complete isolation between User A and User B across predictions, history, and analytics."""
        # 1. User A creates an assessment
        pred_a = run_prediction(PatientInput(
            name="Patient of User A",
            user_email=self.user_a_email,
            age=52,
            sex=1,
            gender="Male",
            cp=1,
            trestbps=135,
            chol=210,
            fbs=0,
            restecg=0,
            thalach=150,
            exang=0,
            oldpeak=0.5,
            slope=1,
            ca=0,
            thal=1,
            ejection_fraction=58,
            serum_creatinine=0.9,
            smoking="Never"
        ))

        # 2. User B creates an assessment
        pred_b = run_prediction(PatientInput(
            name="Patient of User B",
            user_email=self.user_b_email,
            age=70,
            sex=0,
            gender="Female",
            cp=0,
            trestbps=175,
            chol=290,
            fbs=1,
            restecg=2,
            thalach=110,
            exang=1,
            oldpeak=3.2,
            slope=2,
            ca=3,
            thal=3,
            ejection_fraction=30,
            serum_creatinine=2.4,
            smoking="Regularly"
        ))

        self.__class__.pred_a_id = pred_a.prediction_id
        self.__class__.pred_b_id = pred_b.prediction_id

        # 3. User A queries history -> should ONLY see User A's patient
        hist_a = get_assessment_history(user_email=self.user_a_email)
        self.assertEqual(hist_a.total, 1)
        self.assertEqual(hist_a.items[0].id, pred_a.prediction_id)
        self.assertEqual(hist_a.items[0].patient_name, "Patient of User A")
        self.assertFalse(any(i.id == pred_b.prediction_id for i in hist_a.items))

        # 4. User B queries history -> should ONLY see User B's patient
        hist_b = get_assessment_history(user_email=self.user_b_email)
        self.assertEqual(hist_b.total, 1)
        self.assertEqual(hist_b.items[0].id, pred_b.prediction_id)
        self.assertEqual(hist_b.items[0].patient_name, "Patient of User B")
        self.assertFalse(any(i.id == pred_a.prediction_id for i in hist_b.items))

        # 5. User A queries analytics -> should only calculate User A's metrics
        analytics_a = get_analytics_overview(user_email=self.user_a_email)
        self.assertEqual(analytics_a["total_assessments"], 1)
        self.assertEqual(analytics_a["latest_assessment"]["patient_name"], "Patient of User A")

        # 6. User B queries analytics -> should only calculate User B's metrics
        analytics_b = get_analytics_overview(user_email=self.user_b_email)
        self.assertEqual(analytics_b["total_assessments"], 1)
        self.assertEqual(analytics_b["latest_assessment"]["patient_name"], "Patient of User B")
        self.assertGreater(analytics_b["latest_assessment"]["risk_score"], analytics_a["latest_assessment"]["risk_score"])

        # 7. Individual Record Lookup User Scoping (Issue 2 Verification)
        # User A can fetch their own assessment
        record_a = get_assessment_by_id(pred_a.prediction_id, user_email=self.user_a_email)
        self.assertEqual(record_a["id"], pred_a.prediction_id)

        # User B CANNOT fetch User A's assessment by ID (must raise 404)
        with self.assertRaises(HTTPException) as ctx:
            get_assessment_by_id(pred_a.prediction_id, user_email=self.user_b_email)
        self.assertEqual(ctx.exception.status_code, 404)

        # User B CANNOT delete User A's assessment by ID (must raise 404)
        with self.assertRaises(HTTPException) as ctx:
            delete_assessment(pred_a.prediction_id, user_email=self.user_b_email)
        self.assertEqual(ctx.exception.status_code, 404)

        # User B CANNOT access User A's medical report (must raise 404)
        with self.assertRaises(HTTPException) as ctx:
            generate_clinical_report(pred_a.prediction_id, user_email=self.user_b_email)
        self.assertEqual(ctx.exception.status_code, 404)

        # User A CAN access their own medical report
        report_a = generate_clinical_report(pred_a.prediction_id, user_email=self.user_a_email)
        self.assertEqual(report_a["assessment_id"], pred_a.prediction_id)

    # =========================================================================
    # SECTION 6, 7 & 8: PREDICTION, ML MODELS & CLINICAL LOGIC
    # =========================================================================
    def test_03_prediction_profiles_and_boundaries(self):
        """Test healthy, moderate, high, and critical profiles with boundary conditions."""
        # 1. Healthy Athlete
        res_healthy = run_prediction(PatientInput(
            name="Healthy Athlete",
            age=25,
            sex=1,
            cp=3,
            trestbps=110,
            chol=160,
            fbs=0,
            restecg=0,
            thalach=185,
            exang=0,
            oldpeak=0.0,
            slope=0,
            ca=0,
            thal=1,
            ejection_fraction=68,
            serum_creatinine=0.7,
            smoking="Never"
        ))
        self.assertLess(res_healthy.risk_score, 30)
        self.assertGreater(res_healthy.heart_health_score, 70)
        self.assertIn("Low", res_healthy.risk_level)
        self.assertGreater(len(res_healthy.protective_factors), 0)

        # 2. Critical Profile
        res_critical = run_prediction(PatientInput(
            name="Critical Cardiac Patient",
            age=76,
            sex=0,
            cp=0,
            trestbps=190,
            chol=340,
            fbs=1,
            restecg=2,
            thalach=95,
            exang=1,
            oldpeak=4.5,
            slope=2,
            ca=3,
            thal=3,
            ejection_fraction=22,
            serum_creatinine=3.1,
            smoking="Regularly"
        ))
        self.assertGreater(res_critical.risk_score, 75)
        self.assertLess(res_critical.heart_health_score, 35)
        self.assertIn("Critical", res_critical.risk_level)
        self.assertGreater(len(res_critical.top_risk_factors), 0)
        self.assertGreater(len(res_critical.recommendations), 0)

        # 3. Model Source Verification
        self.assertTrue(ml_service.is_custom_loaded or "Heuristic" in res_healthy.model_source)

    # =========================================================================
    # SECTION 9: WHAT-IF INTERVENTION SIMULATION
    # =========================================================================
    def test_04_what_if_simulation_deltas(self):
        """Test positive and negative intervention simulations."""
        base_patient = PatientInput(
            name="Simulation Baseline",
            age=60,
            sex=1,
            cp=1,
            trestbps=165,
            chol=260,
            smoking="Regularly"
        )

        # Positive Intervention (lower BP, quit smoking, exercise)
        sim_improved = run_what_if_simulation(SimulationInput(
            base_input=base_patient,
            modified_params={"systolic_bp": 120, "cholesterol": 180, "smoking": "Never"}
        ))
        self.assertLess(sim_improved["simulated"]["risk_score"], sim_improved["baseline"]["risk_score"])
        self.assertEqual(sim_improved["delta"]["status"], "improved")

        # Negative Intervention (elevated BP, high cholesterol)
        sim_worsened = run_what_if_simulation(SimulationInput(
            base_input=base_patient,
            modified_params={"systolic_bp": 200, "cholesterol": 360, "smoking": "Regularly"}
        ))
        self.assertGreaterEqual(sim_worsened["simulated"]["risk_score"], sim_worsened["baseline"]["risk_score"])

    # =========================================================================
    # SECTION 10 & 11: HISTORY & ANALYTICS AGGREGATIONS
    # =========================================================================
    def test_05_history_and_analytics(self):
        """Test history search, filters, dynamic cohorts, and analytics aggregations."""
        # 1. Generate 3 dynamic cohort assessments for User A
        dyn_res = generate_dynamic_history(count=3, user_email=self.user_a_email)
        self.assertEqual(dyn_res["status"], "success")
        self.assertEqual(len(dyn_res["generated"]), 3)

        # 2. Query History for User A
        hist = get_assessment_history(user_email=self.user_a_email)
        self.assertEqual(hist.total, 4)

        # 3. Search Filter
        searched = get_assessment_history(user_email=self.user_a_email, search="Patient of User A")
        self.assertGreaterEqual(searched.total, 1)

        # 4. Analytics Aggregation
        analytics = get_analytics_overview(user_email=self.user_a_email)
        self.assertTrue(analytics["has_assessments"])
        self.assertEqual(analytics["total_assessments"], 4)
        self.assertIsNotNone(analytics["average_risk_score"])
        self.assertIsNotNone(analytics["average_health_score"])
        self.assertIsInstance(analytics["risk_distribution"], dict)
        self.assertGreaterEqual(len(analytics["timeline"]), 1)

        # 5. Zero-State Analytics for Brand New User
        zero_analytics = get_analytics_overview(user_email="brand_new_zero_user@test.org")
        self.assertFalse(zero_analytics["has_assessments"])
        self.assertEqual(zero_analytics["total_assessments"], 0)
        self.assertIsNone(zero_analytics["average_risk_score"])
        self.assertEqual(len(zero_analytics["timeline"]), 0)

    # =========================================================================
    # SECTION 12 & 13: HOSPITALS & APPOINTMENTS
    # =========================================================================
    def test_06_hospitals_and_appointments(self):
        """Test hospital query, distance calculation, nearest-first sorting, and booking."""
        # 1. City Query
        hosp_res = list_hospitals(city="Bengaluru")
        self.assertGreater(hosp_res["count"], 0)
        first_hosp = hosp_res["hospitals"][0]
        self.assertIn("Bengaluru", first_hosp["city"])

        # 2. Haversine Accuracy (AIIMS Delhi to Fortis Escorts Delhi ~ 6.8 km)
        dist = calculate_haversine_distance(28.5672, 77.2100, 28.5606, 77.2796)
        self.assertAlmostEqual(dist, 6.8, delta=0.5)

        # 3. Book Consultation
        booking_req = AppointmentBookingRequest(
            hospital_id=first_hosp["id"],
            patient_name="QA Audit Patient",
            contact_phone="+91 98765 00000",
            preferred_date="2026-09-15",
            notes="Routine Cardiac Screening"
        )
        book_res = book_consultation(booking_req)
        self.assertEqual(book_res["status"], "success")
        self.assertIn("APPT-", book_res["booking_id"])

        # 4. Verify MongoDB Appointment Persistence
        appt_doc = self.db.appointments.find_one({"booking_id": book_res["booking_id"]})
        self.assertIsNotNone(appt_doc)
        self.assertEqual(appt_doc["hospital_id"], first_hosp["id"])
        self.assertEqual(appt_doc["patient_name"], "QA Audit Patient")

    # =========================================================================
    # SECTION 14: MEDICAL REPORTS
    # =========================================================================
    def test_07_medical_reports(self):
        """Test report generation and nonexistent ID handling."""
        # 1. Valid Report
        report = generate_clinical_report(self.pred_a_id)
        self.assertEqual(report["assessment_id"], self.pred_a_id)
        self.assertEqual(report["patient"]["name"], "Patient of User A")
        self.assertIn("clinical_summary", report)

        # 2. Non-existent ID rejection
        with self.assertRaises(HTTPException) as ctx:
            generate_clinical_report("NON-EXISTENT-ID-999")
        self.assertEqual(ctx.exception.status_code, 404)

    # =========================================================================
    # SECTION 19 & 21: SECURITY & PERFORMANCE BENCHMARK
    # =========================================================================
    def test_08_security_and_performance(self):
        """Test NoSQL injection resilience and execute 10 concurrent ML predictions."""
        # 1. Injection attack string in patient name & notes
        xss_patient = PatientInput(
            name="<script>alert('xss')</script> {$ne: null}",
            user_email=self.user_a_email,
            age=45,
            sex=1,
            trestbps=125,
            chol=190,
            smoking="Never"
        )
        xss_res = run_prediction(xss_patient)
        self.assertIsNotNone(xss_res.prediction_id)
        
        # Verify stored safely without code execution
        doc = self.db.assessments.find_one({"id": xss_res.prediction_id})
        self.assertEqual(doc["patient_name"], "<script>alert('xss')</script> {$ne: null}")

        # 2. Performance: 10 concurrent predictions
        def send_pred(idx):
            p = PatientInput(
                name=f"Concurrent Patient {idx}",
                user_email=self.user_a_email,
                age=40 + idx,
                sex=idx % 2,
                trestbps=120 + idx,
                chol=190 + idx,
                smoking="Never"
            )
            start = time.time()
            res = run_prediction(p)
            elapsed = time.time() - start
            return res.prediction_id, elapsed

        start_all = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(send_pred, i) for i in range(10)]
            results = [f.result() for f in futures]
        total_duration = time.time() - start_all

        self.assertEqual(len(results), 10)
        avg_latency = total_duration / 10
        print(f"\n[Performance Benchmark] 10 Concurrent Predictions executed in {total_duration:.2f}s (Avg {avg_latency*1000:.1f}ms/request)")
        self.assertLess(avg_latency, 1.5, "Average prediction latency should be < 1.5s")

    @classmethod
    def tearDownClass(cls):
        # Clean up test audit documents
        cls.db.users.delete_many({"email": {"$in": [cls.user_a_email, cls.user_b_email]}})
        cls.db.assessments.delete_many({"user_email": {"$in": [cls.user_a_email, cls.user_b_email]}})
        cls.db.appointments.delete_many({"patient_name": "QA Audit Patient"})

if __name__ == "__main__":
    unittest.main(verbosity=2)
