
from pathlib import Path
import networkx as nx

from document_processor import ingest_folder
from traceability_graph import build_traceability_graph


def analyze_change(graph, changed_statement_id):
    """Find requirements potentially affected by a change."""

    if changed_statement_id not in graph:
        return {
            "changed_requirement": changed_statement_id,
            "impacted_requirements": [],
            "message": "Requirement ID not found."
        }

    # Find requirements directly connected to the changed requirement.
    impacted_ids = list(graph.neighbors(changed_statement_id))

    # Get details of the impacted requirements.
    impacted_requirements = []

    for requirement_id in impacted_ids:
        details = graph.nodes[requirement_id]

        impacted_requirements.append({
            "statement_id": requirement_id,
            "statement_text": details["text"],
            "document": details["document"],
            "source": details["source"]
        })

    return {
        "changed_requirement": changed_statement_id,
        "impacted_requirements": impacted_requirements,
        "message": (
            "Potentially impacted requirements identified."
            if impacted_requirements
            else "No connected requirements were found."
        )
    }


if __name__ == "__main__":
    data_folder = Path(__file__).parent / "data"
    statements = ingest_folder(data_folder)
    graph = build_traceability_graph(statements)

    # Example change: update the first requirement.
    changed_id = statements[0]["statement_id"]
    result = analyze_change(graph, changed_id)

    print("\n--- Change Impact Analysis ---")
    print("Changed requirement:", result["changed_requirement"])
    print("Result:", result["message"])

    for item in result["impacted_requirements"]:
        print("\nImpacted ID:", item["statement_id"])
        print("Requirement:", item["statement_text"])
        print("Document:", item["document"])
        print("Source:", item["source"])
