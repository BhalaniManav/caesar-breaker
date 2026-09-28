"""Small I/O and parsing helpers used by the CLI."""

from __future__ import annotations

import sys
from pathlib import Path


def read_text_from_file(path: Path) -> str:
    """Read and return the text content of a file.

    Raises FileNotFoundError with a clear message if the file is missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def read_text_from_stdin() -> str:
    """Read text piped into stdin, if any is available.

    Returns an empty string if stdin is an interactive terminal (nothing
    was piped in), rather than blocking.
    """
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read().strip()


def parse_key(value: str) -> int:
    """Parse a CLI key argument into an integer.

    Raises ValueError with a user-friendly message on failure.
    """
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError("Key must be an integer.")
