from fastapi import APIRouter, status
from backend.app.schemas.query import QueryRequest, QueryResponse
from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.prompt_service import PromptService
from backend.app.services.llm_service import LLMService
from backend.app.core.exceptions import EmptyQueryError
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_documents(payload: QueryRequest):
    question = payload.question
    if not question or not question.strip():
        raise EmptyQueryError("Question field cannot be empty.")
        
    logger.info(f"Processing query: '{question}'")
    
    # 1. Retrieve Context Chunks from Vector DB
    retrieval_service = RetrievalService()
    retrieved_items = retrieval_service.retrieve_context(question)
    
    raw_sources = [item["text"] for item in retrieved_items]
    
    # 2. Build Grounding Prompt
    prompt = PromptService.build_prompt(question, raw_sources)
    
    # 3. Query LLM
    llm_service = LLMService()
    answer = llm_service.generate_answer(prompt)
    
    logger.info(f"Successfully generated answer for query: '{question[:30]}...'")
    
    return QueryResponse(
        answer=answer,
        sources=raw_sources
    )
