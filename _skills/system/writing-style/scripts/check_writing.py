#!/usr/bin/env python3
"""Report em dashes, exclamation points and banned words in prose files.

Usage: check_writing.py FILE [FILE ...]
Exit 0 if every file is clean, 1 if anything is found, 2 if a file can't be read.
Fenced code blocks and inline code are skipped. The writing patterns in SKILL.md are left to the writer.
"""

import re
import sys

DASHES = "—–―⸺⸻"  # em dash, en dash, horizontal bar, two-em and three-em dashes
WORDS = (
    "fluff", "crickets", "here's the thing", "here's the kicker", "void", "authentic",
    "vanity metrics", "pitch-slapped", "through the noise", "puzzle", "lightning", "magic",
    "superpower", "superpowers", "superstar", "superstars", "double-edged sword", "fast track",
    "strike gold", "secret weapon", "secret weapons", "arsenal", "savvy", "transformative",
    "buzzword", "integrity", "game-changer", "forget", "in a world of", "your truth",
    "thank you for it",
    # These verbs are also caught ending in -s, -ed or -ing.
    "harness", "harnesses", "harnessed", "harnessing",
    "thrive", "thrives", "thrived", "thriving",
    "skyrocket", "skyrockets", "skyrocketed", "skyrocketing",
    "soar", "soars", "soared", "soaring",
    "evolve", "evolves", "evolved", "evolving",
    "unlock", "unlocks", "unlocked", "unlocking",
    "unleash", "unleashes", "unleashed", "unleashing",
    "elevate", "elevates", "elevated", "elevating",
    "delve", "delves", "delved", "delving",
)
# Spaces and hyphens inside a phrase match either, so "game changer" and "fast-track" are caught too.
WORD_RE = re.compile(
    r"\b(" + "|".join(r"[\s-]+".join(map(re.escape, re.split(r"[\s-]+", w))) for w in WORDS) + r")\b",
    re.IGNORECASE,
)
BANG_RE = re.compile(r"(?<!<)!(?!\[)")  # skips Markdown images ![..] and HTML comments <!--
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def check(path):
    found = []
    fence = None
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            mark = line.lstrip()[:3]
            if mark in ("```", "~~~"):
                fence = mark if fence is None else (None if mark == fence else fence)
                continue
            if fence:
                continue
            text = INLINE_CODE_RE.sub("", line).replace("’", "'")
            found += [(n, f"em dash or similar ({c})") for c in text if c in DASHES]
            found += [(n, "exclamation point") for _ in BANG_RE.finditer(text)]
            found += [(n, f'banned word "{m.group(0)}"') for m in WORD_RE.finditer(text)]
    return found


def main(paths):
    if not paths:
        print(__doc__)
        return 2
    status = 0
    for path in paths:
        try:
            found = check(path)
        except (OSError, UnicodeDecodeError) as e:
            print(f"{path}: cannot read ({e})")
            return 2
        for n, what in found:
            print(f"{path}:{n}: {what}")
        print(f"{path}: {len(found)} found" if found else f"{path}: clean")
        status = status or (1 if found else 0)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
