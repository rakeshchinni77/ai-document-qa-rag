from fastapi import APIRouter, status
from backend.app.schemas.response import DocumentListResponse
from backend.app.services.vector_store import VectorStore

router = APIRouter()

@router.get("/documents", response_model=DocumentListResponse, status_code=status.HTTP_200_OK)
async def list_documents():
    vector_store = VectorStore()
    summary = vector_store.get_document_summary()
    return DocumentListResponse(
        documents=summary["documents"],
        total_chunks=summary["total_chunks"]
    )
