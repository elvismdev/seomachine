# Data Sources

This directory contains Python modules for analytics, SEO analysis, content scoring, CRO auditing, and WordPress publishing. These modules power the orchestration skills and are invoked by commands and agents.

## Overview

- **27 Python modules** in `modules/` covering 6 categories
- **3 data integrations**: Google Analytics 4, Google Search Console, DataForSEO
- **All modules** support `--json` flag for machine-readable output
- **Symlinked** into 22 skills via `scripts/` directories (41 symlinks total)

## Directory Structure

```
data_sources/
├── config/
│   ├── .env.example       # Template for environment variables
│   └── .env               # Your credentials (gitignored)
├── modules/               # 27 Python modules
│   ├── google_analytics.py          # GA4 traffic and engagement
│   ├── google_search_console.py     # Rankings, impressions, CTR
│   ├── dataforseo.py                # SERP positions, keyword metrics
│   ├── data_aggregator.py           # Combines GA4 + GSC + DataForSEO
│   ├── wordpress_publisher.py       # REST API publishing with Yoast SEO
│   ├── content_scorer.py            # Quality gate (composite 0-100 score)
│   ├── readability_scorer.py        # Flesch, grade level, passive voice
│   ├── engagement_analyzer.py       # Content engagement metrics
│   ├── seo_quality_rater.py         # Comprehensive SEO score (0-100)
│   ├── keyword_analyzer.py          # Density, TF-IDF, stuffing detection
│   ├── search_intent_analyzer.py    # Query intent classification
│   ├── content_length_comparator.py # SERP word count benchmarking
│   ├── content_scrubber.py          # AI watermark removal (Unicode + dashes)
│   ├── opportunity_scorer.py        # 8-factor keyword prioritization
│   ├── competitor_gap_analyzer.py   # Content gap analysis
│   ├── article_planner.py           # Article structure generation
│   ├── section_writer.py            # Section-level content writing
│   ├── above_fold_analyzer.py       # Above-fold CRO analysis
│   ├── cta_analyzer.py              # CTA effectiveness scoring
│   ├── trust_signal_analyzer.py     # Trust signal detection
│   ├── landing_page_scorer.py       # Landing page score (0-100)
│   ├── landing_performance.py       # Landing page GA4/GSC tracking
│   ├── cro_checker.py               # CRO checklist verification
│   ├── social_research_aggregator.py # Social media research
│   ├── sample_size_calculator.py    # A/B test sample size calculation
│   ├── subject_line_scorer.py       # Email subject line scoring
│   └── keyword_pattern_validator.py # Programmatic SEO pattern validation
├── cache/
│   └── .gitkeep
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r data_sources/requirements.txt
```

### 2. Configure Credentials

```bash
cp data_sources/config/.env.example data_sources/config/.env
```

Edit `data_sources/config/.env` with your credentials:

```env
# Google Analytics 4
GA4_PROPERTY_ID=123456789
GA4_CREDENTIALS_PATH=credentials/ga4-credentials.json

# Google Search Console
GSC_SITE_URL=https://yoursite.com
GSC_CREDENTIALS_PATH=credentials/ga4-credentials.json

# DataForSEO
DATAFORSEO_LOGIN=your_login
DATAFORSEO_PASSWORD=your_password

# WordPress
WORDPRESS_URL=https://yoursite.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_app_password
```

GA4/GSC use the same service account JSON. Place it at `credentials/ga4-credentials.json` and add the service account email to your GA4 property and Search Console.

### 3. Test Connectivity

```bash
python3 test_dataforseo.py
```

## Module Categories

### Data Integrations (5 modules)
| Module | Purpose |
|--------|---------|
| `google_analytics.py` | GA4 traffic, engagement, conversions, declining pages |
| `google_search_console.py` | Rankings, quick wins, low CTR, trending queries |
| `dataforseo.py` | SERP data, keyword ideas, competitor analysis |
| `data_aggregator.py` | Combines all three sources, generates reports |
| `wordpress_publisher.py` | Publish drafts to WordPress with Yoast SEO meta |

### Content Scoring (4 modules)
| Module | Purpose |
|--------|---------|
| `content_scorer.py` | Quality gate: composite score across 5 dimensions (threshold: 70) |
| `readability_scorer.py` | Flesch Reading Ease, grade level, passive voice |
| `engagement_analyzer.py` | Content engagement pattern analysis |
| `seo_quality_rater.py` | Comprehensive 0-100 SEO score with category breakdowns |

### SEO Analysis (4 modules)
| Module | Purpose |
|--------|---------|
| `keyword_analyzer.py` | Density, distribution, TF-IDF clustering, LSI keywords |
| `search_intent_analyzer.py` | Query intent classification (informational/commercial/transactional) |
| `content_length_comparator.py` | Benchmarks against top 10 SERP results |
| `content_scrubber.py` | AI watermark removal (12 Unicode chars + dash normalization) |

### CRO Analysis (6 modules)
| Module | Purpose |
|--------|---------|
| `above_fold_analyzer.py` | Above-fold content and value proposition analysis |
| `cta_analyzer.py` | CTA placement, copy, and effectiveness scoring |
| `trust_signal_analyzer.py` | Trust signal detection and recommendations |
| `landing_page_scorer.py` | Landing page score (0-100) with category breakdowns |
| `landing_performance.py` | GA4/GSC performance tracking for landing pages |
| `cro_checker.py` | CRO checklist verification |

### Content Pipeline (4 modules)
| Module | Purpose |
|--------|---------|
| `opportunity_scorer.py` | 8-factor keyword prioritization |
| `competitor_gap_analyzer.py` | Content gap analysis vs competitors |
| `article_planner.py` | Article structure generation |
| `section_writer.py` | Section-level content writing |

### Specialized (4 modules)
| Module | Purpose |
|--------|---------|
| `social_research_aggregator.py` | Social media research aggregation |
| `sample_size_calculator.py` | A/B test sample size and duration |
| `subject_line_scorer.py` | Email subject line scoring (5 dimensions) |
| `keyword_pattern_validator.py` | Programmatic SEO pattern validation |

## CLI Usage

All modules can be run from the repo root:

```bash
# Content scoring
python3 data_sources/modules/content_scorer.py drafts/my-article.md --json

# SEO analysis
python3 data_sources/modules/keyword_analyzer.py drafts/my-article.md "target keyword" --json

# WordPress publishing
python3 data_sources/modules/wordpress_publisher.py drafts/my-article.md --type post --json

# DataForSEO
python3 data_sources/modules/dataforseo.py "podcast hosting" --json
```

## Rate Limits & Costs

| Service | Free Tier | Cost |
|---------|-----------|------|
| Google Analytics 4 | 25,000 requests/day | Free |
| Google Search Console | Unlimited (reasonable use) | Free |
| DataForSEO | Pay-per-request | ~$0.006/keyword |

## Security

- `.env` and credential files are gitignored
- Use service accounts with read-only access
- WordPress uses application passwords (not user passwords)
- Rotate credentials regularly
