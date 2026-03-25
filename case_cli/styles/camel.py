"""Camel case style: firstWordLowerRestCapitalized."""


def convert(tokens):
    """Convert tokens to camelCase.

    Args:
        tokens: List of word tokens.

    Returns:
        String with the first token in lowercase and subsequent tokens
        capitalized, all joined without separators.
    """
    if not tokens:
        return ""
    return tokens[0].lower() + "".join(t.capitalize() for t in tokens[1:])
