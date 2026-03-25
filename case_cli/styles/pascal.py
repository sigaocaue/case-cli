"""Pascal case style: AllWordsCapitalized."""


def convert(tokens):
    """Convert tokens to PascalCase.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens capitalized, joined without separators.
    """
    return "".join(t.capitalize() for t in tokens)
