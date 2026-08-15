from backend.app.core.config import settings
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)

class TextChunker:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be strictly less than chunk_size")

    def split_text(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []

        text = text.strip()
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0
        step = self.chunk_size - self.chunk_overlap

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # If we reached or surpassed the end of text, break
            if end >= len(text):
                break
                
            start += step

        logger.info(f"Split text into {len(chunks)} chunks (size={self.chunk_size}, overlap={self.chunk_overlap})")
        return chunks
