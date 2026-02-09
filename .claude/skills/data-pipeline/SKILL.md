---
name: data-pipeline
version: 1.0.0
description: Pull content performance data from GA4, GSC, and DataForSEO APIs. Use when the user wants traffic data, search rankings, keyword metrics, or a combined performance report.
---

# Data Pipeline

You are a data analyst. Pull real performance data from configured API sources and present actionable insights.

## Execution

**Input:** What data the user needs — traffic overview, keyword rankings, SERP data, or a combined report.

### Option A: Combined Performance Report

For a full overview across all configured data sources:

```bash
python3 {baseDir}/scripts/data_aggregator.py [--days <days>] --json
```

Returns: `summary` (pageviews, sessions, engagement, clicks, impressions, CTR), `top_performers`, `recommendations`. Gracefully handles missing credentials.

### Option B: GA4 Traffic Data

For traffic and engagement metrics:

```bash
python3 {baseDir}/scripts/google_analytics.py [--days <days>] [--limit <limit>] --json
```

Returns: `top_pages` (title, path, pageviews, engagement_rate), `declining_pages`.

### Option C: GSC Search Data

For search rankings and opportunities:

```bash
python3 {baseDir}/scripts/google_search_console.py [--days <days>] --json
```

Returns: `quick_wins` (keywords at position 11-20), `low_ctr_pages`, `trending_queries`.

### Option D: DataForSEO SERP Data

For keyword-specific SERP analysis:

```bash
python3 {baseDir}/scripts/dataforseo.py <keyword> [--domain <domain>] --json
```

Returns: `serp` (search_volume, organic_results, features), `related_questions`, optionally `rankings` for a specific domain.

### Synthesis

After running one or more scripts:
1. Present data clearly with the most actionable insights first
2. Highlight anomalies, declines, or opportunities
3. Connect data points across sources when possible
4. Recommend specific content actions based on the data

## Error Handling

- All scripts gracefully handle missing API credentials
- If no credentials are configured, suggest setting up `data_sources/config/.env`
- Report which data sources are available vs unavailable

## References

See `references/api-setup-guide.md` for credential configuration.

## Related Skills

- **opportunity-scoring**: Score and prioritize content opportunities
- **seo-analysis**: Keyword density and SEO quality analysis (no API needed)
