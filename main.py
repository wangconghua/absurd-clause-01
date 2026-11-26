#!/usr/bin/env python3
"""The Absurd Clause Contest entry.

Writes one original English sentence -- a clause that could sit buried
deep inside a terms-of-service agreement -- to /output/entry.txt
(or $ENTRY_OUTPUT when set). Deterministic: the same bytes every run.
"""

import os
import sys

CLAUSE = (
    "In the event of a dispute, the parties agree to binding arbitration "
    "by competitive yodeling before a panel of three (3) impartial goats, "
    "whose decision shall be final."
)

MAX_CHARS = 200
SENTENCE_ENDERS = (".", "!", "?")


def has_balanced_parentheses(text):
    """True when every opening parenthesis in the clause is closed,
    in order, so the legal numbering (e.g. three (3)) stays well formed."""
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def is_single_sentence(text):
    """True when text holds exactly one sentence: one terminal mark,
    at the very end, with no other sentence-ending punctuation inside."""
    stripped = text.strip()
    if not stripped.endswith(SENTENCE_ENDERS):
        return False
    body = stripped[:-1]
    return not any(ch in SENTENCE_ENDERS for ch in body)


def validate(text):
    """Gate checks from the competition rules. Returns a list of errors."""
    errors = []
    if not text or not text.strip():
        errors.append("entry is empty or only whitespace")
    if len(text) != len(text.encode("utf-8").decode("utf-8")):
        errors.append("entry is not valid UTF-8 text")
    if not 1 <= len(text) <= MAX_CHARS:
        errors.append(
            "entry is %d characters, must be 1-%d" % (len(text), MAX_CHARS)
        )
    if not is_single_sentence(text):
        errors.append("entry must be a single sentence")
    if not has_balanced_parentheses(text):
        errors.append("entry has unbalanced parentheses")
    return errors


def main():
    errors = validate(CLAUSE)
    if errors:
        for error in errors:
            print("error: %s" % error, file=sys.stderr)
        return 1
    output_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(CLAUSE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
