"""Tests for the command-line interface."""

import sys

import pytest

from case_cli.main import main


@pytest.mark.parametrize("option,replacement,expected", [
    ("-s", "_", "hello__world"),
    ("--replace-spaces", "-", "hello--world"),
    ("-s", "", "helloworld"),
])
def test_replace_spaces_without_case(monkeypatch, capsys, option, replacement, expected):
    monkeypatch.setenv("CASE_CLI_DEFAULT_CASE", "upper")
    monkeypatch.setattr(sys, "argv", ["case-cli", "hello  world", option, replacement])
    main()
    assert capsys.readouterr().out == expected + "\n"


def test_replace_spaces_after_case_conversion(monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "argv", ["case-cli", "hello world", "-c", "upper", "-s", "_"]
    )
    main()
    assert capsys.readouterr().out == "HELLO_WORLD\n"


def test_replace_spaces_preserves_other_whitespace(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["case-cli", "hello\t world", "-s", "-"])
    main()
    assert capsys.readouterr().out == "hello\t-world\n"
