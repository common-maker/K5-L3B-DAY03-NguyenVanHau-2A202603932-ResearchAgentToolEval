from __future__ import annotations

import re
from typing import Any

from tools._shared import fold_text, terms


def summarize_text(
    text: str = "",
    max_bullets: int = 5,
    focus: str = "",
) -> dict[str, Any]:
    """Extract key takeaways and bullet points from long text."""
    if not text or not text.strip():
        return {
            "tool": "summarize",
            "summary": "",
            "bullets": [],
            "bullet_count": 0,
            "error": "text is required",
        }

    # Normalize max_bullets
    try:
        max_bullets = max(1, int(max_bullets))
    except (ValueError, TypeError):
        max_bullets = 5

    # Split text into candidate sentences/segments
    raw_sentences = re.split(r"(?<=[.!?\n])\s+", text.strip())
    candidates = [s.strip().replace("\n", " ") for s in raw_sentences if len(s.strip()) > 15]

    if not candidates:
        # Fallback if text has no standard punctuation
        candidates = [text.strip()[:200]]

    # If focus keyword provided, prioritize candidates containing focus terms
    focus_terms = terms(focus) if focus else set()
    if focus_terms:
        scored: list[tuple[int, str]] = []
        for s in candidates:
            sterms = terms(s)
            score = len(focus_terms & sterms)
            scored.append((score, s))
        # Stable sort: highest score first
        scored.sort(key=lambda x: x[0], reverse=True)
        chosen = [s for score, s in scored[:max_bullets]]
    else:
        chosen = candidates[:max_bullets]

    bullets = [f"- {s}" for s in chosen]
    markdown_summary = "\n".join(bullets)

    return {
        "tool": "summarize",
        "summary": markdown_summary,
        "bullets": chosen,
        "bullet_count": len(chosen),
        "focus": focus,
    }
