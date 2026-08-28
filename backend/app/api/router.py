from fastapi import APIRouter
from app.api.endpoints import predict, history, analytics, hospitals, reports, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(predict.router, tags=["Prediction"])
api_router.include_router(history.router, prefix="/history", tags=["History"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(hospitals.router, prefix="/hospitals", tags=["Hospitals"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
