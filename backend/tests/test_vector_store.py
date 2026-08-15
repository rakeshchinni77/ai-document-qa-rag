import pytest
import os
import chromadb
from backend.app.services.vector_store import VectorStore
from backend.app.services.embedding_service import EmbeddingService
from backend.app.core.config import settings

@pytest.fixture(autouse=True)
def setup_teardown_vector_store():
    store = VectorStore()
    store.clear()
    yield
    store.clear()

def test_create_collection():
    store = VectorStore()
    assert store._collection is not None
    assert store._collection.name == "document_qa_collection"

def test_add_and_retrieve_vector():
    store = VectorStore()
    embedding_service = EmbeddingService()
    
    chunks = ["Enterprise RAG Document QA Pipeline.", "ChromaDB vector store storage."]
    embeddings = embedding_service.embed_texts(chunks)
    
    ids = store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename="test_architecture.pdf",
        file_type="pdf"
    )
    
    assert len(ids) == 2
    assert store.count() == 2

def test_query_vector_similarity():
    store = VectorStore()
    embedding_service = EmbeddingService()
    
    chunks = [
        "NovaTech reported Q3 revenue of $42.5 million.",
        "System architecture uses sentence-transformers for vector embeddings.",
        "Supply chain disruptions moved data center deployment to Q4."
    ]
    embeddings = embedding_service.embed_texts(chunks)
    store.add_chunks(chunks=chunks, embeddings=embeddings, filename="report.txt", file_type="txt")
    
    query_vec = embedding_service.embed_query("What was NovaTech revenue in Q3?")
    results = store.search_similar(query_vec, top_k=2)
    
    assert len(results) == 2
    assert "42.5 million" in results[0]["text"]

def test_metadata_retrieval():
    store = VectorStore()
    embedding_service = EmbeddingService()
    
    chunks = ["Sample metadata test chunk."]
    embeddings = embedding_service.embed_texts(chunks)
    store.add_chunks(chunks=chunks, embeddings=embeddings, filename="sample.md", file_type="md")
    
    query_vec = embedding_service.embed_query("Sample metadata")
    results = store.search_similar(query_vec, top_k=1)
    
    meta = results[0]["metadata"]
    assert meta["filename"] == "sample.md"
    assert meta["chunk_index"] == 0
    assert meta["file_type"] == "md"

def test_persistence_after_restart():
    store = VectorStore()
    embedding_service = EmbeddingService()
    
    chunks = ["Persistent storage vector chunk across server restart."]
    embeddings = embedding_service.embed_texts(chunks)
    store.add_chunks(chunks=chunks, embeddings=embeddings, filename="persistent_doc.txt", file_type="txt")
    
    # Verify count is 1
    assert store.count() == 1
    
    # Simulate Server Shutdown & Restart by instantiating a new PersistentClient directly from disk
    persistent_client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
    reloaded_collection = persistent_client.get_collection(name="document_qa_collection")
    
    # Query reloaded collection directly from disk
    query_vec = embedding_service.embed_query("Persistent storage")
    res = reloaded_collection.query(query_embeddings=[query_vec], n_results=1)
    
    assert len(res["documents"][0]) == 1
    assert "Persistent storage vector chunk" in res["documents"][0][0]
