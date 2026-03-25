"""Tests for the config module."""

import json
import os
import pytest

from case_cli.config import get_default_case, set_default_case


@pytest.fixture
def tmp_config(tmp_path, monkeypatch):
    """Set up a temporary config file path."""
    config_file = str(tmp_path / "config.json")
    monkeypatch.setenv("CASE_CLI_CONFIG_PATH", config_file)
    monkeypatch.delenv("CASE_CLI_DEFAULT_CASE", raising=False)
    return config_file


class TestGetDefaultCase:
    def test_returns_none_when_no_config(self, tmp_config):
        assert get_default_case() is None

    def test_returns_value_from_config_file(self, tmp_config):
        os.makedirs(os.path.dirname(tmp_config), exist_ok=True)
        with open(tmp_config, "w") as f:
            json.dump({"default_case": "snake"}, f)
        assert get_default_case() == "snake"

    def test_env_var_overrides_config(self, tmp_config, monkeypatch):
        os.makedirs(os.path.dirname(tmp_config), exist_ok=True)
        with open(tmp_config, "w") as f:
            json.dump({"default_case": "snake"}, f)
        monkeypatch.setenv("CASE_CLI_DEFAULT_CASE", "kebab")
        assert get_default_case() == "kebab"

    def test_handles_corrupt_config(self, tmp_config):
        os.makedirs(os.path.dirname(tmp_config), exist_ok=True)
        with open(tmp_config, "w") as f:
            f.write("not valid json")
        assert get_default_case() is None


class TestSetDefaultCase:
    def test_creates_config_file(self, tmp_config):
        set_default_case("snake")
        assert os.path.exists(tmp_config)
        with open(tmp_config) as f:
            config = json.load(f)
        assert config["default_case"] == "snake"

    def test_updates_existing_config(self, tmp_config):
        set_default_case("snake")
        set_default_case("kebab")
        with open(tmp_config) as f:
            config = json.load(f)
        assert config["default_case"] == "kebab"

    def test_creates_directory_if_needed(self, tmp_path, monkeypatch):
        config_file = str(tmp_path / "subdir" / "config.json")
        monkeypatch.setenv("CASE_CLI_CONFIG_PATH", config_file)
        monkeypatch.delenv("CASE_CLI_DEFAULT_CASE", raising=False)
        set_default_case("pascal")
        assert os.path.exists(config_file)
