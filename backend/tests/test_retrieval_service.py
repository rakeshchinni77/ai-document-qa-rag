import pytest
import io
from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.document_processor import DocumentProcessor
from backend.app.services.chunker import TextChunker
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore
from backend.app.core.exceptions import EmptyQueryError, EmptyVectorStoreError

@pytest.fixture(autouse=True)
def setup_teardown_store():
    store = VectorStore()
    store.clear()
    yield
    store.clear()

def test_same_embedding_model_used():
    retrieval_service = RetrievalService()
    embedding_service = EmbeddingService()
    assert retrieval_service.embedding_service is embedding_service

def test_empty_vector_store_retrieval_raises():
    retrieval_service = RetrievalService()
    with pytest.raises(EmptyVectorStoreError):
        retrieval_service.retrieve_context("What is the revenue?")

def test_empty_query_raises():
    retrieval_service = RetrievalService()
    with pytest.raises(EmptyQueryError):
        retrieval_service.retrieve_context("   ")

def test_retrieval_semantic_search_top_k():
    # 1. Ingest sample document into VectorStore
    with open("data/samples/test_document.txt", "rb") as f:
        content = f.read()

    raw_text = DocumentProcessor.extract_text("test_document.txt", content)
    chunks = TextChunker().split_text(raw_text)
    embeddings = EmbeddingService().embed_texts(chunks)
    VectorStore().add_chunks(chunks, embeddings, "test_document.txt", "txt")

    # 2. Perform semantic search via RetrievalService
    retrieval_service = RetrievalService()
    results = retrieval_service.retrieve_context("What was NovaTech reported total revenue in Q3 2026?", top_k=3)

    assert len(results) <= 3
    assert len(results) > 0
    # Verify that the target revenue information is present within the retrieved top-k chunks
    retrieved_texts = [item["text"] for item in results]
    assert any("42.5 million" in text or "revenue" in text.lower() for text in retrieved_texts)
