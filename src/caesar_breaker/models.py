"""Data models shared across the CLI, breaker, and output layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CipherResult:
    """A single decryption candidate for one key."""

    key: int
    shift: int
    plaintext: str
    score: float = 0.0


@dataclass
class BreakResult:
    """The full outcome of testing all 26 keys against a ciphertext."""

    ciphertext: str
    results: List[CipherResult] = field(default_factory=list)
    best_key: int = 0
    best_plaintext: str = ""
    best_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dict suitable for JSON output."""
        return {
            "cipher": self.ciphertext,
            "alphabet_size": 26,
            "results": [
                {
                    "key": r.key,
                    "plaintext": r.plaintext,
                    "score": round(r.score, 2),
                }
                for r in self.results
            ],
            "best_key": self.best_key,
            "best_plaintext": self.best_plaintext,
        }
