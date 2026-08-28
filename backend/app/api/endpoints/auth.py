import uuid
import datetime
from fastapi import APIRouter, HTTPException, status
from app.db.database import get_db, hash_password
from app.schemas.auth import UserRegister, UserLogin, AuthResponse, UserProfile

router = APIRouter()

@router.post("/register", response_model=AuthResponse)
def register_user(req: UserRegister):
    email_clean = req.email.strip().lower()
    name_clean = req.name.strip()
    
    if not email_clean or not req.password:
        raise HTTPException(status_code=400, detail="Email and password are required.")
    
    db = get_db()

    # Check if user exists in MongoDB
    existing_user = db.users.find_one({"email": email_clean})
    if existing_user:
        raise HTTPException(status_code=400, detail="A clinical account with this email already exists.")

    user_id = f"USER-{uuid.uuid4().hex[:8].upper()}"
    pwd_hash = hash_password(req.password)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    role = req.role or "Cardiologist / Physician"

    user_doc = {
        "id": user_id,
        "email": email_clean,
        "password_hash": pwd_hash,
        "name": name_clean,
        "role": role,
        "created_at": now_str,
        "last_login": now_str
    }
    
    db.users.insert_one(user_doc)

    token = f"jwt_sim_{uuid.uuid4().hex}"
    
    user_profile = UserProfile(
        id=user_id,
        name=name_clean,
        email=email_clean,
        role=role,
        created_at=now_str,
        last_login=now_str
    )

    return AuthResponse(
        status="success",
        message="Clinical account registered successfully!",
        access_token=token,
        user=user_profile
    )

@router.post("/login", response_model=AuthResponse)
def login_user(req: UserLogin):
    email_clean = req.email.strip().lower()
    if not email_clean or not req.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required.")

    db = get_db()
    user_doc = db.users.find_one({"email": email_clean})

    # If user doesn't exist, reject login and require sign up first
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email address. Please click 'Create Account' to sign up first."
        )

    # Check password
    pwd_hash = hash_password(req.password)
    if user_doc["password_hash"] != pwd_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password credentials. Please verify your password and try again."
        )

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.users.update_one({"id": user_doc["id"]}, {"$set": {"last_login": now_str}})

    token = f"jwt_sim_{uuid.uuid4().hex}"
    
    user_profile = UserProfile(
        id=user_doc["id"],
        name=user_doc["name"],
        email=user_doc["email"],
        role=user_doc["role"],
        created_at=user_doc["created_at"],
        last_login=now_str
    )

    return AuthResponse(
        status="success",
        message="Authenticated successfully!",
        access_token=token,
        user=user_profile
    )
