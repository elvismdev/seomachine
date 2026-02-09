# Spec: Skill Wrapper Architecture

## ADDED Requirements

### Requirement: Skills Bundle Python Modules via scripts/ Directories

Each new orchestration skill MUST contain a `scripts/` directory with symlinks to the canonical Python modules in `data_sources/modules/`. The canonical source remains `data_sources/modules/`; skills reference them, never copy them.

#### Scenario: Skill directory structure is valid

- **WHEN** a new orchestration skill is created at `.claude/skills/[skill-name]/`
- **THEN** it contains `SKILL.md` with valid YAML frontmatter (name, version, description)
- **AND** it contains a `scripts/` directory with one or more `.py` symlinks pointing to `data_sources/modules/`
- **AND** it contains a `references/` directory with at least one `.md` file documenting scoring criteria
- **AND** it contains `scripts/requirements.txt` listing Python dependencies for that skill's scripts

#### Scenario: Symlinks resolve correctly from repo root

- **WHEN** a symlink in `.claude/skills/[skill-name]/scripts/[module].py` is followed
- **THEN** it resolves to `data_sources/modules/[module].py`
- **AND** the resolved file is importable and executable via `python data_sources/modules/[module].py`

#### Scenario: Scripts with inter-module imports work from skill directory

- **WHEN** `content_scorer.py` is symlinked into a skill's `scripts/` directory
- **AND** `readability_scorer.py` and `seo_quality_rater.py` are also symlinked in the same `scripts/` directory
- **THEN** running `python {baseDir}/scripts/content_scorer.py --file [path]` succeeds
- **AND** the relative import fallback (`from readability_scorer import ReadabilityScorer`) resolves within the same `scripts/` directory

---

### Requirement: SKILL.md Follows Deterministic-First Pattern

Each SKILL.md MUST instruct Claude to run Python scripts for quantitative metrics BEFORE applying LLM interpretation for qualitative recommendations.

#### Scenario: Content quality analysis execution order

- **WHEN** the `content-quality-analysis` skill is triggered with a file path
- **THEN** Claude runs `python {baseDir}/scripts/content_scorer.py --file [path]` first
- **AND** Claude runs `python {baseDir}/scripts/readability_scorer.py --file [path]` second
- **AND** Claude runs `python {baseDir}/scripts/engagement_analyzer.py --file [path]` third
- **AND** only AFTER all three scripts produce output does Claude synthesize a strategic recommendation
- **AND** the recommendation explicitly cites the numeric scores from each script

#### Scenario: Script failure is reported, not silently skipped

- **WHEN** a Python script fails during skill execution (exit code != 0)
- **THEN** the SKILL.md instructs Claude to report the error with the script name and stderr output
- **AND** Claude does NOT hallucinate or estimate the missing score
- **AND** Claude continues with remaining scripts that can run independently

---

### Requirement: Progressive Disclosure Token Budget

Skills MUST use progressive disclosure to minimize startup token overhead.

#### Scenario: YAML frontmatter stays within token budget

- **WHEN** Claude Code loads all skill frontmatter at startup
- **THEN** each new orchestration skill's frontmatter is <= 50 tokens
- **AND** the frontmatter contains only: name, version, description (one sentence max)

#### Scenario: Full SKILL.md loads only on trigger

- **WHEN** a user invokes a skill (e.g., `/content-quality-analysis`)
- **THEN** the full SKILL.md body loads into context
- **AND** scripts are NOT loaded into context (only their output after execution)
- **AND** references load only when Claude determines they are needed

---

### Requirement: Content Scrubber Expanded Unicode Coverage

`content_scrubber.py` MUST detect and remove 6 additional Unicode characters identified by research as AI text markers.

#### Scenario: New watermark characters are removed

- **WHEN** content containing U+00A0 (Non-Breaking Space), U+2003 (Em Space), U+2004 (Three-Per-Em Space), U+2005 (Four-Per-Em Space), U+2009 (Thin Space), or U+200A (Hair Space) is processed
- **THEN** all instances are removed or replaced with standard spaces
- **AND** the statistics dict includes counts for each character type removed

#### Scenario: New dash variants are handled

- **WHEN** content containing U+2E3A (Two-Em Dash) or U+2E3B (Three-Em Dash) is processed
- **THEN** they are replaced using the same context-aware em-dash logic as standard em-dashes (U+2014)
- **AND** the `emdashes_replaced` stat includes these variants

#### Scenario: Existing scrubbing behavior is preserved

- **WHEN** content containing only the original 6 watermark characters is processed
- **THEN** the output is identical to the output from the pre-enhancement version
- **AND** no regressions in em-dash context analysis (50-char window, attribution patterns, verb presence)

---

### Requirement: Backward Compatibility

The upgrade MUST NOT break any existing functionality.

#### Scenario: Existing commands work unchanged

- **WHEN** a user runs `/write [topic]`, `/scrub [file]`, `/optimize [file]`, or any other existing command
- **THEN** the command produces identical behavior to before the upgrade
- **AND** no command references are modified

#### Scenario: Existing skills work unchanged

- **WHEN** a user invokes any of the 26 existing marketing skills
- **THEN** the skill produces identical behavior to before the upgrade
- **AND** existing SKILL.md files are not modified during Phases 1-3

#### Scenario: Python modules remain terminal-callable

- **WHEN** a user runs `python data_sources/modules/[module].py` from repo root
- **THEN** the module executes identically to before the upgrade
- **AND** symlinks in skill directories do not interfere with direct module execution

---

## MODIFIED Requirements

### Requirement: Existing Marketing Skills Gain Scripts (Phase 4)

Five existing marketing skills receive optional `scripts/` directories to provide deterministic scoring alongside their qualitative analysis.

#### Scenario: seo-audit gains seo_quality_rater.py

- **WHEN** the `seo-audit` skill is triggered
- **THEN** SKILL.md instructions include an optional step to run `python {baseDir}/scripts/seo_quality_rater.py`
- **AND** the existing qualitative audit framework remains the primary output
- **AND** the quantitative score is presented as a supplement, not a replacement
