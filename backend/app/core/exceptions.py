from fastapi import HTTPException, status

class UnsupportedFileTypeError(HTTPException):
    def __init__(self, detail: str = "Unsupported file format. Please upload .txt, .md, or .pdf"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnreadableDocumentError(HTTPException):
    def __init__(self, detail: str = "Document contains no readable text or is corrupted."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class EmptyQueryError(HTTPException):
    def __init__(self, detail: str = "Question field cannot be empty."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class EmptyVectorStoreError(HTTPException):
    def __init__(self, detail: str = "No documents have been indexed yet. Please upload a document first."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class DownstreamLLMError(HTTPException):
    def __init__(self, detail: str = "Error communicating with downstream LLM service."):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)
