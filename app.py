
from pathlib import Path

import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

from document_processor import ingest_folder
from relationship_detector import classify_relationship
from traceability_graph import build_traceability_graph
from impact_analyzer import analyze_change


# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Requirements Traceability System",
    page_icon="🔗",
    layout="wide"
)

st.title("AI-Powered Requirements Traceability")

st.write(
    "Upload requirements documents, analyze relationships, "
    "visualize the traceability graph, and identify "
    "potentially impacted requirements."
)


# --------------------------------------------------
# 2. Document upload
# --------------------------------------------------

data_folder = Path(__file__).parent / "data"
data_folder.mkdir(exist_ok=True)

uploaded_files = st.file_uploader(
    "Upload requirements documents (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = data_folder / uploaded_file.name

        # Save the uploaded document in the data folder.
        save_path.write_bytes(uploaded_file.getvalue())


# --------------------------------------------------
# 3. Extract requirements
# --------------------------------------------------

try:
    statements = ingest_folder(data_folder)

except Exception as error:
    st.error(f"Could not process requirements: {error}")
    st.stop()

if not statements:
    st.info("Upload a PDF or TXT requirements document to begin.")
    st.stop()


# --------------------------------------------------
# 4. Build traceability graph
# --------------------------------------------------

graph = build_traceability_graph(statements)


# --------------------------------------------------
# 5. Project overview
# --------------------------------------------------

st.subheader("Project Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Requirements",
    len(statements)
)

col2.metric(
    "Graph Nodes",
    graph.number_of_nodes()
)

col3.metric(
    "Relationships",
    graph.number_of_edges()
)


# --------------------------------------------------
# 6. Extracted requirements
# --------------------------------------------------

st.subheader("Extracted Requirements")

requirements_df = pd.DataFrame(statements)

st.dataframe(
    requirements_df,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# 7. Visual traceability graph
# --------------------------------------------------

st.subheader("Traceability Graph")

if graph.number_of_nodes() > 0:

    positions = nx.spring_layout(
        graph,
        seed=42,
        k=1.2
    )

    # Prepare relationship lines.
    edge_x = []
    edge_y = []

    for source, target in graph.edges():

        x0, y0 = positions[source]
        x1, y1 = positions[target]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(
            width=1.5,
            color="#8B9BB4"
        ),
        hoverinfo="none",
        name="Relationships"
    )

    # Prepare requirement nodes and visible IDs.
    node_x = []
    node_y = []
    node_labels = []
    hover_details = []

    for node_id, details in graph.nodes(data=True):

        x, y = positions[node_id]

        node_x.append(x)
        node_y.append(y)

        # Shorten IDs for easier viewing.
        short_id = (
            node_id
            .replace("sample_requirements-", "TXT-")
            .replace("System_Requirements-", "PDF-")
        )

        node_labels.append(short_id)

        hover_details.append(
            f"ID: {node_id}<br>"
            f"Requirement: {details['text']}<br>"
            f"Document: {details['document']}<br>"
            f"Source: {details['source']}"
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_labels,
        textposition="top center",
        textfont=dict(
            size=10,
            color="white"
        ),
        hovertext=hover_details,
        hovertemplate="%{hovertext}<extra></extra>",
        marker=dict(
            size=18,
            color="#1685E8",
            line=dict(
                width=1,
                color="white"
            )
        ),
        name="Requirements"
    )

    # Create the graph figure.
    figure = go.Figure(
        data=[
            edge_trace,
            node_trace
        ]
    )

    figure.update_layout(
        title="Requirements and Their Relationships",
        showlegend=False,
        hovermode="closest",
        height=750,
        margin=dict(
            l=30,
            r=30,
            t=70,
            b=30
        ),
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        plot_bgcolor="#111318",
        paper_bgcolor="#111318",
        font=dict(
            color="white"
        )
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        key="traceability_graph"
    )

    st.caption(
        "Each node represents a requirement. Each line represents "
        "a predicted relationship. Hover over a node to view its "
        "full text, document name, and source reference."
    )

else:
    st.info("No requirements are available to visualize.")


# --------------------------------------------------
# 8. Compare two requirements
# --------------------------------------------------

st.subheader("Compare Two Requirements")

statement_ids = [
    item["statement_id"]
    for item in statements
]

first_id = st.selectbox(
    "First requirement",
    statement_ids,
    key="first_requirement"
)

second_id = st.selectbox(
    "Second requirement",
    statement_ids,
    index=min(1, len(statement_ids) - 1),
    key="second_requirement"
)

first_statement = next(
    item for item in statements
    if item["statement_id"] == first_id
)

second_statement = next(
    item for item in statements
    if item["statement_id"] == second_id
)

with st.expander("View selected requirement texts"):

    st.write("**First requirement:**")
    st.write(first_statement["statement_text"])

    st.write("**Second requirement:**")
    st.write(second_statement["statement_text"])


if st.button("Analyze Relationship"):

    if first_id == second_id:

        st.warning(
            "Please select two different requirements."
        )

    else:

        result = classify_relationship(
            first_statement["statement_text"],
            second_statement["statement_text"]
        )

        st.write(
            "**Predicted relationship:**",
            result["relationship"]
        )

        st.write(
            "**Similarity score:**",
            result["similarity"]
        )

        st.write(
            "**Explanation:**",
            result["explanation"]
        )


# --------------------------------------------------
# 9. Change impact analysis
# --------------------------------------------------

st.subheader("Change Impact Analysis")

st.write(
    "Select a requirement that has changed to identify "
    "other requirements connected to it in the graph."
)

changed_id = st.selectbox(
    "Select the changed requirement",
    statement_ids,
    key="changed_requirement"
)

changed_statement = next(
    item for item in statements
    if item["statement_id"] == changed_id
)

st.write("**Selected requirement:**")
st.write(changed_statement["statement_text"])


if st.button("Analyze Impact"):

    result = analyze_change(
        graph,
        changed_id
    )

    st.write(
        "**Result:**",
        result["message"]
    )

    impacted_requirements = result[
        "impacted_requirements"
    ]

    if impacted_requirements:

        impact_df = pd.DataFrame(
            impacted_requirements
        )

        st.write(
            f"**Potentially impacted requirements: "
            f"{len(impacted_requirements)}**"
        )

        st.dataframe(
            impact_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No connected requirements were found. "
            "This does not guarantee that the change has no impact."
        )


# --------------------------------------------------
# 10. Footer
# --------------------------------------------------

st.divider()

st.caption(
    "AI-Powered Requirements Traceability and Change Impact "
    "Analysis System | Academic Project"
)
