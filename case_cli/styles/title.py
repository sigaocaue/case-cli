"""Title case style: Major Words Capitalized with minor words lowercase."""

# Common minor words that should not be capitalized in title case
# (unless they are the first word)
MINOR_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "from",
    "in", "into", "nor", "of", "on", "or", "so", "the", "to",
    "up", "with", "yet",
}


def convert(tokens):
    """Convert tokens to Title Case.

    Minor words (articles, conjunctions, prepositions) are kept lowercase
    unless they are the first word.

    Args:
        tokens: List of word tokens.

    Returns:
        String in title case, separated by spaces.
    """
    if not tokens:
        return ""

    result = []
    for i, token in enumerate(tokens):
        if i == 0 or token.lower() not in MINOR_WORDS:
            result.append(token.capitalize())
        else:
            result.append(token.lower())
    return " ".join(result)
