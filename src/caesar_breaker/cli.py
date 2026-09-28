"""Command-line interface for Caesar Cipher Breaker.

All commands call into the plain Python API in cipher.py / breaker.py -
no cipher logic is duplicated here.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer

from . import __version__
from .breaker import break_cipher
from .cipher import char_to_value, decrypt as cipher_decrypt, encrypt as cipher_encrypt, normalize_key
from .output import (
    console,
    format_csv,
    format_json,
    print_alphabet_plain,
    print_alphabet_table,
    print_banner,
    print_break_table,
    print_debug,
    print_error,
)
from .utils import parse_key, read_text_from_file, read_text_from_stdin

app = typer.Typer(
    name="caesar-breaker",
    help="Break, encrypt, decrypt, and explore Caesar ciphers from the command line.",
    add_completion=False,
    no_args_is_help=True,
)

_STATE = {"debug": False}

KNOWN_COMMANDS = {"encrypt", "decrypt", "break", "auto", "alphabet", "explain", "interactive"}
KNOWN_FLAGS_PREFIX = "-"


def _inject_default_command(argv: list[str]) -> list[str]:
    """Allow raw ciphertext as the first argument, defaulting to `break`.

    `caesar-breaker "KHOOR ZRUOG"` behaves like
    `caesar-breaker break "KHOOR ZRUOG"`. Known subcommands and any
    argument starting with '-' (flags like --help/--version) pass through
    unchanged.
    """
    if not argv:
        return argv
    first = argv[0]
    if first in KNOWN_COMMANDS or first.startswith(KNOWN_FLAGS_PREFIX):
        return argv
    return ["break", *argv]


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"Caesar Cipher Breaker v{__version__}")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the application version and exit.",
    ),
    debug: bool = typer.Option(
        False, "--debug", help="Print debug information to stderr."
    ),
) -> None:
    """Caesar Cipher Breaker: encrypt, decrypt, break, and study Caesar ciphers."""
    _STATE["debug"] = debug


def _resolve_input(text: Optional[str], file: Optional[Path]) -> str:
    """Resolve ciphertext/plaintext from a direct argument, a file, or stdin."""
    if text:
        return text
    if file is not None:
        try:
            return read_text_from_file(file)
        except FileNotFoundError as exc:
            print_error(str(exc))
            raise typer.Exit(code=1)
    stdin_text = read_text_from_stdin()
    if stdin_text:
        return stdin_text
    print_error("No input provided. Pass text directly, use --file, or pipe input via stdin.")
    raise typer.Exit(code=1)


def _parse_key_or_exit(key: str) -> int:
    try:
        return parse_key(key)
    except ValueError as exc:
        print_error(str(exc))
        raise typer.Exit(code=1)


@app.command()
def encrypt(
    text: Optional[str] = typer.Argument(None, help="Plaintext to encrypt."),
    key: str = typer.Option(..., "--key", "-k", help="Shift key (any integer; normalized mod 26)."),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Read plaintext from a file."),
) -> None:
    """Encrypt text with a Caesar cipher shift.

    Examples:
        caesar-breaker encrypt "HELLO WORLD" --key 3
        caesar-breaker encrypt --file plain.txt --key 5
    """
    k = _parse_key_or_exit(key)
    plaintext = _resolve_input(text, file)
    ciphertext = cipher_encrypt(plaintext, k)
    console.print(f"Plaintext : {plaintext}")
    console.print(f"Key       : {normalize_key(k)}")
    console.print(f"Ciphertext: {ciphertext}")


@app.command()
def decrypt(
    text: Optional[str] = typer.Argument(None, help="Ciphertext to decrypt."),
    key: str = typer.Option(..., "--key", "-k", help="Shift key (any integer; normalized mod 26)."),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Read ciphertext from a file."),
) -> None:
    """Decrypt text with a known Caesar cipher shift.

    Examples:
        caesar-breaker decrypt "KHOOR ZRUOG" --key 3
    """
    k = _parse_key_or_exit(key)
    ciphertext = _resolve_input(text, file)
    plaintext = cipher_decrypt(ciphertext, k)
    console.print(f"Ciphertext: {ciphertext}")
    console.print(f"Key       : {normalize_key(k)}")
    console.print(f"Plaintext : {plaintext}")


@app.command(name="break")
def break_command(
    text: Optional[str] = typer.Argument(None, help="Ciphertext to break. Reads stdin if omitted."),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Read ciphertext from a file."),
    format: str = typer.Option("human", "--format", help="Output format: human, json, or csv."),
    verbose: bool = typer.Option(False, "--verbose", help="Show extra diagnostic information."),
) -> None:
    """Show decryptions for all 26 possible keys (0 through 25).

    Examples:
        caesar-breaker break "KHOOR ZRUOG"
        caesar-breaker break --file ciphertext.txt
        caesar-breaker break "KHOOR" --format json
        echo "KHOOR ZRUOG" | caesar-breaker break
    """
    ciphertext = _resolve_input(text, file)

    if format not in {"human", "json", "csv"}:
        print_error(f"Unknown format '{format}'. Choose from: human, json, csv.")
        raise typer.Exit(code=1)

    if _STATE["debug"]:
        print_debug(f"Testing 26 keys against: {ciphertext!r}")

    result = break_cipher(ciphertext)

    if format == "json":
        typer.echo(format_json(result))
    elif format == "csv":
        typer.echo(format_csv(result), nl=False)
    else:
        if verbose:
            console.print(f"Input length       : {len(ciphertext)}")
            console.print("Alphabet            : A-Z")
            console.print("Alphabet size       : 26")
            console.print("Keys tested         : 26")
            console.print("Scoring method      : English frequency + n-grams\n")
        print_break_table(result)


@app.command()
def auto(
    text: Optional[str] = typer.Argument(None, help="Ciphertext to automatically analyze."),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Read ciphertext from a file."),
) -> None:
    """Automatically test all 26 keys and highlight the most likely plaintext.

    Example:
        caesar-breaker auto "KHOOR ZRUOG"
    """
    ciphertext = _resolve_input(text, file)
    result = break_cipher(ciphertext)
    print_break_table(result, title="Automatic Analysis")


@app.command()
def alphabet(
    table: bool = typer.Option(False, "--table", help="Display as a Rich table instead of plain text."),
) -> None:
    """Display the Caesar cipher alphabet mapping (A=0 through Z=25)."""
    if table:
        print_alphabet_table()
    else:
        print_alphabet_plain()


@app.command()
def explain(
    text: Optional[str] = typer.Argument(None, help="Ciphertext to explain."),
    key: str = typer.Option(..., "--key", "-k", help="Key to use for the explanation."),
) -> None:
    """Show the character-by-character math behind decrypting a ciphertext.

    Example:
        caesar-breaker explain "KHOOR" --key 3
    """
    k = _parse_key_or_exit(key)
    ciphertext = _resolve_input(text, None)
    k_norm = normalize_key(k)

    console.print("[bold]Character Calculation[/bold]\n")
    console.print("P = (C - K) mod 26\n")

    plaintext_chars = []
    for ch in ciphertext:
        if ch.isalpha():
            c_val = char_to_value(ch)
            p_val = (c_val - k_norm) % 26
            p_char = chr(ord("A") + p_val) if ch.isupper() else chr(ord("a") + p_val)
            console.print(
                f"{ch.upper()} = {c_val}    ({c_val} - {k_norm}) mod 26 = {p_val}    -> {p_char.upper()}"
            )
            plaintext_chars.append(p_char)
        else:
            plaintext_chars.append(ch)

    console.print()
    console.print(f"Therefore: {ciphertext} -> {''.join(plaintext_chars)}")


@app.command()
def interactive() -> None:
    """Run an interactive, menu-driven session."""
    print_banner("CAESAR CIPHER BREAKER")
    while True:
        console.print(
            "\n1. Encrypt\n2. Decrypt\n3. Break Cipher\n4. Automatic Analysis\n"
            "5. Alphabet Mapping\n6. Exit"
        )
        choice = typer.prompt("Select option").strip()

        if choice == "1":
            text = typer.prompt("Enter plaintext")
            try:
                k = parse_key(typer.prompt("Enter key"))
            except ValueError as exc:
                print_error(str(exc))
                continue
            console.print(f"Ciphertext: {cipher_encrypt(text, k)}")
        elif choice == "2":
            text = typer.prompt("Enter ciphertext")
            try:
                k = parse_key(typer.prompt("Enter key"))
            except ValueError as exc:
                print_error(str(exc))
                continue
            console.print(f"Plaintext: {cipher_decrypt(text, k)}")
        elif choice == "3":
            text = typer.prompt("Enter ciphertext")
            print_break_table(break_cipher(text))
        elif choice == "4":
            text = typer.prompt("Enter ciphertext")
            print_break_table(break_cipher(text), title="Automatic Analysis")
        elif choice == "5":
            print_alphabet_table()
        elif choice == "6":
            console.print("Goodbye.")
            break
        else:
            print_error("Invalid option. Choose 1-6.")


def main() -> None:
    """Console-script entry point: supports raw ciphertext as a default arg."""
    argv = sys.argv[1:]
    sys.argv = [sys.argv[0], *_inject_default_command(argv)]
    app()


if __name__ == "__main__":
    main()
