
import networkx as nx


def build_traceability_graph(statements):
    """Build a graph containing requirements and their relationships."""

    graph = nx.Graph()

    # Add each requirement as a node.
    for statement in statements:
        graph.add_node(
            statement["statement_id"],
            text=statement["statement_text"],
            document=statement["document_name"],
            source=statement["source_reference"]
        )

    # Compare each pair of requirements.
    from itertools import combinations
    from relationship_detector import classify_relationship

    for first, second in combinations(statements, 2):
        result = classify_relationship(
            first["statement_text"],
            second["statement_text"]
        )

        # Store related relationships as graph edges.
        if result["relationship"] in [
            "Direct Dependency",
            "Related"
        ]:
            graph.add_edge(
                first["statement_id"],
                second["statement_id"],
                relationship=result["relationship"],
                similarity=result["similarity"],
                explanation=result["explanation"]
            )

    return graph


if __name__ == "__main__":
    from pathlib import Path
    from document_processor import ingest_folder

    data_folder = Path(__file__).parent / "data"
    statements = ingest_folder(data_folder)

    graph = build_traceability_graph(statements)

    print("\n--- Traceability Graph ---")
    print("Number of requirements:", graph.number_of_nodes())
    print("Number of relationships:", graph.number_of_edges())

    print("\nRelationships:")
    for first, second, details in graph.edges(data=True):
        print(f"\n{first} <--> {second}")
        print("Type:", details["relationship"])
        print("Similarity:", details["similarity"])
        print("Explanation:", details["explanation"])
