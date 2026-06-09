"""Generation — stage 5 of the pipeline.

Feeds the retrieved chunks to Groq's ``llama-3.3-70b-versatile`` with a grounding
prompt that forbids outside knowledge and requires inline source citations, then
appends a deterministic ``Sources:`` list built from the chunks that were
actually retrieved. The result is a grounded answer plus the hits it was built
from, ready for the Gradio UI (stage 5's interface) to display.
"""

from __future__ import annotations

from groq import Groq

from rag.config import GROQ_API_KEY, GROQ_MODEL, TOP_K
from rag.retrieve import retrieve

# Grounding instruction: answer only from context, refuse otherwise, cite inline.
SYSTEM_PROMPT = """You are The Unofficial Guide, a question-answering assistant \
for prospective and current San Diego State University students. You answer \
questions about courses, professors, and campus life using ONLY the \
source-labelled context passages provided in each user message.

Rules:
1. Use ONLY the information in the provided context. Do not use any outside \
knowledge, and do not guess or invent details.
2. If the context does not contain enough information to answer the question, \
say so plainly (e.g. "I don't have enough information in my sources to answer \
that.") instead of making something up.
3. When you state a claim, cite the source it came from inline using its label \
in brackets, e.g. [Michael Rapp at San Diego State University (Rate My \
Professors)].
4. Be concise and directly answer the question. Reflect the sentiment of the \
sources honestly, including when opinions are mixed or conflicting."""

USER_TEMPLATE = """Question: {query}

Context passages:
{context}

Answer the question using only the context above, citing sources inline."""


def _get_client() -> Groq:
    """Return a Groq client, raising a clear error if the API key is missing."""
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to the .env file at the project root."
        )
    return Groq(api_key=GROQ_API_KEY)


def format_context(hits: list[dict]) -> str:
    """Render retrieved chunks into a source-labelled, citable context block.

    Each passage is labelled with its source in brackets so the model can cite
    it inline by name, e.g. ``[Michael Rapp at San Diego State University (Rate
    My Professors)]``, rather than by an opaque number.
    """
    blocks = []
    for hit in hits:
        blocks.append(f"[{hit['source']}]\n{hit['text']}")
    return "\n\n".join(blocks)


def _format_sources(hits: list[dict]) -> str:
    """Build a deterministic ``Sources:`` list from the unique hit sources."""
    seen: list[str] = []
    for hit in hits:
        if hit["source"] not in seen:
            seen.append(hit["source"])
    lines = "\n".join(f"- {source}" for source in seen)
    return f"Sources:\n{lines}"


def generate_answer(query: str, k: int = TOP_K) -> dict:
    """Answer ``query`` grounded in the top-``k`` retrieved chunks.

    Returns ``{"answer", "hits"}`` where ``answer`` is the model's grounded
    response with a deterministic ``Sources:`` list appended, and ``hits`` is the
    list of retrieval results it was built from (for display / inspection).
    """
    hits = retrieve(query, k)
    if not hits:
        return {
            "answer": "I don't have any sources that relate to that question.",
            "hits": [],
        }

    client = _get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.2,  # low temperature keeps answers grounded, not creative
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_TEMPLATE.format(
                    query=query, context=format_context(hits)
                ),
            },
        ],
    )
    answer = response.choices[0].message.content.strip()
    answer = f"{answer}\n\n---\n{_format_sources(hits)}"
    return {"answer": answer, "hits": hits}


# All 5 questions from planning.md's Evaluation Plan.
TEST_QUESTIONS = [
    "Should I apply to the Honors College?",
    "Should I worry about the placement test?",
    "What is a good professor for my communications general education credit?",
    "Who is a math professor I should avoid?",
    "How is the quality of SDSU classes?",
]


if __name__ == "__main__":
    for question in TEST_QUESTIONS:
        print("=" * 80)
        print(f"Q: {question}")
        print("=" * 80)
        result = generate_answer(question)
        print(result["answer"])
        print()
