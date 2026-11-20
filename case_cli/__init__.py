"""case-cli: A command-line tool for converting strings between case styles."""

import sys

if sys.version_info < (3, 8):
    raise SystemExit(
        "Error: case-cli requires Python 3.8 or later. "
        "You are using Python {}.{}.".format(sys.version_info[0], sys.version_info[1])
    )

__version__ = "0.1.2"
