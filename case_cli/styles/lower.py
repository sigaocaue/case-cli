"""Lower case style: all words in lowercase separated by spaces."""


def convert(tokens):
    """Convert tokens to lower case.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens in lowercase, separated by spaces.
    """
    return " ".join(t.lower() for t in tokens)
