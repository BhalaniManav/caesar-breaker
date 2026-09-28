"""Terminal, JSON, and CSV rendering for break/auto/alphabet results."""

from __future__ import annotations

import csv
import io
import json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models import BreakResult

console = Console()
error_console = Console(stderr=True)


def print_banner(title: str, subtitle: str = "") -> None:
    text = title if not subtitle else f"{title}\n{subtitle}"
    console.print(Panel(text, expand=False, border_style="cyan"))


def print_break_table(result: BreakResult, title: str = "Caesar Cipher Breaker") -> None:
    """Render all 26 candidates in a table and highlight the best one."""
    table = Table(title=title, show_lines=False)
    table.add_column("Key", justify="right", style="cyan")
    table.add_column("Shift", justify="right", style="cyan")
    table.add_column("Plaintext", style="white")
    table.add_column("Score", justify="right", style="magenta")

    for r in result.results:
        is_best = r.key == result.best_key
        plaintext_display = f"{r.plaintext} \u2605" if is_best else r.plaintext
        row_style = "bold green" if is_best else None
        table.add_row(
            str(r.key), str(r.shift), plaintext_display, f"{r.score:.2f}",
            style=row_style,
        )

    console.print(table)
    console.print()
    console.print("[bold green]\u2605 MOST LIKELY PLAINTEXT[/bold green]")
    console.print(f"Key       : {result.best_key}")
    console.print(f"Plaintext : {result.best_plaintext}")


def format_json(result: BreakResult) -> str:
    """Serialize a BreakResult to a JSON string containing all 26 keys."""
    return json.dumps(result.to_dict(), indent=2)


def format_csv(result: BreakResult) -> str:
    """Serialize a BreakResult to CSV text containing all 26 keys."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["key", "shift", "plaintext", "score"])
    for r in result.results:
        writer.writerow([r.key, r.shift, r.plaintext, f"{r.score:.2f}"])
    return buf.getvalue()


def print_alphabet_plain() -> None:
    letters = " ".join(chr(ord("A") + i) for i in range(26))
    values = " ".join(str(i) for i in range(26))
    console.print("[bold]Caesar Cipher Alphabet Mapping[/bold]\n")
    console.print("Plain:")
    console.print(letters)
    console.print("\nValue:")
    console.print(values)


def print_alphabet_table() -> None:
    table = Table(title="Alphabet Mapping")
    table.add_column("Letter", justify="center")
    table.add_column("Value", justify="center")
    for i in range(26):
        table.add_row(chr(ord("A") + i), str(i))
    console.print(table)


def print_error(message: str) -> None:
    """Print a user-facing error message to stderr (no traceback)."""
    error_console.print(f"[bold red]Error:[/bold red] {message}")


def print_debug(message: str) -> None:
    """Print a debug message to stderr, keeping stdout clean for JSON/CSV."""
    error_console.print(f"[dim][debug][/dim] {message}")
