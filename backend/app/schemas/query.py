from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., description="User question string", json_schema_extra={"example": "What were the primary causes of revenue decline in Q3?"})

class QueryResponse(BaseModel):
    answer: str = Field(..., description="LLM generated answer grounded in context")
    sources: list[str] = Field(..., description="List of exact raw text chunks retrieved from vector store")
