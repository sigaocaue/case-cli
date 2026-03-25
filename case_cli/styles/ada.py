"""Ada case style: Words_Capitalized_And_Joined_By_Underscores."""


def convert(tokens):
    """Convert tokens to Ada_Case.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens capitalized, joined by underscores.
    """
    return "_".join(t.capitalize() for t in tokens)
