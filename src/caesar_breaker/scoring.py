"""Heuristic scoring of candidate plaintexts.

This module estimates how "English-like" a piece of text is by combining
three signals: common word matches, letter frequency similarity to English,
and common bigram/trigram matches. This is a heuristic, not a guarantee -
on very short or unusual ciphertexts it can pick the wrong key.
"""

from __future__ import annotations

import re
from typing import Dict, Set

COMMON_WORDS: Set[str] = {
    "THE", "AND", "IS", "OF", "TO", "IN", "A", "FOR", "ON", "WITH",
    "THIS", "THAT", "HELLO", "WORLD", "YOU", "ARE", "IT", "AS", "BE",
    "AT", "BY", "AN", "WE", "OR", "FROM", "HAVE", "NOT", "BUT", "ALL",
    "CAN", "WILL", "MY", "YOUR", "HIS", "HER", "THEY", "OUR",
}

# Approximate relative frequency of each letter in English text (percent).
ENGLISH_LETTER_FREQ: Dict[str, float] = {
    "E": 12.70, "T": 9.06, "A": 8.17, "O": 7.51, "I": 6.97, "N": 6.75,
    "S": 6.33, "H": 6.09, "R": 5.99, "D": 4.25, "L": 4.03, "C": 2.78,
    "U": 2.76, "M": 2.41, "W": 2.36, "F": 2.23, "G": 2.02, "Y": 1.97,
    "P": 1.93, "B": 1.29, "V": 0.98, "K": 0.77, "J": 0.15, "X": 0.15,
    "Q": 0.10, "Z": 0.07,
}

COMMON_BIGRAMS: Set[str] = {"TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND"}
COMMON_TRIGRAMS: Set[str] = {"THE", "AND", "ING", "ION", "ENT"}

_WORD_RE = re.compile(r"[A-Za-z]+")


def word_score(text: str) -> float:
    """Percentage of words in `text` that match a small common-word list."""
    words = _WORD_RE.findall(text.upper())
    if not words:
        return 0.0
    hits = sum(1 for w in words if w in COMMON_WORDS)
    return (hits / len(words)) * 100.0


def letter_frequency_score(text: str) -> float:
    """Score based on how closely letter frequencies match English.

    Returns a value roughly in the 0-100 range; higher means the observed
    letter distribution is closer to typical English text.
    """
    letters = [ch for ch in text.upper() if ch.isalpha()]
    if not letters:
        return 0.0

    counts: Dict[str, int] = {}
    for ch in letters:
        counts[ch] = counts.get(ch, 0) + 1

    total = len(letters)
    penalty = 0.0
    for letter, count in counts.items():
        observed_pct = (count / total) * 100.0
        expected_pct = ENGLISH_LETTER_FREQ.get(letter, 0.0)
        penalty += abs(observed_pct - expected_pct)

    return max(0.0, 100.0 - penalty)


def ngram_score(text: str) -> float:
    """Score based on common English bigram/trigram matches."""
    letters_only = "".join(ch for ch in text.upper() if ch.isalpha())
    if len(letters_only) < 2:
        return 0.0

    bigram_hits = sum(
        1 for i in range(len(letters_only) - 1)
        if letters_only[i:i + 2] in COMMON_BIGRAMS
    )
    trigram_hits = sum(
        1 for i in range(len(letters_only) - 2)
        if letters_only[i:i + 3] in COMMON_TRIGRAMS
    )
    total_positions = max(1, len(letters_only) - 1)
    return ((bigram_hits + trigram_hits * 1.5) / total_positions) * 100.0


def score_text(text: str) -> float:
    """Combine word, frequency, and n-gram scoring into one heuristic score.

    Higher scores indicate text that looks more like valid English. This
    is heuristic: for very short ciphertexts, the highest-scoring key is
    not guaranteed to be the correct one.
    """
    w = word_score(text) * 2.0
    f = letter_frequency_score(text) * 0.5
    n = ngram_score(text) * 1.0
    return w + f + n
