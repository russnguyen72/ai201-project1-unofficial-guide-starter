"""Embedding + vector store — stage 3 of the pipeline.

Embeds every chunk with all-MiniLM-L6-v2 (384-dim vectors) and stores them in a
persistent ChromaDB collection alongside their source and chunk position. The
embedding function is attached to the collection, so ChromaDB embeds chunks on
``add`` and queries on ``query`` with the same model automatically.
"""

from __future__ import annotations

import re

import chromadb
from chromadb.utils import embedding_functions

from rag.chunk import chunk_documents
from rag.config import CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL_NAME


def _slug(text: str) -> str:
    """Lowercase ``text`` and collapse non-alphanumerics into single dashes."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def get_embedding_function():
    """Return the all-MiniLM-L6-v2 embedding function ChromaDB will call."""
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL_NAME,
    )


def get_collection():
    """Return the persistent ChromaDB collection (created if absent).

    Uses cosine distance so query distances fall in ``[0, 2]`` (0 = identical),
    which is more interpretable than the default squared-L2 space.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )


def build_index(reset: bool = False):
    """Chunk all documents and store their embeddings + metadata in ChromaDB.

    When ``reset`` is true the collection is dropped and rebuilt from scratch.
    The first run downloads the all-MiniLM-L6-v2 weights (~80 MB).
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass  # nothing to delete on a fresh store

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )

    records = chunk_documents(include_source_prefix=False)
    documents = [r["text"] for r in records]
    metadatas = [{"source": r["source"], "chunk_index": r["chunk_index"]} for r in records]
    ids = [f"{_slug(r['source'])}-{r['chunk_index']}" for r in records]

    if documents:
        collection.add(documents=documents, metadatas=metadatas, ids=ids)

    print(f"Stored {collection.count()} chunks in collection '{COLLECTION_NAME}'.")
    return collection


if __name__ == "__main__":
    build_index(reset=True)
    print(f"ChromaDB persisted at: {CHROMA_DIR}")
