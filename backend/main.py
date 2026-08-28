from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import datetime

from app.core.config import PROJECT_NAME, VERSION, API_V1_STR, CORS_ORIGINS
from app.api.router import api_router
from app.db.database import init_db
from app.ml.model_loader import ml_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and load model
    print("[Server Startup] Initializing SQLite database...")
    init_db()
    print("[Server Startup] Checking ML Model Service status...")
    if ml_service.is_custom_loaded:
        print("[Server Startup] Custom ML Model loaded and ready!")
    else:
        print("[Server Startup] Running with AHA/Cleveland Clinical Heuristic Engine.")
    yield
    print("[Server Shutdown] Cleanup complete.")

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    openapi_url=f"{API_V1_STR}/openapi.json",
    docs_url=f"{API_V1_STR}/docs",
    redoc_url=f"{API_V1_STR}/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix=API_V1_STR)

@app.get("/")
def root():
    return {
        "service": PROJECT_NAME,
        "version": VERSION,
        "status": "online",
        "docs_url": f"{API_V1_STR}/docs",
        "custom_ml_model_active": ml_service.is_custom_loaded
    }

@app.get(f"{API_V1_STR}/health")
def health_check():
    return {
        "status": "healthy",
        "version": VERSION,
        "timestamp": datetime.datetime.now().isoformat(),
        "custom_model_loaded": ml_service.is_custom_loaded,
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
