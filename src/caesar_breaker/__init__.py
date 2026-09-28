"""Caesar Cipher Breaker.

A small, well-tested toolkit for encrypting, decrypting, and automatically
breaking classical Caesar ciphers. Built for cryptography education, CTFs,
and authorized security research.
"""

from __future__ import annotations

__version__ = "1.0.0"

from .cipher import decrypt, encrypt
from .breaker import break_cipher, generate_candidates

__all__ = [
    "__version__",
    "encrypt",
    "decrypt",
    "break_cipher",
    "generate_candidates",
]
