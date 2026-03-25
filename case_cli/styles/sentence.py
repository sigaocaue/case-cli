"""Sentence case style: First word capitalized rest lowercase."""


def convert(tokens):
    """Convert tokens to Sentence case.

    Args:
        tokens: List of word tokens.

    Returns:
        String with only the first token capitalized, separated by spaces.
    """
    if not tokens:
        return ""
    return tokens[0].capitalize() + " " + " ".join(
        t.lower() for t in tokens[1:]
    ) if len(tokens) > 1 else tokens[0].capitalize()
