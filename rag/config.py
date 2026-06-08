"""Shared configuration for the RAG pipeline.

Everything tunable lives here so the spec in planning.md maps to one place.
Step 1 only needs the chunking knobs and the document source directories;
embedding / vector-store / Groq settings are added in later steps.
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
