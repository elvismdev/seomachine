---
name: landing-page-analysis
version: 1.0.0
description: Run deterministic CRO analysis on landing pages (above-fold, CTAs, trust signals, CRO checklist, overall score). Use when the user wants to analyze, audit, or score a landing page for conversion optimization.
---

# Landing Page Analysis

You are a landing page CRO analyst. Run the deterministic Python analyzers first, then synthesize findings into actionable recommendations.

## Execution

**Input:** A file path to a landing page (e.g., `landing-pages/pricing-page.md`), plus optional parameters:
- Page type: `seo` (default) or `ppc`
- Conversion goal: `trial` (default), `demo`, or `lead`
- Primary keyword (for SEO pages)

### Step 1: Run Landing Page Scorer

Get the overall CRO score:

```bash
python3 {baseDir}/scripts/landing_page_scorer.py <file_path> --type <seo|ppc> --goal <trial|demo|lead> [--keyword <keyword>] --json
```

This returns: `overall_score` (0-100), `grade`, `category_scores` (above_fold, ctas, trust_signals, structure, seo), `critical_issues`, `warnings`, `suggestions`, `publishing_ready`.

### Step 2: Run Above-the-Fold Analyzer

Analyze the critical first impression:

```bash
python3 {baseDir}/scripts/above_fold_analyzer.py <file_path> --json
```

This returns: `overall_score`, `passes_5_second_test`, `element_scores` (headline, value_prop, cta, trust_signal), `issues`, `recommendations`.

### Step 3: Run CTA Analyzer

Analyze call-to-action effectiveness:

```bash
python3 {baseDir}/scripts/cta_analyzer.py <file_path> --goal <trial|demo|lead> --json
```

This returns: `summary` (total_ctas, average_quality_score, distribution_score, goal_alignment_score, overall_effectiveness), `ctas` (with positions and scores), `recommendations`.

### Step 4: Run Trust Signal Analyzer

Analyze trust and credibility elements:

```bash
python3 {baseDir}/scripts/trust_signal_analyzer.py <file_path> --json
```

This returns: `overall_score`, `grade`, `summary`, `strengths`, `weaknesses`, `recommendations`.

### Step 5: Run CRO Checklist

Run the full CRO audit checklist:

```bash
python3 {baseDir}/scripts/cro_checker.py <file_path> --type <seo|ppc> --goal <trial|demo|lead> --json
```

This returns: `score`, `grade`, `passes_audit`, `summary` (passed/total_checks), `critical_failures`, `categories`, `recommendations`.

### Step 6: Synthesize and Recommend

Combine all 5 analyses into a unified report:

1. **Overall Assessment**: Lead with the landing page score and grade
2. **Above-the-Fold Verdict**: Does it pass the 5-second test?
3. **CTA Effectiveness**: How many CTAs, quality, distribution, goal alignment
4. **Trust Signal Coverage**: Testimonials, social proof, risk reversals — what's missing?
5. **CRO Checklist**: Critical failures and top recommendations
6. **Priority Actions**: Rank the top 5-7 improvements by impact

## Error Handling

- If a script fails, report the error and continue with remaining analyses
- If all scripts fail, suggest checking that dependencies are installed (`pip install -r {baseDir}/scripts/requirements.txt`)

## References

See `references/cro-benchmarks.md` for CRO scoring benchmarks and best practices.

## Related Skills

- **content-quality-analysis**: For blog/article content quality scoring
- **seo-analysis**: For SEO-specific keyword and structure analysis
- **page-cro**: Marketing-focused CRO optimization guidance
