"""Shared Markdown cleaning utilities used across analysis modules."""

import re


def strip_markdown_for_analysis(content: str) -> str:
    """Strip Markdown formatting, leaving plain text for analysis.

    Removes: YAML frontmatter, bold-style metadata, horizontal rules,
    code blocks (fenced + inline), tables, link syntax, bold/italic,
    heading markers, and collapses whitespace.

    Used by: content_scorer, readability_scorer, and any future scorer
    that needs clean prose text.
    """
    text = content

    # Remove YAML frontmatter
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.DOTALL)

    # Remove frontmatter/metadata block (bold markdown style)
    text = re.sub(r'^\*\*[^*]+\*\*:\s*.+$', '', text, flags=re.MULTILINE)

    # Remove horizontal rules
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)

    # Remove fenced code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)

    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)

    # Remove table rows
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)

    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Remove bold and italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)

    # Remove heading markers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)

    # Collapse whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()

    return text
