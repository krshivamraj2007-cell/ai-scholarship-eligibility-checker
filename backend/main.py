from datetime import datetime, timedelta, timezone
from jose import jwt

from fastapi import HTTPException
from pydantic import BaseModel
from pwdlib import PasswordHash

import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env
load_dotenv()
password_hasher = PasswordHash.recommended()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing from .env")
class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
class LoginRequest(BaseModel):
    email: str
    password: str
app = FastAPI(
    title="AI Scholarship Eligibility Checker",
    description="API for scholarship and government scheme eligibility",
    version="1.0.0"
)

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database connection function
def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Scholarship Eligibility Checker API",
        "status": "Running successfully"
    }


# Backend health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI Scholarship Eligibility Checker"
    }


# Database health check
@app.get("/db-health")
def database_health():
    try:
        with get_db_connection() as connection:
            connection.execute("SELECT 1")

        return {
            "status": "connected",
            "database": "scholarai_db"
        }

    except Exception:
        return {
            "status": "disconnected",
            "database": "scholarai_db"
        }
@app.post("/register")
def register_user(user: RegisterRequest):

    hashed_password = password_hasher.hash(user.password)

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO users (full_name, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                    """,
                    (user.full_name, user.email, hashed_password)
                )

                user_id = cursor.fetchone()[0]

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
# Login API
@app.post("/login")
def login_user(user: LoginRequest):

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id, full_name, email, password_hash
                    FROM users
                    WHERE email = %s;
                    """,
                    (user.email,)
                )

                db_user = cursor.fetchone()

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        user_id, full_name, email, password_hash = db_user

        if not password_hasher.verify(user.password, password_hash):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            data={"sub": str(user_id)}
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "full_name": full_name,
                "email": email
            }
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong during login"
        )