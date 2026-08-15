import os
import uuid
import datetime
import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.app.core.config import settings
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)

class VectorStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)
            logger.info(f"Initializing persistent ChromaDB client at '{settings.CHROMA_DB_DIR}'...")
            cls._client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
            cls._collection = cls._client.get_or_create_collection(
                name="document_qa_collection",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("ChromaDB vector store initialized successfully.")
        return cls._instance

    def add_chunks(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        filename: str,
        file_type: str
    ) -> list[str]:
        if not chunks or not embeddings:
            return []

        ids = [f"{filename}_{idx}_{uuid.uuid4().hex[:8]}" for idx in range(len(chunks))]
        timestamps = [datetime.datetime.now(datetime.timezone.utc).isoformat() for _ in chunks]
        
        metadatas = [
            {
                "filename": filename,
                "chunk_index": idx,
                "file_type": file_type,
                "uploaded_at": timestamps[idx]
            }
            for idx in range(len(chunks))
        ]

        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

        logger.info(f"Successfully added {len(chunks)} chunks for file '{filename}' to ChromaDB.")
        return ids

    def search_similar(self, query_embedding: list[float], top_k: int = None) -> list[dict]:
        k = top_k or settings.TOP_K
        if self._collection.count() == 0:
            return []

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, self._collection.count())
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            retrieved.append({
                "text": doc,
                "metadata": meta,
                "distance": dist
            })

        return retrieved

    def get_document_summary(self) -> dict:
        total_chunks = self._collection.count()
        if total_chunks == 0:
            return {"documents": [], "total_chunks": 0}

        all_records = self._collection.get()
        metadatas = all_records.get("metadatas", [])
        
        doc_map = {}
        for meta in metadatas:
            fname = meta.get("filename", "unknown")
            if fname not in doc_map:
                doc_map[fname] = {
                    "id": fname,
                    "filename": fname,
                    "chunk_count": 0,
                    "uploaded_at": meta.get("uploaded_at", "")
                }
            doc_map[fname]["chunk_count"] += 1

        return {
            "documents": list(doc_map.values()),
            "total_chunks": total_chunks
        }

    def count(self) -> int:
        return self._collection.count()

    def clear(self):
        try:
            self._client.delete_collection(name="document_qa_collection")
        except Exception:
            pass
        self._collection = self._client.get_or_create_collection(
            name="document_qa_collection",
            metadata={"hnsw:space": "cosine"}
        )
