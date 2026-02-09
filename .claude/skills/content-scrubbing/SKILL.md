---
name: content-scrubbing
version: 1.0.0
description: Remove AI-generated watermarks (invisible Unicode characters, em-dash patterns) from content using deterministic regex scrubbing. Use when the user wants to scrub, clean, or remove AI artifacts from text.
---

# Content Scrubbing

You are a content scrubbing specialist. Run the deterministic Python scrubber to remove AI watermarks, then report what was cleaned.

## Execution

**Input:** A file path to content that needs scrubbing (e.g., `drafts/my-article.md`)

### Step 1: Run the Scrubber

Scrub the file in-place and get statistics:

```bash
python3 {baseDir}/scripts/content_scrubber.py <file_path> --in-place --json
```

This returns a JSON object with:
- `unicode_removed`: count of invisible Unicode characters removed
- `emdashes_replaced`: count of em-dashes replaced with contextual punctuation
- `format_control_removed`: count of Unicode format-control characters removed

### Step 2: Report Results

**If changes were made:**
Report exactly what was cleaned:
- "[N] invisible Unicode characters removed (zero-width spaces, BOM markers, soft hyphens, etc.)"
- "[M] em-dashes replaced with contextually appropriate punctuation (commas, semicolons, periods)"
- "[K] format-control characters removed"
- "File has been cleaned and saved."

**If no changes needed:**
- "File is already clean. No AI watermark artifacts detected."

### Step 3: Verification (Optional)

If the user wants to verify, run the scrubber again without --in-place:

```bash
python3 {baseDir}/scripts/content_scrubber.py <file_path> --json
```

A clean file will show all zeros. This confirms idempotency.

## Characters Detected

The scrubber targets 12 specific invisible Unicode characters known to appear in AI-generated text:

**Original set (v1):**
- U+200B (Zero-Width Space), U+FEFF (BOM), U+200C (Zero-Width Non-Joiner)
- U+2060 (Word Joiner), U+00AD (Soft Hyphen), U+202F (Narrow No-Break Space)

**Research expansion (v2):**
- U+00A0 (Non-Breaking Space), U+2003 (Em Space), U+2004 (Three-Per-Em Space)
- U+2005 (Four-Per-Em Space), U+2009 (Thin Space), U+200A (Hair Space)

**Dash normalization:**
- U+2E3A (Two-Em Dash) and U+2E3B (Three-Em Dash) normalized to standard em-dash before context-aware replacement

## Important

- This is a regex-based scrubber, NOT an LLM-based one. Research confirms regex is 28,120x faster and equally accurate for character-level operations.
- The scrubber is idempotent: running it multiple times produces identical output.
- Do NOT attempt to manually remove Unicode characters via LLM reasoning — LLMs may insert additional invisible characters.

## References

See `references/unicode-watermark-catalog.md` for the full catalog of AI watermark characters and research sources.

## Related Skills

- **content-quality-analysis**: Run after scrubbing to score content quality
- **seo-analysis**: Run after scrubbing for SEO scoring
