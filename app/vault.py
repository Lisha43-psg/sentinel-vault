from pathlib import Path


# Location of our protected data
PROTECTED_DIR = Path("data/protected")


def load_protected_documents():
    """
    Read all protected text documents from the vault.

    Returns:
        A list of dictionaries containing:
        - document name
        - document content
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


if __name__ == "__main__":

    documents = load_protected_documents()

    print("=" * 60)
    print("SENTINELVAULT - PROTECTED DATA VAULT")
    print("=" * 60)

    print(f"\nProtected documents found: {len(documents)}")

    for document in documents:

        print("\n" + "-" * 60)
        print(f"Document: {document['document']}")
        print("-" * 60)

        print(document["content"])