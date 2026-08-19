# --------------------------------------------------
# SENTINELVAULT - VAULT SERVICE
# --------------------------------------------------

from app.embeddings import (
    load_documents,
    create_chunks,
    build_index,
    search_protected_information
)


class VaultService:
    """
    Loads the protected-data vault once and reuses
    the FAISS index for multiple AI-output requests.
    """

    def __init__(self):

        print("=" * 60)
        print("SENTINELVAULT - INITIALIZING PROTECTED VAULT")
        print("=" * 60)

        # Load protected documents
        self.documents = load_documents()

        # Create searchable chunks
        self.chunks = create_chunks(
            self.documents
        )

        # Build FAISS index once
        self.index = build_index(
            self.chunks
        )

        print(
            f"\nProtected documents: "
            f"{len(self.documents)}"
        )

        print(
            f"Protected chunks: "
            f"{len(self.chunks)}"
        )

        print(
            f"Vector dimension: "
            f"{self.index.d}"
        )

        print(
            f"Vectors stored: "
            f"{self.index.ntotal}"
        )

        print("\nProtected vault ready.")
        print("=" * 60)


    def search(
        self,
        query,
        top_k=3
    ):
        """
        Search the protected vault for information
        semantically related to the query.
        """

        return search_protected_information(
            query=query,
            index=self.index,
            chunks=self.chunks,
            top_k=top_k
        )


    def get_best_match(
        self,
        query
    ):
        """
        Return the single most relevant protected
        chunk.
        """

        results = self.search(
            query=query,
            top_k=1
        )

        if not results:
            return None

        return results[0]


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    vault = VaultService()

    test_query = (
        "Arjun earns approximately "
        "12.4 lakh rupees per year."
    )

    print("\n" + "-" * 60)
    print("TEST QUERY")
    print("-" * 60)

    print(test_query)

    result = vault.get_best_match(
        test_query
    )

    if result:

        print("\nBEST MATCH")
        print("-" * 60)

        print(
            f"Document: "
            f"{result['document']}"
        )

        print(
            f"Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"Content:\n"
            f"{result['content']}"
        )

    else:

        print(
            "\nNo protected information found."
        )