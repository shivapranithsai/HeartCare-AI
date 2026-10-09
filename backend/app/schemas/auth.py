from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "Cardiologist / Physician"

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: str
    last_login: Optional[str] = None
    phone: Optional[str] = ""
    emergency_contact: Optional[str] = ""
    blood_group: Optional[str] = ""
    email_notifications: Optional[bool] = False
    sms_alerts: Optional[bool] = False

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    blood_group: Optional[str] = None
    email_notifications: Optional[bool] = False
    sms_alerts: Optional[bool] = False

class AuthResponse(BaseModel):
    status: str
    message: str
    access_token: str
    user: UserProfile

