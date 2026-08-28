import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "app" / "ml" / "saved_models"

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

PROJECT_NAME = "HeartCare AI - Heart Failure Prediction API"
VERSION = "1.0.0"
API_V1_STR = "/api"

# CORS origins allowed to communicate with backend
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

# Database path for SQLite history storage
DB_PATH = DATA_DIR / "heartcare.db"
