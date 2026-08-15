import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure both root workspace and backend directories are in sys.path for IDE linter resolution
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from backend.app.core.config import settings
    from backend.app.api import upload, query, report, health, documents
    from backend.app.utils.logging import get_logger
except ImportError:
    from app.core.config import settings
    from app.api import upload, query, report, health, documents
    from app.utils.logging import get_logger

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"ChromaDB persistent store: {settings.CHROMA_DB_DIR}")
    yield
    logger.info("Shutting down AI Document QA RAG application.")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Document Question-Answering RAG REST API",
    lifespan=lifespan
)

# CORS Configuration - Explicitly allow React frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(upload.router, tags=["Ingestion"])
app.include_router(query.router, tags=["Inference"])
app.include_router(report.router, tags=["Evaluation"])
app.include_router(health.router, tags=["System"])
app.include_router(documents.router, tags=["Management"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI-Powered Document QA RAG API",
        "docs": "/docs",
        "health": "/health"
    }
