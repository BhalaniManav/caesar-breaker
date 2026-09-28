from typer.testing import CliRunner

from caesar_breaker.cli import app

runner = CliRunner()


def test_encrypt_command():
    result = runner.invoke(app, ["encrypt", "HELLO WORLD", "--key", "3"])
    assert result.exit_code == 0
    assert "KHOOR ZRUOG" in result.stdout


def test_decrypt_command():
    result = runner.invoke(app, ["decrypt", "KHOOR ZRUOG", "--key", "3"])
    assert result.exit_code == 0
    assert "HELLO WORLD" in result.stdout


def test_break_command_human():
    result = runner.invoke(app, ["break", "KHOOR ZRUOG"])
    assert result.exit_code == 0
    assert "HELLO WORLD" in result.stdout
    assert "MOST LIKELY PLAINTEXT" in result.stdout


def test_break_command_json_has_all_26_keys():
    result = runner.invoke(app, ["break", "KHOOR ZRUOG", "--format", "json"])
    assert result.exit_code == 0
    assert '"best_key": 3' in result.stdout
    assert result.stdout.count('"key":') == 26


def test_break_command_csv():
    result = runner.invoke(app, ["break", "KHOOR ZRUOG", "--format", "csv"])
    assert result.exit_code == 0
    assert "key,shift,plaintext,score" in result.stdout
    # header + 26 data rows
    assert len(result.stdout.strip().splitlines()) == 27


def test_auto_command():
    result = runner.invoke(app, ["auto", "KHOOR ZRUOG"])
    assert result.exit_code == 0
    assert "HELLO WORLD" in result.stdout


def test_alphabet_command_plain():
    result = runner.invoke(app, ["alphabet"])
    assert result.exit_code == 0
    assert "A" in result.stdout and "Z" in result.stdout
    assert "25" in result.stdout


def test_alphabet_command_table():
    result = runner.invoke(app, ["alphabet", "--table"])
    assert result.exit_code == 0


def test_explain_command():
    result = runner.invoke(app, ["explain", "KHOOR", "--key", "3"])
    assert result.exit_code == 0
    assert "HELLO" in result.stdout


def test_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Caesar Cipher Breaker" in result.stdout


def test_invalid_key_produces_clean_error_not_traceback():
    result = runner.invoke(app, ["encrypt", "HELLO", "--key", "abc"])
    assert result.exit_code != 0
    assert "Traceback" not in result.output
    assert "Error" in result.output


def test_help_flag():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "break" in result.stdout.lower() or "Break" in result.stdout


def test_break_help_flag():
    result = runner.invoke(app, ["break", "--help"])
    assert result.exit_code == 0
