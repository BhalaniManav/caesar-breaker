from caesar_breaker.breaker import break_cipher, generate_candidates
from caesar_breaker.cipher import encrypt


def test_generates_exactly_26_candidates():
    candidates = generate_candidates("KHOOR ZRUOG")
    assert len(candidates) == 26
    assert {c.key for c in candidates} == set(range(26))


def test_candidate_zero_is_unshifted_input():
    candidates = generate_candidates("KHOOR ZRUOG")
    key_zero = next(c for c in candidates if c.key == 0)
    assert key_zero.plaintext == "KHOOR ZRUOG"


def test_break_known_cipher():
    result = break_cipher("KHOOR ZRUOG")
    assert result.best_key == 3
    assert result.best_plaintext == "HELLO WORLD"
    assert len(result.results) == 26


def test_break_finds_correct_key_for_common_phrase():
    plaintext = "THIS IS THE WORLD"
    for key in [1, 5, 10, 15, 20, 25]:
        ciphertext = encrypt(plaintext, key)
        result = break_cipher(ciphertext)
        assert result.best_key == key
        assert result.best_plaintext == plaintext
