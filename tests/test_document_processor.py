
from document_processor import ingest_document


def test_txt_ingestion(tmp_path):
    # Create a temporary TXT file for testing.
    file_path = tmp_path / "test_requirements.txt"
    file_path.write_text(
        "1. The system shall allow user login.\n"
        "2. The system shall record user activity.\n",
        encoding="utf-8"
    )

    results = ingest_document(file_path)

    assert len(results) == 2
    assert results[0]["document_name"] == "test_requirements.txt"
    assert results[0]["statement_id"] == "test_requirements-S001"
    assert "allow user login" in results[0]["statement_text"]
    assert results[1]["statement_id"] == "test_requirements-S002"


def test_unsupported_file_type(tmp_path):
    file_path = tmp_path / "requirements.docx"
    file_path.write_text("Example", encoding="utf-8")

    try:
        ingest_document(file_path)
        assert False, "Expected ValueError for unsupported file"
    except ValueError as error:
        assert "Unsupported file type" in str(error)
