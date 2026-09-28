"""Automatic Caesar cipher breaking: generate and score all 26 keys."""

from __future__ import annotations

from typing import List

from .cipher import decrypt
from .models import BreakResult, CipherResult
from .scoring import score_text


def generate_candidates(ciphertext: str) -> List[CipherResult]:
    """Generate all 26 possible decryptions of `ciphertext`, each scored.

    Always returns exactly 26 results, keys 0 through 25 inclusive,
    including key 0 (no shift).
    """
    candidates: List[CipherResult] = []
    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = score_text(plaintext)
        candidates.append(
            CipherResult(key=key, shift=key, plaintext=plaintext, score=score)
        )
    return candidates


def break_cipher(ciphertext: str) -> BreakResult:
    """Break a Caesar cipher by testing all 26 keys and scoring each result.

    Returns a BreakResult containing every candidate plus the highest
    scoring one as the "most likely" plaintext. No candidates are hidden.
    """
    candidates = generate_candidates(ciphertext)
    best = max(candidates, key=lambda c: c.score)
    return BreakResult(
        ciphertext=ciphertext,
        results=candidates,
        best_key=best.key,
        best_plaintext=best.plaintext,
        best_score=best.score,
    )
