
import re


# 1. Check annual family income
def check_income_eligibility(student_income, scheme_income_limit):
    """
    Checks whether the student's annual family income
    satisfies the scheme's income requirement.
    """

    if student_income is None or scheme_income_limit is None:
        return "unknown"

    if student_income <= scheme_income_limit:
        return "eligible"

    return "not_eligible"


# 2. Check previous academic marks
def check_marks_eligibility(student_marks, scheme_minimum_marks):
    """
    Checks whether the student's marks satisfy
    the scheme's minimum marks requirement.
    """

    if student_marks is None or scheme_minimum_marks is None:
        return "unknown"

    if student_marks >= scheme_minimum_marks:
        return "eligible"

    return "not_eligible"


# 3. Check student category
def check_category_eligibility(student_category, scheme_category):
    """
    Checks category restrictions only when the scheme's
    category field clearly identifies a social category.

    Examples:
    SC, ST, OBC, General, ALL

    Scheme classifications such as Education Loan or
    Technical Education Scholarship are not caste categories.
    """

    if not student_category:
        return "unknown"

    if not scheme_category:
        return "unknown"

    student_category = student_category.strip().upper()
    scheme_category = scheme_category.strip().upper()

    # Scheme open to all categories
    if scheme_category in ["ALL", "ALL CATEGORIES", "ANY"]:
        return "eligible"

    # Recognized social categories
    categories = {
        "SC": ["SC", "SCHEDULED CASTE"],
        "ST": ["ST", "SCHEDULED TRIBE"],
        "OBC": ["OBC", "OTHER BACKWARD CLASS"],
        "GENERAL": ["GENERAL", "GEN", "UR", "UNRESERVED"],
        "EWS": ["EWS", "ECONOMICALLY WEAKER SECTION"]
    }

    # Find the social category specified by the scheme
    required_category = None

    for category, keywords in categories.items():
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, scheme_category):
                required_category = category
                break

        if required_category:
            break

    # No explicit social-category restriction found
    if required_category is None:
        return "unknown"

    # Find the student's normalized category
    student_normalized = None

    for category, keywords in categories.items():
        if student_category in keywords:
            student_normalized = category
            break

    if student_normalized is None:
        return "unknown"

    if student_normalized == required_category:
        return "eligible"

    return "not_eligible"

# 4. Check education-level eligibility
def check_education_level_eligibility(student_course, scheme_education_level):
    """
    Checks whether the student's course matches
    the education level supported by the scheme.
    """

    if not student_course or not scheme_education_level:
        return "unknown"

    course = student_course.strip().lower()
    scheme_level = scheme_education_level.strip().lower()

    # Map student courses to education levels
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
        "mba": "postgraduate"
    }

    student_level = course_mapping.get(course)

    if student_level is None:
        return "unknown"

    # Match the student's education level against the scheme
    if student_level in scheme_level:
        return "eligible"

    if "higher education" in scheme_level:
        return "potentially_eligible"

    return "not_eligible"
# 4. Combine all eligibility checks

# 5. Combine all eligibility checks
def check_basic_eligibility(student, scheme):
    """
    Combines income, marks, category and education-level checks.
    """

    income_result = check_income_eligibility(
        student.get("annual_family_income"),
        scheme.get("annual_income_limit")
    )

    marks_result = check_marks_eligibility(
        student.get("previous_marks"),
        scheme.get("minimum_marks")
    )

    category_result = check_category_eligibility(
        student.get("category"),
        scheme.get("category")
    )

    education_result = check_education_level_eligibility(
        student.get("course"),
        scheme.get("education_level")
    )

    results = [
        income_result,
        marks_result,
        category_result,
        education_result
    ]

    if "not_eligible" in results:
        status = "not_eligible"

    elif "unknown" in results or "potentially_eligible" in results:
        status = "potentially_eligible"

    else:
        status = "eligible"

    return {
        "status": status,
        "checks": {
            "income": income_result,
            "marks": marks_result,
            "category": category_result,
            "education_level": education_result
        }
    }

# 5. Test the eligibility functions
if __name__ == "__main__":

    student = {
        "annual_family_income": 400000,
        "previous_marks": 85,
        "category": "SC"
    }

    scheme = {
        "annual_income_limit": 800000,
        "minimum_marks": 60,
        "category": "SC"
    }

    print("Basic Eligibility:")
    print(check_basic_eligibility(student, scheme))

    print("\nCategory Eligibility Tests:")

    print("SC vs SC:",
          check_category_eligibility("SC", "SC"))

    print("OBC vs SC:",
          check_category_eligibility("OBC", "SC"))

    print("General vs ALL:",
          check_category_eligibility("General", "ALL"))

    print("SC vs Education Loan:",
          check_category_eligibility("SC", "Education Loan"))
