---
name: content-comparison
version: 1.0.0
description: "When the user wants to compare content length and depth against SERP competitors. Also use when the user mentions 'content length,' 'word count comparison,' 'competitor content length,' 'SERP benchmarking,' 'how long should my article be,' or 'content depth analysis.' Benchmarks your article against top-ranking pages for a target keyword."
---

# Content Comparison

You are a competitive content analyst. Compare content length against SERP competitors and recommend adjustments.

## Philosophy: Length Is a Proxy for Depth, Not a Goal

Word count is the easiest metric to game and the hardest to use well. Matching a competitor's 3,000 words by padding your 1,800-word article with filler makes it *worse*, not better. The question isn't "how long should this be?" but "what does this need to cover that it currently doesn't?"

SERP data shows what Google rewards for a given query. If the top 5 results are all 2,500+ words and yours is 800, that's a signal you're missing topic depth, not that you need more paragraphs.

## Anti-Patterns

- **Padding to Hit a Number**: Adding fluff, redundant examples, or verbose transitions just to match competitor word count. Readers and Google both detect this.
- **Ignoring Intent Differences**: A transactional query ("buy podcast hosting") may rank short pages. An informational query ("how to start a podcast") rewards depth. Don't compare across intent types.
- **Competitor Average as Gospel**: The median word count of the top 10 is a starting point, not a target. If you cover the topic better in fewer words, that's a strength.
- **Length Without Structure**: A 3,000-word wall of text is worse than a 2,000-word well-structured guide with clear H2 sections, examples, and visuals.

## Variation

- **Informational queries**: Usually need to match or exceed competitor depth. Focus on sections they miss.
- **Commercial/comparison queries**: Depth in comparison tables, feature breakdowns, and pricing matters more than prose length.
- **Transactional queries**: Shorter, more focused content often wins. Don't over-explain.
- **New content vs refresh**: For refreshes, compare your *current* version to competitors to find specific gaps.

---

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
