# Tasks: Skills-as-Orchestration-Wrappers

## Phase 0: Foundation (Prerequisites)

- [x] 0.1 Audit all 24 Python modules for `if __name__ == "__main__"` entry points — all 24 have them, but only content_scorer.py accepts file args. Rest use hardcoded samples and need CLI upgrades.
- [x] 0.2 Add `__main__` CLI entry point to `content_scorer.py` — accept file path arg, output JSON to stdout
- [x] 0.3 Add `__main__` CLI entry point to `readability_scorer.py` — accept file path arg, output JSON to stdout
- [x] 0.4 Add `__main__` CLI entry point to `engagement_analyzer.py` — accept file path arg, output JSON to stdout
- [x] 0.5 Add `__main__` CLI entry point to `content_scrubber.py` — accept file path arg, scrub in-place, output stats JSON to stdout
- [x] 0.6 Add `__main__` CLI entry point to `keyword_analyzer.py` — accept file path + keyword args, output JSON to stdout
- [x] 0.7 Add `__main__` CLI entry point to `seo_quality_rater.py` — accept file path + keyword arg, output JSON to stdout
- [x] 0.8 Add `__main__` CLI entry point to `search_intent_analyzer.py` — accept keyword arg, output JSON to stdout
- [x] 0.9 Verify `content_scorer.py` import fallback works from a different directory (test the `from readability_scorer import` path)
- [x] 0.10 Enhance `content_scrubber.py` — add 6 new Unicode characters (U+00A0, U+2003, U+2004, U+2005, U+2009, U+200A) and 2 dash variants (U+2E3A, U+2E3B) to WATERMARK_CHARS

## Phase 1: Core Analysis Skills

### 1.1 content-quality-analysis skill

- [x] 1.1.1 Create directory structure: `.claude/skills/content-quality-analysis/{SKILL.md,scripts/,references/}`
- [x] 1.1.2 Create symlinks in `scripts/`: content_scorer.py, readability_scorer.py, seo_quality_rater.py, engagement_analyzer.py (all → `../../../../data_sources/modules/[name].py`)
- [x] 1.1.3 Write `SKILL.md` with YAML frontmatter + deterministic-first execution instructions (run 3 scripts → synthesize)
- [x] 1.1.4 Write `references/scoring-rubric.md` — extract scoring criteria from content-analyzer agent docs + content_scorer.py docstrings
- [x] 1.1.5 Write `scripts/requirements.txt` — list textstat dependency
- [x] 1.1.6 Test: verify symlinks resolve, scripts run from scripts/ dir, SKILL.md is well-formed — all 4 scripts (content_scorer, readability_scorer, engagement_analyzer, seo_quality_rater) produce valid JSON from symlinked directory

### 1.2 seo-analysis skill

- [x] 1.2.1 Create directory structure: `.claude/skills/seo-analysis/{SKILL.md,scripts/,references/}`
- [x] 1.2.2 Create symlinks in `scripts/`: keyword_analyzer.py, seo_quality_rater.py, search_intent_analyzer.py
- [x] 1.2.3 Write `SKILL.md` with YAML frontmatter + deterministic-first execution instructions
- [x] 1.2.4 Write `references/seo-scoring-criteria.md` — extract from seo-optimizer agent docs + module docstrings
- [x] 1.2.5 Write `scripts/requirements.txt` — list scikit-learn, numpy dependencies
- [x] 1.2.6 Test: verify symlinks resolve, scripts run, SKILL.md is well-formed — all 3 scripts (keyword_analyzer, seo_quality_rater, search_intent_analyzer) produce valid JSON from symlinked directory

### 1.3 content-scrubbing skill

- [x] 1.3.1 Create directory structure: `.claude/skills/content-scrubbing/{SKILL.md,scripts/,references/}`
- [x] 1.3.2 Create symlink in `scripts/`: content_scrubber.py
- [x] 1.3.3 Write `SKILL.md` with YAML frontmatter + execution instructions (run scrubber → report changes)
- [x] 1.3.4 Write `references/unicode-watermark-catalog.md` — document all 12+ watermark characters with sources and descriptions
- [x] 1.3.5 Write `scripts/requirements.txt` — (no external deps, just stdlib)
- [x] 1.3.6 Test: verify symlink resolves, scrubber runs from scripts/ dir, SKILL.md is well-formed — dry-run + in-place + idempotency all verified from symlinked directory

### 1.4 Phase 1 Integration Test

- [x] 1.4.1 Test all 3 Phase 1 skills end-to-end: tested with sample podcast hosting draft — content-quality (score 81.4), seo-analysis (score 72.5, keyword density 1.48%), content-scrubbing (6 emdashes replaced, idempotent on 2nd run)
- [x] 1.4.2 Regression: `/write` command unchanged — still references `data_sources/modules/` directly, skills are additive (no command modifications)
- [x] 1.4.3 Regression: `/scrub` command unchanged — still calls `content_scrubber.py` directly, skill is additive

## Phase 2: CRO & Landing Page Skills

- [x] 2.1 Add `__main__` CLI entry points to: above_fold_analyzer.py, cta_analyzer.py, trust_signal_analyzer.py, cro_checker.py, landing_page_scorer.py, landing_performance.py — also fixed pre-existing bug in cta_analyzer.py (missing cta_count in empty CTA distribution dict)
- [x] 2.2 Create `landing-page-analysis` skill: SKILL.md + scripts/ (5 symlinks) + references/cro-benchmarks.md + requirements.txt
- [x] 2.3 Create `landing-performance` skill: SKILL.md + scripts/ (1 symlink) + references/benchmark-grades.md + requirements.txt
- [x] 2.4 Test Phase 2 skills end-to-end — all 6 scripts produce valid JSON from symlinked directories, landing_performance gracefully degrades without credentials
- [x] 2.5 Regression: `/landing-audit` and `/landing-write` commands unchanged — skills are additive (no command modifications)

## Phase 3: Data Integration Skills

- [x] 3.1 Add `__main__` CLI entry points to: google_analytics.py, google_search_console.py, dataforseo.py, data_aggregator.py, opportunity_scorer.py, competitor_gap_analyzer.py — all with --json flag and graceful error handling
- [x] 3.2 Create `data-pipeline` skill: SKILL.md + scripts/ (4 symlinks) + references/api-setup-guide.md + requirements.txt
- [x] 3.3 Create `opportunity-scoring` skill: SKILL.md + scripts/ (2 symlinks) + references/scoring-methodology.md + requirements.txt
- [x] 3.4 Test Phase 3 skills — opportunity_scorer and competitor_gap_analyzer produce valid JSON, data_aggregator gracefully reports missing credentials
- [x] 3.5 Regression: `/performance-review` and `/priorities` commands unchanged — skills are additive

## Phase 4: Content Pipeline Skills + Marketing Skill Enhancements

- [x] 4.1 Add `__main__` CLI entry points to: content_length_comparator.py (file+keyword args), wordpress_publisher.py (added --json flag), article_planner.py (topic+keyword args), section_writer.py (--json output)
- [x] 4.2 Create `content-comparison` skill: SKILL.md + scripts/ (1 symlink) + references/serp-benchmarks.md + requirements.txt
- [x] 4.3 Create `wordpress-publishing` skill: SKILL.md + scripts/ (1 symlink) + references/yoast-fields-reference.md + requirements.txt
- [x] 4.4 Create `article-planning` skill: SKILL.md + scripts/ (2 symlinks) + references/writing-guidelines.md + requirements.txt
- [x] 4.5 Enhance `seo-audit` skill: added scripts/seo_quality_rater.py symlink
- [x] 4.6 Enhance `page-cro` skill: added scripts/ with cro_checker.py + landing_page_scorer.py symlinks
- [x] 4.7 Enhance `copywriting` skill: added scripts/content_scorer.py symlink
- [x] 4.8 Enhance `analytics-tracking` skill: added scripts/data_aggregator.py symlink
- [x] 4.9 Enhance `form-cro` skill: added scripts/cta_analyzer.py symlink
- [x] 4.10 Test: all new skills appear in Claude skill listing, symlinks resolve, scripts produce valid JSON
- [x] 4.11 Regression: all existing commands unchanged — skills are additive, no command files modified

## Phase 5: Documentation

- [x] 5.1 Update CLAUDE.md — added Orchestration Skills table (10 skills with scripts and purpose) and Skill Architecture section
- [x] 5.2 Update CLAUDE.md — documented symlink pattern, progressive disclosure, and deterministic-first execution
- [x] 5.3 Create `docs/skill-wrapper-guide.md` — developer guide covering template, principles, CLI pattern, testing, and reference table
