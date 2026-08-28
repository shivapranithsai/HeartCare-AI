from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AssessmentHistoryItem(BaseModel):
    id: str
    timestamp: str
    patient_name: str
    age: int
    gender: str
    risk_score: int
    risk_level: str
    probability_percentage: float
    heart_health_score: int
    systolic_bp: Optional[int]
    diastolic_bp: Optional[int]
    cholesterol: Optional[int]
    ejection_fraction: Optional[int]
    serum_creatinine: Optional[float]
    smoking: Optional[str]
    chest_pain: Optional[str]
    model_source: str
    summary_message: str
    input_data: Dict[str, Any]

class HistoryListResponse(BaseModel):
    total: int
    items: List[AssessmentHistoryItem]
