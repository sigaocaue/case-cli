"""Train case style: Words-Capitalized-And-Joined-By-Hyphens."""


def convert(tokens):
    """Convert tokens to Train-Case.

    Args:
        tokens: List of word tokens.

    Returns:
        String with all tokens capitalized, joined by hyphens.
    """
    return "-".join(t.capitalize() for t in tokens)
