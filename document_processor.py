
from pathlib import Path
import re

from pypdf import PdfReader


def split_into_statements(text):
    """Split a line of text into individual statements."""
    text = text.strip()

    # Remove common bullets and numbering, such as "1." or "-".
    text = re.sub(r"^\s*(?:[-*•]\s*|\d+[.)]\s*)", "", text)

    # Split sentences when punctuation is followed by whitespace.
    parts = re.split(r"(?<=[.!?])\s+", text)

    return [part.strip() for part in parts if part.strip()]


def extract_from_text(text, document_name, source_type):
    """Convert text into structured statement records."""
    statements = []
    statement_number = 1

    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue

        parts = split_into_statements(line)

        for part in parts:
            # Ignore very short fragments such as isolated symbols.
            if len(part) < 10:
                continue
            if part.strip().lower() in {
                "system requirements",
                "requirements",
                "introduction",
                "table of contents"
            }:
                continue

            if source_type == "pdf":
                source_reference = f"page {line_number}"
            else:
                source_reference = f"line {line_number}"

            statements.append({
                "statement_id": (
                    f"{Path(document_name).stem}-S{statement_number:03d}"
                ),
                "document_name": document_name,
                "source_reference": source_reference,
                "statement_text": part
            })

            statement_number += 1

    return statements


def ingest_document(file_path):
    """Read a PDF or TXT file and extract its statements."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = file_path.suffix.lower()
    statements = []

    if extension == ".txt":
        text = file_path.read_text(
            encoding="utf-8-sig",
            errors="replace"
        )

        statements.extend(
            extract_from_text(text, file_path.name, "txt")
        )

    elif extension == ".pdf":
        reader = PdfReader(str(file_path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            page_statements = extract_from_text(
                text,
                file_path.name,
                "pdf"
            )

            # Store the real PDF page number.
            for statement in page_statements:
                statement["source_reference"] = f"page {page_number}"

            statements.extend(page_statements)

    else:
        raise ValueError(
            "Unsupported file type. Please use a PDF or TXT file."
        )

    if not statements:
        raise ValueError(
            f"No statements extracted from {file_path.name}. "
            "Check that the file contains readable text."
        )

    return statements


def ingest_folder(folder_path):
    """Read every PDF and TXT file in a folder."""
    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    all_statements = []

    files = sorted(
        file for file in folder_path.iterdir()
        if file.is_file() and file.suffix.lower() in {".pdf", ".txt"}
    )

    for file_path in files:
        try:
            statements = ingest_document(file_path)
            all_statements.extend(statements)
            print(f"Processed {file_path.name}: {len(statements)} statements")

        except (ValueError, OSError) as error:
            print(f"Could not process {file_path.name}: {error}")

    return all_statements


if __name__ == "__main__":
    data_folder = Path(__file__).parent / "data"
    results = ingest_folder(data_folder)

    print("\n--- Extracted Statements ---")

    for item in results:
        print(f"\nID: {item['statement_id']}")
        print(f"Document: {item['document_name']}")
        print(f"Source: {item['source_reference']}")
        print(f"Statement: {item['statement_text']}")

    print(f"\nTotal statements extracted: {len(results)}")
