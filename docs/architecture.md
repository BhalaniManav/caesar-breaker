# Architecture

The project separates cipher logic, breaking/scoring logic, and
presentation, so each piece can be tested and reused independently. The
CLI is a thin layer over the same public API you can import directly in
Python.

```
src/caesar_breaker/
├── __init__.py    Public API surface and package version
├── __main__.py     Enables `python -m caesar_breaker`
├── cli.py          Typer commands, argument parsing, interactive mode
├── cipher.py       encrypt / decrypt / shift_character / normalize_key
├── breaker.py      generate_candidates / break_cipher
├── analyzer.py      analyze_candidate / rank_candidates
├── scoring.py       score_text / word_score / letter_frequency_score / ngram_score
├── models.py         CipherResult / BreakResult dataclasses
├── utils.py          file / stdin reading, key parsing
└── output.py         Rich tables, JSON, and CSV rendering
```

## Data flow

1. `cli.py` resolves input from a direct argument, `--file`, or stdin
   (`utils.py`).
2. For breaking, `breaker.py` calls `cipher.decrypt()` for all 26 keys
   and scores each result with `scoring.py`.
3. Results are wrapped in a `BreakResult` (`models.py`).
4. `output.py` renders the result as a Rich table, JSON, or CSV,
   depending on the requested format.

## Design choices

- **No duplicated cipher logic.** The CLI calls the same
  `encrypt()` / `decrypt()` / `break_cipher()` functions that are
  exposed as the public Python API, so behavior is identical whether
  you use the command line or import the package.
- **Heuristic scoring is isolated.** `scoring.py` has no dependency on
  the CLI or on I/O, so its scoring functions can be unit tested and
  swapped out without touching anything else.
- **Only alphabetic ASCII characters are shifted.** Everything else
  (spaces, digits, punctuation, non-ASCII characters) passes through
  unchanged, and case is preserved.
- **stdout stays machine-readable.** JSON and CSV output only ever go
  to stdout; debug and error messages always go to stderr.
