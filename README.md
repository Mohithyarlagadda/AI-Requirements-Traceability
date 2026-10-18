# AI-Powered Requirements Traceability and Change Impact Analysis System

## 🚀 Live Application

**Try the application here:**  
https://ai-requirements-traceability-jbkbbaut9cp2rlcscscohw.streamlit.app/

## 📌 Project Overview

This project is designed to analyze software requirements, identify relationships between statements, build a traceability graph, and determine potentially impacted requirements when a requirement changes.

It supports PDF and TXT document inputs and provides explanations for predicted relationships.

## ✨ Features

- Extract requirements from PDF and TXT documents.
- Identify relationships as Direct Dependency, Related, or Unrelated.
- Display a traceability graph.
- Compare two requirements and view prediction explanations.
- Analyze potential impacts of requirement changes.
- Display extracted requirements and project metrics.

## 🛠️ Technologies Used

- Python
- Streamlit
- Scikit-learn
- NetworkX
- Plotly
- PyPDF

## 📂 Project Structure

```text
AI-Requirements-Traceability/
├── app.py
├── analyze_requirements.py
├── document_processor.py
├── relationship_detector.py
├── traceability_graph.py
├── impact_analyzer.py
├── requirements.txt
├── README.md
├── data/
└── tests/
```

## ▶️ Run Locally

1. Clone this repository:

   ```bash
   git clone https://github.com/Mohithyarlagadda/AI-Requirements-Traceability.git
   ```

2. Open the project folder:

   ```bash
   cd AI-Requirements-Traceability
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   streamlit run app.py
   ```

## 👨‍💻 Source Code

GitHub Repository:  
https://github.com/Mohithyarlagadda/AI-Requirements-Traceability

## ⚠️ Note

Relationship classification and change impact results are predictions intended to support requirements analysis. They should be reviewed by a human before making engineering decisions.
