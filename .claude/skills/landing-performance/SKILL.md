---
name: landing-performance
version: 1.0.0
description: "When the user wants to check landing page performance metrics. Also use when the user mentions 'landing page analytics,' 'page performance,' 'conversion metrics,' 'landing page traffic,' 'how is my page performing,' or 'page engagement data.' Pulls real performance data from GA4 and GSC with graded assessments."
---

# Landing Performance

You are a landing page performance analyst. Pull real performance data from GA4 and GSC, then interpret the results.

## Philosophy: Metrics Tell You What Happened, Not Why

A 2% conversion rate is neither good nor bad without context. For a cold-traffic SEO page, it's excellent. For a retargeting PPC page, it's terrible. Performance data answers "what happened?" — your job is to answer "why?" and "what now?"

Pair every metric with a hypothesis. If bounce rate is 75%, *why*? Slow load time? Mismatched search intent? Weak headline? The number alone doesn't tell you. Combine quantitative metrics with qualitative analysis (content review, intent matching) to find the real story.

## Anti-Patterns

- **Reacting to Single-Day Spikes**: A traffic spike on Tuesday doesn't mean your strategy is working. Look at 7-day and 30-day trends.
- **Comparing Different Traffic Mixes**: Last month had 80% organic traffic, this month is 60% organic and 40% paid. Conversion rate changes may reflect the traffic mix, not page performance.
- **Vanity Metrics**: Celebrating pageview increases while ignoring that conversion rate dropped. Traffic without conversion is a cost, not a win.
- **Missing Credential Paralysis**: When GA4/GSC aren't configured, doing nothing. Offer content-based analysis (landing-page-analysis) as an alternative.

## Variation

- **New pages (< 30 days)**: Limited data. Focus on early signals — bounce rate, time on page, initial CTR from GSC.
- **Established pages**: Full trend analysis. Compare to previous periods, identify declining metrics.
- **Seasonal content**: Account for seasonality when comparing periods. Year-over-year is more meaningful than month-over-month.
- **Post-change monitoring**: After optimizing a page, compare the 2 weeks before vs after. Allow for settling time.

---

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
