from ai_service import ask_ai
from eligibility import check_basic_eligibility
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

from datetime import date
from typing import Optional

class StudentProfileRequest(BaseModel):
    # Existing fields
    state: str
    district: str
    category: str
    course: str
    branch: str
    current_year: str
    previous_marks: float
    annual_family_income: float

    # Additional eligibility fields
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    disability_status: Optional[bool] = None
    disability_percentage: Optional[float] = None
    domicile_state: Optional[str] = None
    institution_name: Optional[str] = None
    institution_type: Optional[str] = None
    institution_approval: Optional[str] = None
    admission_type: Optional[str] = None
    admission_year: Optional[int] = None
    education_level: Optional[str] = None
    class_12_marks: Optional[float] = None
    class_12_percentile: Optional[float] = None
    entrance_exam: Optional[str] = None
    entrance_exam_qualified: Optional[bool] = None
    research_program: Optional[str] = None


@app.post("/student-profile/{user_id}")
def save_student_profile(user_id: int, profile: StudentProfileRequest):

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO student_profiles (
                        user_id,
                        state,
                        district,
                        category,
                        course,
                        branch,
                        current_year,
                        previous_marks,
                        annual_family_income,
                        date_of_birth,
                        gender,
                        disability_status,
                        disability_percentage,
                        domicile_state,
                        institution_name,
                        institution_type,
                        institution_approval,
                        admission_type,
                        admission_year,
                        education_level,
                        class_12_marks,
                        class_12_percentile,
                        entrance_exam,
                        entrance_exam_qualified,
                        research_program
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (user_id)
                    DO UPDATE SET
                        state = EXCLUDED.state,
                        district = EXCLUDED.district,
                        category = EXCLUDED.category,
                        course = EXCLUDED.course,
                        branch = EXCLUDED.branch,
                        current_year = EXCLUDED.current_year,
                        previous_marks = EXCLUDED.previous_marks,
                        annual_family_income = EXCLUDED.annual_family_income,
                        date_of_birth = EXCLUDED.date_of_birth,
                        gender = EXCLUDED.gender,
                        disability_status = EXCLUDED.disability_status,
                        disability_percentage = EXCLUDED.disability_percentage,
                        domicile_state = EXCLUDED.domicile_state,
                        institution_name = EXCLUDED.institution_name,
                        institution_type = EXCLUDED.institution_type,
                        institution_approval = EXCLUDED.institution_approval,
                        admission_type = EXCLUDED.admission_type,
                        admission_year = EXCLUDED.admission_year,
                        education_level = EXCLUDED.education_level,
                        class_12_marks = EXCLUDED.class_12_marks,
                        class_12_percentile = EXCLUDED.class_12_percentile,
                        entrance_exam = EXCLUDED.entrance_exam,
                        entrance_exam_qualified = EXCLUDED.entrance_exam_qualified,
                        research_program = EXCLUDED.research_program,
                        updated_at = CURRENT_TIMESTAMP;
                    """,
                    (
                        user_id,
                        profile.state,
                        profile.district,
                        profile.category,
                        profile.course,
                        profile.branch,
                        profile.current_year,
                        profile.previous_marks,
                        profile.annual_family_income,
                        profile.date_of_birth,
                        profile.gender,
                        profile.disability_status,
                        profile.disability_percentage,
                        profile.domicile_state,
                        profile.institution_name,
                        profile.institution_type,
                        profile.institution_approval,
                        profile.admission_type,
                        profile.admission_year,
                        profile.education_level,
                        profile.class_12_marks,
                        profile.class_12_percentile,
                        profile.entrance_exam,
                        profile.entrance_exam_qualified,
                        profile.research_program
                    )
                )

        return {
            "message": "Student profile saved successfully",
            "user_id": user_id
        }

    except Exception as error:
        print("PROFILE SAVE ERROR:", repr(error))
        raise HTTPException(
            status_code=500,
            detail="Unable to save student profile"
        )

# Get all active government schemes
@app.get("/government-schemes")
def get_government_schemes():

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        scheme_name,
                        government_level,
                        state_ut,
                        category,
                        description,
                        eligibility_criteria,
                        benefits,
                        required_documents,
                        education_level,
                        application_url,
                        official_source_url,
                        scheme_type,
                        benefit_type,
                        annual_income_limit,
                        minimum_marks,
                        scholarship_amount,
                        maximum_loan_amount,
                        interest_rate,
                        interest_subvention_rate,
                        repayment_period_years,
                        moratorium_period,
                        collateral_requirement,
                        credit_guarantee_details,
                        eligible_institutions,
                        eligible_courses,
                        renewal_conditions,
                        application_start_date,
                        application_deadline
                    FROM government_schemes
                    WHERE is_active = TRUE
                    ORDER BY id;
                    """
                )

                rows = cursor.fetchall()

                columns = [column.name for column in cursor.description]

                schemes = [
                    dict(zip(columns, row))
                    for row in rows
                ]

        return {
            "total": len(schemes),
            "schemes": schemes
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to fetch government schemes"
        )

@app.get("/eligible-schemes/{user_id}")

@app.get("/eligible-schemes/{user_id}")
def get_eligible_schemes(user_id: int):

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:

                # 1. Fetch complete student profile
                cursor.execute(
                    """
                    SELECT
                        state,
                        district,
                        category,
                        course,
                        branch,
                        current_year,
                        previous_marks,
                        annual_family_income,
                        gender,
                        disability_status,
                        disability_percentage,
                        domicile_state,
                        institution_name,
                        institution_type,
                        institution_approval,
                        admission_type,
                        admission_year,
                        education_level,
                        class_12_marks,
                        class_12_percentile,
                        entrance_exam,
                        entrance_exam_qualified,
                        research_program
                    FROM student_profiles
                    WHERE user_id = %s;
                    """,
                    (user_id,)
                )

                profile_row = cursor.fetchone()

                if profile_row is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Student profile not found"
                    )

                profile_columns = [
                    column.name for column in cursor.description
                ]

                student = dict(zip(profile_columns, profile_row))

                # 2. Fetch all active government schemes
                cursor.execute(
                    """
                    SELECT *
                    FROM government_schemes
                    WHERE is_active = TRUE
                    ORDER BY id;
                    """
                )

                scheme_rows = cursor.fetchall()

                scheme_columns = [
                    column.name for column in cursor.description
                ]

                schemes = [
                    dict(zip(scheme_columns, row))
                    for row in scheme_rows
                ]

        # 3. Match student profile against every scheme
        matched_schemes = []

        for scheme in schemes:

            eligibility_result = check_basic_eligibility(
                student,
                scheme
            )

            matched_schemes.append({
                "scheme_id": scheme["id"],
                "scheme_name": scheme["scheme_name"],
                "government_level": scheme["government_level"],
                "official_source_url": scheme["official_source_url"],
                "benefits": scheme["benefits"],
                "state_ut": scheme["state_ut"],
                "scheme_type": scheme["scheme_type"],
                "benefit_type": scheme["benefit_type"],

                "status": eligibility_result["status"],

                "checks": eligibility_result["checks"]
            })

        # 4. Calculate matching summary
        eligible_count = sum(
            1 for scheme in matched_schemes
            if scheme["status"] == "eligible"
        )

        potentially_eligible_count = sum(
            1 for scheme in matched_schemes
            if scheme["status"] == "potentially_eligible"
        )

        not_eligible_count = sum(
            1 for scheme in matched_schemes
            if scheme["status"] == "not_eligible"
        )

        # 5. Return eligibility results
        return {
            "user_id": user_id,

            "total_schemes": len(schemes),

            "summary": {
                "eligible": eligible_count,
                "potentially_eligible": potentially_eligible_count,
                "not_eligible": not_eligible_count
            },

            "matched_schemes": matched_schemes
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            "ELIGIBILITY MATCHING ERROR:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to match government schemes"
        )




@app.post("/ai-chat")
def ai_chat(data: dict):

    message = data.get("message", "").strip()
    user_id = data.get("user_id")

    if not message:
        return {"error": "Message cannot be empty"}

    if not user_id:
        return {"error": "Student ID is required"}

    try:
        # 1. Get student's eligibility results
        eligibility_data = get_eligible_schemes(int(user_id))

        print("ELIGIBILITY SUMMARY:", eligibility_data["summary"])

        # 2. Select eligible and potentially eligible schemes
        eligible_matches = [
            scheme
            for scheme in eligibility_data["matched_schemes"]
            if scheme["status"] in [
                "eligible",
                "potentially_eligible"
            ]
        ]

        # 3. Build eligibility context
        eligibility_context = ""

        for scheme in eligible_matches:
            eligibility_context += f"""
Scheme: {scheme['scheme_name']}
Eligibility Status: {scheme['status']}
Benefits: {scheme['benefits']}
Official Source: {scheme['official_source_url']}
Eligibility Checks: {scheme['checks']}
"""

        if not eligible_matches:
            eligibility_context = (
                "No eligible or potentially eligible schemes "
                "were found by the eligibility evaluator."
            )

        # 4. Fetch government scheme information
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                scheme_name,
                description,
                eligibility_criteria,
                benefits,
                required_documents,
                official_source_url
            FROM government_schemes
            WHERE is_active = TRUE
            ORDER BY id
        """)

        schemes = cursor.fetchall()

        cursor.close()
        conn.close()

        # 5. Build database context
        scheme_context = ""

        for scheme in schemes:
            scheme_context += f"""
Scheme: {scheme[0]}
Description: {scheme[1]}
Eligibility Criteria: {scheme[2]}
Benefits: {scheme[3]}
Required Documents: {scheme[4]}
Official Source: {scheme[5]}
"""

        # 6. Build AI prompt
        prompt = f"""
You are ScholarAI, an AI assistant for Indian scholarships
and government education schemes.

IMPORTANT RULES:

1. Use only the supplied database information.
2. Use eligibility evaluator results for personalized recommendations.
3. Never invent scheme names, benefits, amounts or URLs.
4. Use only official source URLs supplied in the database.
5. Clearly distinguish eligible and potentially eligible schemes.
6. Never describe potentially eligible as confirmed eligible.
7. Explain unknown eligibility checks honestly.
8. Do not recommend schemes marked not eligible.
9. Use simple English.

DATABASE INFORMATION:
{scheme_context}

STUDENT ELIGIBILITY RESULTS:
Recommend only schemes listed here.
Never change their eligibility status.

{eligibility_context}

STUDENT QUESTION:
{message}

Provide a short conversational introduction only.
Do not list individual scheme names.
Do not repeat scheme benefits or eligibility statuses.
The frontend will display recommendations separately.

Tell the student that matching schemes are displayed below.
"""

        # 7. Generate AI response
        response = ask_ai(prompt)

        return {
            "message": message,
            "response": response,
            "recommendations": [
                {
                    "scheme_name": scheme["scheme_name"],
                    "status": scheme["status"],
                    "benefits": scheme["benefits"],
                    "official_source_url": scheme["official_source_url"],
                    "checks": scheme["checks"]
                }
                for scheme in eligible_matches
            ]
        }

    except Exception as error:

        print("AI Chat Error:", repr(error))

        return {
            "error": "Unable to process your question right now."
        }
