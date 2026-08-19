from embeddings import (
    load_documents,
    create_chunks,
    build_index,
    search_protected_information
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

# This is NOT our final risk threshold.
# It is only used to decide whether something
# is worth investigating further.
RETRIEVAL_THRESHOLD = 0.50


# --------------------------------------------------
# Build the protected-data index
# --------------------------------------------------

def initialize_detector():
    """
    Load protected documents, create chunks,
    and build the FAISS vector index.
    """

    documents = load_documents()

    chunks = create_chunks(documents)

    index = build_index(chunks)

    return index, chunks


# --------------------------------------------------
# Analyze AI output
# --------------------------------------------------

def analyze_output(
    output,
    index,
    chunks,
    top_k=3
):
    """
    Analyze an AI-generated output against
    the protected data vault.
    """

    results = search_protected_information(
        output,
        index,
        chunks,
        top_k=top_k
    )

    # Keep only sufficiently relevant matches
    relevant_results = [
        result
        for result in results
        if result["similarity"] >= RETRIEVAL_THRESHOLD
    ]

    # If nothing relevant was found
    if not relevant_results:

        return {
            "output": output,
            "potential_leak": False,
            "message": "No strongly related protected information found.",
            "matches": []
        }

    # Highest similarity result
    strongest_match = relevant_results[0]

    return {
        "output": output,
        "potential_leak": True,
        "message": "Potential protected-data overlap detected.",
        "strongest_match": strongest_match,
        "matches": relevant_results
    }


# --------------------------------------------------
# Test detector
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("SENTINELVAULT - SEMANTIC LEAK DETECTOR")
    print("=" * 60)

    # Build detector
    index, chunks = initialize_detector()

    print(
        f"\nProtected chunks indexed: {index.ntotal}"
    )

    # Test outputs
    test_outputs = [

        # Paraphrased protected information
        "Arjun earns approximately 12.4 lakh rupees per year.",

        # Unrelated information
        "The company cafeteria serves lunch from 12 PM to 2 PM.",

        # Project information
        "Project Orion is expected to launch in December 2026."
    ]

    for output in test_outputs:

        print("\n" + "=" * 60)
        print("AI OUTPUT")
        print("=" * 60)

        print(output)

        result = analyze_output(
            output,
            index,
            chunks
        )

        print("\n" + "-" * 60)

        if result["potential_leak"]:

            print("🚨 POTENTIAL DATA OVERLAP DETECTED")

            strongest = result["strongest_match"]

            print(
                f"\nSimilarity: "
                f"{strongest['similarity']:.4f}"
            )

            print(
                f"Source: "
                f"{strongest['document']}"
            )

            print("\nMatched protected information:")

            print(
                strongest["content"]
            )

        else:

            print("🟢 NO STRONG PROTECTED-DATA MATCH")

        print("-" * 60)