# Usage Guide

## Installation

```bash
git clone <repository>
cd caesar-breaker
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Then:

```bash
pip install -e .
```

## Commands

### encrypt

```bash
caesar-breaker encrypt "HELLO WORLD" --key 3
```

### decrypt

```bash
caesar-breaker decrypt "KHOOR ZRUOG" --key 3
```

### break

Shows all 26 possible keys, with the most likely one marked.

```bash
caesar-breaker break "KHOOR ZRUOG"
caesar-breaker break --file examples/sample_ciphertexts.txt
echo "KHOOR ZRUOG" | caesar-breaker break
```

Output formats:

```bash
caesar-breaker break "KHOOR" --format json
caesar-breaker break "KHOOR" --format csv
```

### auto

Same 26-key analysis as `break`, framed for automatic use.

```bash
caesar-breaker auto "KHOOR ZRUOG"
```

### explain

Shows the character-by-character math for a given key.

```bash
caesar-breaker explain "KHOOR" --key 3
```

### alphabet

```bash
caesar-breaker alphabet
caesar-breaker alphabet --table
```

### interactive

```bash
caesar-breaker interactive
```

### Direct input shortcut

If you just want the full 26-key breakdown, you can skip the `break`
keyword entirely and pass the ciphertext straight in:

```bash
caesar-breaker "KHOOR ZRUOG"
```

This is equivalent to `caesar-breaker break "KHOOR ZRUOG"`.

## Global options

- `--version` - print the version and exit.
- `--debug` - print diagnostic information to stderr (stdout stays clean
  for JSON/CSV piping).
- `--help` - available on the app itself and on every subcommand.

## Notes on scoring

Automatic key selection in `break` and `auto` uses a heuristic score
combining common-word matches, English letter frequency, and common
bigrams/trigrams. It works well on real English sentences of a
reasonable length, but on very short or unusual ciphertexts it can pick
the wrong key. All 26 candidates are always shown so you can check the
alternatives yourself.
