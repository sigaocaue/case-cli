"""Tokenizer utility for splitting input strings into word tokens."""

import re


def tokenize(text):
    """Split input text into tokens by common delimiters and case transitions.

    Handles spaces, hyphens, underscores, dots, and camelCase/PascalCase
    transitions. Preserves trailing special characters on the last token.

    Args:
        text: The input string to tokenize.

    Returns:
        A list of lowercase word tokens. Trailing non-alpha characters
        from the original input are appended to the last token.
    """
    if not text:
        return []

    # Capture trailing special characters (non-alphanumeric)
    trailing = ""
    match = re.search(r'([^a-zA-Z0-9]+)$', text)
    if match:
        trailing = match.group(1)
        text = text[:match.start()]

    if not text:
        return [trailing] if trailing else []

    # Replace delimiters (spaces, hyphens, underscores, dots) with a single space
    text = re.sub(r'[\s\-_\.]+', ' ', text)

    # Insert space before uppercase letters that follow lowercase letters (camelCase)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Insert space between consecutive uppercase letters followed by lowercase (PascalCase)
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)

    tokens = [t.lower() for t in text.split() if t]

    if tokens and trailing:
        tokens[-1] = tokens[-1] + trailing

    return tokens
