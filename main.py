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
    if "  " in text:
        problems.append("entry contains double spaces")
    if text and text[-1] not in ".!?":
        problems.append("entry should end with terminal punctuation (. ! ?)")
    if len(text.split()) < 2:
        problems.append("entry should contain at least two words")
    if not text.startswith("Fixed:"):
        problems.append("patch note entry should start with 'Fixed:'")
    return problems


def check_matches_entry_file(text):
    """The shipped entry.txt next to this script must match the ENTRY constant.

    Guards against the two copies of the line drifting apart silently.
    Returns a list of problems (empty when they agree).
    """
    entry_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    if not os.path.exists(entry_file):
        return ["entry.txt is missing next to main.py"]
    with open(entry_file, encoding="utf-8") as fh:
        shipped = fh.read().rstrip("\n")
    if shipped != text:
        return ["ENTRY constant does not match entry.txt"]
    return []


def main():
    problems = validate(ENTRY) + check_matches_entry_file(ENTRY)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_path = os.path.join(out_dir, "entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(ENTRY)
    print(f"wrote {len(ENTRY)} chars to {out_path}")
    print(
        f"validated: {len(ENTRY)} chars, {len(ENTRY.split())} words, "
        f"{MAX_CHARS - len(ENTRY)} chars under the {MAX_CHARS} limit"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
