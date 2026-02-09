# PRD v2: SEO Machine Post-Implementation Roadmap

## Research-Backed Upgrade Plan Following Skills-as-Orchestration-Wrappers Completion

**Version:** 2.0
**Date:** 2026-02-08
**Based on:** `docs/skills-vs-modules-analysis.md` (validated claims), PRD v1.0 (completed implementation), Perplexity deep research (3 research sessions, 180+ citations)
**Status:** Draft
**Prerequisites:** PRD v1.0 fully implemented (55/55 tasks, 3 commits, 15 skills with scripts/, 24 CLI-upgraded modules)

---

## 1. Executive Summary

PRD v1.0 is complete. SEO Machine now has 15 Skills wrapping 24 Python modules via symlinks, with deterministic-first execution and progressive disclosure. This PRD v2.0 identifies the **next phase of improvements** based on:

1. **New Claude Code platform capabilities** (Agent Skills open standard, Skills API, subagent integration, agent teams, Opus 4.6 1M context)
2. **SEO industry shifts** (Generative Engine Optimization, query fan-out, dense retrieval, December 2025 core update, topical authority)
3. **Updated research** (Source Code Agent framework validating deterministic-first, Surfer's Content Score correlation study — 0.28 overall but varies by intent type and diminishes above score 95, CRO benchmark data from 41K landing pages)
4. **Gaps found during v1.0 review passes** (14 bugs fixed across 2 review commits)

The core architectural thesis from v1.0 remains validated and strengthened by 2025-2026 research. This PRD focuses on **exploiting the completed foundation** rather than re-architecting.

---

## 2. What Changed Since PRD v1.0

### 2.1 Platform Developments (Claude Code / Skills Ecosystem)

| Development | Date | Impact on SEO Machine |
|-------------|------|----------------------|
| **Agent Skills Open Standard** (agentskills.io) | Dec 2025 | Skills are now portable across Cursor, VS Code, GitHub Copilot, Claude Code. SEO Machine skills could be published to the ecosystem. |
| **Skills API** | Late 2025 | Programmatic skill creation, management, and invocation via `container.skills` parameter in Messages API. Enables CI/CD for skills. |
| **Organization-level skill management** | Dec 2025 | Team/Enterprise plans can deploy skills workspace-wide with auto-updates. SEO Machine could be distributed as an org skill package. |
| **Skill Directory** (79 connectors) | Dec 2025 | Partner-driven ecosystem (Notion, Figma, Atlassian, Vercel). SEO Machine could publish skills to the directory. |
| **Claude Code 2.1.0 hot-reload** | Jan 2026 | Skills auto-reload on file changes without session restart. Faster iteration for skill development. |
| **Claude Opus 4.6** (1M token context) | Feb 2026 | 2x context window, better long-running agentic tasks, adaptive thinking. Enables more sophisticated multi-skill workflows. |
| **Agent teams** (research preview) | Feb 2026 | Multiple agents working in parallel, each with specialized skills. Could parallelize content analysis across skills. |
| **Subagent skill preloading** | 2025 | Skills can be injected into subagent contexts via `skills` field. Enables delegated analysis workflows. |
| **`context: fork` frontmatter** | 2025 | Skills can run in isolated subagent contexts with independent context. Heavy skills don't pollute main context. |

**Sources:** [Anthropic Skills docs](https://code.claude.com/docs/en/skills), [Agent Skills spec](https://agentskills.io/specification), [Opus 4.6 announcement](https://www.anthropic.com/news/claude-opus-4-6), [Skills guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)

### 2.2 SEO Industry Shifts (2025-2026)

| Shift | Evidence | Impact |
|-------|----------|--------|
| **Generative Engine Optimization (GEO)** | Google AI Mode uses "query fan-out" expanding single queries into dozens of semantic variants for retrieval | Content must optimize for implicit semantic variants, not just explicit keywords |
| **Dense retrieval dominance** | Vector embeddings now primary retrieval mechanism for both traditional search and AI search | Passage-level semantic clarity matters as much as page-level optimization |
| **Content Score correlation** | Surfer's 1M SERP study: Content Score correlates at 0.28 with rankings (exceeds backlink metrics at 0.17), but varies by intent type (consequence: 0.2961, short-fact: 0.19) and diminishes above score 95 | Deterministic content scoring has measurable ranking impact; intent-aware thresholds needed |
| **December 2025 core update** | Broad re-evaluation of content relevance, not penalty-based. Middle-ranking content saw most movement | Quality gates and content refresh become more critical |
| **Topical authority over keyword targeting** | Organizations building comprehensive topic coverage outperform page-by-page optimization | Need topic cluster analysis and gap identification tools |
| **Schema markup for AI citation** | Schema markup improves AI citation likelihood by 11%+ vs unstructured text | Should integrate structured data recommendations |
| **E-E-A-T reinforcement** | Experience dimension increasingly important for content quality evaluation | Content scoring should factor author expertise signals |

**Sources:** [Surfer Content Score study](https://surferseo.com/blog/surfer-content-score-study/), [Surfer ranking factors](https://surferseo.com/blog/ranking-factors-study/), [iPullRank AI Mode analysis](https://ipullrank.com/how-ai-mode-works), [Google December 2025 update](https://thinklittlebig.com/blog/google-december-2025-core-update-key-takeaways-for-seo-in-2026/)

### 2.3 Research Validation Updates

All v1.0 claims remain validated. New supporting evidence strengthens key findings:

| Claim | New Evidence (2025-2026) |
|-------|--------------------------|
| **Deterministic-first, LLM-second** | **Source Code Agent framework** (arXiv 2508.02721, 2025): Codifying procedures as executable blueprints outperformed strongest baseline by 10.1pp on tau-bench, reduced tool calls by 81.8%. Validates our `scripts/` execution pattern. |
| **LLM syllable counting still broken** | No improvement in Claude Opus 4.5 or 4.6 for phonological tasks. Advances in reasoning don't fix architectural tokenization constraints. PhonologyBench findings (55% accuracy) remain current. |
| **LLM word counting still broken** | Fifth Dimension AI's "Precision Word Count" (best-in-class) achieves only 3-10% margin. Standard LLMs still deviate 50%+. |
| **Regex still 28,120x faster** | JAMIA Open 2025 study confirmed on 7,764-report dataset: 18,404x faster for regex on larger corpus. No accuracy difference (P=.56). |
| **Hybrid clustering validated** | EMNLP 2025: Co-evolving LLMs and embedding models for text clustering confirms LLMs provide semantic interpretation but traditional algorithms must handle computation. |
| **Quality gate architecture validated** | Industry CI/CD quality gate research confirms: automated checks preferred over manual approval, layered gates catch different issue types, false positive management critical. |

**Sources:** [Source Code Agent, arXiv 2508.02721](https://arxiv.org/html/2508.02721v1), [EMNLP 2025 text clustering](https://aclanthology.org/2025.emnlp-main.241.pdf), [JAMIA Open regex study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12612664/), [Quality gates in pipelines](https://www.infoq.com/articles/pipeline-quality-gates/)

---

## 3. Completed Foundation (v1.0 Recap)

### What Was Built

| Category | Count | Details |
|----------|-------|---------|
| New orchestration skills | 10 | content-quality-analysis, seo-analysis, content-scrubbing, landing-page-analysis, landing-performance, data-pipeline, opportunity-scoring, content-comparison, wordpress-publishing, article-planning |
| Enhanced marketing skills | 5 | seo-audit, page-cro, copywriting, analytics-tracking, form-cro (gained scripts/ directories) |
| CLI-upgraded Python modules | 24 | All accept `--json` flag, file/keyword args, stderr errors |
| Bugs found and fixed | 14 | 3 critical, 5 moderate, 2 minor, 2 doc issues, 2 additional in second review |
| Total symlinks | 32 | All resolving correctly across 15 skills |

### Architecture Achieved

```
.claude/skills/[name]/
  SKILL.md              # YAML frontmatter + deterministic-first instructions
  scripts/
    module.py           # Symlink -> ../../../../data_sources/modules/module.py
    requirements.txt    # Skill-specific dependencies
  references/
    rubric.md           # Domain context for LLM interpretation
```

### What's Working

- All 24 modules produce valid JSON via CLI
- All 32 symlinks resolve from skill directories
- All 15 skills discoverable via progressive disclosure
- Deterministic-first execution verified across all skills
- Backward compatibility maintained (all commands/agents unchanged)
- Documentation accurate (CLAUDE.md, skill-wrapper-guide.md)

---

## 4. Proposed v2.0 Improvements

### Phase A: Skill Architecture Hardening (Priority: Critical)

#### A.1 Add `allowed-tools` to SKILL.md Frontmatter

**Problem:** Currently, skills require manual permission approval for each Bash command execution when running Python scripts. This creates friction during skill invocation.

**Solution:** Add `allowed-tools` field to each orchestration skill's YAML frontmatter to pre-approve script execution:

```yaml
---
name: content-quality-analysis
version: 1.1.0
description: Run deterministic content quality scoring...
allowed-tools: "Bash(python3 {baseDir}/scripts/*:*)"
---
```

**Impact:** Zero-friction skill invocation. Users invoke the skill and scripts run automatically.

**Scope:** Update 15 SKILL.md files with appropriate `allowed-tools` declarations.

#### A.2 Add `context: fork` for Heavy Skills

**Problem:** Skills like `landing-page-analysis` (5 scripts) and `data-pipeline` (4 scripts) produce substantial output that can consume main conversation context.

**Solution:** Add `context: fork` frontmatter to heavy analysis skills so they run in isolated subagent contexts:

```yaml
---
name: landing-page-analysis
version: 1.1.0
context: fork
description: Run deterministic CRO analysis...
---
```

**Candidates for forked context:**
- `landing-page-analysis` (5 scripts, ~2000 tokens of JSON output)
- `data-pipeline` (4 scripts, variable output depending on API availability)
- `content-quality-analysis` (4 scripts, ~1500 tokens of JSON output)

**Impact:** Heavy analysis skills don't pollute the main conversation context, preserving tokens for interpretation and follow-up.

#### A.3 Co-locate Dependent Module Imports

**Problem:** `content_scorer.py` imports `readability_scorer.py`. When symlinked into a skill's `scripts/` directory, the import works only because both are symlinked into the same directory. But if a skill only symlinks `content_scorer.py` (like the `copywriting` skill), the import fails.

**Solution:** Audit all inter-module imports and ensure every skill's `scripts/` directory contains all required dependencies.

**Full inter-module import dependency map:**

| Module | Imports | Used By Skills |
|--------|---------|---------------|
| `content_scorer.py` | `readability_scorer.py`, `seo_quality_rater.py` | content-quality-analysis (has both), copywriting (was missing both — **fixed in this review**) |
| `data_aggregator.py` | `google_analytics.py`, `google_search_console.py`, `dataforseo.py` | data-pipeline (has all three) |

**Previously missing dependencies (now fixed):**

| Skill | Was Missing | Status |
|-------|------------|--------|
| `copywriting` | `readability_scorer.py`, `seo_quality_rater.py` | Fixed — symlinks added |

**Prevention:** Any future skill that symlinks `content_scorer.py` MUST also symlink `readability_scorer.py` and `seo_quality_rater.py`. Any skill that symlinks `data_aggregator.py` MUST also symlink all three API client modules.

**Scope:** Document the co-location requirement and dependency map in skill-wrapper-guide.md. Add import dependency checks to E.2 integration tests.

#### A.4 Standardize CLI Flag Conventions

**Problem:** Review passes revealed inconsistent CLI patterns across modules. Some use positional args, some use `--keyword` flags, wordpress_publisher uses argparse while others use manual sys.argv parsing.

**Solution:** Document and enforce a standard CLI convention:

```
# File-based analysis
python3 module.py <file_path> [--keyword <kw>] [--type <type>] [--goal <goal>] [--json]

# Topic/keyword-based analysis
python3 module.py <topic_or_keyword> [--keyword <kw>] [--json]

# API-based data retrieval
python3 module.py [--days <N>] [--limit <N>] [--json]

# All modules:
# - Errors on stderr
# - Data on stdout
# - Exit 1 on error (even with --json)
# - --json produces machine-readable JSON
```

**Scope:** No code changes needed (v1.0 already standardized most modules). Document the convention in skill-wrapper-guide.md for future modules.

---

### Phase B: Generative Engine Optimization (GEO) (Priority: High)

#### B.1 Create `semantic-coverage-analysis` Skill

**Problem:** Google AI Mode uses query fan-out, expanding queries into semantic variants. Current SEO analysis focuses on keyword density, not semantic coverage of related concepts.

**Proposal:** Create a new skill that analyzes content against semantic coverage requirements:

```
.claude/skills/semantic-coverage-analysis/
  SKILL.md
  scripts/
    keyword_analyzer.py     # Symlink - TF-IDF clustering provides deterministic semantic field baseline
  references/
    query-fanout-patterns.md    # Common expansion patterns by intent type
    entity-coverage-guide.md    # How to identify missing semantic entities
```

**SKILL.md behavior:**
1. Accept a file path and target keyword
2. Run `keyword_analyzer.py` with `--keyword <target>` to get TF-IDF clusters and LSI keywords as a deterministic semantic field baseline
3. Use LLM reasoning to expand the deterministic baseline — identify additional semantic entities, subtopics, and questions the TF-IDF model misses
4. Analyze content for coverage of each identified entity/subtopic (both deterministic and LLM-identified)
5. Score semantic coverage as percentage of identified entities present
6. Recommend specific entities/subtopics to add

**Note:** Hybrid skill following the deterministic-first pattern. `keyword_analyzer.py` provides a reproducible TF-IDF baseline of related terms, then LLM reasoning expands beyond what statistical clustering can identify (semantic relationships, entity associations, question variants). This aligns with the project's core architectural thesis rather than relying solely on LLM reasoning.

**Research basis:** iPullRank's analysis of Google AI Mode shows query fan-out generates 20-100 semantic variants per query. Content covering more variants gets cited more frequently in AI responses.

#### B.2 Create `topical-authority-mapper` Skill

**Problem:** December 2025 core update emphasized topical authority over individual page optimization. SEO Machine currently optimizes pages individually.

**Proposal:** Create a skill for analyzing and building topical authority:

```
.claude/skills/topical-authority-mapper/
  SKILL.md
  scripts/
    keyword_analyzer.py     # Symlink - reuse TF-IDF clustering
  references/
    topic-cluster-strategy.md
    internal-linking-patterns.md
```

**SKILL.md behavior:**
1. Accept a topic/keyword cluster
2. Run `keyword_analyzer.py` for TF-IDF clustering of related terms
3. Map existing content in `published/` and `drafts/` against the topic cluster
4. Identify gaps: subtopics with no content, orphan pages with no cluster links
5. Generate a content roadmap: what to write next, what to update, what to consolidate
6. Suggest internal linking structure to build cluster authority

**Research basis:** Surfer's ranking factors study shows topical coverage correlates with rankings. Dense retrieval systems favor comprehensive topic clusters over isolated optimized pages.

#### B.3 Create `schema-markup-generator` Skill

**Problem:** Schema markup improves AI citation likelihood by 11%+. Current skills don't generate structured data.

**Proposal:** Create a skill that generates appropriate schema markup for content:

```
.claude/skills/schema-markup-generator/
  SKILL.md
  references/
    schema-types-by-content.md    # Article, FAQ, HowTo, Product, etc.
    google-structured-data-guide.md
```

**SKILL.md behavior:**
1. Accept a file path and content type
2. Analyze content structure to identify applicable schema types (Article, FAQ, HowTo, etc.)
3. Generate JSON-LD schema markup
4. Validate against Google's structured data requirements
5. Output ready-to-embed schema block

**Note:** LLM-native skill. Schema generation is a semantic task where LLMs excel.

**Research basis:** Lily Ray's TechSEO Connect 2025 research shows schema markup improves AI system understanding of content by providing explicit entity relationships.

---

### Phase C: Quality Pipeline Enhancements (Priority: High)

#### C.1 Add Content Score Correlation Awareness

**Problem:** Surfer's study of 1M SERPs shows Content Score correlates at 0.28 with rankings, but the correlation varies by intent type (consequence queries: 0.2961, short-fact queries: 0.19). Current quality scoring doesn't account for intent-specific thresholds.

**Proposal:** Update `content-quality-analysis` SKILL.md to include intent-aware scoring interpretation:

```
After running content_scorer.py and search_intent_analyzer.py:
- If intent is "informational/consequence": optimal score range 80-95
- If intent is "navigational/short-fact": optimal score range 65-80
- If intent is "transactional": focus on CRO metrics over content score
- Warn if score exceeds 95 (over-optimization risk)
```

**Research basis:** Surfer's study shows chasing perfect scores (95+) produces diminishing returns and can harm quality by forcing unnatural keyword variations. The optimal range varies by intent.

**Scope:** Update 1 SKILL.md file + add reference doc with intent-specific benchmarks.

#### C.2 Add Content Freshness Monitoring

**Problem:** December 2025 core update penalizes stale content. No current skill monitors content age or recommends refresh.

**Proposal:** Create a lightweight skill for content freshness analysis:

```
.claude/skills/content-freshness-monitor/
  SKILL.md
  scripts/
    data_aggregator.py    # Symlink - reuse for performance data
  references/
    refresh-criteria.md
```

**SKILL.md behavior:**
1. Scan `published/` directory for articles with dates in filenames
2. Run `data_aggregator.py` to get performance trends (if APIs available)
3. Flag articles older than N months with declining traffic
4. Prioritize refresh candidates by (age x traffic decline x opportunity score)
5. Generate refresh brief: what to update, what data points are stale

#### C.3 Enhance CRO Benchmarks with Industry Data

**Problem:** Current CRO scoring uses internal benchmarks. Unbounce's study of 41K landing pages provides industry-specific conversion benchmarks.

**Proposal:** Update `landing-page-analysis` references with industry benchmark data:

| Industry | Median CR | Top 25% CR |
|----------|-----------|------------|
| SaaS | 3.8% | 11.6% |
| Financial Services | 4.9% | 15.2% |
| Insurance | 18.2% | 30.1% |
| E-commerce | 5.2% | 12.8% |

**Scope:** Update `references/cro-benchmarks.md` in the landing-page-analysis skill. No code changes.

**Source:** [Unbounce Conversion Benchmark Report](https://unbounce.com/landing-pages/whats-a-good-conversion-rate/)

---

### Phase D: Measurement & Analytics (Priority: Medium)

#### D.1 Create `performance-baseline` Skill

**Problem:** Modern SEO measurement requires connecting organic activity to business outcomes, not just tracking rankings and impressions.

**Proposal:** Create a skill for establishing and monitoring performance baselines:

```
.claude/skills/performance-baseline/
  SKILL.md
  scripts/
    google_analytics.py           # Symlink
    google_search_console.py      # Symlink
    data_aggregator.py            # Symlink
    opportunity_scorer.py         # Symlink
  references/
    kpi-framework.md
    metric-definitions.md
```

**SKILL.md behavior:**
1. Run all data scripts to collect current metrics
2. Establish baselines: organic traffic, conversion rate, visitor quality, content-to-revenue timeline
3. Identify ratio anomalies (organic/paid shift, organic/direct divergence)
4. Generate monthly comparison vs baseline
5. Flag metrics requiring attention

**Research basis:** Previsible's 2026 performance baseline framework emphasizes ratio analysis and business outcome metrics over vanity metrics.

#### D.2 Create `ai-visibility-tracker` Skill

**Problem:** Generative search engines (ChatGPT, Perplexity, Google AI Overviews) now drive traffic. No current skill tracks visibility in AI responses.

**Proposal:** Create a skill for tracking AI search visibility:

```
.claude/skills/ai-visibility-tracker/
  SKILL.md
  references/
    ai-platform-citation-patterns.md
    geo-optimization-guide.md
```

**SKILL.md behavior:**
1. Accept a list of target keywords
2. Research which content appears in AI responses for those keywords (via web search)
3. Compare AI visibility to traditional SERP rankings
4. Identify gaps: content ranking well traditionally but absent from AI responses
5. Recommend GEO-specific optimizations (semantic clarity, entity coverage, schema markup)

**Note:** LLM-native skill. AI visibility research requires web search and semantic analysis.

**Research basis:** Multiple studies show AI citation patterns differ from traditional rankings. Content optimized for traditional SEO may not appear in AI-generated responses without additional optimization.

---

### Phase E: Developer Experience (Priority: Medium)

#### E.1 Create Skill Scaffolding Script

**Problem:** Creating new skills requires manually creating directories, symlinks, SKILL.md boilerplate, and requirements.txt. The skill-wrapper-guide.md documents the process but doesn't automate it.

**Proposal:** Create a `scripts/create-skill.sh` utility:

```bash
./scripts/create-skill.sh content-freshness-monitor \
  --modules data_aggregator.py \
  --description "Monitor content freshness and recommend updates"
```

This would:
1. Create `.claude/skills/content-freshness-monitor/{scripts/,references/}`
2. Create symlinks for specified modules
3. Generate SKILL.md boilerplate with YAML frontmatter
4. Generate empty `requirements.txt` and `references/` placeholder
5. Verify symlinks resolve

#### E.2 Add Skill Integration Tests

**Problem:** v1.0 review passes found 14 bugs. Two full review cycles were needed. Automated tests would catch regressions.

**Proposal:** Create `tests/test_skill_integration.py`:

```python
# For each skill with scripts/:
# 1. Verify all symlinks resolve
# 2. Run each script with --json and validate JSON output
# 3. Verify SKILL.md has valid YAML frontmatter
# 4. Verify referenced scripts exist in scripts/ directory
# 5. Verify requirements.txt is present
```

**Scope:** ~100 lines of Python using stdlib only. Run with `python3 tests/test_skill_integration.py`.

#### E.3 Skills API Distribution Package

**Problem:** SEO Machine skills could benefit other teams but have no distribution mechanism.

**Proposal:** Create a manifest for the Skills API that packages skills for organization-level deployment:

```json
{
  "name": "seo-machine-skills",
  "version": "1.0.0",
  "skills": [
    "content-quality-analysis",
    "seo-analysis",
    "content-scrubbing",
    ...
  ]
}
```

**Research basis:** Anthropic's Skills API (container.skills parameter) enables programmatic skill deployment. Organization-level skill management allows workspace-wide deployment with auto-updates.

---

## 5. Prioritization Matrix

| Phase | Effort | Impact | Dependencies | Priority |
|-------|--------|--------|--------------|----------|
| A.1 allowed-tools | Low (15 file edits) | High (zero-friction invocation) | None | P0 |
| A.2 context: fork | Low (3 file edits) | Medium (context savings) | None | P0 |
| A.3 co-locate imports | Low (audit + symlinks) | High (prevents runtime errors) | None | P0 |
| A.4 CLI conventions doc | Low (doc update) | Low (developer guide) | None | P1 |
| B.1 semantic-coverage | Medium (new skill) | High (GEO readiness) | keyword_analyzer | P1 |
| B.2 topical-authority | Medium (new skill) | High (cluster strategy) | keyword_analyzer | P1 |
| B.3 schema-markup | Low (new skill, LLM-native) | Medium (AI citation) | None | P2 |
| C.1 intent-aware scoring | Low (SKILL.md update) | Medium (scoring accuracy) | None | P1 |
| C.2 content freshness | Medium (new skill) | High (core update response) | data_aggregator | P1 |
| C.3 CRO benchmarks | Low (reference doc update) | Low (better context) | None | P2 |
| D.1 performance baseline | Medium (new skill) | High (business metrics) | GA4/GSC APIs | P2 |
| D.2 AI visibility | Medium (new skill) | High (GEO tracking) | Web search (graceful degradation) | P2 |
| E.1 scaffolding script | Low (shell script) | Medium (DX improvement) | None | P2 |
| E.2 integration tests | Medium (test suite) | High (regression prevention) | **A.3 must complete first** (tests would fail on unfixed import deps) | P1 |
| E.3 distribution package | Low (manifest) | Medium (portability) | Skills API | P3 |

---

## 6. Non-Goals (Explicitly Out of Scope)

| Non-Goal | Rationale |
|----------|-----------|
| Replace any Python module with LLM reasoning | All research reconfirms deterministic modules outperform LLMs for computation tasks. PhonologyBench (55% syllable accuracy), CWUM (66% word counting), regex 28,120x speed advantage. |
| Migrate to CrewAI/AutoGen/LangGraph | Claude Code's native Skills + agent teams is purpose-built for this pattern. External frameworks add complexity without benefit. |
| Real-time streaming analysis | All analysis remains batch/on-demand. Real-time adds infrastructure complexity without SEO value. |
| Fine-tune LLMs for SEO tasks | Generic Claude models with deterministic Python scripts outperform fine-tuned models for hybrid content analysis. |
| Build MCP servers for analysis modules | Skills with `scripts/` is the correct pattern. MCP is for external service connectivity (databases, APIs), not local computation. Skills provide knowledge, MCP provides connectivity. |
| Remove the command/agent layers | Commands and agents remain functional. Skills are complementary, not replacements. |

---

## 7. Risks & Limitations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **`context: fork` breaks conversational workflows** | Skills running in forked contexts cannot reference earlier conversation (e.g., user discusses a draft, then invokes `landing-page-analysis` — the skill can't see the discussion). | Only apply `context: fork` to skills that are invoked as standalone analysis (A.2 candidates are all analysis-first skills). Document in each SKILL.md that forked skills require explicit file paths, not conversational references. |
| **`allowed-tools` and symlink trust** | Pre-approving `Bash(python3 {baseDir}/scripts/*:*)` trusts that symlinked scripts won't be modified to do something harmful. If a symlink target changes (e.g., via malicious commit or accidental overwrite), the pre-approved tool runs the modified code without user confirmation. | Symlinks point to `data_sources/modules/` which is version-controlled. Code review on PRs to `data_sources/modules/` is the appropriate mitigation. Integration tests (E.2) verify symlink targets resolve to expected files. |
| **Web search dependency for Phase B/D skills** | `ai-visibility-tracker` (D.2) and parts of `semantic-coverage-analysis` (B.1) depend on web search availability. If search is unavailable (rate limits, network issues), these skills produce no output. | Design these skills with graceful degradation: if web search fails, fall back to deterministic-only analysis (TF-IDF baseline for B.1, cached data for D.2). Document the degradation behavior in each SKILL.md. |
| **Content Score over-optimization** | Surfer's study shows diminishing returns above score 95 and potential quality harm from forcing unnatural keyword variations. Users may chase perfect scores. | Intent-aware thresholds (C.1) explicitly warn when scores exceed 95. SKILL.md instructions should frame scores as diagnostic tools, not optimization targets. |
| **Inter-module import fragility** | Adding new imports to existing modules (e.g., `content_scorer.py` adding a third import) silently breaks skills that don't have the new dependency symlinked. | Integration tests (E.2) must verify all imports resolve from each skill's `scripts/` directory. The dependency map in A.3 must be updated whenever module imports change. |

---

## 8. Success Metrics (updated post-review)

| Metric | Current (v1.0) | Target (v2.0) |
|--------|----------------|---------------|
| Skills with `allowed-tools` | 0/15 | 15/15 |
| Skills with `context: fork` | 0/15 | 3/15 (heavy skills) |
| GEO-ready analysis skills | 0 | 3 (semantic coverage, topical authority, schema markup) |
| Content freshness monitoring | Manual | Automated via skill |
| Integration test coverage | Manual review passes | Automated test suite |
| Skill creation time | 30-60 min manual | 5 min via scaffolding script |
| AI visibility tracking | None | Skill-based tracking |
| Quality gate false positive rate | Unknown | Tracked via intent-aware thresholds |

---

## 9. Research Citations

### Academic Papers (2024-2026)
1. PhonologyBench: Evaluating Phonological Skills of LLMs. Suvarna et al. ACL KnowLLM 2024. [arXiv:2404.02456](https://arxiv.org/abs/2404.02456)
2. CWUM: Word Counting in LLMs. EMNLP Findings 2024. [ACL Anthology](https://aclanthology.org/2024.findings-emnlp.691.pdf)
3. Source Code Agent: Enhancing LLM Agents with Executable Code-Based Knowledge. 2025. [arXiv:2508.02721](https://arxiv.org/html/2508.02721v1)
4. k-LLMmeans: Scalable Text Clustering. Diaz-Rodriguez. 2025. [arXiv:2502.09667](https://arxiv.org/pdf/2502.09667v2.pdf)
5. Regex vs LLM for Structured Data Extraction. JAMIA Open 2025. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12612664/)
6. RegexPSPACE: LLM Regex Evaluation. 2025. [arXiv:2510.09227](https://arxiv.org/html/2510.09227v1)
7. Co-evolving LLMs and Embedding Models for Text Clustering. EMNLP 2025. [ACL Anthology](https://aclanthology.org/2025.emnlp-main.241.pdf)
8. LLM Readability Assessment of Orthopedic Content. 2025. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12117680/)
9. Blueprint First, Model Second: Deterministic Automation. Itential. 2025. [Blog](https://www.itential.com/blog/beyond-deterministic-automation-why-ai-reasoning-is-the-future-of-infrastructure-orchestration/)

### Industry Research & Benchmarks
10. Surfer Content Score Correlation Study (1M SERPs). [Surfer](https://surferseo.com/blog/surfer-content-score-study/)
11. Surfer Ranking Factors Study. [Surfer](https://surferseo.com/blog/ranking-factors-study/)
12. Unbounce Conversion Benchmark Report (41K landing pages). [Unbounce](https://unbounce.com/landing-pages/whats-a-good-conversion-rate/)
13. How AI Mode Works (query fan-out). iPullRank. [iPullRank](https://ipullrank.com/how-ai-mode-works)
14. Google December 2025 Core Update Analysis. [ThinkLittleBig](https://thinklittlebig.com/blog/google-december-2025-core-update-key-takeaways-for-seo-in-2026/)
15. Frase Content Intelligence Platform Rebuild. [Frase](https://frase.io/blog/introducing-the-new-frase-content-intelligence-platform)
16. Quality Gates in CI/CD Pipelines. InfoQ. [InfoQ](https://www.infoq.com/articles/pipeline-quality-gates/)
17. 2026 SEO Performance Baseline Framework. Previsible. [Previsible](https://previsible.io/seo-strategy/2026-performance-baseline/)

### Claude Code / Skills Platform
18. Claude Code Skills Documentation. [Anthropic](https://code.claude.com/docs/en/skills)
19. Agent Skills Open Standard Specification. [agentskills.io](https://agentskills.io/specification)
20. Claude Opus 4.6 Release. [Anthropic](https://www.anthropic.com/news/claude-opus-4-6)
21. Complete Guide to Building Skills for Claude. [Anthropic](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
22. MCP vs Skills Comparison. [CosmicJS](https://www.cosmicjs.com/blog/mcp-vs-skills-ai-coding-assistant-integrations-guide)
23. Skills API Documentation. [Anthropic](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
24. Claude Code Subagents. [Anthropic](https://code.claude.com/docs/en/sub-agents)
25. Skills Deep Dive. Lee Han Chung. [Blog](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
