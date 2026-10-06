"""Keep recipe identifiers inside their intended URL path segment."""

from urllib.parse import quote, unquote


def validate_recipe_slug(value: str) -> str:
    """Reject URL structure, including nested escapes, without slugifying names.

    Mealie preserves explicitly supplied slugs; only generated slugs are
    slugified. Unicode, spaces and punctuation are therefore retained.
    """
    decoded = value
    while True:
        if (
            not decoded
            or decoded in {".", ".."}
            or any(char in decoded for char in "/\\?#")
            or any(ord(char) < 32 or ord(char) == 127 for char in decoded)
        ):
            raise ValueError("Recipe slug must be a single safe URL path segment")
        unescaped = unquote(decoded)
        if unescaped == decoded:
            return value
        decoded = unescaped


def recipe_slug_segment(value: str) -> str:
    """Validate before URL joining and encode the identifier exactly once."""
    return quote(validate_recipe_slug(value), safe="")
