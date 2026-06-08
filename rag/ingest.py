"""Document ingestion — stage 1 of the pipeline.

Loads every cleaned ``.txt`` document from the configured source directories and
returns them with a human-readable source label for downstream attribution.
"""

from __future__ import annotations

from pathlib import Path

from rag.config import SOURCE_DIRS


def _source_label(path: Path) -> str:
    """Build a readable source label from a file's name.

    "Michael Rapp at San Diego State University _ Rate My Professors.txt"
        -> "Michael Rapp at San Diego State University (Rate My Professors)"
    """
    stem = path.stem
    if " _ " in stem:
        subject, site = stem.split(" _ ", 1)
        return f"{subject} ({site})"
    return stem


def load_documents() -> list[dict]:
    """Return all source documents as ``{"source", "path", "text"}`` dicts."""
    documents: list[dict] = []
    for directory in SOURCE_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.txt")):
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                continue
            documents.append({
                "source": _source_label(path),
                "path": str(path),
                "text": text,
            })
    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents:")
    for doc in docs:
        print(f"  - {doc['source']} ({len(doc['text'])} chars)")
