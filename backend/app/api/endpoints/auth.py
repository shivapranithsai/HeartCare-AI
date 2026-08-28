import uuid
import datetime
from fastapi import APIRouter, HTTPException, status
from app.db.database import get_db_connection, hash_password
from app.schemas.auth import UserRegister, UserLogin, AuthResponse, UserProfile

router = APIRouter()

@router.post("/register", response_model=AuthResponse)
def register_user(req: UserRegister):
    email_clean = req.email.strip().lower()
    name_clean = req.name.strip()
    
    if not email_clean or not req.password:
        raise HTTPException(status_code=400, detail="Email and password are required.")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email_clean,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="A clinical account with this email already exists.")

    user_id = f"USER-{uuid.uuid4().hex[:8].upper()}"
    pwd_hash = hash_password(req.password)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    role = req.role or "Cardiologist / Physician"

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, name, role, created_at, last_login)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, email_clean, pwd_hash, name_clean, role, now_str, now_str))
    conn.commit()
    conn.close()

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

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email_clean,))
    user_row = cursor.fetchone()

    # If user doesn't exist, reject login and require sign up first
    if not user_row:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email address. Please click 'Create Account' to sign up first."
        )

    # Check password
    pwd_hash = hash_password(req.password)
    if user_row["password_hash"] != pwd_hash:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password credentials. Please verify your password and try again."
        )

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now_str, user_row["id"]))
    conn.commit()
    conn.close()

    token = f"jwt_sim_{uuid.uuid4().hex}"
    
    user_profile = UserProfile(
        id=user_row["id"],
        name=user_row["name"],
        email=user_row["email"],
        role=user_row["role"],
        created_at=user_row["created_at"],
        last_login=now_str
    )

    return AuthResponse(
        status="success",
        message="Authenticated successfully!",
        access_token=token,
        user=user_profile
    )
