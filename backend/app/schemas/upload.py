from pydantic import BaseModel, Field

class UploadResponse(BaseModel):
    message: str = Field(..., json_schema_extra={"example": "File uploaded and indexed successfully."})
    filename: str = Field(..., json_schema_extra={"example": "test_document.txt"})
    chunks_indexed: int = Field(..., json_schema_extra={"example": 5})
