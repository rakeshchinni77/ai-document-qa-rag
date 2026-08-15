import pytest
import io
import PyPDF2
from backend.app.services.document_processor import DocumentProcessor
from backend.app.core.exceptions import UnsupportedFileTypeError, UnreadableDocumentError

def test_extract_txt():
    content = "Hello, this is a plain text file for RAG processing.".encode("utf-8")
    extracted = DocumentProcessor.extract_text("test.txt", content)
    assert extracted == "Hello, this is a plain text file for RAG processing."

def test_extract_md():
    content = "# Title\n\nThis is a **markdown** file.".encode("utf-8")
    extracted = DocumentProcessor.extract_text("test.md", content)
    assert "# Title" in extracted
    assert "markdown" in extracted

def test_extract_pdf_valid():
    # Generate a simple in-memory PDF using PyPDF2 Writer
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=100, height=100)
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    
    # Text extraction on PDF (even if blank page returns empty text check)
    with pytest.raises(UnreadableDocumentError):
        DocumentProcessor.extract_text("empty.pdf", pdf_bytes.getvalue())

def test_unsupported_file_extension():
    with pytest.raises(UnsupportedFileTypeError):
        DocumentProcessor.validate_file_extension("data.csv")

    with pytest.raises(UnsupportedFileTypeError):
        DocumentProcessor.validate_file_extension("image.png")

def test_empty_document_raises_unreadable():
    with pytest.raises(UnreadableDocumentError):
        DocumentProcessor.extract_text("empty.txt", b"   \n\t  ")
