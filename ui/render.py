"""Format-aware rendering of source text for display (see D-16, D-20).

All internal processing works on the raw source; this module only decides
how the source is shown on screen. Today every format is shown literally.
"""

from rich.text import Text


def render_literal(text: str) -> Text:
    """Show the text exactly as it is: no markup, no rendering."""
    return Text(text)


# format -> function that turns raw text into something displayable
RENDERERS = {
    "md": render_literal,
    "txt": render_literal,
    "tex": render_literal,
}


def render_source(text: str, fmt: str) -> Text:
    """Single entry point used by the UI to display source text."""
    renderer = RENDERERS.get(fmt, render_literal)
    return renderer(text)