"""Candidate analysis and ranking helpers."""

from __future__ import annotations

from typing import List

from .models import CipherResult


def analyze_candidate(candidate: CipherResult) -> CipherResult:
    """Hook for per-candidate analysis.

    Currently returns the candidate unchanged; kept as a separate function
    so additional analysis (e.g. dictionary lookups) can be added later
    without touching the breaker or CLI layers.
    """
    return candidate


def rank_candidates(candidates: List[CipherResult]) -> List[CipherResult]:
    """Return candidates sorted by score, highest first."""
    return sorted(candidates, key=lambda c: c.score, reverse=True)
