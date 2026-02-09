---
name: landing-performance
version: 1.0.0
description: Track landing page performance metrics via GA4 and GSC. Use when the user wants to check how a landing page is performing, get traffic data, or review conversion metrics.
---

# Landing Performance

You are a landing page performance analyst. Pull real performance data from GA4 and GSC, then interpret the results.

## Execution

**Input:** A landing page URL (e.g., `https://yoursite.com/pricing/`), plus optional parameters:
- Lookback period in days (default: 30)
- Conversion goal: `trial` (default), `demo`, or `lead`

### Step 1: Run Performance Tracker

```bash
python3 {baseDir}/scripts/landing_performance.py <url> [--days <days>] [--goal trial|demo|lead] --json
```

This returns:
- `url`, `period_days`, `conversion_goal`
- `data_available`: whether GA4/GSC data was accessible
- `traffic`: page views, sessions, users, traffic sources
- `engagement`: bounce rate, avg time on page, scroll depth
- `conversions`: conversion rate, total conversions, by source
- `seo` (for SEO pages): impressions, clicks, CTR, avg position
- `grades`: A-F grades per category
- `recommendations`: prioritized improvement suggestions

### Step 2: Interpret Results

**If data is available:**
- Lead with overall performance grades
- Highlight any category below a B grade
- Compare metrics to benchmarks (see references)
- Provide specific, actionable recommendations

**If data is not available:**
- Report that GA4/GSC credentials are not configured
- Suggest the user set up API credentials (see `data_sources/config/.env`)
- Offer to do a content-based analysis instead using the `landing-page-analysis` skill

## Error Handling

- This module requires GA4 and/or GSC API credentials
- It gracefully handles missing credentials by returning `data_available: false`
- If credentials are missing, suggest alternative analysis approaches

## References

See `references/benchmark-grades.md` for performance benchmarks and grading criteria.

## Related Skills

- **landing-page-analysis**: Content-based CRO analysis (no API credentials needed)
- **analytics-tracking**: Set up and audit analytics tracking
