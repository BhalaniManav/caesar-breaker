"""Core Caesar cipher mathematics.

Alphabet mapping used throughout this project:

    A=0  B=1  C=2  D=3  E=4  F=5  G=6  H=7  I=8  J=9  K=10 L=11 M=12
    N=13 O=14 P=15 Q=16 R=17 S=18 T=19 U=20 V=21 W=22 X=23 Y=24 Z=25

Encryption:  C = (P + K) mod 26
Decryption:  P = (C - K) mod 26

Only alphabetic ASCII characters are shifted. Case, spaces, digits,
punctuation, and any other characters are preserved unchanged.
"""

from __future__ import annotations

ALPHABET_SIZE = 26


def normalize_key(key: int) -> int:
    """Normalize any integer key into the 0-25 range using modulo 26.

    Examples:
        normalize_key(26) == 0
        normalize_key(27) == 1
        normalize_key(-1) == 25
    """
    return key % ALPHABET_SIZE


def char_to_value(char: str) -> int:
    """Convert a single alphabetic character to its 0-25 value (A/a = 0)."""
    if len(char) != 1 or not char.isalpha():
        raise ValueError(f"{char!r} is not a single alphabetic character")
    base = ord("A") if char.isupper() else ord("a")
    return ord(char) - base


def value_to_char(value: int, upper: bool = True) -> str:
    """Convert a 0-25 value back into a letter, upper or lower case."""
    value = normalize_key(value)
    base = ord("A") if upper else ord("a")
    return chr(base + value)


def shift_character(char: str, key: int) -> str:
    """Shift a single character by `key` positions, preserving case.

    Non-alphabetic characters (spaces, digits, punctuation, unicode
    symbols, etc.) are returned unchanged.
    """
    if len(char) != 1 or not char.isalpha() or ord(char) > 127:
        return char

    key = normalize_key(key)
    base = ord("A") if char.isupper() else ord("a")
    shifted = (ord(char) - base + key) % ALPHABET_SIZE
    return chr(base + shifted)


def encrypt(text: str, key: int) -> str:
    """Encrypt `text` with a Caesar cipher shift of `key` positions.

    Case, spaces, numbers, punctuation, and non-ASCII characters are
    preserved. The key is normalized with modulo 26, so any integer
    (including negative numbers or values above 25) is accepted.
    """
    key = normalize_key(key)
    return "".join(shift_character(ch, key) for ch in text)


def decrypt(text: str, key: int) -> str:
    """Decrypt `text` with a Caesar cipher shift of `key` positions.

    This is equivalent to encrypting with the inverse shift.
    """
    key = normalize_key(key)
    return "".join(shift_character(ch, -key) for ch in text)
