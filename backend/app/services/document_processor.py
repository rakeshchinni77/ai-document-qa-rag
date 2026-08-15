import os
import io
import PyPDF2
from backend.app.core.exceptions import UnsupportedFileTypeError, UnreadableDocumentError
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)

class DocumentProcessor:
    ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}

    @classmethod
    def validate_file_extension(cls, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise UnsupportedFileTypeError(
                f"Unsupported file format '{ext}'. Please upload .txt, .md, or .pdf"
            )
        return ext

    @classmethod
    def extract_text(cls, filename: str, content: bytes) -> str:
        ext = cls.validate_file_extension(filename)
        text = ""

        try:
            if ext in {".txt", ".md"}:
                text = content.decode("utf-8", errors="ignore")
            elif ext == ".pdf":
                file_stream = io.BytesIO(content)
                reader = PyPDF2.PdfReader(file_stream)
                for page_idx, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.error(f"Error parsing file {filename}: {str(e)}")
            raise UnreadableDocumentError(f"Failed to parse document '{filename}': {str(e)}")

        text = text.strip()
        if not text:
            raise UnreadableDocumentError(f"Document '{filename}' contains no readable text.")

        return text
