"""Case style dispatch logic for converting strings between case styles."""

from case_cli.styles import (
    upper, lower, snake, kebab, header, camel, pascal,
    title, random_case, constant, ada, cobol, train, sentence, dot
)
from case_cli.styles.base import tokenize

# Map of case style names and aliases to their converter modules
STYLE_MAP = {
    "upper": upper,
    "u": upper,
    "lower": lower,
    "l": lower,
    "snake": snake,
    "s": snake,
    "kebab": kebab,
    "k": kebab,
    "header": header,
    "h": header,
    "camel": camel,
    "c": camel,
    "pascal": pascal,
    "p": pascal,
    "title": title,
    "t": title,
    "random": random_case,
    "r": random_case,
    "constant": constant,
    "ada": ada,
    "cobol": cobol,
    "train": train,
    "sentence": sentence,
    "dot": dot,
}

# Canonical style names (excludes aliases)
STYLE_NAMES = [
    "upper", "lower", "snake", "kebab", "header", "camel", "pascal",
    "title", "random", "constant", "ada", "cobol", "train", "sentence", "dot",
]


def convert(text, case_style):
    """Convert a string to the specified case style.

    Args:
        text: The input string to convert.
        case_style: The name or alias of the target case style.

    Returns:
        The converted string.

    Raises:
        ValueError: If the case style is not recognized.
    """
    style_key = case_style.lower()
    module = STYLE_MAP.get(style_key)
    if module is None:
        raise ValueError(
            "Unknown case style: '{}'. Available styles: {}".format(
                case_style, ", ".join(STYLE_NAMES)
            )
        )
    tokens = tokenize(text)
    if not tokens:
        return ""
    return module.convert(tokens)
