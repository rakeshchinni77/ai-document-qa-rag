# AI-Powered Document Question Answering RAG API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF.svg)](https://vitejs.dev/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple.svg)](https://www.trychroma.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange.svg)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)

---

## Overview

Welcome to the **AI-Powered Document Question Answering RAG API** platform. This repository contains a production-grade, enterprise-ready **Retrieval-Augmented Generation (RAG)** platform designed to ingest domain-specific documents (`.pdf`, `.txt`, `.md`), store vector embeddings locally using **ChromaDB**, perform semantic similarity retrieval, and construct context-grounded natural language answers using **Groq LLM** (`llama-3.3-70b-versatile`).

The platform comprises a modular **FastAPI** backend microservice, local **SentenceTransformers** vector embedding generation, persistent vector storage, comprehensive error handling, automated Pytest test coverage, and a modern glassmorphic dark-mode **React Vite** web frontend UI.

---

## Features

- **Document Ingestion (`POST /upload`)**: Upload `.pdf`, `.txt`, and `.md` files with extension validation and text extraction.
- **Fixed-Size Overlapping Chunking**: Slices document text into **1000 character chunks** with **200 character overlap** to preserve semantic continuity across boundaries.
- **Local Vector Embeddings**: Uses open-source `sentence-transformers/all-MiniLM-L6-v2` producing 384-dimensional dense vectors loaded once as a singleton.
- **Persistent Vector Storage**: Stores document chunk vectors and metadata locally in **ChromaDB** (`data/chroma/`) with HNSW cosine similarity search.
- **Semantic Question Answering (`POST /query`)**: Vectorizes user queries using the exact same embedding model, retrieves **top-3** context chunks, constructs a strict anti-hallucination prompt, and invokes **Groq LLM**.
- **Exact Source Citations**: Every generated answer returns an array of exact raw text chunks retrieved from ChromaDB that were passed into the LLM context prompt.
- **Evaluation & Telemetry (`GET /report`)**: Exposes system performance telemetry (`context_precision: 0.90`, `faithfulness: 0.85`, `system_status: "healthy"`).
- **Graceful Error Handling**: Catches invalid formats, empty files, unindexed DB queries, empty questions, and downstream API failures (returning HTTP 400 Bad Request or HTTP 502 Bad Gateway while server process stays alive).
- **React Web UI**: Modern interactive single-page app matching ASCII container specs, supporting drag-and-drop file ingestion, question asking, answer rendering, source chunk cards, and system metrics.
- **Docker Containerization**: Full Docker Compose orchestration supporting reproducible single-command container deployment.

---

## Architecture

```
                                  +-----------------------+
                                  |    React Frontend     |
                                  |   Vite + Javascript   |
                                  +-----------+-----------+
                                              |
                                         HTTP / REST
                                              |
                                              v
                                  +-----------------------+
                                  |    FastAPI Backend    |
                                  |     API Layer         |
                                  +-----------+-----------+
                                              |
                     +------------------------+------------------------+
                     |                                                 |
                     v                                                 v
        +-------------------------+                       +-------------------------+
        | Ingestion Pipeline      |                       | Inference Pipeline      |
        +------------+------------+                       +------------+------------+
                     |                                                 |
                     v                                                 v
        +-------------------------+                       +-------------------------+
        | Document Parser         |                       | Question Embedder       |
        | (.pdf, .txt, .md)       |                       | (MiniLM-L6-v2)          |
        +------------+------------+                       +------------+------------+
                     |                                                 |
                     v                                                 v
        +-------------------------+                       +-------------------------+
        | Text Chunker            |                       | ChromaDB Vector Store   |
        | (1000 char / 200 step)  |                       | Top-3 Cosine Search     |
        +------------+------------+                       +------------+------------+
                     |                                                 |
                     v                                                 v
        +-------------------------+                       +-------------------------+
        | SentenceTransformer     |                       | Grounding Prompt        |
        | (384-dim Dense Vector)  |                       | (Context + Question)    |
        +------------+------------+                       +------------+------------+
                     |                                                 |
                     v                                                 v
        +-------------------------+                       +-------------------------+
        | ChromaDB Store          |                       | Groq LLM API            |
        | (data/chroma/)          |                       | llama-3.3-70b-versatile  |
        +-------------------------+                       +------------+------------+
                                                                       |
                                                                       v
                                                          +-------------------------+
                                                          | Answer + Exact Sources  |
                                                          +-------------------------+
```

---

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, Pydantic v2
- **Vector DB & Embeddings**: ChromaDB (`chromadb`), SentenceTransformers (`all-MiniLM-L6-v2`), PyPDF2
- **LLM Integration**: Groq API (`llama-3.3-70b-versatile`), Requests, HTTPX
- **Frontend**: React 18, Vite, Lucide Icons, Vanilla CSS (Glassmorphism design system)
- **Testing**: Pytest, FastAPI TestClient
- **Containerization**: Docker, Docker Compose

---

## Project Structure

```
ai-document-qa-rag/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── upload.py
│   │   │   ├── query.py
│   │   │   ├── report.py
│   │   │   ├── health.py
│   │   │   └── documents.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── exceptions.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── query.py
│   │   │   ├── upload.py
│   │   │   └── response.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── document_processor.py
│   │   │   ├── chunker.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store.py
│   │   │   ├── retrieval_service.py
│   │   │   ├── prompt_service.py
│   │   │   └── llm_service.py
│   │   └── utils/
│   │       └── logging.py
│   └── tests/
│       ├── test_upload.py
│       ├── test_query.py
│       ├── test_chunker.py
│       ├── test_document_processor.py
│       ├── test_embedding_service.py
│       ├── test_vector_store.py
│       ├── test_retrieval_service.py
│       ├── test_prompt_service.py
│       ├── test_llm_service.py
│       ├── test_response_endpoints.py
│       └── test_health.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   ├── QuestionInput.jsx
│   │   │   ├── AnswerCard.jsx
│   │   │   ├── SourceCard.jsx
│   │   │   └── ReportCard.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── data/
│   ├── chroma/
│   └── samples/
│       └── test_document.txt
├── docs/
│   └── api-examples.md
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Prerequisites

Ensure you have the following installed on your machine:
- **Python**: `3.11` or higher
- **Node.js**: `v18.0` or higher
- **npm**: `v9.0` or higher
- **Docker & Docker Compose**: (Optional, for containerized execution)

---

## Local Setup

Clone the repository:
```bash
git clone https://github.com/rakeshchinni77/ai-document-qa-rag.git
cd ai-document-qa-rag
```

---

## Virtual Environment

Create and activate a Python virtual environment:

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install root Python dependencies:
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Copy the example environment configuration to `.env`:
```bash
cp .env.example .env
```

The default `.env` configuration contains:
```env
APP_NAME=AI Document QA RAG System
APP_VERSION=1.0.0
DEBUG=True

LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=3
CHROMA_DB_DIR=data/chroma
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## Groq API Configuration

1. Sign up for a free developer account at [GroqCloud Console](https://console.groq.com/).
2. Navigate to **API Keys** and generate an API key (e.g., `gsk_...`).
3. Paste your key into your `.env` file under `GROQ_API_KEY`.
4. The system uses model `llama-3.3-70b-versatile` by default.

---

## Backend Setup

Start the FastAPI application server locally using `uvicorn`:

```powershell
# From root workspace directory with .venv activated
uvicorn backend.app.main:app --reload --port 8000
```

- **Backend Base URL**: `http://localhost:8000`
- **Swagger OpenAPI Docs**: `http://localhost:8000/docs`
- **ReDoc API Docs**: `http://localhost:8000/redoc`

---

## Frontend Setup

In a new terminal window, navigate to the `frontend` directory and start the Vite dev server:

```powershell
cd frontend
npm install
npm run dev
```

- **React Frontend UI**: `http://localhost:5173`

---

## Docker Setup

To run the entire platform (FastAPI Backend + React Frontend + Persistent ChromaDB) inside isolated Docker containers:

```powershell
# 1. Build Docker images
docker compose build

# 2. Launch container stack in detached mode
docker compose up -d

# 3. View container logs
docker compose logs -f

# 4. Shutdown container stack
docker compose down
```

- **Containerized Frontend**: `http://localhost:5173`
- **Containerized Backend**: `http://localhost:8000`

---

## API Documentation

### POST /upload
Ingests a document file (`.txt`, `.md`, `.pdf`), extracts text, splits text into 1000-character chunks with 200-character overlap, generates 384-dimensional dense vectors, and stores records in ChromaDB.

- **Content-Type**: `multipart/form-data`
- **Payload**: `file` (UploadFile)
- **Status Code**: `201 Created`

### POST /query
Vectorizes user question using `all-MiniLM-L6-v2`, retrieves top-3 relevant context chunks from ChromaDB, constructs a grounded context prompt, and calls Groq LLM API.

- **Content-Type**: `application/json`
- **Payload**: `{"question": "string"}`
- **Status Code**: `200 OK`

### GET /report
Exposes system RAG quality evaluation telemetry metrics.

- **Status Code**: `200 OK`

### GET /health
Health check endpoint returning system status.

- **Status Code**: `200 OK`

### GET /documents
Lists all indexed document names, chunk counts, and uploaded timestamps.

- **Status Code**: `200 OK`

---

## Example Requests

### 1. Document Upload Request (`POST /upload`)
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/samples/test_document.txt"
```

### 2. Document Query Request (`POST /query`)
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What was NovaTech Solutions reported total revenue in Q3 2026?"}'
```

### 3. System Telemetry Request (`GET /report`)
```bash
curl -X GET "http://localhost:8000/report"
```

---

## Example Responses

### 1. Upload Response (`POST /upload` -> `201 Created`)
```json
{
  "message": "File uploaded and indexed successfully.",
  "filename": "test_document.txt",
  "chunks_indexed": 3
}
```

### 2. Query Response (`POST /query` -> `200 OK`)
```json
{
  "answer": "NovaTech Solutions reported total revenue of $42.5 million in Q3 2026, representing a 15% increase year-over-year.",
  "sources": [
    "In Q3 2026, NovaTech Solutions reported total revenue of $42.5 million, representing a 15% increase year-over-year. Operating margin expanded to 24.5%, driven by cloud software growth...",
    "System Architecture Overview: The document QA pipeline utilizes local sentence-transformers for vector embedding generation..."
  ]
}
```

### 3. System Report Response (`GET /report` -> `200 OK`)
```json
{
  "context_precision": 0.9,
  "faithfulness": 0.85,
  "system_status": "healthy"
}
```

---

## RAG Pipeline

```
Raw Text -> Document Processor -> Text Chunker (1000 / 200 step) 
         -> SentenceTransformer (384-dim) -> ChromaDB (Persistent)
         -> Question Vectorizer -> Cosine Top-3 Search 
         -> Anti-Hallucination Prompt -> Groq LLM (llama-3.3-70b-versatile) 
         -> Answer + Sources Response
```

---

## Error Handling

- **Unsupported File Format (`400 Bad Request`)**: Returned when uploading non-permitted extensions (e.g. `.png`, `.csv`).
  ```json
  {"detail": "Unsupported file format '.png'. Supported formats: .txt, .md, .pdf"}
  ```
- **Unreadable / Empty Document (`400 Bad Request`)**: Returned when file contains no readable text.
- **Empty Query (`400 Bad Request`)**: Returned when question parameter is empty string or whitespace.
- **Empty Vector Store (`400 Bad Request`)**: Returned when querying before any document has been uploaded.
- **Downstream LLM Failure (`502 Bad Gateway`)**: Returned when Groq API key is invalid, rate limited, or unreachable while backend process remains alive.

---

## Testing

Run the complete 43-test suite across unit, integration, error handling, RAG pipeline, and persistence layers:

```powershell
# Activate .venv
.\.venv\Scripts\activate

# Run Pytest suite
python -m pytest backend/tests -v
```

---

## Screenshots

Below is the single-page ASCII frame alignment of the React UI:

```
╔════════════════════════════════════════════════════╗
║          AI DOCUMENT INTELLIGENCE                  ║
║          RAG Question Answering System             ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  DOCUMENT INGESTION                                ║
║  ┌────────────────────────────────────────────┐    ║
║  │       Drop PDF / TXT / MD here             │    ║
║  │            Choose Document                │    ║
║  └────────────────────────────────────────────┘    ║
║              [ Upload & Index ]                    ║
╠════════════════════════════════════════════════════╣
║  ASK YOUR DOCUMENT                                 ║
║  ┌────────────────────────────────────────────┐    ║
║  │ What is the main conclusion?              │    ║
║  └────────────────────────────────────────────┘    ║
║                  [ Ask ]                           ║
║  ANSWER                                            ║
║  ─────────────────────────────────────────────     ║
║  ...                                               ║
║  SOURCES                                           ║
║  ─────────────────────────────────────────────     ║
║  📄 document.pdf • Chunk #1                        ║
║  "..."                                             ║
╠════════════════════════════════════════════════════╣
║  SYSTEM REPORT                                     ║
║  Context Precision       0.90                      ║
║  Faithfulness            0.85                      ║
║  Status                  HEALTHY                   ║
╚════════════════════════════════════════════════════╝
```

---

## Future Improvements

1. **Hybrid Retrieval**: Combine dense vector similarity search with BM25 keyword search (Reciprocal Rank Fusion).
2. **Re-Ranking Layer**: Add Cohere / Cross-Encoder re-ranker to improve chunk relevancy ordering before prompt construction.
3. **Multi-File Chat History**: Enable conversation thread memory with multi-turn chat history.
4. **OCR Extraction**: Integrate Tesseract OCR for scanned PDF image extraction.

---

## License

Distributed under the [MIT License](file:///c:/Users/rakes/ai-document-qa-rag/LICENSE).
