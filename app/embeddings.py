from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROTECTED_DIR = Path("data/protected")

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# --------------------------------------------------
# Load protected documents
# --------------------------------------------------

def load_documents():
    """
    Load all protected text files.
    """

    documents = []

    for file_path in PROTECTED_DIR.glob("*.txt"):

        content = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "document": file_path.name,
            "content": content
        })

    return documents


# --------------------------------------------------
# Create chunks
# --------------------------------------------------

def create_chunks(documents):
    """
    Split protected documents into smaller chunks.

    For our initial version, each non-empty paragraph
    becomes a separate chunk.
    """

    chunks = []

    for document in documents:

        paragraphs = document["content"].split("\n\n")

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if paragraph:

                chunks.append({
                    "document": document["document"],
                    "content": paragraph
                })

    return chunks


# --------------------------------------------------
# Create vector index
# --------------------------------------------------

def build_index(chunks):
    """
    Convert chunks into embeddings and store them
    inside a FAISS vector index.
    """

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


# --------------------------------------------------
# Search protected information
# --------------------------------------------------

def search_protected_information(
    query,
    index,
    chunks,
    top_k=3
):
    """
    Search the protected vault for the most
    semantically similar chunks.
    """

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        results.append({
            "document": chunks[index_position]["document"],
            "content": chunks[index_position]["content"],
            "similarity": float(score)
        })

    return results


# --------------------------------------------------
# Test the vector vault
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("SENTINELVAULT - VECTOR VAULT")
    print("=" * 60)

    documents = load_documents()

    print(
        f"\nDocuments loaded: {len(documents)}"
    )

    chunks = create_chunks(documents)

    print(
        f"Chunks created: {len(chunks)}"
    )

    index = build_index(chunks)

    print(
        f"Vector dimension: {index.d}"
    )

    print(
        f"Vectors stored: {index.ntotal}"
    )

    # Test query
    test_query = (
        "Arjun earns approximately "
        "12.4 lakh rupees per year."
    )

    print("\n" + "-" * 60)
    print("TEST QUERY")
    print("-" * 60)

    print(test_query)

    results = search_protected_information(
        test_query,
        index,
        chunks,
        top_k=3
    )

    print("\nMOST RELEVANT PROTECTED INFORMATION:")

    for result in results:

        print("\n" + "-" * 60)

        print(
            f"Document: {result['document']}"
        )

        print(
            f"Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"Content:\n{result['content']}"
        )