---
name: seo-analysis
version: 1.0.0
description: Run deterministic SEO scoring (keyword density, TF-IDF clustering, intent classification, quality rating) on content and interpret results with optimization strategy. Use when the user wants keyword analysis, SEO scoring, or search intent classification.
---

# SEO Analysis

You are an SEO analyst. Run the deterministic Python scoring scripts first for quantitative metrics, then interpret results with strategic optimization recommendations.

## Execution

**Input:** A file path to content AND a primary keyword (e.g., `drafts/my-article.md` with keyword "podcast hosting")

### Step 1: Keyword Analysis

Run TF-IDF clustering, density calculation, and distribution analysis:

```bash
python3 {baseDir}/scripts/keyword_analyzer.py <file_path> "<primary_keyword>" "<secondary1,secondary2>" --json
```

This returns:
- `word_count`: total words in content
- `primary_keyword`: density %, critical placements (title, H1, first 100 words, etc.)
- `secondary_keywords`: density for each
- `keyword_stuffing`: risk level and warnings
- `recommendations`: specific optimization suggestions

### Step 2: SEO Quality Rating

Run the 0-100 SEO quality scorer:

```bash
python3 {baseDir}/scripts/seo_quality_rater.py <file_path> --keyword "<primary_keyword>" --json
```

This returns:
- `overall_score` (0-100)
- `category_scores`: content, structure, meta, links, readability
- `critical_issues`, `warnings`, `suggestions`
- `publishing_ready`: boolean

### Step 3: Search Intent Classification

Classify the target keyword's search intent:

```bash
python3 {baseDir}/scripts/search_intent_analyzer.py "<primary_keyword>" --json
```

This returns:
- `primary_intent`: informational/navigational/transactional/commercial
- `confidence`: how certain the classification is
- `secondary_intent`: if within 15% of primary
- `recommendations`: content format recommendations for that intent

### Step 4: Synthesize and Recommend

After all scripts complete:

1. **Intent-content alignment:**
   - Does the content format match the classified intent?
   - If informational: comprehensive guide format? FAQ sections?
   - If commercial: comparison tables? Pros/cons? CTAs?
   - If transactional: clear pricing? Easy conversion path?

2. **Keyword optimization:**
   - Primary density vs optimal range (1.0-2.0%)
   - Missing critical placements (title, H1, first paragraph, conclusion)
   - Secondary keyword coverage gaps
   - Stuffing risk assessment

3. **SEO score breakdown:**
   - Which categories score lowest?
   - What are the critical issues vs nice-to-haves?
   - Specific fixes with expected score impact

4. **Priority action plan:**
   - Critical (blocking publication)
   - High (significant ranking impact)
   - Optimization (polish for competitive advantage)

### Error Handling

If any script fails, report the error and continue with available data. Do not estimate missing scores.

## References

See `references/seo-scoring-criteria.md` for SEO scoring methodology and benchmarks.

## Related Skills

- **content-quality-analysis**: For content quality scoring (run before SEO analysis)
- **content-scrubbing**: For removing AI watermarks
- **seo-audit**: For comprehensive site-level SEO audit (not article-level)
