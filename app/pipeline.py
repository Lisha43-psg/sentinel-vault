import os
import sys

# Allow imports from the app directory
sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

from embeddings import (
    load_documents,
    create_chunks,
    build_index,
    search_protected_information
)

from llm_factual_checker import check_factual_overlap
from risk_engine import calculate_risk


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

SEMANTIC_THRESHOLD = 0.60


# --------------------------------------------------
# ANALYZE AI OUTPUT
# --------------------------------------------------

def analyze_ai_output(ai_output):

    print("\n" + "=" * 70)
    print("SENTINELVAULT - AI OUTPUT SECURITY ANALYSIS")
    print("=" * 70)

    print("\nAI OUTPUT:")
    print(ai_output)


    # --------------------------------------------------
    # LOAD PROTECTED VAULT
    # --------------------------------------------------

    print("\n" + "-" * 70)
    print("LOADING PROTECTED DATA")
    print("-" * 70)

    documents = load_documents()

    chunks = create_chunks(
        documents
    )

    index = build_index(
        chunks
    )

    print(
        f"Protected documents: "
        f"{len(documents)}"
    )

    print(
        f"Protected chunks: "
        f"{len(chunks)}"
    )

    print(
        f"Vector dimension: "
        f"{index.d}"
    )


    # --------------------------------------------------
    # SEMANTIC SEARCH
    # --------------------------------------------------

    print("\n" + "-" * 70)
    print("SEMANTIC ANALYSIS")
    print("-" * 70)

    results = search_protected_information(
        ai_output,
        index,
        chunks,
        top_k=3
    )


    # No results
    if not results:

        print(
            "No protected information matched."
        )

        semantic_score = 0.0

        matched_chunk = {
            "document": "None",
            "content": ""
        }

    else:

        matched_chunk = results[0]

        semantic_score = (
            matched_chunk["similarity"]
        )

        print(
            f"Similarity Score: "
            f"{semantic_score:.4f}"
        )

        print(
            f"Source: "
            f"{matched_chunk['document']}"
        )

        print(
            "\nMatched Protected Information:"
        )

        print(
            matched_chunk["content"]
        )


        # Show additional matches

        if len(results) > 1:

            print(
                "\nOther relevant protected chunks:"
            )

            for result in results[1:]:

                print(
                    f"\n  {result['document']} "
                    f"→ "
                    f"{result['similarity']:.4f}"
                )


    # --------------------------------------------------
    # FACTUAL ANALYSIS
    # --------------------------------------------------

    print("\n" + "-" * 70)
    print("FACTUAL ANALYSIS")
    print("-" * 70)


    if (
        results
        and semantic_score >= SEMANTIC_THRESHOLD
    ):

        factual_result = check_factual_overlap(
            ai_output=ai_output,
            protected_context=matched_chunk["content"]
        )

    else:

        factual_result = {
            "relationship": "NONE",
            "overlap_score": 0.0,
            "exposed_facts": [],
            "contradicted_facts": [],
            "explanation": (
                "Semantic similarity is below "
                "the factual-analysis threshold."
            )
        }


    print(
        f"Relationship: "
        f"{factual_result['relationship']}"
    )

    print(
        f"Factual Score: "
        f"{factual_result['overlap_score']}"
    )

    print(
        f"Exposed Facts: "
        f"{factual_result['exposed_facts']}"
    )

    print(
        f"Contradicted Facts: "
        f"{factual_result['contradicted_facts']}"
    )

    print(
        f"Explanation: "
        f"{factual_result['explanation']}"
    )


    # --------------------------------------------------
    # RISK ENGINE
    # --------------------------------------------------

    print("\n" + "-" * 70)
    print("RISK ANALYSIS")
    print("-" * 70)

    risk_result = calculate_risk(
        semantic_score=semantic_score,
        factual_result=factual_result
    )


    print(
        f"Risk Score: "
        f"{risk_result['risk_score']}/100"
    )

    print(
        f"Risk Level: "
        f"{risk_result['risk_level']}"
    )

    print(
        f"Decision: "
        f"{risk_result['decision']}"
    )


    print("\nReasons:")

    for reason in risk_result["reasons"]:

        print(
            f"  - {reason}"
        )


    # --------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------

    print("\n" + "=" * 70)

    print(
        f"FINAL DECISION: "
        f"{risk_result['decision']}"
    )

    print("=" * 70)


    return {
        "ai_output": ai_output,
        "semantic_score": semantic_score,
        "matched_chunk": matched_chunk,
        "factual_result": factual_result,
        "risk_result": risk_result
    }


# --------------------------------------------------
# DEMO
# --------------------------------------------------

if __name__ == "__main__":

    test_outputs = [

        "Arjun earns approximately 12.4 lakh rupees per year.",

        "Arjun works in Finance but earns only 5 lakh rupees annually.",

        "Arjun works in the Finance department.",

        "The company cafeteria serves lunch from 12 PM to 2 PM."
    ]


    for output in test_outputs:

        analyze_ai_output(
            output
        )