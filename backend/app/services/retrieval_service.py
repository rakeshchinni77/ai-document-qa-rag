from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore
from backend.app.core.exceptions import EmptyVectorStoreError, EmptyQueryError
from backend.app.core.config import settings
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)

class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve_context(self, question: str, top_k: int = None) -> list[dict]:
        if not question or not question.strip():
            raise EmptyQueryError("Question field cannot be empty.")

        if self.vector_store.count() == 0:
            raise EmptyVectorStoreError("No documents have been indexed yet. Please upload a document first.")

        k = top_k or settings.TOP_K
        query_embedding = self.embedding_service.embed_query(question.strip())
        results = self.vector_store.search_similar(query_embedding, top_k=k)
        
        logger.info(f"Retrieved {len(results)} chunks for query: '{question[:50]}...'")
        return results
