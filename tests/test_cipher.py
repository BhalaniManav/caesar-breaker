from caesar_breaker.cipher import (
    decrypt,
    encrypt,
    normalize_key,
    shift_character,
)


def test_encrypt_basic():
    assert encrypt("HELLO", 3) == "KHOOR"


def test_decrypt_basic():
    assert decrypt("KHOOR", 3) == "HELLO"


def test_key_zero_is_identity():
    assert encrypt("HELLO", 0) == "HELLO"
    assert decrypt("HELLO", 0) == "HELLO"


def test_key_twenty_five():
    assert encrypt("A", 25) == "Z"
    assert decrypt("Z", 25) == "A"


def test_wraparound_forward():
    assert shift_character("Z", 1) == "A"


def test_wraparound_backward():
    assert shift_character("A", -1) == "Z"


def test_case_preservation():
    assert encrypt("Hello", 3) == "Khoor"
    assert decrypt("Khoor", 3) == "Hello"


def test_spaces_preserved():
    assert encrypt("HELLO WORLD", 3) == "KHOOR ZRUOG"


def test_punctuation_preserved():
    assert encrypt("HELLO, WORLD!", 3) == "KHOOR, ZRUOG!"


def test_numbers_preserved():
    assert encrypt("Hello, World! 123", 3) == "Khoor, Zruog! 123"


def test_key_normalization():
    assert normalize_key(26) == 0
    assert normalize_key(27) == 1
    assert normalize_key(-1) == 25


def test_full_alphabet_shift_by_one():
    plain = "abcdefghijklmnopqrstuvwxyz"
    cipher = "bcdefghijklmnopqrstuvwxyza"
    assert encrypt(plain, 1) == cipher


def test_round_trip_all_keys():
    original = "The Quick Brown Fox Jumps Over The Lazy Dog!"
    for key in range(26):
        assert decrypt(encrypt(original, key), key) == original
