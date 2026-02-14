# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SEO Machine is an open-source Claude Code workspace for creating SEO-optimized blog content. It combines custom commands, specialized agents, Python-based analytics, and marketing skills to research, write, optimize, and publish articles for any business.

## Setup

```bash
pip install -r data_sources/requirements.txt
cp .env.example data_sources/config/.env  # then fill in credentials
cp config/competitors.example.json config/competitors.json  # customize for your business
```

API credentials in `data_sources/config/.env`: GA4, GSC, DataForSEO, WordPress. GA4 service account JSON goes in `credentials/ga4-credentials.json`. WordPress needs `WORDPRESS_URL`, `WORDPRESS_USERNAME`, `WORDPRESS_APP_PASSWORD`. Test connectivity with `python3 test_dataforseo.py`.

## Commands

All commands are defined in `.claude/commands/` and invoked as slash commands:

### Core Content Workflow
- `/research [topic]` - Keyword/competitor research, generates brief in `research/`
- `/write [topic]` - Create full article in `drafts/`, auto-runs scrubber + quality loop + 5 optimization agents
- `/rewrite [topic]` - Update existing content, saves to `rewrites/`
- `/optimize [file]` - Final SEO polish pass
- `/analyze-existing [URL or file]` - Content health audit
- `/scrub [file]` - Remove AI watermarks (Unicode, em-dashes); idempotent and safe to re-run
- `/publish-draft [file] [--type post|page|custom]` - Publish to WordPress via REST API as draft
- `/article [topic]` - Simplified article creation

### Analytics & Strategy
- `/performance-review` - Analytics-driven content priorities
- `/priorities` - Content prioritization matrix

### Research
- `/research-serp [keyword]`, `/research-gaps`, `/research-trending`, `/research-performance`, `/research-topics`

### Landing Pages
- `/landing-write [topic]`, `/landing-audit [file]`, `/landing-research [topic]`, `/landing-publish [file]`, `/landing-competitor [URL]`

## Architecture

### Command-Agent Model

**Commands** (`.claude/commands/`) orchestrate workflows. **Agents** (`.claude/agents/`) are specialized roles invoked by commands.

After `/write`, this pipeline runs automatically:
1. Save draft to `drafts/[topic-slug]-[date].md`
2. `/scrub` removes AI watermarks
3. `content_scorer.py` evaluates quality (composite score, threshold = 70)
4. If score < 70: auto-revise top fixes and re-score (max 2 iterations)
5. If still < 70 after 2 iterations: route to `review-required/` with `_REVIEW_NOTES.md`
6. If score >= 70: run 5 optimization agents (Content Analyzer, SEO Optimizer, Meta Creator, Internal Linker, Keyword Mapper)

Agents: `content-analyzer.md`, `seo-optimizer.md`, `meta-creator.md`, `internal-linker.md`, `keyword-mapper.md`, `editor.md`, `headline-generator.md`, `cro-analyst.md`, `landing-page-optimizer.md`, `performance.md`.

### Content Quality Scoring

`content_scorer.py` evaluates 5 weighted dimensions:
- Humanity/Voice (30%) - No AI phrases, contractions, personality
- Specificity (25%) - Concrete examples, numbers, names
- Structure Balance (20%) - 40-70% prose ratio (not all lists)
- SEO Compliance (15%) - Keywords, meta, structure
- Readability (10%) - Flesch 60-70, grade 8-10

### Python Analysis Pipeline

Located in `data_sources/modules/`. The Content Analyzer agent chains these modules:
1. `search_intent_analyzer.py` - Query intent classification (informational/navigational/transactional/commercial)
2. `keyword_analyzer.py` - Density, distribution, stuffing detection, TF-IDF clustering, LSI keywords
3. `content_length_comparator.py` - Benchmarks against top 10 SERP results
4. `readability_scorer.py` - Flesch Reading Ease, grade level, passive voice, sentence complexity
5. `seo_quality_rater.py` - Comprehensive 0-100 SEO score with category breakdowns

Additional modules: `content_scorer.py` (quality gate), `content_scrubber.py` (AI watermark removal), `opportunity_scorer.py` (8-factor prioritization), `engagement_analyzer.py`, `competitor_gap_analyzer.py`, `article_planner.py`, `section_writer.py`, `social_research_aggregator.py`, `sample_size_calculator.py` (A/B test sample size), `subject_line_scorer.py` (email subject scoring), `keyword_pattern_validator.py` (programmatic SEO validation).

### CRO Analysis Modules

Six modules for landing page conversion optimization:
- `above_fold_analyzer.py`, `cta_analyzer.py`, `trust_signal_analyzer.py`
- `landing_page_scorer.py` (0-100 with category breakdowns), `landing_performance.py` (GA4/GSC), `cro_checker.py`

### Data Integrations

- `google_analytics.py` - GA4 traffic/engagement
- `google_search_console.py` - Rankings, impressions, CTR
- `dataforseo.py` - SERP positions, keyword metrics
- `data_aggregator.py` - Combines GA4 + GSC + DataForSEO (gracefully handles missing credentials)
- `wordpress_publisher.py` - REST API publishing with Yoast SEO metadata

### Opportunity Scoring

`opportunity_scorer.py` uses 8 weighted factors: Volume (25%), Position (20%), Intent (20%), Competition (15%), Cluster (10%), CTR (5%), Freshness (5%), Trend (5%). Priority levels: CRITICAL, HIGH, MEDIUM, LOW, SKIP.

### Skills with Script Integration (Deterministic-First)

22 of the 36 skills wrap Python modules via symlinks in `scripts/` directories. These run deterministic Python analysis first, then use LLM reasoning to interpret results. The first 10 are dedicated orchestration skills; the remaining 12 are marketing skills enhanced with data pipelines:

| Skill | Scripts | Purpose |
|-------|---------|---------|
| `content-quality-analysis` | content_scorer, readability_scorer, engagement_analyzer, seo_quality_rater | Composite quality scoring |
| `seo-analysis` | keyword_analyzer, seo_quality_rater, search_intent_analyzer | Keyword density, TF-IDF, intent |
| `content-scrubbing` | content_scrubber | AI watermark removal (12 Unicode chars + dash normalization) |
| `landing-page-analysis` | landing_page_scorer, above_fold_analyzer, cta_analyzer, trust_signal_analyzer, cro_checker | Full CRO audit |
| `landing-performance` | landing_performance | GA4/GSC performance tracking |
| `data-pipeline` | google_analytics, google_search_console, dataforseo, data_aggregator | Traffic and search data |
| `opportunity-scoring` | opportunity_scorer, competitor_gap_analyzer | Keyword prioritization + gap analysis |
| `content-comparison` | content_length_comparator | SERP word count benchmarking |
| `wordpress-publishing` | wordpress_publisher | WordPress REST API publishing |
| `article-planning` | article_planner, section_writer | Article structure generation |
| `seo-audit` | seo_quality_rater | SEO audit with deterministic scoring |
| `page-cro` | cro_checker, landing_page_scorer | CRO audit with deterministic checks |
| `copywriting` | content_scorer | Copy quality with deterministic scoring |
| `analytics-tracking` | data_aggregator | Analytics with aggregated data |
| `form-cro` | cta_analyzer | Form CRO with CTA analysis |
| `ab-test-setup` | sample_size_calculator | A/B test sample size and duration |
| `competitor-alternatives` | competitor_gap_analyzer | Competitor comparison pages |
| `content-strategy` | competitor_gap_analyzer, opportunity_scorer | Content strategy with gap + opportunity data |
| `copy-editing` | content_scorer, readability_scorer | Copy editing with quality scoring |
| `email-sequence` | subject_line_scorer | Email sequences with subject line scoring |
| `popup-cro` | cta_analyzer | Popup CRO with CTA analysis |
| `programmatic-seo` | keyword_pattern_validator | Programmatic SEO pattern validation |

All scripts accept `--json` flags for machine-readable output. Skills use `{baseDir}/scripts/` to reference scripts portably.

### Marketing Skills Library

36 skills in `.claude/skills/`, each with a `SKILL.md` and optional `references/` and `scripts/` directories. Categories: Copywriting, CRO (page/form/signup/onboarding/popup/paywall), Strategy, Channels (email/social/paid-ads), SEO, Analytics. Invoked as slash commands (e.g., `/copywriting`, `/page-cro`, `/seo-audit`).

### Skill Architecture (Symlinks)

Skills with script integration use relative symlinks to share Python modules without copying:

```
.claude/skills/[skill-name]/
  SKILL.md              # YAML frontmatter + execution instructions
  scripts/
    module.py -> ../../../../data_sources/modules/module.py  (symlink)
    requirements.txt    # Dependencies
  references/
    reference-doc.md    # Scoring criteria, benchmarks, etc.
```

This pattern provides: progressive disclosure (frontmatter loaded at startup, full skill on trigger), deterministic-first execution (Python runs before LLM interprets), and zero module duplication (symlinks to single source of truth).

## Running Python Scripts

All scripts run from repo root. SEO analysis scripts load from `config/competitors.json`.

```bash
python3 research_quick_wins.py          # Quick win opportunities
python3 research_competitor_gaps.py     # Competitor content gaps
python3 research_performance_matrix.py  # Performance-based priorities
python3 research_priorities_comprehensive.py
python3 research_serp_analysis.py
python3 research_topic_clusters.py
python3 research_trending.py
python3 seo_baseline_analysis.py        # Requires config/competitors.json
python3 seo_bofu_rankings.py
python3 seo_competitor_analysis.py
```

## Content Pipeline

`topics/` (ideas) → `research/` (briefs) → `drafts/` (articles) → `review-required/` (failed quality gate) → `published/` (final)

Rewrites go to `rewrites/`. Landing pages go to `landing-pages/`. Audits go to `audits/`.

### File Naming Conventions
- Articles: `topic-slug-YYYY-MM-DD.md`
- Research briefs: `brief-topic-slug-YYYY-MM-DD.md`
- Reports: `[type]-report-topic-slug-YYYY-MM-DD.md`

## Context Files

`context/` contains brand guidelines that inform all content generation. These must be customized per business (see `examples/castos/` for a complete reference):
- `brand-voice.md` - Tone, messaging pillars, voice pillars
- `style-guide.md` - Grammar, formatting standards
- `seo-guidelines.md` - Keyword and structure rules
- `internal-links-map.md` - Key pages for internal linking
- `features.md` - Product features and differentiators
- `competitor-analysis.md` - Competitive intelligence
- `cro-best-practices.md` - Conversion optimization guidelines
- `target-keywords.md` - Keyword clusters and intent classification
- `writing-examples.md` - 3-5 exemplary posts that teach writing style

Content quality depends heavily on how well these files are populated. All commands and agents reference them.

## WordPress Integration

Publishing uses the WordPress REST API with a custom MU-plugin (`wordpress/seo-machine-yoast-rest.php`) that exposes Yoast SEO fields. Also requires `wordpress/functions-snippet.php` in your theme. Posts are always created as drafts (never auto-published). Articles use WordPress block format (HTML comments in Markdown).

## Contributing

Commands go in `.claude/commands/` with sections: "What This Command Does", "Process", "Output", "File Management". Agents go in `.claude/agents/` with: "Core Mission", "Expertise Areas", "Output Format", "Quality Standards". Follow existing file structure and conventions.
