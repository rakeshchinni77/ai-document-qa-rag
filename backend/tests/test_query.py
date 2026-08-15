import io
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.vector_store import VectorStore
from backend.app.services.llm_service import LLMService

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_vector_store():
    store = VectorStore()
    store.clear()
    yield
    store.clear()

def test_query_empty_question():
    response = client.post("/query", json={"question": ""})
    assert response.status_code == 400
    data = response.json()
    assert "cannot be empty" in data["detail"]

def test_query_no_documents_indexed():
    response = client.post("/query", json={"question": "What is the revenue?"})
    assert response.status_code == 400
    data = response.json()
    assert "No documents have been indexed yet" in data["detail"]

def test_query_successful_rag_with_exact_sources():
    # 1. Ingest document via /upload
    doc_content = b"In Q3 2026, NovaTech Solutions reported total revenue of $42.5 million, representing a 15% increase year-over-year."
    upload_res = client.post(
        "/upload",
        files={"file": ("financial_report.txt", io.BytesIO(doc_content), "text/plain")}
    )
    assert upload_res.status_code == 201

    # 2. Query document via /query
    query_res = client.post("/query", json={"question": "What was NovaTech's Q3 2026 revenue?"})
    assert query_res.status_code == 200
    data = query_res.json()
    
    # 3. Verify response schema
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0

    # 4. Critical Source Test: Exact chunk text returned in sources array
    exact_chunk = doc_content.decode("utf-8")
    assert data["sources"][0] == exact_chunk

def test_query_downstream_groq_failure(monkeypatch):
    # Ingest document first
    doc_content = b"Sample document text content for RAG testing."
    client.post("/upload", files={"file": ("sample.txt", io.BytesIO(doc_content), "text/plain")})

    # Monkeypatch LLMService generate_answer to simulate a DownstreamLLMError (HTTP 502)
    from backend.app.core.exceptions import DownstreamLLMError

    def mock_generate_answer_failure(self, prompt):
        raise DownstreamLLMError("LLM service communication failure (HTTP 502).")

    monkeypatch.setattr(LLMService, "generate_answer", mock_generate_answer_failure)

    response = client.post("/query", json={"question": "What is in sample?"})
    assert response.status_code == 502
    data = response.json()
    assert "LLM service communication failure" in data["detail"]
