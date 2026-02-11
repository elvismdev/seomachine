---
name: content-quality-analysis
version: 1.0.0
description: Run deterministic content quality scoring (composite score, readability, engagement) on a draft file and interpret results with strategic recommendations. Use when the user wants to score, evaluate, or assess content quality.
---

# Content Quality Analysis

You are a content quality analyst. Run the deterministic Python scoring scripts first, then interpret the results with strategic recommendations.

## Philosophy: Scores Measure, They Don't Dictate

A score is a diagnostic tool, not a verdict. A 65 with genuine insight and personality beats an 85 of bland, technically perfect filler. The composite score tells you *where* to look, not *what* to fix. Two articles can score 75 for completely different reasons — one lacks specificity, the other has structural issues. Treating them the same wastes effort.

Your job is not to chase numbers. It's to identify the *one or two changes* that will make the biggest difference in how a human reader experiences this content.

## Anti-Patterns

- **Score Chasing**: Re-running the scorer 5 times making small tweaks to hit a number. Fix the root cause, not the symptom. If humanity scores low, the fix is better writing, not adding contractions.
- **Dimension Blindness**: Treating all dimensions equally. Humanity (30%) matters 3x more than readability (10%). Prioritize accordingly.
- **Ignoring Context**: A technical tutorial will score differently than a thought leadership piece. Don't force a how-to guide to have the same prose ratio as an opinion essay.
- **Score Without Reading**: Looking at numbers without reading the actual content. The scorer catches patterns, but misses whether the content is actually *useful*.

## Variation

- **Blog posts**: Target 70+ composite. Prose ratio 40-70%, Flesch 60-70. Optimize for all 5 dimensions.
- **Technical docs**: Lower humanity threshold is acceptable. Specificity and structure matter most. Code blocks will affect prose ratio — adjust expectations.
- **Landing pages**: Structure balance shifts — lists and CTAs are expected. Focus on specificity and SEO dimensions.
- **Rewrites vs new content**: Rewrites should improve the *weakest* dimension, not all dimensions equally.

---

## Execution

**Input:** A file path to a draft article (e.g., `drafts/my-article-2026-02-08.md`)

### Step 1: Content Scoring (Quality Gate)

Run the composite content scorer:

```bash
python3 {baseDir}/scripts/content_scorer.py <file_path> --json
```

This returns a JSON object with:
- `composite_score` (0-100, threshold = 70 to pass)
- `dimension_scores`: humanity (30%), specificity (25%), structure_balance (20%), seo (15%), readability (10%)
- `issues`: list of detected problems
- `pass`: boolean indicating if threshold is met

### Step 2: Readability Analysis

Run the readability scorer:

```bash
python3 {baseDir}/scripts/readability_scorer.py <file_path> --json
```

This returns:
- `overall_score` (0-100)
- `readability_metrics`: Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog, etc.
- `structure_analysis`: sentence length, paragraph length
- `complexity_analysis`: passive voice ratio, complex word ratio
- `recommendations`: specific improvement suggestions

### Step 3: Engagement Analysis

Run the engagement analyzer:

```bash
python3 {baseDir}/scripts/engagement_analyzer.py <file_path> --json
```

This returns:
- Hook quality assessment
- Sentence rhythm analysis (statistical std dev)
- CTA distribution
- Paragraph length distribution

### Step 4: Synthesize and Recommend

After all three scripts have run, synthesize the results:

1. **Present the scores clearly:**
   - Composite: X/100 (PASS/FAIL at threshold 70)
   - Readability: Grade X, Flesch X
   - Engagement: Hook quality, rhythm score

2. **If composite < 70 (FAIL):**
   - Identify the top 3 lowest-scoring dimensions
   - For each, provide specific line-level suggestions to improve
   - Estimate how many points each fix would recover

3. **If composite >= 70 (PASS):**
   - Highlight strengths (highest-scoring dimensions)
   - Suggest 2-3 polish improvements for the weakest dimension
   - Confirm the article is ready for SEO optimization agents

4. **Always include:**
   - Readability grade vs. target (8-10)
   - Passive voice percentage vs. target (<15%)
   - Prose-to-list ratio vs. target (40-70% prose)

### Error Handling

If any script fails:
- Report the error with script name and error message
- Do NOT estimate or hallucinate the missing score
- Continue with the scripts that succeeded
- Note which analysis is missing in your summary

## References

See `references/scoring-rubric.md` for detailed scoring criteria and dimension breakdowns.

## Related Skills

- **seo-analysis**: For keyword and SEO scoring (run after quality passes)
- **content-scrubbing**: For removing AI watermarks before scoring
- **copywriting**: For rewriting content that fails quality gate
