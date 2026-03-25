"""Random case style: rAnDoM MiX oF uPpEr AnD LoWeR cAsE."""

import random


def convert(tokens):
    """Convert tokens to rAnDoM cAsE.

    Each character is randomly converted to uppercase or lowercase.

    Args:
        tokens: List of word tokens.

    Returns:
        String with random capitalization, separated by spaces.
    """
    text = " ".join(tokens)
    return "".join(
        ch.upper() if random.randint(0, 1) else ch.lower()
        for ch in text
    )
