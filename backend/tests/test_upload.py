import io
import pytest
import PyPDF2
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_upload_valid_txt_file():
    txt_content = b"In Q3 2026, NovaTech Solutions reported total revenue of $42.5 million, representing a 15% increase year-over-year."
    response = client.post(
        "/upload",
        files={"file": ("sample.txt", io.BytesIO(txt_content), "text/plain")}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "File uploaded and indexed successfully."
    assert data["filename"] == "sample.txt"
    assert data["chunks_indexed"] >= 1

def test_upload_valid_md_file():
    md_content = b"# Architecture Overview\n\nThe RAG pipeline uses ChromaDB for persistent vector search and MiniLM for embeddings."
    response = client.post(
        "/upload",
        files={"file": ("architecture.md", io.BytesIO(md_content), "text/markdown")}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "architecture.md"
    assert data["chunks_indexed"] >= 1

def test_upload_rejection_png():
    response = client.post(
        "/upload",
        files={"file": ("image.png", io.BytesIO(b"fake image data"), "image/png")}
    )
    assert response.status_code == 400
    data = response.json()
    assert "Unsupported file format" in data["detail"]

def test_upload_rejection_csv():
    response = client.post(
        "/upload",
        files={"file": ("data.csv", io.BytesIO(b"col1,col2\nval1,val2"), "text/csv")}
    )
    assert response.status_code == 400
    data = response.json()
    assert "Unsupported file format" in data["detail"]

def test_upload_empty_txt_file():
    empty_content = b"   "
    response = client.post(
        "/upload",
        files={"file": ("empty.txt", io.BytesIO(empty_content), "text/plain")}
    )
    assert response.status_code == 400
    data = response.json()
    assert "contains no readable text" in data["detail"]

def test_upload_empty_pdf_file():
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=100, height=100)
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)

    response = client.post(
        "/upload",
        files={"file": ("blank.pdf", pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 400
    data = response.json()
    assert "contains no readable text" in data["detail"]
