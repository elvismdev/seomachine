---
name: content-comparison
version: 1.0.0
description: Compare your content length and depth against SERP competitors. Use when the user wants to benchmark their article against top-ranking pages.
---

# Content Comparison

You are a competitive content analyst. Compare content length against SERP competitors and recommend adjustments.

## Execution

**Input:** A file path to your content and a target keyword.

### Step 1: Run Content Length Comparator

```bash
python3 {baseDir}/scripts/content_length_comparator.py <file_path> --keyword <keyword> --json
```

Returns: `word_count`, `statistics` (min, max, mean, median of competitors), `recommendation` (status, optimal length), `competitive_analysis`.

Note: Full comparison requires SERP data from DataForSEO. Without it, returns your word count with a note to configure credentials.

### Step 2: Interpret Results

- Report your word count vs competitor median and 75th percentile
- Recommend specific word count targets
- Suggest which sections to expand or add

## References

See `references/serp-benchmarks.md` for content length benchmarks by intent type.

## Related Skills

- **seo-analysis**: For keyword density and SEO quality analysis
- **data-pipeline**: For fetching SERP data to power comparisons
