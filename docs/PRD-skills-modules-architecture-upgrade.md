# PRD: SEO Machine Architecture Upgrade
## Skills-as-Orchestration-Wrappers for Python Modules

**Version:** 1.0
**Date:** 2026-02-08
**Based on:** `docs/skills-vs-modules-analysis.md` (validated claims + additional research)
**Status:** Draft

---

## 1. Executive Summary

This PRD proposes upgrading SEO Machine from its current command+agent+module architecture to a **Skills-as-orchestration-wrappers** architecture, where Claude Code Skills bundle Python modules in `scripts/` directories and use LLM reasoning to interpret deterministic output. This "wrap, don't replace" approach is validated by both Anthropic's official Skills documentation and academic research confirming that hybrid deterministic+LLM pipelines outperform either approach alone.

The upgrade preserves all 24 Python modules while making them **self-contained, portable, and automatically discoverable** through the Skills progressive disclosure system.

---

## 2. Research Validation Summary

Every major claim from the original analysis has been independently validated through academic papers, industry benchmarks, and official documentation.

### 2.1 Skills Architecture (CONFIRMED)

**Claim:** Skills support `scripts/` directories with executable Python/shell/Node.js code.

**Evidence:**
- Anthropic official docs at `code.claude.com/docs/en/skills` confirm Skills are filesystem-based packages supporting `SKILL.md`, `scripts/`, `references/`, and `assets/` directories
- The `{baseDir}` variable auto-resolves to the skill's directory path, enabling portable script references like `python {baseDir}/scripts/analyzer.py`
- Progressive disclosure loads only YAML frontmatter at startup (~30-50 tokens), full SKILL.md on trigger, and scripts/references on demand
- Third-party deep dives (Lee Han Chung, 2025) confirm the architecture and best practices
- The official Anthropic guide ("The Complete Guide to Building Skills for Claude") documents `scripts/` as a first-class pattern

**Sources:**
- [Anthropic Skills docs](https://code.claude.com/docs/en/skills)
- [Anthropic best practices guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- [Skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)

### 2.2 LLM Syllable Counting Limitations (CONFIRMED)

**Claim:** Claude-3-Sonnet achieves 55% accuracy on syllable counting, GPT-4 ~33%, human baseline 90%.

**Evidence:**
- PhonologyBench (4,000 datapoints, published ACL 2024) confirms exact figures: Claude-3-Sonnet = **55.3%**, human baseline = **90.0%**
- GPT-4 falls behind Claude-3-Sonnet by ~22% on syllable counting while being at-par on G2P tasks
- The gap is attributed to **subword tokenization** (architectural limitation, not training gap): "subword tokenization may lead to loss of phonological information that eventually affects the phonological skills of LLMs"
- Performance degrades further with sentence complexity and length

**Sources:**
- [PhonologyBench, arXiv 2404.02456](https://arxiv.org/html/2404.02456v2) (Suvarna, Khandelwal, Peng)
- [ACL KnowLLM 2024 proceedings](https://aclanthology.org/2024.knowllm-1.1.pdf)

**Implication:** `readability_scorer.py` (which uses `textstat` for Flesch formulas requiring syllable counts) CANNOT be replaced by LLM reasoning. The Python module is architecturally irreplaceable.

### 2.3 LLM Word Counting Failures (CONFIRMED)

**Claim:** LLMs deviate 50%+ from requested word counts and cannot reliably calculate keyword density.

**Evidence:**
- **CWUM benchmark** (EMNLP Findings 2024): GPT-4 achieves only **66.64%** accuracy on English word-counting tasks; open-source models like Qwen-72B underpredict word counts in **over 75%** of cases
- Standard LLMs deviate **up to 50% or more** from requested word counts (Fifth Dimension AI, 2024)
- Stanford research (Katherine Li, CS224N) demonstrates the root cause: autoregressive generation + subword tokenization prevents LLMs from planning word count in advance
- Instruction-tuning yields minimal gains: only +1.44% for LLaMA-3-70B-Instruct vs base model
- A separate 2024 study on letter counting found "most models fail in more than half of the words" with "even the best model fails to correctly count the letters in 17% of the words"
- **Cascading impact on keyword density**: since keyword density = (keyword count / total word count) * 100, inaccurate word counting makes LLM-based keyword density calculation unreliable

**Sources:**
- [CWUM benchmark, EMNLP Findings 2024](https://aclanthology.org/2024.findings-emnlp.691.pdf)
- [Fifth Dimension AI precision word count](https://www.fifthdimensionai.com/en-us/blogs-news/precision-word-count-revolutionising-ai-writing-accuracy)
- [Stanford WCC research](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1244/final-projects/KatherineLi.pdf)
- [LLM letter counting failures, arXiv 2412.18626](https://arxiv.org/html/2412.18626v1)
- [NAACL 2025 Long Paper](https://aclanthology.org/2025.naacl-long.172.pdf)

**Implication:** `keyword_analyzer.py` (TF-IDF, density calculation, K-means clustering) is irreplaceable. The hybrid approach validated by k-LLMmeans research (see 2.4) is correct.

### 2.4 Hybrid LLM+Clustering (CONFIRMED)

**Claim:** LLMs cannot perform reliable TF-IDF and K-means clustering alone; the hybrid approach (deterministic computation + LLM interpretation) is the research consensus.

**Evidence:**
- **k-LLMmeans** (arXiv 2502.09667, Feb 2025): Introduces a hybrid modification of k-means that uses LLMs to generate textual summaries as cluster centroids. Key finding: "k-LLMmeans consistently outperforms k-means and other traditional baselines" but **still requires the traditional k-means algorithm for actual clustering** - the LLM enhances centroids, it doesn't replace the algorithm
- Text clustering with LLM embeddings (2024): OpenAI embeddings + k-means outperformed other combinations in most experiments, but k-means remained the clustering engine
- **LLMEdgeRefine** (EMNLP 2024): "K-means clustering determines cluster centroids based on the mean" - all advanced LLM-based clustering methods still initialize with k-means and use it as the computational backbone
- Research consensus: LLMs provide semantic understanding for centroid interpretation and edge case refinement; deterministic algorithms handle the actual clustering computation

**Sources:**
- [k-LLMmeans, arXiv 2502.09667](https://www.arxiv.org/pdf/2502.09667v2.pdf)
- [Text clustering with LLM embeddings](https://arxiv.org/html/2403.15112v1)
- [LLMEdgeRefine, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.1025.pdf)
- [LiSA, ACL 2025](https://aclanthology.org/2025.acl-long.902.pdf)

**Implication:** `keyword_analyzer.py`'s scikit-learn TF-IDF + K-means pipeline is correct architecture. The upgrade should have Skills run the Python clustering, then use Claude to interpret results and provide strategic recommendations.

### 2.5 Regex vs LLM Performance (CONFIRMED)

**Claim:** Regex is 28,120x faster than LLM-based text processing for pattern extraction.

**Evidence:**
- **Exact figure validated**: A peer-reviewed study published in JAMIA Open (2025) comparing regex vs LLM-based extraction of BI-RADS scores from radiology reports found: "Regex processing was more efficient, completing the task **28,120 times faster** (0.06 seconds vs 1687.20 seconds)"
- The study found **no statistically significant difference in accuracy** between regex (89.20%) and LLM (87.69%) for structured pattern extraction (P = .56)
- On a larger 7,764-report dataset, the ratio was 18,404x faster for regex
- The study's conclusion: "Despite the impressive capabilities of LLMs, a Regex-based approach was much faster without being less accurate in extracting BI-RADS scores"
- Additional benchmarks show even basic string operations are 30x faster than regex in Java; LLMs add orders of magnitude more overhead

**Sources:**
- [JAMIA Open 2025 - Regex vs LLM comparison](https://boris-portal.unibe.ch/server/api/core/bitstreams/def72aa6-6a9e-4fd1-9235-2f19c1bfcb09/content) (Bern University Hospital)
- [RegexPSPACE benchmark, arXiv 2510.09227](https://arxiv.org/html/2510.09227v1)
- [LLMs and regular expressions](https://www.johndcook.com/blog/2024/12/15/llm-and-regex/)

**Implication:** All regex-based modules (`content_scrubber.py`, `seo_quality_rater.py`, `cro_checker.py`, pattern-based scorers) should remain as Python scripts. Their speed, accuracy, and determinism are superior to LLM alternatives.

### 2.6 Unicode Watermark Behavior (CONFIRMED)

**Claim:** LLMs insert invisible Unicode characters; ChatGPT specifically embeds Narrow No-Break Space (U+202F).

**Evidence:**
- **Rumi (rumidocs.com, April 2025)** discovered that GPT-o3 and o4-mini models embed U+202F (Narrow No-Break Space) characters in generated text. These are invisible to the naked eye but detectable by tools
- OpenAI officially responded: "the special characters are not a watermark... they're simply a quirk of large-scale reinforcement learning"
- Multiple independent analyses confirm: U+202F, U+00A0, U+200B, U+FEFF, U+200C, U+200D, U+00AD are commonly found in AI-generated text
- These characters **survive copy-paste** across editors and platforms
- Tools like gptwatermark.com now track **34+ invisible Unicode characters** used by various AI models
- The issue was reportedly resolved for newer ChatGPT models as of April 2025, but the broader pattern of LLMs learning to emit formatting characters from training data persists
- **Critical implication for this project**: `content_scrubber.py` targets exactly these characters (`\u200B`, `\uFEFF`, `\u200C`, `\u2060`, `\u00AD`, `\u202F`). An LLM asked to remove them may **insert additional ones**

**Sources:**
- [Rumi watermark discovery](https://www.rumidocs.com/newsroom/new-chatgpt-models-seem-to-leave-watermarks-on-text)
- [GPT Watermark Remover analysis](https://gpt-watermark-remover.com/blog/invisible-characters-chatgpt)
- [Clemens Jarnach Unicode analysis](https://clemensjarnach.github.io/02-articles/2025-04-24-article.html)
- [WindowsForum technical analysis](https://windowsforum.com/threads/unveiling-hidden-unicode-characters-in-openais-chatgpt-models-the-invisible-watermark-debate.361510/)
- [GetGPT watermark tool](https://getgpt.app/watermark)

**Implication:** `content_scrubber.py` is critical infrastructure. Regex-based scrubbing is the only reliable approach. This module must remain Python and should be expanded to cover newly discovered AI watermark characters.

### 2.7 Multi-Agent SEO Content Automation (CONFIRMED as Emerging Pattern)

**Claim:** Multi-agent architectures for SEO content workflows are an emerging industry pattern.

**Evidence:**
- **CrewAI** (30.5k GitHub stars, 1M+ monthly downloads): Role-based agent teams specifically designed for content pipelines (drafter + editor + publisher). Used by DocuSign, PwC, Gelato
- **AutoGen** (43.6k GitHub stars): Microsoft's multi-agent conversation framework, used by Novo Nordisk for data science workflows
- **Multi-Agent SEO Blog Generator**: Open-source framework using specialized agents (SEO keyword agent, outline agent, content agent, optimization agent)
- **LangGraph**: Enterprise-grade graph-based agent orchestration used by Uber and Klarna for stateful workflows
- Industry practitioners confirm the pattern: "One SEO professional with these tools can now do the work of 5-10 people" (AI SEO automation, 2025)
- The pattern consistently involves: **specialized agents with defined roles** + **deterministic tool execution** + **LLM interpretation layer** - matching SEO Machine's existing architecture

**Sources:**
- [CrewAI](https://www.crewai.com)
- [Best open-source agent frameworks 2025](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks-2025)
- [Multi-Agent SEO Blog Generator](https://creati.ai/ai-tools/multi-agent-seo-blog-generator/)
- [Open-source stack for AI agents 2025](https://futureagi.com/blogs/open-source-stack-ai-agents-2025)

**Implication:** SEO Machine's architecture is ahead of the curve. The upgrade to Skills-wrapped modules would formalize what most teams are still building from scratch with generic agent frameworks.

---

## 3. Problem Statement

SEO Machine's current architecture has four layers that work but are **loosely coupled**:

| Layer | Location | Function | Integration |
|-------|----------|----------|-------------|
| Skills | `.claude/skills/` | 26 marketing prompt frameworks | Markdown only, no `scripts/` |
| Agents | `.claude/agents/` | 10 specialized LLM personas | Pure markdown, no Python execution |
| Commands | `.claude/commands/` | 19 workflow orchestrators | **Only layer referencing Python** |
| Modules | `data_sources/modules/` | 24 Python analysis tools | Called from commands or terminal |

**The gap:** Commands are the only bridge between LLM reasoning (agents/skills) and deterministic computation (modules). This creates:

1. **Discoverability issues**: Users must know which Python scripts exist and how to invoke them
2. **Portability limitations**: Moving the project or sharing modules requires understanding the full command chain
3. **No progressive disclosure**: All Python capabilities require reading command docs to discover
4. **Duplication potential**: Agent instructions describe module capabilities in pseudocode rather than executing them
5. **No self-contained analysis packages**: Running a content analysis requires chaining multiple manual steps

---

## 4. Proposed Solution: Skills-as-Orchestration-Wrappers

### 4.1 Architecture Overview

Convert the current command+agent architecture into **self-contained Skills** that bundle Python modules in `scripts/` directories with LLM interpretation instructions in `SKILL.md`.

```
BEFORE:                              AFTER:
Command ──> Agent (reasoning)        Skill
Command ──> Python (computation)       ├── SKILL.md (reasoning + orchestration)
                                       ├── scripts/ (computation)
                                       │   ├── scorer.py
                                       │   └── analyzer.py
                                       └── references/ (context)
                                           └── rubric.md
```

### 4.2 Design Principles

1. **Wrap, don't replace**: Every Python module stays as-is. Skills wrap them with orchestration instructions.
2. **Deterministic first, LLM second**: Scripts run first for quantitative metrics. Claude interprets results for qualitative recommendations.
3. **Progressive disclosure**: Only skill name/description loads at startup. Full instructions load on trigger. Scripts execute on demand.
4. **Backward compatibility**: All existing commands continue to work. Skills are an additional, more integrated interface.
5. **Zero-cost determinism**: Python scoring runs locally with no API tokens. LLM reasoning only adds interpretation value.

---

## 5. Detailed Implementation Plan

### Phase 1: Core Analysis Skills (Priority: Critical)

These wrap the most-used, highest-value Python modules. Each skill bundles related modules into a coherent analysis package.

#### 5.1.1 `content-quality-analysis/` Skill

**Wraps:** `content_scorer.py`, `readability_scorer.py`, `engagement_analyzer.py`

```
.claude/skills/content-quality-analysis/
├── SKILL.md
├── scripts/
│   ├── content_scorer.py      (symlink or copy from data_sources/modules/)
│   ├── readability_scorer.py
│   └── engagement_analyzer.py
└── references/
    └── scoring-rubric.md      (extracted from current agent docs)
```

**SKILL.md behavior:**
1. Accept a draft file path as input
2. Run `python {baseDir}/scripts/content_scorer.py <file>` - get composite score (0-100)
3. Run `python {baseDir}/scripts/readability_scorer.py <file>` - get Flesch, grade level, passive voice %
4. Run `python {baseDir}/scripts/engagement_analyzer.py <file>` - get hook quality, rhythm, CTA distribution
5. Synthesize all scores into a strategic recommendation with specific improvement actions
6. If composite score < 70: flag top 3 fixable issues with line-level suggestions

**Research justification:** PhonologyBench (Section 2.2) confirms readability formulas require deterministic syllable counting (55% LLM accuracy vs 90% human). CWUM benchmark (Section 2.3) confirms word counting failures cascade into all metrics. Quality gates MUST be deterministic (Section 2.5).

#### 5.1.2 `seo-analysis/` Skill

**Wraps:** `keyword_analyzer.py`, `seo_quality_rater.py`, `search_intent_analyzer.py`

```
.claude/skills/seo-analysis/
├── SKILL.md
├── scripts/
│   ├── keyword_analyzer.py
│   ├── seo_quality_rater.py
│   └── search_intent_analyzer.py
└── references/
    └── seo-scoring-criteria.md
```

**SKILL.md behavior:**
1. Run keyword analysis (TF-IDF clustering, density, distribution)
2. Run SEO quality rating (0-100 with category breakdowns)
3. Run intent classification (informational/navigational/transactional/commercial)
4. Synthesize: "Your article targets [intent] queries. Keyword density is [X%] (optimal: 0.5-3%). Top cluster gaps: [list]. SEO score: [N]/100. Priority fixes: [list]."

**Research justification:** k-LLMmeans research (Section 2.4) confirms TF-IDF + K-means requires deterministic computation; LLMs enhance interpretation but cannot replace the algorithm. CWUM (Section 2.3) confirms LLMs cannot calculate keyword density.

#### 5.1.3 `content-scrubbing/` Skill

**Wraps:** `content_scrubber.py`

```
.claude/skills/content-scrubbing/
├── SKILL.md
├── scripts/
│   └── content_scrubber.py
└── references/
    └── unicode-watermark-catalog.md
```

**SKILL.md behavior:**
1. Run `python {baseDir}/scripts/content_scrubber.py <file>` - remove invisible Unicode + context-aware em-dash replacement
2. Report: "[N] invisible characters removed ([types]). [M] em-dashes replaced. File is now clean."
3. If no changes needed: "File is already clean. No AI watermark artifacts detected."

**Research justification:** Rumi/OpenAI watermark research (Section 2.6) confirms LLMs insert U+202F and other invisible characters. JAMIA Open study (Section 2.5) confirms regex is 28,120x faster and equally accurate for pattern extraction. LLMs asked to remove Unicode may insert more.

**Enhancement opportunity:** Update `content_scrubber.py` to also detect U+00A0 (Non-Breaking Space) and U+2003 (Em Space), which recent research identifies as additional AI text markers.

### Phase 2: CRO & Landing Page Skills (Priority: High)

#### 5.2.1 `landing-page-analysis/` Skill

**Wraps:** `landing_page_scorer.py`, `above_fold_analyzer.py`, `cta_analyzer.py`, `trust_signal_analyzer.py`, `cro_checker.py`

```
.claude/skills/landing-page-analysis/
├── SKILL.md
├── scripts/
│   ├── landing_page_scorer.py
│   ├── above_fold_analyzer.py
│   ├── cta_analyzer.py
│   ├── trust_signal_analyzer.py
│   └── cro_checker.py
└── references/
    └── cro-benchmarks.md
```

**SKILL.md behavior:**
1. Run all 5 CRO scripts in sequence
2. Present unified CRO dashboard: overall score, above-fold grade, CTA effectiveness, trust signal coverage, checklist pass/fail
3. Provide conversion-focused recommendations ranked by expected impact
4. Flag any critical failures from `cro_checker.py` as blockers

#### 5.2.2 `landing-performance/` Skill

**Wraps:** `landing_performance.py` (requires GA4/GSC APIs)

```
.claude/skills/landing-performance/
├── SKILL.md
├── scripts/
│   └── landing_performance.py
└── references/
    └── benchmark-grades.md
```

**SKILL.md behavior:**
1. Run performance script (graceful degradation if APIs unavailable)
2. Grade metrics: bounce rate (A-F), time on page, conversion rate
3. Compare against industry benchmarks
4. Recommend specific optimizations based on grade gaps

### Phase 3: Data Integration Skills (Priority: Medium)

#### 5.3.1 `data-pipeline/` Skill

**Wraps:** `google_analytics.py`, `google_search_console.py`, `dataforseo.py`, `data_aggregator.py`

```
.claude/skills/data-pipeline/
├── SKILL.md
├── scripts/
│   ├── google_analytics.py
│   ├── google_search_console.py
│   ├── dataforseo.py
│   └── data_aggregator.py
└── references/
    └── api-setup-guide.md
```

**SKILL.md behavior:**
1. Check credential availability for each API
2. Fetch data from available sources (graceful degradation)
3. Aggregate via `data_aggregator.py`
4. Present unified analytics dashboard with trend analysis
5. Identify anomalies and opportunities from the aggregated data

#### 5.3.2 `opportunity-scoring/` Skill

**Wraps:** `opportunity_scorer.py`, `competitor_gap_analyzer.py`

```
.claude/skills/opportunity-scoring/
├── SKILL.md
├── scripts/
│   ├── opportunity_scorer.py
│   └── competitor_gap_analyzer.py
└── references/
    └── scoring-methodology.md
```

**SKILL.md behavior:**
1. Run opportunity scoring (8-factor weighted: volume 25%, position 20%, intent 20%, competition 15%, cluster 10%, CTR 5%, freshness 5%, trend 5%)
2. Run competitor gap analysis
3. Present prioritized opportunity matrix: CRITICAL, HIGH, MEDIUM, LOW, SKIP
4. For each CRITICAL/HIGH opportunity: specific action plan with content brief outline

### Phase 4: Content Pipeline Skills (Priority: Medium)

#### 5.4.1 `content-comparison/` Skill

**Wraps:** `content_length_comparator.py`

```
.claude/skills/content-comparison/
├── SKILL.md
├── scripts/
│   └── content_length_comparator.py
└── references/
    └── serp-benchmarks.md
```

#### 5.4.2 `wordpress-publishing/` Skill

**Wraps:** `wordpress_publisher.py`

```
.claude/skills/wordpress-publishing/
├── SKILL.md
├── scripts/
│   └── wordpress_publisher.py
└── references/
    └── yoast-fields-reference.md
```

#### 5.4.3 `article-planning/` Skill (Category C - Lightweight)

**Wraps:** `article_planner.py`, `section_writer.py`

These are Category C modules (orchestration/config). The Skill wrapping here is primarily for discoverability and integration, not because the Python is irreplaceable.

```
.claude/skills/article-planning/
├── SKILL.md
├── scripts/
│   ├── article_planner.py
│   └── section_writer.py
└── references/
    └── writing-guidelines.md
```

---

## 6. Script Integration Strategy

### 6.1 Symlinks vs Copies

**Recommended: Symlinks** for development, copies for distribution.

```bash
# Development: symlink to avoid duplication
ln -s ../../../../data_sources/modules/content_scorer.py \
  .claude/skills/content-quality-analysis/scripts/content_scorer.py

# Distribution: copy for self-contained portability
cp data_sources/modules/content_scorer.py \
  .claude/skills/content-quality-analysis/scripts/content_scorer.py
```

### 6.2 Dependency Management

Each skill's `scripts/` directory should include a `requirements.txt` for its specific dependencies:

```
# content-quality-analysis/scripts/requirements.txt
textstat>=0.7.3
```

```
# seo-analysis/scripts/requirements.txt
scikit-learn>=1.3.0
numpy>=1.24.0
```

### 6.3 Import Path Handling

Scripts in `scripts/` directories may need import path adjustments. Two approaches:

**Option A (Preferred):** Make each script callable standalone with `--file` argument:
```bash
python {baseDir}/scripts/content_scorer.py --file drafts/my-article.md
```

**Option B:** Set PYTHONPATH in SKILL.md instructions:
```
Run: PYTHONPATH={baseDir}/scripts python {baseDir}/scripts/content_scorer.py <file>
```

---

## 7. Migration Plan

### 7.1 Phase Sequence

| Phase | Skills | Timeline | Dependencies |
|-------|--------|----------|--------------|
| 1 | content-quality-analysis, seo-analysis, content-scrubbing | First | None - core functionality |
| 2 | landing-page-analysis, landing-performance | Second | Phase 1 patterns established |
| 3 | data-pipeline, opportunity-scoring | Third | API credentials tested |
| 4 | content-comparison, wordpress-publishing, article-planning | Fourth | Full pipeline validated |

### 7.2 Backward Compatibility

- All existing commands in `.claude/commands/` continue to work unchanged
- All existing agents in `.claude/agents/` remain functional
- Skills are an **additive layer**, not a replacement for commands
- Root-level Python scripts (`research_quick_wins.py`, etc.) remain callable from terminal
- The `/write` pipeline (`scrub -> score -> auto-revise -> agents`) is preserved but gains an alternative entry point through Skills

### 7.3 Testing Strategy

For each new Skill:
1. **Script isolation test**: Verify each `scripts/*.py` file runs correctly from its new location
2. **Skill trigger test**: Invoke the skill via slash command and verify SKILL.md instructions execute correctly
3. **Pipeline integration test**: Run the full `/write` pipeline and verify skills integrate with existing commands
4. **Regression test**: Ensure existing command behavior is unchanged

---

## 8. Content Scrubber Enhancement

Based on the Unicode watermark research (Section 2.6), `content_scrubber.py` should be enhanced to detect additional AI text markers discovered since its last update:

### 8.1 New Characters to Add

| Character | Unicode | Source |
|-----------|---------|--------|
| Non-Breaking Space | U+00A0 | Common in ChatGPT output |
| Em Space | U+2003 | Identified by gptwatermark.com |
| Three-Per-Em Space | U+2004 | Emerging in newer models |
| Four-Per-Em Space | U+2005 | Emerging in newer models |
| Thin Space | U+2009 | Typography artifacts from training |
| Hair Space | U+200A | Typography artifacts from training |

### 8.2 Current Characters (Already Handled)

| Character | Unicode | Status |
|-----------|---------|--------|
| Zero-Width Space | U+200B | Handled |
| BOM / Zero-Width No-Break Space | U+FEFF | Handled |
| Zero-Width Non-Joiner | U+200C | Handled |
| Word Joiner | U+2060 | Handled |
| Soft Hyphen | U+00AD | Handled |
| Narrow No-Break Space | U+202F | Handled |

### 8.3 Em Dash Handling Update

Current: Context-aware em-dash replacement analyzing 50-char windows.
Enhancement: Also detect Two-Em Dash (U+2E3A) and Three-Em Dash (U+2E3B), which some AI models emit.

---

## 9. New Marketing Skills Enhancement

The existing 26 marketing skills use only `SKILL.md` + `references/`. Where applicable, these should gain `scripts/` directories for deterministic analysis:

| Existing Skill | Potential Script Addition |
|----------------|--------------------------|
| `/seo-audit` | Bundle `seo_quality_rater.py` for automated scoring alongside qualitative audit |
| `/page-cro` | Bundle `cro_checker.py` + `landing_page_scorer.py` for quantitative CRO scoring |
| `/copywriting` | Bundle `content_scorer.py` for quality gate on generated copy |
| `/analytics-tracking` | Bundle `data_aggregator.py` for live data integration |
| `/form-cro` | Bundle `cta_analyzer.py` for CTA effectiveness scoring |

---

## 10. Success Metrics

| Metric | Current State | Target |
|--------|---------------|--------|
| Module discoverability | Users must read CLAUDE.md or command docs | Skills auto-discovered via progressive disclosure |
| Pipeline invocation steps | 3-5 manual steps for full analysis | Single skill invocation triggers full pipeline |
| Token overhead at startup | N/A (modules not referenced) | ~30-50 tokens per skill (YAML frontmatter only) |
| Script portability | Modules tied to `data_sources/modules/` path | Self-contained in skill directory with `{baseDir}` |
| Content scrubber coverage | 6 Unicode characters | 12+ Unicode characters (expanded catalog) |
| Quality gate consistency | Deterministic (Python) - maintained | Deterministic (Python) - maintained (zero regression) |

---

## 11. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Symlink breakage on different OS | Scripts fail to load | Use `{baseDir}` paths in SKILL.md; test on Linux/macOS/Windows |
| Python dependency conflicts between skills | Import errors | Each skill has its own `requirements.txt`; document minimum versions |
| Script import path issues | Modules can't import shared utils | Make scripts standalone with CLI arguments; avoid inter-module imports in skill copies |
| SKILL.md instructions too complex | Claude misinterprets orchestration | Keep instructions concise; test with multiple invocations; provide examples |
| Backward compatibility regression | Existing commands break | Skills are additive only; never modify existing commands in this upgrade |
| Progressive disclosure loading latency | Slow skill activation | Keep YAML frontmatter minimal; defer script execution to Level 3 |

---

## 12. Out of Scope

- **Replacing any Python module with LLM reasoning**: All research confirms this degrades quality for computation-heavy and regex-based modules
- **Removing the command layer**: Commands remain the primary orchestration interface; skills are complementary
- **Removing the agent layer**: Agents remain available as personas for qualitative guidance
- **Multi-agent framework migration**: No migration to CrewAI/AutoGen/LangGraph. Claude Code's native Skills system is purpose-built for this pattern
- **Real-time streaming processing**: All analysis remains batch/on-demand
- **API credential management changes**: No changes to `.env` or credential setup

---

## 13. References

### Academic Papers
1. PhonologyBench: Evaluating Phonological Skills of Large Language Models. Suvarna, Khandelwal, Peng. ACL KnowLLM 2024. [arXiv:2404.02456](https://arxiv.org/html/2404.02456v2)
2. Large Language Models Can Not Perform Well in Understanding Manipulation. EMNLP Findings 2024. [CWUM](https://aclanthology.org/2024.findings-emnlp.691.pdf)
3. k-LLMmeans: Scalable, Stable, and Interpretable Text Clustering. Diaz-Rodriguez. Feb 2025. [arXiv:2502.09667](https://www.arxiv.org/pdf/2502.09667v2.pdf)
4. A Comparative Performance Analysis of Regular Expressions and an LLM-Based Approach. JAMIA Open 2025. [Bern Study](https://boris-portal.unibe.ch/server/api/core/bitstreams/def72aa6-6a9e-4fd1-9235-2f19c1bfcb09/content)
5. A Linguistic and Math Expert's Struggle with Simple Word-Based Counting. NAACL 2025. [ACL Anthology](https://aclanthology.org/2025.naacl-long.172.pdf)
6. Why Do Large Language Models Struggle to Count Letters? Dec 2024. [arXiv:2412.18626](https://arxiv.org/html/2412.18626v1)
7. LLMEdgeRefine: Enhancing Text Clustering with LLM-Powered Edge Points. EMNLP 2024. [ACL Anthology](https://aclanthology.org/2024.emnlp-main.1025.pdf)
8. Investigating Word Count Control. Katherine Li, Stanford CS224N. 2024. [Stanford](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1244/final-projects/KatherineLi.pdf)

### Industry & Documentation
9. Claude Code Skills Documentation. Anthropic. [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
10. The Complete Guide to Building Skills for Claude. Anthropic. [Resource Hub](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
11. Claude Skills Deep Dive. Lee Han Chung. Oct 2025. [Blog](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
12. New ChatGPT Models Seem to Leave Watermarks on Text. Rumi. Apr 2025. [rumidocs.com](https://www.rumidocs.com/newsroom/new-chatgpt-models-seem-to-leave-watermarks-on-text)
13. Invisible Characters in ChatGPT Text. GPT Watermark Remover. [Analysis](https://gpt-watermark-remover.com/blog/invisible-characters-chatgpt)
14. Precision Word Count: Revolutionising AI Writing Accuracy. Fifth Dimension AI. Aug 2024. [Blog](https://www.fifthdimensionai.com/en-us/blogs-news/precision-word-count-revolutionising-ai-writing-accuracy)

### Multi-Agent Frameworks
15. CrewAI: The Leading Multi-Agent Platform. [crewai.com](https://www.crewai.com)
16. Best Open Source Agent Frameworks 2025. Firecrawl. [Blog](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks-2025)
17. The Open-Source Stack for AI Agents in 2025. FutureAGI. [Blog](https://futureagi.com/blogs/open-source-stack-ai-agents-2025)
