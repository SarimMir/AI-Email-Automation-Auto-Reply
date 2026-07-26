"""
StyleSync AI Mail — RAG Setup
================================
Initializes and manages the ChromaDB vector store for the StyleSync knowledge base.
Uses sentence-transformers for local embeddings (no API key needed for RAG).
"""

import os
import chromadb
from chromadb.utils import embedding_functions

# ── Constants ──────────────────────────────────────────────────────────────
KB_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
COLLECTION_NAME = "stylesync_kb"

# Global client + collection (initialized once)
_client = None
_collection = None


def _get_embedding_fn():
    """Use sentence-transformers for local, free embeddings."""
    try:
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    except Exception:
        # Fallback to ChromaDB's default (no external model needed)
        return embedding_functions.DefaultEmbeddingFunction()


def initialize_rag():
    """
    Initialize ChromaDB and populate the knowledge base collection.
    Idempotent — safe to call multiple times.
    """
    global _client, _collection

    if _collection is not None:
        return _collection  # Already initialized

    print("[RAG] Initializing ChromaDB knowledge base...")

    # In-memory client (ephemeral — reloads from files each run)
    _client = chromadb.Client()

    # Delete existing collection if present (for clean reload)
    try:
        _client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    emb_fn = _get_embedding_fn()
    _collection = _client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )

    # Load knowledge base documents
    docs, ids, metadatas = [], [], []
    kb_files = {
        "return_policy":  "return_policy.txt",
        "sizing_guide":   "sizing_guide.txt",
        "shipping_info":  "shipping_info.txt",
    }

    chunk_id = 0
    for doc_key, filename in kb_files.items():
        filepath = os.path.join(KB_DIR, filename)
        if not os.path.exists(filepath):
            print(f"[RAG] Warning: {filepath} not found, skipping.")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Chunk by paragraph (double newline)
        chunks = [c.strip() for c in raw_text.split("\n\n") if c.strip() and len(c.strip()) > 30]

        for chunk in chunks:
            docs.append(chunk)
            ids.append(f"{doc_key}_{chunk_id}")
            metadatas.append({"source": doc_key, "filename": filename})
            chunk_id += 1

    if docs:
        _collection.add(documents=docs, ids=ids, metadatas=metadatas)
        print(f"[RAG] Loaded {len(docs)} chunks into ChromaDB.")
    else:
        print("[RAG] No documents loaded — knowledge base directory may be empty.")

    return _collection


def retrieve_context(query: str, n_results: int = 3) -> str:
    """
    Retrieve top-N most relevant knowledge base chunks for a given query.
    Returns a formatted string ready to inject into a prompt.
    """
    global _collection

    if _collection is None:
        initialize_rag()

    if _collection is None:
        return "No knowledge base available."

    try:
        results = _collection.query(
            query_texts=[query],
            n_results=min(n_results, 3),
            include=["documents", "metadatas", "distances"]
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        if not docs:
            return "No relevant information found in knowledge base."

        formatted_chunks = []
        for doc, meta in zip(docs, metas):
            source_label = meta.get("source", "knowledge_base").replace("_", " ").title()
            formatted_chunks.append(f"[{source_label}]\n{doc}")

        return "\n\n---\n\n".join(formatted_chunks)

    except Exception as e:
        print(f"[RAG] Query error: {e}")
        return "Unable to retrieve context from knowledge base."


def get_collection_stats() -> dict:
    """Return stats about the current knowledge base collection."""
    global _collection
    if _collection is None:
        return {"status": "not_initialized", "count": 0}
    try:
        count = _collection.count()
        return {"status": "ready", "count": count, "collection": COLLECTION_NAME}
    except Exception:
        return {"status": "error", "count": 0}
