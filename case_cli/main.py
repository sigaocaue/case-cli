"""CLI entry point for case-cli: argument parsing and command dispatch."""

import argparse
import logging
import os
import sys

from case_cli import __version__
from case_cli.converter import convert, STYLE_MAP, STYLE_NAMES
from case_cli.config import get_default_case, set_default_case


def _setup_logging():
    """Configure logging based on the CASE_CLI_LOG_LEVEL environment variable."""
    level = os.environ.get("CASE_CLI_LOG_LEVEL", "WARNING").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.WARNING),
        format="%(levelname)s: %(message)s",
    )


def main():
    """Main entry point for the case-cli command."""
    _setup_logging()

    parser = argparse.ArgumentParser(
        prog="case-cli",
        description="Convert strings between different case styles.",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="case-cli {}".format(__version__),
    )
    parser.add_argument(
        "-c", "--case",
        metavar="STYLE",
        help="Target case style ({})".format(", ".join(STYLE_NAMES)),
    )
    parser.add_argument(
        "input",
        nargs="*",
        help="Input string to convert, or 'set <style>' to set default case",
    )

    args = parser.parse_args()
    input_parts = args.input

    # Handle 'set' subcommand
    if input_parts and input_parts[0] == "set":
        if len(input_parts) < 2:
            print("Error: Please specify a case style. Example: case-cli set snake",
                  file=sys.stderr)
            sys.exit(1)
        case_name = input_parts[1].lower()
        if case_name not in STYLE_MAP:
            print("Error: Unknown case style '{}'. Available: {}".format(
                case_name, ", ".join(STYLE_NAMES)), file=sys.stderr)
            sys.exit(1)
        set_default_case(case_name)
        print("Default case style set to '{}'.".format(case_name))
        return

    # Need input text for conversion
    if not input_parts:
        parser.print_help()
        sys.exit(1)

    text = " ".join(input_parts)
    case_style = args.case

    # If no --case flag, try default
    if not case_style:
        case_style = get_default_case()
        if not case_style:
            print(
                "Error: No case style specified. Use --case/-c or set a default with: "
                "case-cli set <style>",
                file=sys.stderr,
            )
            sys.exit(1)

    try:
        result = convert(text, case_style)
        print(result)
    except ValueError as e:
        print("Error: {}".format(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
