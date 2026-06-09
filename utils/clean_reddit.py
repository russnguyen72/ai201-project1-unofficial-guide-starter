"""Clean raw Reddit thread exports into embedding-ready text.

The .txt files in ``documents/reddit/dirty/`` are saved straight from a Reddit
post page. They carry a lot of noise: site navigation, "Sign Up / Log In",
promoted ads, the comment sort bar, per-comment "Reply / Share" buttons,
avatar/profile-badge lines, "More replies", a "People also ask" block, a long
list of unrelated related-posts, and the site footer.

This script rewrites each dirty file into the same shape as the hand-cleaned
file in ``documents/reddit/clean_examples/`` and writes the result to
``documents/reddit/clean/``. The kept content is:

    <post age>

    <OP username>


      <post title>

    <flair>

    <post body, one line>


    Q&A

    <comment username>
    • <comment age>

    <comment body, one line>
    ...

Per the chosen options: body URLs are de-duplicated/unwrapped to a single bare
URL, and each post/comment body is collapsed to one line.

Usage:
    python clean_reddit.py
"""

from __future__ import annotations

import re
from pathlib import Path

DIRTY_DIR = Path("documents/reddit/dirty")
CLEAN_DIR = Path("documents/reddit/clean")

# "20d ago", "1mo ago", "7d ago", "6mo ago", ...
AGE_RE = re.compile(r"^\d+\s*(mo|yr|y|w|d|h|m|s)\s+ago$")

# Lines that terminate the OP body / a comment body.
BODY_STOP = {"Read more", "Share", "Reply", "Promoted"}


def strip_links(text: str) -> str:
    """Drop <...> angle-bracket links and collapse whitespace.

    Reddit renders a body URL twice: a bare URL followed by a wrapped
    `<...>` duplicate. Removing the `<...>` token leaves exactly one clean,
    inline URL.
    """
    text = re.sub(r"<[^>]*>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def strip_user(line: str) -> str:
    """Pull a bare username out of a Reddit author line.

    'Ok_Lifeguard101 <https://www.reddit.com/user/Ok_Lifeguard101/>' -> 'Ok_Lifeguard101'
    'u/koncha22 avatar <...>'                                        -> 'koncha22'
    """
    s = line.strip().split(" <", 1)[0].strip()
    s = s.replace(" avatar", "").strip()
    if s.startswith("u/"):
        s = s[2:]
    return s


def _first_nonblank_above(lines: list[str], idx: int) -> int:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    return j


def parse_post(lines: list[str], title: str) -> dict:
    """Extract the original post: age, OP username, flair, and body."""
    # The H1 title is the first line (after the page <title>) that equals it.
    title_idx = next(
        (i for i in range(1, len(lines)) if lines[i].strip() == title),
        None,
    )
    if title_idx is None:
        return {"age": "", "user": "", "flair": "", "body": ""}

    # Walk up: username sits just above the title, age just above that.
    user_idx = _first_nonblank_above(lines, title_idx)
    op_user = strip_user(lines[user_idx]) if user_idx >= 0 else ""

    j = user_idx - 1
    while j >= 0 and (not lines[j].strip() or lines[j].strip() == "•"):
        j -= 1
    age = lines[j].strip() if j >= 0 else ""
    if not AGE_RE.match(age):
        age = ""

    # Walk down: flair (first non-blank), then body until a stop word.
    k = title_idx + 1
    while k < len(lines) and not lines[k].strip():
        k += 1
    flair = lines[k].strip() if k < len(lines) else ""
    k += 1

    body_lines: list[str] = []
    while k < len(lines):
        s = lines[k].strip()
        if s in BODY_STOP:
            break
        if not s or "flair_name" in lines[k]:
            k += 1
            continue
        body_lines.append(s)
        k += 1

    return {"age": age, "user": op_user, "flair": flair,
            "body": strip_links(" ".join(body_lines))}


def parse_comments(lines: list[str]) -> list[dict]:
    """Extract every comment (flattened) as {user, age, body}.

    Comments are anchored on their "• <age> ago <.../comment/...>" marker line,
    which distinguishes them from the OP age line (no URL) and from "More
    replies" links (no leading bullet).
    """
    comments: list[dict] = []
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("•") or "/comment/" not in line:
            continue

        user_idx = _first_nonblank_above(lines, i)
        user = strip_user(lines[user_idx]) if user_idx >= 0 else ""

        age = strip_links(line).lstrip("•").strip()

        body_lines: list[str] = []
        b = i + 1
        while b < len(lines):
            s = lines[b].strip()
            if s in BODY_STOP or s.startswith("More replies"):
                break
            if s.startswith("•") and "/comment/" in lines[b]:
                break  # next comment marker
            if not s or s.startswith("Profile Badge"):
                b += 1
                continue
            body_lines.append(s)
            b += 1

        comments.append({"user": user, "age": age,
                         "body": strip_links(" ".join(body_lines))})
    return comments


def clean_text(raw: str) -> str:
    lines = raw.splitlines()

    # The page <title> on line 2 is "<post title> : r/<sub>".
    title = lines[1].split(" : r/", 1)[0].strip() if len(lines) > 1 else ""

    post = parse_post(lines, title)
    comments = parse_comments(lines)

    out: list[str] = [
        post["age"], "",
        post["user"], "", "",
        f"  {title}", "",
        post["flair"], "",
        post["body"], "", "",
        "Q&A", "",
    ]
    for idx, c in enumerate(comments):
        if idx > 0:
            out.extend(["", ""])
        out.append(c["user"])
        out.append(f"• {c['age']}")
        out.append("")
        out.append(c["body"])

    return "\n".join(out) + "\n"


def main() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    dirty_files = sorted(DIRTY_DIR.glob("*.txt"))
    if not dirty_files:
        print(f"No .txt files found in {DIRTY_DIR}")
        return
    for path in dirty_files:
        raw = path.read_text(encoding="utf-8")
        cleaned = clean_text(raw)
        out_path = CLEAN_DIR / path.name
        out_path.write_text(cleaned, encoding="utf-8")
        print(f"Cleaned {path.name} -> {out_path}")


if __name__ == "__main__":
    main()
