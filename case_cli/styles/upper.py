"""Upper case style: ALL WORDS IN UPPERCASE separated by spaces."""


def convert(tokens):
    """Convert tokens to UPPER CASE.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens in uppercase, separated by spaces.
    """
    return " ".join(t.upper() for t in tokens)
