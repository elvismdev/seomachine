# Unicode Watermark Character Catalog

## Characters Detected and Removed

### Original Set (v1)

| Character | Unicode | Hex | Description | Source |
|-----------|---------|-----|-------------|--------|
| Zero-Width Space | U+200B | `\u200B` | Invisible space with zero width | Common in all LLM output |
| BOM / ZWNBSP | U+FEFF | `\uFEFF` | Byte Order Mark, often a remnant | Copy-paste artifact |
| Zero-Width Non-Joiner | U+200C | `\u200C` | Prevents ligature formation | Found in GPT output |
| Word Joiner | U+2060 | `\u2060` | Invisible word boundary | Found in Claude/GPT output |
| Soft Hyphen | U+00AD | `\u00AD` | Invisible hyphenation hint | Typography artifact |
| Narrow No-Break Space | U+202F | `\u202F` | Narrower than regular NBSP | ChatGPT o3/o4-mini (Rumi discovery, Apr 2025) |

### Research Expansion (v2 - Feb 2026)

| Character | Unicode | Hex | Description | Source |
|-----------|---------|-----|-------------|--------|
| Non-Breaking Space | U+00A0 | `\u00A0` | Space that prevents line breaks | Common in ChatGPT output |
| Em Space | U+2003 | `\u2003` | Space width of letter 'M' | Identified by gptwatermark.com |
| Three-Per-Em Space | U+2004 | `\u2004` | 1/3 of an em space | Emerging in newer models |
| Four-Per-Em Space | U+2005 | `\u2005` | 1/4 of an em space | Emerging in newer models |
| Thin Space | U+2009 | `\u2009` | Narrow space for typography | Training data artifact |
| Hair Space | U+200A | `\u200A` | Very narrow space | Training data artifact |

### Dash Variants (Normalized to Em Dash Before Replacement)

| Character | Unicode | Hex | Description |
|-----------|---------|-----|-------------|
| Two-Em Dash | U+2E3A | `\u2E3A` | Double-length em dash |
| Three-Em Dash | U+2E3B | `\u2E3B` | Triple-length em dash |

## Research Sources

- **Rumi (Apr 2025)**: Discovered U+202F in GPT-o3 and o4-mini. OpenAI responded: "a quirk of large-scale reinforcement learning"
- **gptwatermark.com**: Tracks 34+ invisible characters across AI models
- **JAMIA Open (2025)**: Regex is 28,120x faster than LLM for character-level extraction (P = .56, no accuracy difference)
- **Clemens Jarnach (Apr 2025)**: Independent Unicode analysis confirming character patterns
- **AWS Security Blog**: Unicode character smuggling as LLM attack vector

## Why Regex, Not LLM

1. LLMs may INSERT additional invisible characters when asked to remove them
2. Regex is deterministic — same input always produces same output
3. Regex is 28,120x faster for character-level operations (peer-reviewed)
4. Running regex twice produces identical output; LLMs do not guarantee this
