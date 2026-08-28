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

class AuthResponse(BaseModel):
    status: str
    message: str
    access_token: str
    user: UserProfile
