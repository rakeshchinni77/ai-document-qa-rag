from sentence_transformers import SentenceTransformer
from backend.app.core.config import settings
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)

class EmbeddingService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            logger.info(f"Loading SentenceTransformer model '{settings.EMBEDDING_MODEL}'...")
            cls._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("SentenceTransformer model loaded successfully.")
        return cls._instance

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        embeddings = self._model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        embedding = self._model.encode(query, show_progress_bar=False, convert_to_numpy=True)
        return embedding.tolist()
