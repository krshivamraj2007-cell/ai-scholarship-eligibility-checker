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
class RegisterRequest(BaseModel):
    full_name: str
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