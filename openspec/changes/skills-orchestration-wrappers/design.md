# Design: Skills-as-Orchestration-Wrappers

## Context

SEO Machine has 24 Python analysis modules in `data_sources/modules/` and 26 Skills in `.claude/skills/` that have zero integration. Commands are the only bridge. The Skills platform supports `scripts/` directories with executable code, but the project doesn't use this. The PRD proposes creating 10 new orchestration Skills that bundle Python modules via symlinks.

## Goals / Non-Goals

**Goals:**
- Bundle Python modules into Skills using `scripts/` directories with symlinks
- Each skill runs deterministic scripts first, then interprets with LLM reasoning
- Preserve all backward compatibility (commands, agents, direct module invocation)
- Expand content scrubber Unicode coverage based on research findings
- Minimize startup token overhead via progressive disclosure

**Non-Goals:**
- Replacing any Python module with LLM reasoning
- Modifying the command layer or agent layer
- Migrating to external agent frameworks (CrewAI, AutoGen, LangGraph)
- Changing API credential management
- Removing or deprecating `data_sources/modules/`

## Decisions

### Decision 1: Symlinks over copies for scripts/ directories

**Approach:** Use relative symlinks from `.claude/skills/[name]/scripts/[module].py` → `data_sources/modules/[module].py`

**Rationale:**
- Single source of truth: edits to modules automatically reflected in skills
- No file duplication or sync drift
- Git tracks symlinks natively on Linux/macOS
- The `{baseDir}` variable in SKILL.md makes paths portable

**Tradeoff:** Symlinks may break on Windows. Mitigation: document Linux/macOS requirement, or provide a `setup.sh` that creates copies on Windows.

**Symlink depth calculation:**
```
.claude/skills/content-quality-analysis/scripts/content_scorer.py
→ ../../../../data_sources/modules/content_scorer.py

Path segments from scripts/ to repo root: 4 levels up
  .claude (1) / skills (2) / [name] (3) / scripts (4)
```

### Decision 2: Co-locate dependent modules in the same scripts/ directory

**Problem:** `content_scorer.py` imports `readability_scorer.py` and `seo_quality_rater.py` via:
```python
try:
    from .readability_scorer import ReadabilityScorer
    from .seo_quality_rater import SEOQualityRater
except ImportError:
    from readability_scorer import ReadabilityScorer
    from seo_quality_rater import SEOQualityRater
```

**Approach:** Symlink ALL required modules into the same `scripts/` directory. The fallback `from readability_scorer import ReadabilityScorer` (without dot) will resolve because Python adds the script's directory to `sys.path` when running a script directly.

**For `content-quality-analysis/scripts/`:**
```
content_scorer.py      → ../../../../data_sources/modules/content_scorer.py
readability_scorer.py  → ../../../../data_sources/modules/readability_scorer.py
seo_quality_rater.py   → ../../../../data_sources/modules/seo_quality_rater.py
engagement_analyzer.py → ../../../../data_sources/modules/engagement_analyzer.py
```

This means `content_scorer.py` can import its dependencies whether run from `data_sources/modules/` or from the skill's `scripts/` directory.

### Decision 3: SKILL.md execution pattern — sequential script runs with error handling

**Approach:** Each SKILL.md follows this template:

```markdown
## Execution

1. Run: `python3 {baseDir}/scripts/[script1].py --file "$FILE_PATH"`
   - Capture output as [METRIC_1]

2. Run: `python3 {baseDir}/scripts/[script2].py --file "$FILE_PATH"`
   - Capture output as [METRIC_2]

3. If any script fails, report the error and continue with available data.

4. Synthesize findings:
   - Present all numeric scores with labels
   - Identify top 3 issues by severity
   - Provide specific, actionable recommendations
   - Reference the scoring rubric in references/ for context
```

**Rationale:** Sequential execution gives Claude time to process each output. Parallel execution could overload context. Error handling prevents one script failure from blocking the entire skill.

### Decision 4: CLI interface for Python modules

**Problem:** Most modules are class-based (`ContentScorer`, `ReadabilityScorer`) with no `__main__` entry point. They can't be called via `python script.py --file path`.

**Approach:** Add a minimal `if __name__ == "__main__"` block to each module that needs to be invoked from a Skill. This is a non-breaking addition — existing import-based usage continues to work.

**Pattern:**
```python
if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python [module].py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'r') as f:
        content = f.read()

    # Instantiate class and run
    scorer = ContentScorer()
    result = scorer.score(content)

    # Output as JSON for Claude to parse
    print(json.dumps(result, indent=2))
```

**Modules requiring CLI entry points:**
- `content_scorer.py` — already has import fallback, needs `__main__`
- `readability_scorer.py` — needs `__main__`
- `engagement_analyzer.py` — needs `__main__`
- `keyword_analyzer.py` — needs `__main__`
- `seo_quality_rater.py` — needs `__main__`
- `search_intent_analyzer.py` — needs `__main__`
- `content_scrubber.py` — needs `__main__` (read file, scrub, write back, print stats)
- `above_fold_analyzer.py` — needs `__main__`
- `cta_analyzer.py` — needs `__main__`
- `trust_signal_analyzer.py` — needs `__main__`
- `cro_checker.py` — needs `__main__`
- `landing_page_scorer.py` — needs `__main__`
- `opportunity_scorer.py` — needs `__main__`
- `competitor_gap_analyzer.py` — needs `__main__`
- `content_length_comparator.py` — needs `__main__` (this one makes HTTP requests)
- `landing_performance.py` — needs `__main__` (this one calls APIs)

**Output format:** JSON to stdout. Claude parses JSON naturally. Errors go to stderr.

### Decision 5: YAML frontmatter token budget

**Constraint:** Each skill's YAML frontmatter must be <= 50 tokens to keep startup overhead minimal across all skills.

**Pattern:**
```yaml
---
name: content-quality-analysis
version: 1.0.0
description: Run deterministic content quality scoring (composite score, readability, engagement) and interpret results with strategic recommendations.
---
```

The description must be a single sentence that tells Claude WHEN to trigger the skill and WHAT it does.

### Decision 6: Phase execution order

| Phase | Skills | Blocking Dependencies |
|-------|--------|----------------------|
| Phase 1 | content-quality-analysis, seo-analysis, content-scrubbing | None. These modules have no API dependencies (except textstat/sklearn). Establish the pattern. |
| Phase 2 | landing-page-analysis, landing-performance | Phase 1 patterns validated. landing-performance requires API credentials (graceful degradation). |
| Phase 3 | data-pipeline, opportunity-scoring | Phase 1-2 patterns stable. Requires GA4/GSC/DataForSEO credentials. |
| Phase 4 | content-comparison, wordpress-publishing, article-planning + marketing skill enhancements | Full pipeline validated. content-comparison makes HTTP requests. wordpress-publishing requires WordPress credentials. |

### Decision 7: References/ directory content

Each skill's `references/` directory contains ONE markdown file extracted from:
1. The corresponding agent's documentation (e.g., `content-analyzer.md` → `scoring-rubric.md`)
2. The module's docstring and class documentation
3. The PRD's research validation for that module category

These are Claude's "interpretation guides" — they tell Claude what scores mean and how to prioritize recommendations.

## Architecture Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                    SKILL (new layer)                          │
│  .claude/skills/content-quality-analysis/                     │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ SKILL.md                                                │  │
│  │  1. Run python {baseDir}/scripts/content_scorer.py      │  │
│  │  2. Run python {baseDir}/scripts/readability_scorer.py  │  │
│  │  3. Run python {baseDir}/scripts/engagement_analyzer.py │  │
│  │  4. Synthesize recommendations (LLM reasoning)          │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────┐  ┌──────────────────────────────────┐   │
│  │ scripts/         │  │ references/                      │   │
│  │  content_scorer  │──│  scoring-rubric.md               │   │
│  │  readability_*   │  │  (interpretation guide)          │   │
│  │  engagement_*    │  └──────────────────────────────────┘   │
│  │  seo_quality_*   │                                         │
│  │  (all symlinks)  │                                         │
│  └────────┬─────────┘                                         │
└───────────┼───────────────────────────────────────────────────┘
            │ symlinks
            ▼
┌───────────────────────────────────────────────────────────────┐
│  MODULES (unchanged, canonical source)                        │
│  data_sources/modules/                                        │
│    content_scorer.py ← single source of truth                 │
│    readability_scorer.py                                      │
│    seo_quality_rater.py                                       │
│    engagement_analyzer.py                                     │
│    ... (24 total)                                             │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│  COMMANDS (unchanged, backward compatible)                    │
│  .claude/commands/write.md, scrub.md, optimize.md, etc.       │
│    Still invoke Python directly and chain agents.             │
│    Users who know the commands keep using them.               │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│  AGENTS (unchanged, backward compatible)                      │
│  .claude/agents/content-analyzer.md, seo-optimizer.md, etc.   │
│    Still available as LLM personas for qualitative guidance.  │
└───────────────────────────────────────────────────────────────┘
```

## Testing Approach

For each skill:
1. **Symlink resolution**: Verify `ls -la` shows symlinks resolving to correct modules
2. **Standalone execution**: Run each symlinked script directly and verify JSON output
3. **Import chain**: For scripts with dependencies (content_scorer), verify imports resolve from scripts/ directory
4. **SKILL.md trigger**: Invoke skill and verify it runs scripts in order, handles errors, synthesizes output
5. **Regression**: Run existing `/write` and `/optimize` commands and verify identical behavior
