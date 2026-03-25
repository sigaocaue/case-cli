"""Default case style persistence using a local config file."""

import json
import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.expanduser("~"), ".case-cli", "config.json"
)


def _get_config_path():
    """Return the config file path, respecting the environment variable override."""
    return os.environ.get("CASE_CLI_CONFIG_PATH", DEFAULT_CONFIG_PATH)


def get_default_case():
    """Retrieve the default case style.

    Checks CASE_CLI_DEFAULT_CASE env var first, then falls back to
    the config file.

    Returns:
        The default case style name as a string, or None if not set.
    """
    env_default = os.environ.get("CASE_CLI_DEFAULT_CASE")
    if env_default:
        logger.debug("Using default case from environment: %s", env_default)
        return env_default

    config_path = _get_config_path()
    if not os.path.exists(config_path):
        logger.debug("Config file not found: %s", config_path)
        return None

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        default_case = config.get("default_case")
        logger.debug("Using default case from config: %s", default_case)
        return default_case
    except (json.JSONDecodeError, IOError) as e:
        logger.warning("Failed to read config file: %s", e)
        return None


def set_default_case(case_name):
    """Save the default case style to the config file.

    Creates the config directory if it does not exist.

    Args:
        case_name: The case style name to save as default.
    """
    config_path = _get_config_path()
    config_dir = os.path.dirname(config_path)

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        logger.debug("Created config directory: %s", config_dir)

    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    config["default_case"] = case_name

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    logger.info("Default case set to '%s' in %s", case_name, config_path)
