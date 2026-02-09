# Proposal: Skills-as-Orchestration-Wrappers

## Why

SEO Machine has 24 Python analysis modules and 26 Skills that exist in completely separate worlds. The only bridge is the command layer — users must know which commands invoke which scripts, and Skills have zero access to deterministic computation. This creates discoverability gaps (users don't know Python capabilities exist), portability issues (modules aren't self-contained), and missed integration opportunities (Skills can't run scripts even though the platform supports it).

Anthropic's Skills specification officially supports `scripts/` directories with executable Python code, using progressive disclosure so only ~30-50 tokens load at startup. This project's 26 skills use none of this capability. The research-backed PRD (`docs/PRD-skills-modules-architecture-upgrade.md`) validates that wrapping Python modules inside Skills is the correct hybrid architecture — deterministic computation first, LLM interpretation second.

## What Changes

- Create **10 new Skills** across 4 phases, each with `SKILL.md` + `scripts/` + `references/` directories
- Bundle existing Python modules into skill `scripts/` directories (symlinks for development)
- Each SKILL.md instructs Claude to: (1) run Python scripts for quantitative metrics, (2) interpret results with LLM reasoning for qualitative recommendations
- Enhance `content_scrubber.py` with 6 additional Unicode watermark characters identified by recent research
- Augment 5 existing marketing skills (`seo-audit`, `page-cro`, `copywriting`, `analytics-tracking`, `form-cro`) with `scripts/` directories

## Capabilities

### New Capabilities
- `content-quality-analysis`: Single-invocation quality gate — runs content_scorer + readability_scorer + engagement_analyzer, synthesizes strategic recommendations
- `seo-analysis`: Unified SEO scoring — runs keyword_analyzer + seo_quality_rater + search_intent_analyzer, provides keyword strategy
- `content-scrubbing`: Enhanced AI watermark removal — runs content_scrubber with expanded Unicode catalog (12+ characters), reports what was cleaned
- `landing-page-analysis`: CRO dashboard — runs 5 CRO scripts in sequence, presents unified conversion scoring
- `landing-performance`: Performance grading with benchmarks — runs landing_performance with graceful API degradation
- `data-pipeline`: Unified analytics — runs GA4 + GSC + DataForSEO clients, aggregates with LLM trend interpretation
- `opportunity-scoring`: Prioritized content opportunities — runs opportunity_scorer + competitor_gap_analyzer, generates action plans
- `content-comparison`: SERP benchmarking — runs content_length_comparator against top 10 results
- `wordpress-publishing`: Publishing with Yoast metadata — runs wordpress_publisher with LLM-generated meta content
- `article-planning`: Structured planning — runs article_planner + section_writer for outline generation

### Modified Capabilities
- `content_scrubber.py`: Add 6 new Unicode characters (U+00A0, U+2003, U+2004, U+2005, U+2009, U+200A) and 2 dash variants (U+2E3A, U+2E3B)
- Existing marketing skills gain optional `scripts/` directories for deterministic scoring alongside qualitative analysis

## Impact

### New Files
- `10 x SKILL.md` files in `.claude/skills/[skill-name]/`
- `10 x scripts/` directories with symlinked Python modules
- `10 x references/` directories with scoring rubrics extracted from agent docs
- `10 x scripts/requirements.txt` for per-skill dependency documentation

### Modified Files
- `data_sources/modules/content_scrubber.py`: Expanded WATERMARK_CHARS list + new dash patterns
- `.claude/skills/seo-audit/SKILL.md`: Add scripts/ reference (Phase 4 enhancement)
- `.claude/skills/page-cro/SKILL.md`: Add scripts/ reference (Phase 4 enhancement)
- `.claude/skills/copywriting/SKILL.md`: Add scripts/ reference (Phase 4 enhancement)
- `.claude/skills/analytics-tracking/SKILL.md`: Add scripts/ reference (Phase 4 enhancement)
- `.claude/skills/form-cro/SKILL.md`: Add scripts/ reference (Phase 4 enhancement)

### Unchanged
- All 19 commands in `.claude/commands/` — backward compatible
- All 10 agents in `.claude/agents/` — remain as LLM personas
- All 24 Python modules in `data_sources/modules/` — source of truth stays put
- Root-level Python scripts (`research_*.py`, `seo_*.py`) — terminal-callable as before
