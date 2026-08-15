import io
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.vector_store import VectorStore

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_vector_store():
    store = VectorStore()
    store.clear()
    yield
    store.clear()

def test_get_report_endpoint_exact_schema():
    response = client.get("/report")
    assert response.status_code == 200
    data = response.json()
    assert data["context_precision"] == 0.90
    assert data["faithfulness"] == 0.85
    assert data["system_status"] == "healthy"

def test_get_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data

def test_get_documents_endpoint_empty_and_populated():
    # 1. Empty state
    res_empty = client.get("/documents")
    assert res_empty.status_code == 200
    data_empty = res_empty.json()
    assert data_empty["documents"] == []
    assert data_empty["total_chunks"] == 0

    # 2. Upload document
    doc_content = b"Sample document text content for indexed documents test."
    client.post("/upload", files={"file": ("indexed_test.txt", io.BytesIO(doc_content), "text/plain")})

    # 3. Populated state
    res_pop = client.get("/documents")
    assert res_pop.status_code == 200
    data_pop = res_pop.json()
    assert len(data_pop["documents"]) == 1
    assert data_pop["documents"][0]["filename"] == "indexed_test.txt"
    assert data_pop["total_chunks"] >= 1
