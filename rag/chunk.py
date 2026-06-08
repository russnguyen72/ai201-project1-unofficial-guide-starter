"""Chunking — stage 2 of the pipeline.

Splits documents into fixed-size, overlapping character windows
(600 chars / 100 overlap, per planning.md). Each chunk is tagged with its
source label so attribution survives into the embedding and the vector store.
"""

from __future__ import annotations

from rag.config import CHUNK_OVERLAP, CHUNK_SIZE
from rag.ingest import load_documents
import random


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split ``text`` into overlapping windows of ``size`` characters.

    Consecutive chunks share ``overlap`` characters so a thought split across a
    boundary still appears whole in at least one chunk.
    """
    if size <= 0:
        raise ValueError("size must be positive")
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")

    text = text.strip()
    if not text:
        return []

    step = size - overlap
    chunks: list[str] = []
    for start in range(0, len(text), step):
        chunk = text[start:start + size].strip()
        if chunk:
            chunks.append(chunk)
        if start + size >= len(text):
            break
    return chunks


def chunk_documents(documents: list[dict] | None = None) -> list[dict]:
    """Chunk every document into ``{"text", "source", "chunk_index"}`` records.

    The source label is prepended to each chunk's text so it is embedded
    alongside the content and is available for citation at generation time.
    """
    if documents is None:
        documents = load_documents()

    records: list[dict] = []
    for doc in documents:
        for i, chunk in enumerate(chunk_text(doc["text"])):
            records.append({
                "text": f"[Source: {doc['source']}]\n{chunk}",
                "source": doc["source"],
                "chunk_index": i,
            })
    return records


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"Documents loaded : {len(docs)}")
    print(f"Total chunks     : {len(chunks)}")
    if chunks:
        avg = sum(len(c["text"]) for c in chunks) / len(chunks)
        print(f"Avg chunk length : {avg:.0f} chars")
        for i in range(5):
            random_num = random.randint(0, len(chunks) - 1)
            print(f"\nChunk {random_num} (source: {chunks[random_num]['source']}):\n{chunks[random_num]['text']}")
