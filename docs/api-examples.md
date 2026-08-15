# API Documentation & Examples

This document outlines the API endpoints, request formats, response schemas, and cURL examples for the AI-Powered Document Question-Answering RAG API.

---

## 1. Document Upload Endpoint (`POST /upload`)

Ingests a document file (`.txt`, `.md`, or `.pdf`), validates extension and readability, chunks content (1000 chars / 200 overlap), computes vector embeddings (`all-MiniLM-L6-v2`), and indexes into ChromaDB.

### Request Contract
- **HTTP Method**: `POST`
- **Path**: `/upload`
- **Content-Type**: `multipart/form-data`
- **Payload**: `file` (File input field)

### Example cURL Request (TXT)
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/samples/test_document.txt"
```

### Successful Response (`201 Created`)
```json
{
  "message": "File uploaded and indexed successfully.",
  "filename": "test_document.txt",
  "chunks_indexed": 4
}
```

### Error Responses (`400 Bad Request`)
- **Unsupported File Format**:
  ```json
  {
    "detail": "Unsupported file format '.png'. Please upload .txt, .md, or .pdf"
  }
  ```
- **Unreadable / Empty Document**:
  ```json
  {
    "detail": "Document 'empty.pdf' contains no readable text."
  }
  ```

---

## 2. Document Query Endpoint (`POST /query`)

Embeds the question using the same model (`all-MiniLM-L6-v2`), retrieves top-k (k=3) similar document chunks from ChromaDB, constructs a strict grounding prompt, and calls the LLM API to generate an answer with cited sources.

### Request Contract
- **HTTP Method**: `POST`
- **Path**: `/query`
- **Content-Type**: `application/json`
- **Payload Schema**:
  ```json
  {
    "question": "What were the primary causes of revenue decline in Q3?"
  }
  ```

### Example cURL Request
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What was NovaTech reported total revenue in Q3 2026?"
  }'
```

### Successful Response (`200 OK`)
```json
{
  "answer": "In Q3 2026, NovaTech Solutions reported total revenue of $42.5 million, representing a 15% increase year-over-year.",
  "sources": [
    "AI-Powered Document Question-Answering RAG System Overview\n\n1. Executive Summary\nIn Q3 2026, NovaTech Solutions reported total revenue of $42.5 million, representing a 15% increase year-over-year. The strong financial performance was driven by accelerated enterprise adoption of the NovaAI Cloud Platform and strategic expansion into EMEA markets.",
    "3. Key Q3 Financial Highlights & Operational Challenges\nDespite revenue growth, Q3 operational expenses rose by 8% due to increased R&D investment in fine-tuning domain-specific LLM models."
  ]
}
```

### Error Responses
- **Empty Question (`400 Bad Request`)**:
  ```json
  {
    "detail": "Question field cannot be empty."
  }
  ```
- **No Documents Indexed (`400 Bad Request`)**:
  ```json
  {
    "detail": "No documents have been indexed yet. Please upload a document first."
  }
  ```
- **LLM API Unreachable (`502 Bad Gateway`)**:
  ```json
  {
    "detail": "LLM service communication failure (HTTP 502)."
  }
  ```

---

## 3. Evaluation Report Endpoint (`GET /report`)

Returns telemetry and quality evaluation metrics for the RAG system.

### Example cURL Request
```bash
curl -X GET "http://localhost:8000/report" -H "accept: application/json"
```

### Response (`200 OK`)
```json
{
  "context_precision": 0.90,
  "faithfulness": 0.85,
  "system_status": "healthy"
}
```

---

## 4. Health Check Endpoint (`GET /health`)

Returns system status and version information.

### Example cURL Request
```bash
curl -X GET "http://localhost:8000/health" -H "accept: application/json"
```

### Response (`200 OK`)
```json
{
  "status": "healthy",
  "app": "AI-Powered Document Question-Answering RAG API",
  "version": "1.0.0"
}
```

---

## 5. Document List Endpoint (`GET /documents`)

Returns summary list of indexed files and total vector chunk count in ChromaDB.

### Example cURL Request
```bash
curl -X GET "http://localhost:8000/documents" -H "accept: application/json"
```

### Response (`200 OK`)
```json
{
  "documents": [
    {
      "id": "test_document.txt",
      "filename": "test_document.txt",
      "chunk_count": 4,
      "uploaded_at": "2026-08-14T18:15:35.000Z"
    }
  ],
  "total_chunks": 4
}
```
