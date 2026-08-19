from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load pretrained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


protected_text = (
    "Arjun Kumar works in the Finance department "
    "and earns 12.4 lakh rupees annually."
)


test_outputs = [
    # 1. Exact / almost exact information
    "Arjun Kumar works in the Finance department and earns 12.4 lakh rupees annually.",

    # 2. Paraphrased information
    "Arjun is part of the finance team and receives approximately 12.4 lakh per year.",

    # 3. Partially related information
    "Arjun works for the company in the finance division.",

    "Arjun works in Finance but earns only 5 lakh rupees annually.",

    # 4. Unrelated information
    "The company cafeteria serves lunch from 12 PM to 2 PM.",
]


print("=" * 60)
print("SENTINELVAULT - SEMANTIC SIMILARITY TEST")
print("=" * 60)

print("\nProtected information:")
print(protected_text)

# Generate embedding for protected text
protected_embedding = model.encode([protected_text])


for i, output in enumerate(test_outputs, start=1):

    output_embedding = model.encode([output])

    similarity = cosine_similarity(
        protected_embedding,
        output_embedding
    )[0][0]

    print("\n" + "-" * 60)
    print(f"Test Case {i}")
    print("-" * 60)

    print("AI Output:")
    print(output)

    print(f"\nSimilarity Score: {similarity:.4f}")