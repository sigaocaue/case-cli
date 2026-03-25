"""Constant case style: ALL_UPPERCASE_WITH_UNDERSCORES."""


def convert(tokens):
    """Convert tokens to CONSTANT_CASE.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens in uppercase, joined by underscores.
    """
    return "_".join(t.upper() for t in tokens)
