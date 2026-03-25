"""Kebab case style: words-joined-by-hyphens."""


def convert(tokens):
    """Convert tokens to kebab-case.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens in lowercase, joined by hyphens.
    """
    return "-".join(t.lower() for t in tokens)
