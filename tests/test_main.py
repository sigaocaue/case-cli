"""Tests for the command-line interface."""

import runpy
import sys

import pytest

from case_cli import __version__
from case_cli.main import main


@pytest.fixture
def run_cli(monkeypatch, capsys, tmp_path):
    config_path = tmp_path / "config.json"
    monkeypatch.setenv("CASE_CLI_CONFIG_PATH", str(config_path))
    monkeypatch.delenv("CASE_CLI_DEFAULT_CASE", raising=False)

    def run(*args, exit_code=None):
        monkeypatch.setattr(sys, "argv", ["case-cli", *args])
        if exit_code is None:
            main()
        else:
            with pytest.raises(SystemExit) as error:
                main()
            assert error.value.code == exit_code
        return capsys.readouterr()

    return run


@pytest.mark.parametrize("option", ["-h", "--help"])
def test_help(run_cli, option):
    output = run_cli(option, exit_code=0)
    assert "usage: case-cli" in output.out
    assert "--case" in output.out
    assert "--replace-spaces" in output.out
    assert not output.err


@pytest.mark.parametrize("option", ["-v", "--version"])
def test_version(run_cli, option):
    assert run_cli(option, exit_code=0).out == "case-cli {}\n".format(__version__)


@pytest.mark.parametrize("shell", ["bash", "zsh"])
def test_completion_prints_shell_script(run_cli, shell):
    output = run_cli("--completion", shell)
    assert "# {} completion for case-cli".format(shell.capitalize()) in output.out
    assert "--case" in output.out
    assert "--replace-spaces" in output.out
    assert not output.err


def test_completion_handles_missing_package_data(run_cli, monkeypatch):
    monkeypatch.setattr("pkgutil.get_data", lambda *args: None)
    output = run_cli("--completion", "bash", exit_code=1)
    assert "completion script 'case-cli.bash' not found" in output.err
    assert not output.out


def test_set_persists_style_alias(run_cli):
    assert "set to 's'" in run_cli("set", "S").out
    assert run_cli("Hello", "World").out == "hello_world\n"


def test_style_precedence(run_cli, monkeypatch):
    run_cli("set", "snake")
    monkeypatch.setenv("CASE_CLI_DEFAULT_CASE", "upper")
    assert run_cli("Hello World").out == "HELLO WORLD\n"
    assert run_cli("--case=pascal", "Hello World").out == "HelloWorld\n"


def test_no_arguments_shows_usage(run_cli):
    output = run_cli(exit_code=1)
    assert "usage: case-cli" in output.out
    assert not output.err


@pytest.mark.parametrize("args,message", [
    (("hello world",), "No case style specified"),
    (("hello world", "-c", "invalid"), "Unknown case style: 'invalid'"),
    (("set",), "Please specify a case style"),
    (("set", "invalid"), "Unknown case style 'invalid'"),
])
def test_command_errors(run_cli, args, message):
    output = run_cli(*args, exit_code=1)
    assert message in output.err
    assert not output.out


@pytest.mark.parametrize("args,message", [
    (("hello world", "-c"), "expected one argument"),
    (("hello world", "--replace-spaces"), "expected one argument"),
    (("--completion", "invalid"), "invalid choice"),
    (("--unknown",), "unrecognized arguments"),
])
def test_argument_errors(run_cli, args, message):
    output = run_cli(*args, exit_code=2)
    assert message in output.err
    assert not output.out


def test_invalid_set_preserves_saved_style(run_cli):
    run_cli("set", "snake")
    run_cli("set", "invalid", exit_code=1)
    assert run_cli("hello world").out == "hello_world\n"


def test_module_entry_point(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["case_cli", "hello world", "-c", "snake"])
    runpy.run_module("case_cli", run_name="__main__")
    assert capsys.readouterr().out == "hello_world\n"


@pytest.mark.parametrize("args,expected", [
    ((" hello world ", "--replace-spaces=::"), "::hello::world::"),
    (("hello", "world", "--replace-spaces=-"), "hello-world"),
    (("hello world", "-c", "s", "-s", "-"), "hello_world"),
    (("hello world", "-s", r"\t"), r"hello\tworld"),
    (("", "-s", "_"), ""),
])
def test_replace_spaces_edge_cases(run_cli, args, expected):
    assert run_cli(*args).out == expected + "\n"


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
