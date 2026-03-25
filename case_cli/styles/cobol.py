"""COBOL case style: ALL-UPPERCASE-WITH-HYPHENS."""


def convert(tokens):
    """Convert tokens to COBOL-CASE.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens in uppercase, joined by hyphens.
    """
    return "-".join(t.upper() for t in tokens)
