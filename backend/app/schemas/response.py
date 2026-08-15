from pydantic import BaseModel, Field
from typing import List

class ReportResponse(BaseModel):
    context_precision: float = Field(default=0.90, json_schema_extra={"example": 0.90})
    faithfulness: float = Field(default=0.85, json_schema_extra={"example": 0.85})
    system_status: str = Field(default="healthy", json_schema_extra={"example": "healthy"})

class DocumentItem(BaseModel):
    id: str
    filename: str
    chunk_count: int
    uploaded_at: str

class DocumentListResponse(BaseModel):
    documents: List[DocumentItem]
    total_chunks: int
