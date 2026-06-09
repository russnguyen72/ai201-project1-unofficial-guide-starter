"""Clean raw RateMyProfessors page exports into embedding-ready text.

The .txt files in ``documents/rmp_docs/dirty/`` are saved straight from a
RateMyProfessors professor page. They carry a lot of noise that bloats chunks
and pollutes retrieval: site navigation, duplicated headers, "Helpful / Thumbs
up" counters, per-review flag URLs, and a trailing cookie-consent block. They
also concatenate each review's tags with no delimiter
(``Tough graderLecture heavyTest heavy``).

This script rewrites each dirty file into the same shape as the hand-cleaned
files in ``documents/rmp_docs/clean_examples/`` and writes the result to
``documents/rmp_docs/clean/``.

Usage:
    python clean_rmp.py
"""

from __future__ import annotations

import re
from pathlib import Path

DIRTY_DIR = Path("documents/rmp_docs/dirty")
CLEAN_DIR = Path("documents/rmp_docs/clean")

# The five overall-rating buckets, in display order.
DISTRIBUTION_LABELS = ["Awesome 5", "Great 4", "Good 3", "OK 2", "Awful 1"]

# Per-review metadata fields we keep, identified by their "Key:" prefix.
META_RE = re.compile(r"^(For Credit|Attendance|Would Take Again|Grade|Textbook|Online Class):")

DATE_RE = re.compile(r"^[A-Z][a-z]{2}\.? \d{1,2}(st|nd|rd|th), \d{4}$")

# The fixed RateMyProfessors tag vocabulary. Tags are rendered concatenated with
# no separator, so we segment them by longest match against this list.
RMP_TAGS = [
    "Skip class? You won't pass.",
    "Accessible outside class",
    "Clear grading criteria",
    "Graded by few things",
    "Participation matters",
    "Beware of pop quizzes",
    "Gives good feedback",
    "Lots of homework",
    "Group projects",
    "Amazing lectures",
    "Get ready to read",
    "So many papers",
    "Tough grader",
    "Lecture heavy",
    "Inspirational",
    "EXTRA CREDIT",
    "Online savvy",
    "Test heavy",
    "Hilarious",
    "Respected",
    "Caring",
]
# Longest first so greedy prefix matching never stops short.
RMP_TAGS_BY_LEN = sorted(RMP_TAGS, key=len, reverse=True)


def _norm_apostrophes(text: str) -> str:
    """Fold curly apostrophes to straight so tag matching is encoding-agnostic."""
    return text.replace("’", "'")


def strip_icon(line: str) -> str:
    """Drop the leading 'Computer Icon ' marker that prefixes online courses."""
    return line.replace("Computer Icon ", "").strip()


def segment_tags(line: str) -> list[str] | None:
    """Split a concatenated tag string into its component tags.

    Returns the ordered list of tags if the whole line is consumed by known
    tags, otherwise ``None`` (meaning the line is not a tag line).
    """
    remaining = _norm_apostrophes(line.strip())
    tags: list[str] = []
    while remaining:
        for tag in RMP_TAGS_BY_LEN:
            if remaining.startswith(_norm_apostrophes(tag)):
                tags.append(tag)
                remaining = remaining[len(tag):]
                break
        else:
            return None  # hit text that isn't a known tag
    return tags or None


def parse_distribution(lines: list[str]) -> list[tuple[str, str]]:
    """Pull the (label, count) pairs out of the Rating Distribution block.

    The dirty file lists each count twice ("26" then "*26"); we take the first
    plain integer that follows each label.
    """
    stripped = [ln.strip() for ln in lines]
    result: list[tuple[str, str]] = []
    for label in DISTRIBUTION_LABELS:
        try:
            idx = stripped.index(label)
        except ValueError:
            continue
        for follow in stripped[idx + 1:]:
            if follow.isdigit():
                result.append((label, follow))
                break
    return result


def parse_review(block_lines: list[str]) -> str | None:
    """Turn one raw review block into the cleaned, indented review text.

    Returns ``None`` if the block doesn't look like a review (e.g. stray
    bullets between reviews).
    """
    # Keep only meaningful content lines; drop bullets and blank lines.
    content = [ln.strip() for ln in block_lines if ln.strip() and ln.strip() != "*"]
    if len(content) < 6:
        return None

    course = strip_icon(content[0])
    date = content[1]

    # Expect: course, date, "Quality", q, "Difficulty", d
    if content[2] != "Quality" or content[4] != "Difficulty":
        return None
    quality, difficulty = content[3], content[5]
    i = 6

    # The course code + date repeat right after the difficulty score; skip them.
    if i + 1 < len(content) and strip_icon(content[i]) == course and content[i + 1] == date:
        i += 2

    # Collect the metadata fields (variable set, order preserved).
    meta: list[str] = []
    while i < len(content) and META_RE.match(content[i]):
        meta.append(content[i])
        i += 1

    # Everything up to the "Helpful" footer is review text (+ maybe a tag line).
    rest: list[str] = []
    while i < len(content) and content[i] != "Helpful":
        rest.append(content[i])
        i += 1

    tags: list[str] | None = None
    if rest:
        maybe_tags = segment_tags(rest[-1])
        if maybe_tags is not None:
            tags = maybe_tags
            rest = rest[:-1]

    # Assemble the cleaned, 4-space-indented review.
    out = ["  *", f"    {course}", f"    {date}", "    Quality", f"    {quality}",
           "    Difficulty", f"    {difficulty}"]
    out.extend(f"    {m}" for m in meta)
    out.extend(f"    {line}" for line in rest)
    if tags:
        out.append(f"    Tags: {', '.join(tags)}")
    return "\n".join(out)


def clean_text(raw: str) -> str:
    lines = raw.splitlines()
    stripped = [ln.strip() for ln in lines]

    # --- Header: name, overall score, ratings count ---
    name = ""
    if "Share this rating" in stripped:
        start = stripped.index("Share this rating")
        for ln in stripped[start + 1:]:
            if ln:
                name = ln
                break

    score = ""
    if "/ 5" in stripped:
        slash = stripped.index("/ 5")
        for ln in reversed(stripped[:slash]):
            if ln:
                score = ln
                break

    count_match = re.search(r"Overall Quality Based on (\d+) ratings", raw)
    rating_count = count_match.group(1) if count_match else ""

    distribution = parse_distribution(lines)

    # --- Reviews region: between "All courses" and "Load More Ratings" ---
    try:
        region_start = stripped.index("All courses") + 1
    except ValueError:
        region_start = 0
    try:
        region_end = stripped.index("Load More Ratings")
    except ValueError:
        region_end = len(lines)
    region = lines[region_start:region_end]

    # Split the region into review blocks on the trailing flag URL line.
    reviews: list[str] = []
    block: list[str] = []
    for ln in region:
        if "flag/professor-rating" in ln:
            parsed = parse_review(block)
            if parsed:
                reviews.append(parsed)
            block = []
        else:
            block.append(ln)
    # Tail block (no trailing flag URL) — process if it holds a review.
    if block:
        parsed = parse_review(block)
        if parsed:
            reviews.append(parsed)

    # --- Assemble the cleaned document ---
    out: list[str] = [name, "", f"{score} / 5", f"Overall Quality Based on {rating_count} ratings",
                      "", "", "            Rating Distribution", ""]

    blocks: list[str] = []
    for label, cnt in distribution:
        blocks.append(f"  *\n    {label}\n\n    {cnt}")
    blocks.extend(reviews)

    out.append("\n\n".join(blocks))
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
