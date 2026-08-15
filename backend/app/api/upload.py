from fastapi import APIRouter, UploadFile, File, status
from backend.app.services.document_processor import DocumentProcessor
from backend.app.services.chunker import TextChunker
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore
from backend.app.schemas.upload import UploadResponse
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    logger.info(f"Received file upload request for '{file.filename}'")
    
    # 1. Read file content
    content = await file.read()
    
    # 2. Validate & Extract Text
    ext = DocumentProcessor.validate_file_extension(file.filename)
    raw_text = DocumentProcessor.extract_text(file.filename, content)
    
    # 3. Chunk Text
    chunker = TextChunker()
    chunks = chunker.split_text(raw_text)
    
    # 4. Generate Embeddings
    embedding_service = EmbeddingService()
    embeddings = embedding_service.embed_texts(chunks)
    
    # 5. Store in ChromaDB
    vector_store = VectorStore()
    vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename,
        file_type=ext.replace(".", "")
    )
    
    logger.info(f"File '{file.filename}' successfully processed and indexed into {len(chunks)} chunks.")
    
    return UploadResponse(
        message="File uploaded and indexed successfully.",
        filename=file.filename,
        chunks_indexed=len(chunks)
    )
