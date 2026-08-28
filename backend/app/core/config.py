import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent

# Load environment variables from .env in project root or backend dir
if (PROJECT_ROOT / ".env").exists():
    load_dotenv(PROJECT_ROOT / ".env")
elif (BASE_DIR / ".env").exists():
    load_dotenv(BASE_DIR / ".env")
else:
    load_dotenv()

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "app" / "ml" / "saved_models"

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

PROJECT_NAME = os.getenv("PROJECT_NAME", "HeartCare AI - Heart Failure Prediction API")
VERSION = os.getenv("VERSION", "1.0.0")
API_V1_STR = os.getenv("API_V1_STR", "/api")

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "heartcare")

# CORS origins allowed to communicate with backend
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

# Legacy Database path for SQLite migration
DB_PATH = DATA_DIR / "heartcare.db"
