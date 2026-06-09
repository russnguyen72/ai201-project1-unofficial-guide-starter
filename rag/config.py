"""Shared configuration for the RAG pipeline.

Everything tunable lives here so the spec in planning.md maps to one place.
Holds the chunking knobs, document source directories, and the
embedding / vector-store settings; Groq settings are added in a later step.
"""

from __future__ import annotations

from pathlib import Path

# Project root = the directory that contains this `rag/` package.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_ROOT = PROJECT_ROOT / "documents"

# Chunking strategy (from planning.md): fixed-size character split.
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

# Directories of embedding-ready .txt documents, relative to DOCUMENTS_ROOT.
#   - rmp_docs/clean_examples : the 5 hand-cleaned RateMyProfessors reference files
#   - rmp_docs/clean          : output of clean_rmp.py (dirty pages, cleaned)
#   - reddit/clean_examples   : the hand-cleaned r/SDSU thread reference file
#   - reddit/clean            : output of clean_reddit.py (dirty threads, cleaned)
#   - niche                   : Niche reviews (already clean, ingested as-is)
SOURCE_DIRS = [
    DOCUMENTS_ROOT / "rmp_docs" / "clean_examples",
    DOCUMENTS_ROOT / "rmp_docs" / "clean",
    DOCUMENTS_ROOT / "reddit" / "clean_examples",
    DOCUMENTS_ROOT / "reddit" / "clean",
    DOCUMENTS_ROOT / "niche",
]

# Embedding + vector store (from planning.md): all-MiniLM-L6-v2 -> 384-dim
# vectors stored in a persistent ChromaDB collection, top-5 retrieval.
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"  # on-disk store (gitignored)
COLLECTION_NAME = "unofficial_guide"
TOP_K = 5
