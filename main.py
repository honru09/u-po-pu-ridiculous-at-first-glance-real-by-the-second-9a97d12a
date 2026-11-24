#!/usr/bin/env python3
"""Entry for make.fun: Ridiculous at First Glance, Real by the Second.

Writes one sentence (at most 200 characters) pitching a bizarre startup
idea that sounds absurd until you realise it would actually sell, to
/output/entry.txt. Standard library only. Deterministic: the same bytes
are written on every run.

The pitch: retired librarians, hired out to shush open-plan offices.
Ridiculous at first glance (librarians as office enforcers); real by the
second (noise kills focus, firms already pay for quiet, and a shush is
cheaper than building a wall).
"""

import os
import sys

SENTENCE = (
    "We rent out retired librarians in cardigans to patrol open-plan "
    "offices and shush loud talkers, because noise kills focus, "
    "companies already pay for quiet, and a shush is cheaper than a wall."
)

MAX_CHARS = 200


def validate(text):
    """Check the entry meets the competition gate before anything is written."""
    if not isinstance(text, str) or not text.strip():
        return "entry text is blank"
    if len(text) != len(text.strip()):
        return "entry text has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "entry text must be a single line"
    if len(text) > MAX_CHARS:
        return "entry text is %d characters, over the %d limit" % (
            len(text),
            MAX_CHARS,
        )
    # One sentence: exactly one terminal period, at the very end.
    if text.count(".") != 1 or not text.endswith("."):
        return "entry text must be exactly one sentence ending in a period"
    return None


def main() -> int:
    error = validate(SENTENCE)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1

    payload = SENTENCE.encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    tmp_path = out_path + ".tmp"

    # Atomic write: the gate never sees a half-written file.
    with open(tmp_path, "wb") as fh:
        fh.write(payload)
    os.chmod(tmp_path, 0o644)
    os.replace(tmp_path, out_path)

    # Re-read verification: what is on disk must be exactly what we wrote.
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != payload:
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    decoded = written.decode("utf-8")
    if not 1 <= len(decoded) <= MAX_CHARS:
        print("verification failed: entry.txt length out of range", file=sys.stderr)
        return 1

    print("wrote %s (%d characters)" % (out_path, len(decoded)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
