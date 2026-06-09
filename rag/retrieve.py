"""Retrieval — stage 4 of the pipeline.

Embeds a user query with the same all-MiniLM-L6-v2 model and returns the
``TOP_K`` nearest chunks from ChromaDB, each carrying its source, chunk
position, and cosine distance. The returned dicts are the exact context
Milestone 5's LLM will consume.
"""

from __future__ import annotations

from rag.config import TOP_K
from rag.embed import build_index, get_collection


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """Return the ``k`` chunks nearest to ``query`` as ranked dicts.

    Each result is ``{"text", "source", "chunk_index", "distance"}``, ordered
    from nearest (smallest cosine distance) to farthest. Builds the index on
    first use if the store is empty.
    """
    collection = get_collection()
    if collection.count() == 0:
        collection = build_index()

    res = collection.query(query_texts=[query], n_results=k)
    documents = res["documents"][0]
    metadatas = res["metadatas"][0]
    distances = res["distances"][0]

    return [
        {
            "text": doc,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": dist,
        }
        for doc, meta, dist in zip(documents, metadatas, distances)
    ]


# Q1, Q3, Q5 from planning.md's Evaluation Plan (a spread across all 3 source types).
TEST_QUESTIONS = [
    "Should I apply to the Honors College?",
    "What is a good professor for my communications general education credit?",
    "How is the quality of SDSU classes?",
]


if __name__ == "__main__":
    for question in TEST_QUESTIONS:
        print("=" * 80)
        print(f"Q: {question}")
        print("=" * 80)
        for rank, hit in enumerate(retrieve(question), start=1):
            print(
                f"\n[{rank}] distance={hit['distance']:.4f}  "
                f"source={hit['source']}  chunk_index={hit['chunk_index']}"
            )
            print(hit["text"])
        print()
