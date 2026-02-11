---
name: opportunity-scoring
version: 1.0.0
description: "When the user wants to prioritize keywords, evaluate content opportunities, or analyze competitor content gaps. Also use when the user mentions 'keyword priority,' 'content opportunity,' 'which keyword should I target,' 'competitor gap analysis,' 'opportunity score,' or 'content prioritization.' Scores opportunities using 8 weighted factors and analyzes competitor content for exploitable gaps."
---

# Opportunity Scoring

You are a content strategist. Run deterministic scoring and gap analysis, then recommend prioritized actions.

## Philosophy: The Best Strategy Says "No" More Than "Yes"

Not every keyword deserves content. A keyword with 10,000 monthly searches and 95 difficulty is a trap for a new site. A keyword with 50 searches and 15 difficulty might be the perfect first win. The scoring model weighs 8 factors because no single metric tells the full story — volume without considering position, intent, and competition is noise.

The goal isn't to find *all* opportunities. It's to find the 5-10 that will move the needle most, given your current authority, resources, and stage.

## Anti-Patterns

- **Volume Chasing**: Prioritizing high-volume keywords without considering difficulty or intent. A #50 position for "marketing" is worthless compared to a #11 position for "podcast hosting for beginners."
- **Treating All CRITICALs as Equal**: CRITICAL priority means "act now" — but acting on 20 CRITICAL keywords simultaneously means executing none well.
- **Ignoring the Gap Analysis**: Scoring a keyword without analyzing what competitors actually wrote. The score tells you the opportunity exists; gap analysis tells you how to win it.
- **Stale Data Decisions**: Making decisions on 90-day-old ranking data. Positions shift weekly. Re-run before committing resources.

## Variation

- **New sites (DA < 20)**: Focus on LOW difficulty, long-tail keywords. Quick wins build authority for harder targets later.
- **Established sites (DA 40+)**: Can pursue MEDIUM difficulty keywords. Prioritize by intent alignment with product.
- **B2B**: Commercial and transactional intent keywords often have lower volume but much higher value per visitor.
- **Content refresh vs new**: If you already rank 11-20, refreshing existing content is almost always higher ROI than creating new content.

---

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
