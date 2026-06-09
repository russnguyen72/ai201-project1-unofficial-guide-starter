"""The Unofficial Guide — Gradio web UI (Milestone 5 interface).

A simple front end over the RAG pipeline: type a question, get a grounded answer
from ``rag.generate.generate_answer``, and optionally expand the retrieved
source chunks the answer was built from.

Run with:  python app.py
"""

from __future__ import annotations

import gradio as gr

from rag.generate import generate_answer


def _format_hits(hits: list[dict]) -> str:
    """Render retrieval results as Markdown for the collapsible sources panel."""
    if not hits:
        return "_No sources retrieved._"
    blocks = []
    for rank, hit in enumerate(hits, start=1):
        blocks.append(
            f"**[{rank}] {hit['source']}**  \n"
            f"_distance: {hit['distance']:.4f}_\n\n"
            f"{hit['text']}"
        )
    return "\n\n---\n\n".join(blocks)


def ask(question: str) -> tuple[str, str]:
    """Answer ``question`` and return ``(answer, sources_markdown)``."""
    question = (question or "").strip()
    if not question:
        return "Please enter a question.", ""
    result = generate_answer(question)
    return result["answer"], _format_hits(result["hits"])


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown(
        "# The Unofficial Guide\n"
        "Ask about SDSU courses, professors, and campus life. Answers are "
        "grounded in student reviews and forum posts."
    )
    question = gr.Textbox(
        label="Your question",
        placeholder="e.g. What is a good professor for my communications credit?",
    )
    ask_btn = gr.Button("Ask", variant="primary")
    answer = gr.Markdown(label="Answer")
    with gr.Accordion("Retrieved sources", open=False):
        sources = gr.Markdown()

    ask_btn.click(ask, inputs=question, outputs=[answer, sources])
    question.submit(ask, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
