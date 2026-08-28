import unittest
import sys
from pathlib import Path
from fastapi import HTTPException

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.db.database import get_db, init_db
from app.schemas.auth import UserRegister, UserLogin
from app.api.endpoints.auth import register_user, login_user

class TestAuthEnforcement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        # Clean test accounts
        db = get_db()
        db.users.delete_many({"email": {"$in": ["new_user_unregistered@health.in", "registered_user@health.in"]}})

    def test_01_unregistered_user_cannot_login_without_signup(self):
        """Unregistered user attempting to sign in must be rejected with 404 error requiring sign up."""
        req = UserLogin(email="new_user_unregistered@health.in", password="secretpassword123")
        with self.assertRaises(HTTPException) as ctx:
            login_user(req)
        
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertIn("No account found", ctx.exception.detail)
        self.assertIn("sign up first", ctx.exception.detail)

    def test_02_register_new_user_succeeds(self):
        """Registering a new account with valid credentials must succeed."""
        req = UserRegister(
            name="Dr. Alok Verma",
            email="registered_user@health.in",
            password="securepassword456",
            role="Cardiologist / Physician"
        )
        resp = register_user(req)
        self.assertEqual(resp.status, "success")
        self.assertEqual(resp.user.email, "registered_user@health.in")
        self.assertEqual(resp.user.name, "Dr. Alok Verma")

    def test_03_duplicate_registration_fails(self):
        """Attempting to register an already registered email must fail with 400."""
        req = UserRegister(
            name="Dr. Duplicate",
            email="registered_user@health.in",
            password="anotherpassword",
            role="Cardiologist / Physician"
        )
        with self.assertRaises(HTTPException) as ctx:
            register_user(req)

        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("already exists", ctx.exception.detail)

    def test_04_registered_user_login_succeeds(self):
        """Registered user logging in with correct credentials must succeed."""
        req = UserLogin(email="registered_user@health.in", password="securepassword456")
        resp = login_user(req)
        self.assertEqual(resp.status, "success")
        self.assertEqual(resp.user.email, "registered_user@health.in")
        self.assertEqual(resp.user.name, "Dr. Alok Verma")
        self.assertIsNotNone(resp.access_token)

    def test_05_registered_user_wrong_password_fails(self):
        """Registered user logging in with incorrect password must fail with 401."""
        req = UserLogin(email="registered_user@health.in", password="wrongpassword999")
        with self.assertRaises(HTTPException) as ctx:
            login_user(req)

        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Invalid password", ctx.exception.detail)

    @classmethod
    def tearDownClass(cls):
        db = get_db()
        db.users.delete_many({"email": {"$in": ["new_user_unregistered@health.in", "registered_user@health.in"]}})

if __name__ == "__main__":
    unittest.main(verbosity=2)
