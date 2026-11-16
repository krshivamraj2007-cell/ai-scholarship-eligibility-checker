
import re


# ============================================================
# 1. COMMON HELPER FUNCTIONS
# ============================================================

def normalize(value):
    if value is None:
        return ""

    return str(value).strip().lower()


def normalize_category(value):
    value = normalize(value).upper()

    category_aliases = {
        "SC": ["SC", "SCHEDULED CASTE"],
        "ST": ["ST", "SCHEDULED TRIBE"],
        "OBC": ["OBC", "OTHER BACKWARD CLASS"],
        "GENERAL": ["GENERAL", "GEN", "UR", "UNRESERVED"],
        "EWS": ["EWS", "ECONOMICALLY WEAKER SECTION"]
    }

    for category, aliases in category_aliases.items():
        if value in aliases:
            return category

    return None


# ============================================================
# 2. INCOME ELIGIBILITY
# ============================================================

def check_income_eligibility(student_income, scheme_income_limit):

    if student_income is None or scheme_income_limit is None:
        return "unknown"

    if student_income <= scheme_income_limit:
        return "eligible"

    return "not_eligible"


# ============================================================
# 3. EDUCATION LOAN ELIGIBILITY
# ============================================================

def check_loan_income_eligibility(student_income, scheme_name):

    scheme_name = normalize(scheme_name)

    if "pm-vidyalaxmi" in scheme_name:
        # Loan availability is not restricted by family income.
        return "eligible"

    return "unknown"


# ============================================================
# 4. INTEREST SUBVENTION ELIGIBILITY
# ============================================================

def check_interest_subvention_eligibility(
    student_income,
    scheme_name,
    income_limit
):

    scheme_name = normalize(scheme_name)

    if "pm-vidyalaxmi" not in scheme_name:
        return "not_applicable"

    if student_income is None or income_limit is None:
        return "unknown"

    if student_income <= income_limit:
        return "eligible"

    return "not_eligible"


# ============================================================
# 5. MARKS ELIGIBILITY
# ============================================================

def check_marks_eligibility(student_marks, scheme_minimum_marks):

    if student_marks is None or scheme_minimum_marks is None:
        return "unknown"

    if student_marks >= scheme_minimum_marks:
        return "eligible"

    return "not_eligible"


# ============================================================
# 6. CATEGORY ELIGIBILITY
# ============================================================

def check_category_eligibility(student_category, scheme_categories):

    if not scheme_categories:
        return "unknown"

    allowed_categories = [
        item.strip()
        for item in str(scheme_categories).split(",")
        if item.strip()
    ]

    allowed_categories = [
        item.upper() for item in allowed_categories
    ]

    if any(
        item in ["ALL", "ALL CATEGORIES", "ANY"]
        for item in allowed_categories
    ):
        return "eligible"

    if not student_category:
        return "unknown"

    student_normalized = normalize_category(student_category)

    if student_normalized is None:
        return "unknown"

    normalized_allowed = set()

    for category in allowed_categories:

        normalized = normalize_category(category)

        if normalized:
            normalized_allowed.add(normalized)

    if not normalized_allowed:
        return "unknown"

    if student_normalized in normalized_allowed:
        return "eligible"

    return "not_eligible"


# ============================================================
# 7. GENDER ELIGIBILITY
# ============================================================

def check_gender_eligibility(student_gender, scheme_criteria):

    criteria = normalize(scheme_criteria)

    if not criteria:
        return "unknown"

    # Recognize explicit female-only restrictions.
    female_restriction = (
        "girl students" in criteria
        or "female students" in criteria
        or "women candidates" in criteria
        or "women students" in criteria
    )

    # No recognized gender restriction.
    if not female_restriction:
        return "not_applicable"

    if not student_gender:
        return "unknown"

    gender = normalize(student_gender)

    if gender in ["female", "girl"]:
        return "eligible"

    if gender in ["male", "boy"]:
        return "not_eligible"

    return "unknown"


# ============================================================
# 8. DISABILITY ELIGIBILITY
# ============================================================

def check_disability_eligibility(
    student_disability,
    scheme_criteria,
    disability_percentage=None
):

    criteria = normalize(scheme_criteria)

    if not criteria:
        return "unknown"

    disability_required = (
        "disabilit" in criteria
        or "persons with disabilities" in criteria
    )

    if not disability_required:
        return "not_applicable"

    if student_disability is None:
        return "unknown"

    if student_disability is False:
        return "not_eligible"

    # Check for a minimum disability percentage.
    percentage_match = re.search(
        r"(\d+)\s*(?:%|percent)",
        criteria
    )

    if percentage_match:

        required_percentage = int(percentage_match.group(1))

        if disability_percentage is None:
            return "unknown"

        if disability_percentage < required_percentage:
            return "not_eligible"

    return "eligible"


# ============================================================
# 9. INSTITUTION ELIGIBILITY
# ============================================================

def check_institution_eligibility(
    student_approval,
    scheme_institutions
):

    if not student_approval or not scheme_institutions:
        return "unknown"

    student = normalize(student_approval)
    scheme = normalize(scheme_institutions)

    # AICTE approval requirement.
    if "aicte-approved" in scheme or "aicte approved" in scheme:

        if "aicte" in student:
            return "eligible"

        return "not_eligible"

    # These require checking the actual institution against
    # an official designated/approved institution list.
    verification_keywords = [
        "quality higher educational institution",
        "designated",
        "empanelled",
        "participating lender",
        "ugc-recognized",
        "ugc recognized",
        "national importance",
        "naac-accredited",
        "nba-accredited"
    ]

    if any(keyword in scheme for keyword in verification_keywords):
        return "unknown"

    return "unknown"


# ============================================================
# 10. ADMISSION TYPE ELIGIBILITY
# ============================================================

def check_admission_type_eligibility(
    student_admission,
    scheme_criteria
):

    criteria = normalize(scheme_criteria)

    if not criteria:
        return "unknown"

    requires_merit = (
        "merit-based admission" in criteria
        or "admitted on merit" in criteria
    )

    excludes_management = (
        "management quota" in criteria
        and (
            "not eligible" in criteria
            or "not be eligible" in criteria
            or "excluded" in criteria
        )
    )

    if not requires_merit and not excludes_management:
        return "not_applicable"

    if not student_admission:
        return "unknown"

    admission = normalize(student_admission)

    if admission in ["management", "management quota"]:

        if excludes_management:
            return "not_eligible"

        return "unknown"

    if requires_merit:

        if admission in ["merit", "merit-based"]:
            return "eligible"

        return "not_eligible"

    return "eligible"


# ============================================================
# 11. EDUCATION LEVEL ELIGIBILITY
# ============================================================

def get_student_education_level(course):

    course = normalize(course)

    course_mapping = {
        "b.tech": "undergraduate",
        "b.e.": "undergraduate",
        "bachelor of technology": "undergraduate",
        "bachelor of engineering": "undergraduate",
        "bca": "undergraduate",
        "b.sc": "undergraduate",
        "b.com": "undergraduate",
        "ba": "undergraduate",
        "diploma": "diploma",
        "m.tech": "postgraduate",
        "m.e.": "postgraduate",
        "mca": "postgraduate",
        "m.sc": "postgraduate",
        "mba": "postgraduate",
        "ph.d": "research",
        "phd": "research",
        "m.phil": "research"
    }

    return course_mapping.get(course)


def check_education_level_eligibility(
    student_course,
    scheme_education_level
):

    if not student_course or not scheme_education_level:
        return "unknown"

    student_level = get_student_education_level(student_course)

    if student_level is None:
        return "unknown"

    scheme_level = normalize(scheme_education_level)

    if student_level in scheme_level:
        return "eligible"

    if "higher education" in scheme_level:
        return "potentially_eligible"

    return "not_eligible"


# ============================================================
# 12. COURSE ELIGIBILITY
# ============================================================

def check_course_eligibility(student_course, scheme_courses):

    if not student_course or not scheme_courses:
        return "unknown"

    course = normalize(student_course)
    scheme = normalize(scheme_courses)

    course_mapping = {
        "b.tech": [
            "b.tech",
            "bachelor of technology",
            "technical degree"
        ],

        "b.e.": [
            "b.e.",
            "bachelor of engineering",
            "technical degree"
        ],

        "bca": [
            "bca",
            "bachelor of computer applications"
        ],

        "b.sc": [
            "b.sc",
            "bachelor of science"
        ],

        "b.com": [
            "b.com",
            "bachelor of commerce"
        ],

        "diploma": [
            "diploma",
            "technical diploma"
        ],

        "m.tech": [
            "m.tech",
            "master of technology",
            "technical postgraduate degree"
        ],

        "mca": [
            "mca",
            "master of computer applications"
        ]
    }

    student_variations = course_mapping.get(course, [course])

    # Direct course matching.
    for variation in student_variations:

        if variation in scheme:
            return "eligible"

    # General degree courses.
    student_level = get_student_education_level(course)

    if (
        student_level == "undergraduate"
        and "degree courses" in scheme
    ):
        return "eligible"

    # Technical courses may require verification against
    # the scheme's official eligible-course list.
    if (
        "professional and technical courses" in scheme
        and student_level in ["undergraduate", "postgraduate"]
    ):
        return "potentially_eligible"

    return "unknown"


# ============================================================
# 13. STATE / DOMICILE ELIGIBILITY
# ============================================================


def check_state_eligibility(
    student_domicile,
    scheme_government_level,
    scheme_state,
    scheme_name=None
):

    if not scheme_government_level:
        return "unknown"

    government_level = normalize(scheme_government_level)

    # Special condition: Ishan Uday is for North Eastern Region students
    if scheme_name and "ishan uday" in normalize(scheme_name):

        north_eastern_states = {
            "arunachal pradesh",
            "assam",
            "manipur",
            "meghalaya",
            "mizoram",
            "nagaland",
            "sikkim",
            "tripura"
        }

        if not student_domicile:
            return "unknown"

        student_state = normalize(student_domicile)

        if student_state in north_eastern_states:
            return "eligible"

        return "not_eligible"

    # Central Government schemes
    if government_level == "central":
        return "eligible"

    # State Government schemes
    if government_level == "state":

        if not student_domicile or not scheme_state:
            return "unknown"

        student_state = normalize(student_domicile)
        required_state = normalize(scheme_state)

        if student_state == required_state:
            return "eligible"

        return "not_eligible"

    return "unknown"

# ============================================================
# 14. ENTRANCE EXAM ELIGIBILITY
# ============================================================

def check_entrance_exam_eligibility(
    student_exam,
    exam_qualified,
    scheme_criteria
):

    criteria = normalize(scheme_criteria)

    if not criteria:
        return "unknown"

    has_ugc = (
        "ugc-net" in criteria
        or "ugc net" in criteria
    )

    has_csir = (
        "csir-net" in criteria
        or "csir net" in criteria
    )

    requires_jrf = "jrf" in criteria

    # Recognized UGC/CSIR NET requirement.
    if has_ugc or has_csir:

        if not student_exam or exam_qualified is None:
            return "unknown"

        if exam_qualified is False:
            return "not_eligible"

        exam = normalize(student_exam)

        is_ugc = "ugc-net" in exam or "ugc net" in exam
        is_csir = "csir-net" in exam or "csir net" in exam

        if has_ugc and has_csir:
            exam_match = is_ugc or is_csir

        elif has_ugc:
            exam_match = is_ugc

        else:
            exam_match = is_csir

        if not exam_match:
            return "not_eligible"

        if requires_jrf and "jrf" not in exam:
            return "not_eligible"

        return "eligible"

    # Other entrance-exam requirements are not yet supported
    # by this checker, so do not assume they are irrelevant.
    other_exam_keywords = [
        "entrance examination",
        "entrance exam",
        "qualifying examination",
        "qualifying exam",
        "jee",
        "neet",
        "gate",
        "cat"
    ]

    if any(keyword in criteria for keyword in other_exam_keywords):
        return "unknown"

    return "not_applicable"


# ============================================================
# 15. COMBINE ALL ELIGIBILITY CHECKS
# ============================================================

def check_basic_eligibility(student, scheme):

    scheme_name = normalize(scheme.get("scheme_name"))

    # Income check
    if "pm-vidyalaxmi" in scheme_name:

        income_result = check_loan_income_eligibility(
            student.get("annual_family_income"),
            scheme.get("scheme_name")
        )

    else:

        income_result = check_income_eligibility(
            student.get("annual_family_income"),
            scheme.get("annual_income_limit")
        )

    # Separate loan and interest subsidy checks
    loan_income_result = check_loan_income_eligibility(
        student.get("annual_family_income"),
        scheme.get("scheme_name")
    )

    interest_subvention_result = check_interest_subvention_eligibility(
        student.get("annual_family_income"),
        scheme.get("scheme_name"),
        scheme.get("annual_income_limit")
    )

    # Academic marks
    marks_result = check_marks_eligibility(
        student.get("previous_marks"),
        scheme.get("minimum_marks")
    )

    # Social category
    category_result = check_category_eligibility(
        student.get("category"),
        scheme.get("eligible_categories")
    )

    # Gender
    gender_result = check_gender_eligibility(
        student.get("gender"),
        scheme.get("eligibility_criteria")
    )

    # Disability
    disability_result = check_disability_eligibility(
        student.get("disability_status"),
        scheme.get("eligibility_criteria"),
        student.get("disability_percentage")
    )

    # Education level
    education_result = check_education_level_eligibility(
        student.get("course"),
        scheme.get("education_level")
    )

    # Course
    course_result = check_course_eligibility(
        student.get("course"),
        scheme.get("eligible_courses")
    )

    # Institution
    institution_result = check_institution_eligibility(
        student.get("institution_approval"),
        scheme.get("eligible_institutions")
    )

    # Admission type
    admission_result = check_admission_type_eligibility(
        student.get("admission_type"),
        scheme.get("eligibility_criteria")
    )

    # Domicile
    # Domicile
    state_result = check_state_eligibility(
        student.get("domicile_state"),
        scheme.get("government_level"),
        scheme.get("state_ut"),
        scheme.get("scheme_name")
    )

    # Entrance examination
    entrance_exam_result = check_entrance_exam_eligibility(
        student.get("entrance_exam"),
        student.get("entrance_exam_qualified"),
        scheme.get("eligibility_criteria")
    )

    # Core eligibility results
    results = [
        income_result,
        marks_result,
        category_result,
        gender_result,
        disability_result,
        education_result,
        course_result,
        institution_result,
        admission_result,
        state_result,
        entrance_exam_result
    ]

    # Final eligibility status
    if "not_eligible" in results:

        status = "not_eligible"

    elif (
        "unknown" in results
        or "potentially_eligible" in results
    ):

        status = "potentially_eligible"

    else:

        status = "eligible"

    return {
        "status": status,

        "checks": {
            "income": income_result,
            "marks": marks_result,
            "category": category_result,
            "gender": gender_result,
            "disability": disability_result,
            "education_level": education_result,
            "institution": institution_result,
            "admission_type": admission_result,
            "loan_income": loan_income_result,
            "interest_subvention": interest_subvention_result,
            "course": course_result,
            "state": state_result,
            "entrance_exam": entrance_exam_result
        }
    }


# ============================================================
# 16. LOCAL TESTING
# ============================================================

if __name__ == "__main__":

    student = {
        "annual_family_income": 400000,
        "previous_marks": 85,
        "category": "SC",
        "gender": "Male",
        "disability_status": False,
        "disability_percentage": None,
        "course": "B.Tech",
        "institution_approval": "AICTE Approved",
        "admission_type": "Merit",
        "domicile_state": "Karnataka",
        "entrance_exam": None,
        "entrance_exam_qualified": None
    }

    scheme = {
        "scheme_name": "Test Scheme",
        "government_level": "Central",
        "state_ut": None,
        "annual_income_limit": 800000,
        "minimum_marks": 60,
        "eligible_categories": "SC",
        "eligibility_criteria": "SC students admitted through merit",
        "education_level": "Undergraduate",
        "eligible_courses": "Technical Degree",
        "eligible_institutions": "AICTE-approved institutions"
    }

    print("BASIC ELIGIBILITY RESULT")
    print(check_basic_eligibility(student, scheme))

    print("\nCATEGORY TESTS")

    print("SC vs SC:",
          check_category_eligibility("SC", "SC"))

    print("OBC vs SC:",
          check_category_eligibility("OBC", "SC"))

    print("General vs ALL:",
          check_category_eligibility("General", "ALL"))

    print("\nGENDER TESTS")

    print("Male vs Girl Students:",
          check_gender_eligibility("Male", "Girl students only"))

    print("Female vs Girl Students:",
          check_gender_eligibility("Female", "Girl students only"))

    print("Male vs No Restriction:",
          check_gender_eligibility("Male", "Merit-based admission"))
