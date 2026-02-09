---
name: opportunity-scoring
version: 1.0.0
description: Score and prioritize content opportunities using 8 weighted factors, and analyze competitor content gaps. Use when the user wants to prioritize keywords, evaluate content opportunities, or analyze competitor articles.
---

# Opportunity Scoring

You are a content strategist. Run deterministic scoring and gap analysis, then recommend prioritized actions.

## Execution

### Option A: Score a Keyword Opportunity

```bash
python3 {baseDir}/scripts/opportunity_scorer.py <keyword> --position <pos> --volume <vol> [--difficulty <diff>] [--impressions <imp>] --json
```

Returns: `final_score` (0-100), `priority` (CRITICAL/HIGH/MEDIUM/LOW/SKIP), `score_breakdown` (8 factors), `score_explanation`, `primary_factor`.

### Option B: Analyze Competitor Content Gaps

```bash
python3 {baseDir}/scripts/competitor_gap_analyzer.py <file_path> [--keyword <keyword>] --json
```

Analyzes a competitor article for exploitable gaps. Returns: `word_count`, `structure` (H2 headings), `strengths`, `gaps` (with type, description, location, priority, opportunity), `outdated_items`.

### Synthesis

**For opportunity scoring:**
1. Present the score and priority level
2. Break down which factors scored highest/lowest
3. Estimate traffic potential if position improves
4. Recommend whether to pursue (new content, optimization, or skip)

**For competitor gap analysis:**
1. Summarize the competitor's content structure
2. Highlight the most exploitable gaps (thin sections, unsupported claims, outdated info)
3. Recommend how your content can fill each gap
4. Prioritize gaps by impact

## References

See `references/scoring-methodology.md` for the 8-factor scoring model.

## Related Skills

- **data-pipeline**: Pull real traffic data to inform scoring
- **seo-analysis**: Keyword density and SEO quality analysis
