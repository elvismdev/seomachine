# Skill Wrapper Developer Guide

How to create new orchestration skills that wrap Python modules.

## Quick Start

```bash
# 1. Create directory structure
mkdir -p .claude/skills/my-skill/{scripts,references}

# 2. Symlink Python module(s)
cd .claude/skills/my-skill/scripts
ln -s ../../../../data_sources/modules/my_module.py my_module.py

# 3. Create SKILL.md (see template below)
# 4. Create references/ docs and scripts/requirements.txt
```

## SKILL.md Template

```yaml
---
name: my-skill
version: 1.0.0
description: One-line description shown in skill listing. Use when the user wants to...
---

# My Skill

You are a [specialist role]. Run deterministic scripts first, then interpret results.

## Execution

**Input:** What the user provides.

### Step 1: Run Script

\`\`\`bash
python3 {baseDir}/scripts/my_module.py <args> --json
\`\`\`

Returns: [describe JSON output fields]

### Step 2: Interpret Results

[How to synthesize and present the data]

## Error Handling

[Graceful degradation instructions]

## References

See `references/my-reference.md` for [what].

## Related Skills

- **other-skill**: For [related purpose]
```

## Key Principles

### 1. Deterministic-First

Always run Python scripts before applying LLM reasoning. This ensures:
- Reproducible results (same input = same output)
- No hallucinated metrics
- 28,000x faster for character-level operations (vs LLM)

### 2. Symlinks, Not Copies

Use relative symlinks to avoid module duplication:
```
ln -s ../../../../data_sources/modules/module.py module.py
```

The 4 levels up (`../../../../`) goes from:
`.claude/skills/[name]/scripts/` → repo root → `data_sources/modules/`

### 3. Co-locate Dependencies

If Module A imports Module B, both must be symlinked into the same `scripts/` directory. Python resolves imports from the script's directory first.

### 4. CLI Convention

All modules should accept:
- File path as first positional argument (for file-based analysis)
- `--json` flag for machine-readable JSON output
- `--keyword`, `--type`, `--goal` flags for configuration
- Error output on stderr, data on stdout

### 5. Progressive Disclosure

Claude Code loads skill metadata in stages:
1. **Startup**: Only YAML frontmatter (~30-50 tokens per skill)
2. **Trigger**: Full SKILL.md loaded when skill is invoked
3. **On demand**: Scripts run only when explicitly called

Keep the YAML `description` concise — it's loaded for every conversation.

### 6. References Directory

Include reference docs that give the LLM context without hardcoding values:
- Scoring rubrics and grade scales
- Benchmark data and thresholds
- API setup guides
- Best practice checklists

## Module CLI Upgrade Pattern

When upgrading a module's `__main__` block:

```python
if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python module.py <file_path> [--json]", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    output_json = '--json' in sys.argv

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    result = analyze(content)  # Your module's analysis function

    if output_json:
        print(json.dumps(result, indent=2, default=str))
    else:
        # Human-readable output
        print(f"Score: {result['score']}/100")
```

## Testing

Verify a new skill works:

```bash
# 1. Check symlinks resolve
ls -la .claude/skills/my-skill/scripts/

# 2. Run script from symlinked directory
cd .claude/skills/my-skill/scripts
python3 my_module.py /path/to/test-file.md --json

# 3. Verify idempotency (for scrubbing/modification skills)
python3 my_module.py /path/to/file.md --json  # Run twice, same result

# 4. Check skill appears in Claude's listing
# Look for it in the skill list when starting a conversation
```

## Existing Skills Reference

| Skill | Modules | Input |
|-------|---------|-------|
| content-quality-analysis | 4 modules | File path |
| seo-analysis | 3 modules | File path + keyword |
| content-scrubbing | 1 module | File path |
| landing-page-analysis | 5 modules | File path + page type + goal |
| landing-performance | 1 module | URL |
| data-pipeline | 4 modules | Various (API-based) |
| opportunity-scoring | 2 modules | Keyword + metrics |
| content-comparison | 1 module | File path + keyword |
| wordpress-publishing | 1 module | File path |
| article-planning | 2 modules | Topic |
| seo-audit | 1 module | File path |
| page-cro | 2 modules | File path + page type + goal |
| copywriting | 1 module | File path |
| analytics-tracking | 1 module | Various (API-based) |
| form-cro | 1 module | File path + goal |
