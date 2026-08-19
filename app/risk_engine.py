# --------------------------------------------------
# SENTINELVAULT - RISK ENGINE
# --------------------------------------------------

def calculate_risk(
    semantic_score,
    factual_result
):
    """
    Combine semantic similarity and factual analysis
    into an explainable risk score.

    Returns:
        risk_score
        decision
        risk_level
        reasons
    """

    relationship = factual_result.get(
        "relationship",
        "NONE"
    )

    factual_score = factual_result.get(
        "overlap_score",
        0.0
    )

    exposed_facts = factual_result.get(
        "exposed_facts",
        []
    )

    contradicted_facts = factual_result.get(
        "contradicted_facts",
        []
    )


    # --------------------------------------------------
    # CONTRADICTION HANDLING
    # --------------------------------------------------

    # A contradiction should not be treated as a
    # confirmed protected-data leak.

    if relationship == "CONTRADICTION":

        risk_score = semantic_score * 25

        decision = "ALLOW"

        risk_level = "LOW"

        reasons = [
            "Semantic relationship with protected data detected",
            "Factual checker identified a contradiction",
            "No confirmed protected fact disclosure"
        ]

        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "decision": decision,
            "reasons": reasons,
            "factual_relationship": relationship
        }


    # --------------------------------------------------
    # FACTUAL WEIGHTS
    # --------------------------------------------------

    if relationship == "MATCH":

        factual_weight = 0.90

    elif relationship == "PARTIAL":

        factual_weight = 0.50

    else:

        factual_weight = 0.0


    # --------------------------------------------------
    # SEMANTIC WEIGHT
    # --------------------------------------------------

    semantic_weight = 0.40


    # --------------------------------------------------
    # CALCULATE BASE RISK
    # --------------------------------------------------

    risk_score = (
        semantic_score * semantic_weight
        +
        factual_weight * 0.60
    ) * 100


    # --------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------

    reasons = []


    if semantic_score >= 0.80:

        reasons.append(
            "Very high semantic similarity with protected data"
        )

    elif semantic_score >= 0.60:

        reasons.append(
            "High semantic similarity with protected data"
        )

    elif semantic_score >= 0.40:

        reasons.append(
            "Moderate semantic similarity with protected data"
        )

    else:

        reasons.append(
            "Low semantic similarity with protected data"
        )


    if relationship == "MATCH":

        reasons.append(
            "Protected facts were factually matched"
        )

    elif relationship == "PARTIAL":

        reasons.append(
            "Some protected facts were exposed"
        )

    elif relationship == "NONE":

        reasons.append(
            "No meaningful factual overlap detected"
        )


    if exposed_facts:

        reasons.append(
            "Exposed facts: "
            + ", ".join(exposed_facts)
        )


    # --------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------

    if risk_score >= 70:

        decision = "BLOCK"

        risk_level = "HIGH"


    elif risk_score >= 35:

        decision = "REVIEW"

        risk_level = "MEDIUM"


    else:

        decision = "ALLOW"

        risk_level = "LOW"


    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "decision": decision,
        "reasons": reasons,
        "factual_relationship": relationship
    }


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("SENTINELVAULT - RISK ENGINE")
    print("=" * 60)


    test_cases = [

        {
            "name": "Confirmed salary disclosure",
            "semantic_score": 0.8526,
            "factual_result": {
                "relationship": "MATCH",
                "overlap_score": 0.90,
                "exposed_facts": [
                    "matching financial information"
                ],
                "contradicted_facts": []
            }
        },


        {
            "name": "Contradictory salary",
            "semantic_score": 0.8526,
            "factual_result": {
                "relationship": "CONTRADICTION",
                "overlap_score": 0.75,
                "exposed_facts": [
                    "finance"
                ],
                "contradicted_facts": [
                    "conflicting financial information"
                ]
            }
        },


        {
            "name": "Partial department disclosure",
            "semantic_score": 0.6805,
            "factual_result": {
                "relationship": "PARTIAL",
                "overlap_score": 0.11,
                "exposed_facts": [
                    "finance"
                ],
                "contradicted_facts": []
            }
        },


        {
            "name": "Unrelated information",
            "semantic_score": 0.0718,
            "factual_result": {
                "relationship": "NONE",
                "overlap_score": 0.0,
                "exposed_facts": [],
                "contradicted_facts": []
            }
        }
    ]


    for number, test in enumerate(
        test_cases,
        start=1
    ):

        print("\n" + "=" * 60)

        print(
            f"TEST CASE {number}: "
            f"{test['name']}"
        )

        print("=" * 60)


        result = calculate_risk(
            semantic_score=test["semantic_score"],
            factual_result=test["factual_result"]
        )


        print(
            f"\nSemantic Score: "
            f"{test['semantic_score']}"
        )

        print(
            f"Factual Relationship: "
            f"{result['factual_relationship']}"
        )

        print(
            f"Risk Score: "
            f"{result['risk_score']}/100"
        )

        print(
            f"Risk Level: "
            f"{result['risk_level']}"
        )

        print(
            f"Decision: "
            f"{result['decision']}"
        )

        print("\nReasons:")

        for reason in result["reasons"]:

            print(
                f"  - {reason}"
            )