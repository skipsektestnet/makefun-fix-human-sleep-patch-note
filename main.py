#!/usr/bin/env python3
"""Fix Human Sleep: Funniest Patch Note — entry writer.

Writes the one-line entry to /output/entry.txt and validates it:
non-empty, at most 160 characters, exactly one line, no trailing
whitespace.
"""

import os
import sys

ENTRY = (
    "Fixed: humans now fall asleep in under eight minutes. Known issue: dreams still ship without a skip button."
)

MAX_CHARS = 160


def validate(text):
    """Check the entry against the bounty rules. Returns a list of problems."""
    problems = []
    if not text:
        problems.append("entry is empty")
    if len(text) > MAX_CHARS:
        problems.append(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text:
        problems.append("entry must be a single line")
    if text != text.strip():
        problems.append("entry has leading or trailing whitespace")
    return problems


def main():
    problems = validate(ENTRY)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    out_path = "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(ENTRY)
    print(f"wrote {len(ENTRY)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
