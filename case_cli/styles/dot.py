"""Dot case style: words.joined.by.dots."""


def convert(tokens):
    """Convert tokens to dot.case.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens in lowercase, joined by dots.
    """
    return ".".join(t.lower() for t in tokens)
