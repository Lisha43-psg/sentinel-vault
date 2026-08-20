import re


# --------------------------------------------------
# FACT EXTRACTION
# --------------------------------------------------

def extract_facts(text):
    """
    Extract important factual elements from text.
    This is our local development baseline.
    """

    facts = {
        "names": set(),
        "money": set(),
        "numbers": set(),
        "departments": set(),
        "dates": set(),
        "projects": set(),
        "keywords": set()
    }

    text_lower = text.lower()

    # Money / salary / financial values
    money_patterns = [
        r'\d+(?:\.\d+)?\s*(?:lakh|lakhs|crore|crores)',
        r'\d[\d,]*\s*(?:inr|rs|rupees)',
        r'₹\s*\d[\d,]*'
    ]

    for pattern in money_patterns:
        matches = re.findall(pattern, text_lower)
        facts["money"].update(matches)

    # Departments
    departments = [
        "finance", "engineering", "human resources", "hr",
        "marketing", "sales", "operations", "research",
        "development", "information technology", "it"
    ]

    for department in departments:
        if department in text_lower:
            facts["departments"].add(department)

    # Dates / years
    date_patterns = [
        r'\b\d{1,2}\s+(?:january|february|march|april|may|june|july|august|'
        r'september|october|november|december)\s+\d{4}\b',

        r'\b(?:january|february|march|april|may|june|july|august|'
        r'september|october|november|december)\s+\d{4}\b',

        r'\b20\d{2}\b'
    ]

    for pattern in date_patterns:
        matches = re.findall(pattern, text_lower)
        facts["dates"].update(matches)

    # Project names
    project_matches = re.findall(r'\bproject\s+[a-z0-9_-]+\b', text_lower)
    facts["projects"].update(project_matches)

    known_projects = ["project orion", "project atlas"]
    for project in known_projects:
        if project in text_lower:
            facts["projects"].add(project)

    # Important numeric values
    numeric_matches = re.findall(r'\b\d+(?:\.\d+)?\b', text_lower)
    facts["numbers"].update(numeric_matches)

    # Security-sensitive keywords
    sensitive_keywords = [
        "salary", "manager", "employee", "customer", "contract",
        "revenue", "profit", "budget", "internal", "confidential",
        "launch date", "annual", "financial"
    ]

    for keyword in sensitive_keywords:
        if keyword in text_lower:
            facts["keywords"].add(keyword)

    return facts


# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------

def normalize_money(value):
    """
    Normalize common representations of money.
    12.4 lakh and 1240000 INR are treated as equivalent.
    """

    value = value.lower().strip()

    lakh_match = re.search(r'(\d+(?:\.\d+)?)\s*lakh', value)
    if lakh_match:
        amount = float(lakh_match.group(1))
        return round(amount * 100000)

    crore_match = re.search(r'(\d+(?:\.\d+)?)\s*crore', value)
    if crore_match:
        amount = float(crore_match.group(1))
        return round(amount * 10000000)

    number_match = re.search(r'\d[\d,]*', value)
    if number_match:
        return int(number_match.group(0).replace(",", ""))

    return None


# --------------------------------------------------
# MONEY COMPARISON
# --------------------------------------------------

def money_overlap(protected_facts, output_facts):
    """
    Compare financial values between protected information
    and AI output. Detects exact matches and conflicts.
    """

    protected_values = []
    for value in protected_facts["money"]:
        normalized = normalize_money(value)
        if normalized is not None:
            protected_values.append(normalized)

    output_values = []
    for value in output_facts["money"]:
        normalized = normalize_money(value)
        if normalized is not None:
            output_values.append(normalized)

    if not protected_values or not output_values:
        return {"match": False, "contradiction": False}

    for protected_value in protected_values:
        for output_value in output_values:
            if protected_value == output_value:
                return {"match": True, "contradiction": False}

    return {"match": False, "contradiction": True}


# --------------------------------------------------
# FACTUAL OVERLAP
# --------------------------------------------------

def check_factual_overlap(ai_output, protected_context):
    """
    Compare AI output with protected information.
    Returns: MATCH, PARTIAL, CONTRADICTION, or NONE
    """

    protected = extract_facts(protected_context)
    output = extract_facts(ai_output)

    matched_facts = []
    contradicted_facts = []

    # Money
    money_result = money_overlap(protected, output)

    if money_result["match"]:
        matched_facts.append("matching financial information")

    if money_result["contradiction"]:
        contradicted_facts.append("conflicting financial information")

    # Departments
    common_departments = protected["departments"] & output["departments"]
    if common_departments:
        matched_facts.extend(list(common_departments))

    # Projects
    common_projects = protected["projects"] & output["projects"]
    if common_projects:
        matched_facts.extend(list(common_projects))

    # Dates
    common_dates = protected["dates"] & output["dates"]
    if common_dates:
        matched_facts.extend(list(common_dates))

    # Sensitive keywords — assigned before it is ever read below
    common_keywords = protected["keywords"] & output["keywords"]

    if common_keywords:
        matched_facts.extend(list(common_keywords))

    # Relationship classification
    if contradicted_facts:
        relationship = "CONTRADICTION"

    elif matched_facts:
        if len(matched_facts) >= 2 or money_result["match"]:
            relationship = "MATCH"
        else:
            relationship = "PARTIAL"

    elif common_keywords:
        relationship = "PARTIAL"

    else:
        relationship = "NONE"

    # Overlap score
    total_signals = (
        len(protected["departments"])
        + len(protected["projects"])
        + len(protected["dates"])
        + len(protected["money"])
        + len(protected["keywords"])
    )

    matched_signal_count = len(matched_facts) + len(common_keywords)

    if total_signals == 0:
        overlap_score = 0.0
    else:
        overlap_score = matched_signal_count / total_signals

    if relationship == "CONTRADICTION":
        overlap_score = 0.75

    overlap_score = round(min(overlap_score, 1.0), 2)

    return {
        "relationship": relationship,
        "overlap_score": overlap_score,
        "exposed_facts": matched_facts,
        "contradicted_facts": contradicted_facts,
        "explanation": generate_explanation(
            relationship, matched_facts, contradicted_facts
        )
    }


# --------------------------------------------------
# EXPLANATION
# --------------------------------------------------

def generate_explanation(relationship, matched_facts, contradicted_facts):

    if relationship == "MATCH":
        return (
            "The AI output contains factual information "
            "that overlaps with protected information."
        )

    if relationship == "PARTIAL":
        return (
            "The AI output reveals some information "
            "associated with the protected context."
        )

    if relationship == "CONTRADICTION":
        return (
            "The AI output discusses protected information "
            "but contains a conflicting factual value."
        )

    return "No meaningful factual overlap was detected."


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    protected_information = """
    Employee ID: EMP001
    Name: Arjun Kumar
    Department: Finance
    Salary: 1240000 INR annually
    Manager: Priya Sharma
    Joining Date: 14 June 2023
    """

    test_outputs = [
        "Arjun earns approximately 12.4 lakh rupees per year.",
        "Arjun works in Finance but earns only 5 lakh rupees annually.",
        "Arjun works in the Finance department.",
        "The company cafeteria serves lunch from 12 PM to 2 PM."
    ]

    print("=" * 60)
    print("SENTINELVAULT - FACTUAL OVERLAP BASELINE")
    print("=" * 60)

    for number, output in enumerate(test_outputs, start=1):
        print("\n" + "=" * 60)
        print(f"TEST CASE {number}")
        print("=" * 60)
        print("\nAI Output:")
        print(output)

        result = check_factual_overlap(
            ai_output=output,
            protected_context=protected_information
        )

        print("\nFACTUAL ANALYSIS")
        print("-" * 60)
        print(f"Relationship: {result['relationship']}")
        print(f"Overlap Score: {result['overlap_score']}")
        print(f"Exposed Facts: {result['exposed_facts']}")
        print(f"Contradicted Facts: {result['contradicted_facts']}")
        print(f"Explanation: {result['explanation']}")