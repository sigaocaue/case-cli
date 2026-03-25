"""Snake case style: words_joined_by_underscores."""


def convert(tokens):
    """Convert tokens to snake_case.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens in lowercase, joined by underscores.
    """
    return "_".join(t.lower() for t in tokens)
