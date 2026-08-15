import pytest
from backend.app.services.embedding_service import EmbeddingService

def test_embedding_service_singleton():
    service1 = EmbeddingService()
    service2 = EmbeddingService()
    assert service1 is service2

def test_embed_single_text_shape():
    service = EmbeddingService()
    embeddings = service.embed_texts(["hello world"])
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384
    assert isinstance(embeddings[0][0], float)

def test_embed_query_shape():
    service = EmbeddingService()
    query_vector = service.embed_query("what is the financial report?")
    assert len(query_vector) == 384
    assert isinstance(query_vector[0], float)

def test_embed_multiple_chunks():
    service = EmbeddingService()
    chunks = [
        "Chunk 1: Financial revenue highlights.",
        "Chunk 2: System architecture and RAG pipeline.",
        "Chunk 3: Security and compliance protocols.",
        "Chunk 4: Vector embedding and ChromaDB storage.",
        "Chunk 5: Evaluation metrics context precision."
    ]
    embeddings = service.embed_texts(chunks)
    assert len(embeddings) == 5
    for vec in embeddings:
        assert len(vec) == 384
