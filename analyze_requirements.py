
from document_processor import ingest_folder
from relationship_detector import classify_relationship
from pathlib import Path
from itertools import combinations


def analyze_requirements():
    data_folder = Path(__file__).parent / "data"

    # Extract statements from every PDF and TXT document.
    statements = ingest_folder(data_folder)

    print(f"\nTotal statements: {len(statements)}")

    # Compare every unique pair of statements.
    print("\n--- Relationship Analysis ---")

    for first, second in combinations(statements, 2):
        result = classify_relationship(
            first["statement_text"],
            second["statement_text"]
        )

        print("\n-----------------------------")
        print("Statement A:", first["statement_text"])
        print("Statement B:", second["statement_text"])
        print("Relationship:", result["relationship"])
        print("Similarity:", result["similarity"])
        print("Explanation:", result["explanation"])


if __name__ == "__main__":
    analyze_requirements()
