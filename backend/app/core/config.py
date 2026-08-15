import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "AI-Powered Document Question-Answering RAG API"
    APP_VERSION: str = "1.0.0"
    
    # LLM Settings
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    LLM_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K: int = 3
    
    # Storage Settings
    CHROMA_DB_DIR: str = os.path.join(str(BASE_DIR), "data", "chroma")
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Supported File Extensions
    ALLOWED_EXTENSIONS: set[str] = {".txt", ".md", ".pdf"}

    model_config = SettingsConfigDict(
        env_file=os.path.join(str(BASE_DIR), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
