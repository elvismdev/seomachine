#!/usr/bin/env python3
"""
SEO Machine Integration Test Suite

Verifies symlinks, module CLIs, import chains, content pipelines,
scrubber behavior, SKILL.md frontmatter, command references, and agent files.

Uses Python stdlib only (no pytest). Exit code 0 = all pass, 1 = any fail.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = ROOT / "data_sources" / "modules"
SKILLS_DIR = ROOT / ".claude" / "skills"
COMMANDS_DIR = ROOT / ".claude" / "commands"
AGENTS_DIR = ROOT / ".claude" / "agents"
FIXTURE = ROOT / "examples" / "castos" / "writing-examples.md"

passed = 0
failed = 0
errors = []


def ok(msg):
    global passed
    passed += 1
    print(f"  PASS  {msg}")


def fail(msg, detail=""):
    global failed
    failed += 1
    info = f" ({detail})" if detail else ""
    errors.append(f"{msg}{info}")
    print(f"  FAIL  {msg}{info}")


# ── 1. Symlink Verification ────────────────────────────────────────────────

EXPECTED_SYMLINKS = {
    "analytics-tracking": ["data_aggregator.py"],
    "article-planning": ["article_planner.py", "section_writer.py"],
    "content-comparison": ["content_length_comparator.py"],
    "content-quality-analysis": [
        "content_scorer.py", "engagement_analyzer.py",
        "readability_scorer.py", "seo_quality_rater.py",
    ],
    "content-scrubbing": ["content_scrubber.py"],
    "copywriting": ["content_scorer.py", "readability_scorer.py", "seo_quality_rater.py"],
    "data-pipeline": [
        "data_aggregator.py", "dataforseo.py",
        "google_analytics.py", "google_search_console.py",
    ],
    "form-cro": ["cta_analyzer.py"],
    "landing-page-analysis": [
        "above_fold_analyzer.py", "cro_checker.py", "cta_analyzer.py",
        "landing_page_scorer.py", "trust_signal_analyzer.py",
    ],
    "landing-performance": ["landing_performance.py"],
    "opportunity-scoring": ["competitor_gap_analyzer.py", "opportunity_scorer.py"],
    "page-cro": ["cro_checker.py", "landing_page_scorer.py"],
    "seo-analysis": ["keyword_analyzer.py", "search_intent_analyzer.py", "seo_quality_rater.py"],
    "seo-audit": ["seo_quality_rater.py"],
    "wordpress-publishing": ["wordpress_publisher.py"],
}


def test_symlinks():
    print("\n[1/8] Symlink Verification")
    count = 0
    for skill, scripts in sorted(EXPECTED_SYMLINKS.items()):
        for script in sorted(scripts):
            link = SKILLS_DIR / skill / "scripts" / script
            label = f"{skill}/scripts/{script}"
            if not link.exists():
                fail(label, "missing")
                continue
            if not link.is_symlink():
                fail(label, "not a symlink")
                continue
            target = link.resolve()
            if not target.exists():
                fail(label, f"broken -> {target}")
                continue
            if target.parent != MODULES_DIR:
                fail(label, f"target not in data_sources/modules: {target}")
                continue
            ok(f"{label} -> {target.name}")
            count += 1
    expected_total = sum(len(v) for v in EXPECTED_SYMLINKS.values())
    if count == expected_total:
        print(f"  {count}/{expected_total} symlinks OK")
    else:
        fail(f"symlink count", f"expected {expected_total}, got {count}")


# ── 2. Module CLI Tests ────────────────────────────────────────────────────

# Modules that take a file path as first positional arg
FILE_MODULES = [
    "content_scorer", "readability_scorer", "seo_quality_rater",
    "content_scrubber", "engagement_analyzer", "above_fold_analyzer",
    "cta_analyzer", "trust_signal_analyzer", "cro_checker",
    "landing_page_scorer", "content_length_comparator",
    "competitor_gap_analyzer",
]

# keyword_analyzer requires file + keyword positional args
# These take a topic/keyword as first positional arg
TOPIC_MODULES = ["social_research_aggregator", "search_intent_analyzer"]

# Modules that need specific positional + flag args
SPECIAL_MODULES = {
    "opportunity_scorer": ["podcast", "--position", "15", "--volume", "1000", "--json"],
    "article_planner": ["podcast advertising", "--json"],
    "landing_performance": ["/pricing", "--json"],
}

# No-arg modules (just --json)
NOARG_MODULES = ["section_writer", "data_aggregator"]

# API modules that should exit 1 with JSON error (missing credentials)
API_MODULES = ["google_analytics", "google_search_console", "dataforseo", "wordpress_publisher"]

# Modules that gracefully degrade (exit 0 even without creds)
GRACEFUL_MODULES = ["data_aggregator"]


def run_module(module_name, extra_args=None, timeout=30):
    """Run a module CLI and return (exit_code, stdout, stderr)."""
    script = MODULES_DIR / f"{module_name}.py"
    cmd = [sys.executable, str(script)] + (extra_args or [])
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=str(ROOT)
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"


def is_valid_json(text):
    """Check if text is parseable JSON. Returns (bool, parsed_or_None)."""
    text = text.strip()
    if not text:
        return False, None
    try:
        data = json.loads(text)
        return True, data
    except (json.JSONDecodeError, ValueError):
        return False, None


def test_module_cli():
    print("\n[2/8] Module CLI Tests")
    fixture = str(FIXTURE)

    # File-based modules
    for mod in FILE_MODULES:
        args = [fixture, "--json"]
        # keyword_analyzer needs keyword as 2nd positional
        if mod == "seo_quality_rater":
            args = [fixture, "--keyword", "podcast", "--json"]
        code, stdout, stderr = run_module(mod, args)
        valid, data = is_valid_json(stdout)
        if code == 0 and valid:
            ok(f"{mod}.py (exit=0, valid JSON)")
        else:
            fail(f"{mod}.py", f"exit={code}, valid_json={valid}, stderr={stderr[:120]}")

    # keyword_analyzer: file + keyword positional
    code, stdout, stderr = run_module("keyword_analyzer", [fixture, "podcast", "--json"])
    valid, data = is_valid_json(stdout)
    if code == 0 and valid:
        ok("keyword_analyzer.py (exit=0, valid JSON)")
    else:
        fail("keyword_analyzer.py", f"exit={code}, valid_json={valid}, stderr={stderr[:120]}")

    # Topic-based modules
    for mod in TOPIC_MODULES:
        code, stdout, stderr = run_module(mod, ["podcast advertising", "--json"])
        valid, data = is_valid_json(stdout)
        if code == 0 and valid:
            ok(f"{mod}.py (exit=0, valid JSON)")
        else:
            fail(f"{mod}.py", f"exit={code}, valid_json={valid}, stderr={stderr[:120]}")

    # Special modules with custom args
    for mod, args in SPECIAL_MODULES.items():
        code, stdout, stderr = run_module(mod, args)
        valid, data = is_valid_json(stdout)
        if code == 0 and valid:
            ok(f"{mod}.py (exit=0, valid JSON)")
        elif mod in GRACEFUL_MODULES and valid:
            ok(f"{mod}.py (exit={code}, valid JSON - graceful)")
        else:
            fail(f"{mod}.py", f"exit={code}, valid_json={valid}, stderr={stderr[:120]}")

    # No-arg modules
    for mod in NOARG_MODULES:
        code, stdout, stderr = run_module(mod, ["--json"])
        valid, data = is_valid_json(stdout)
        if mod in GRACEFUL_MODULES:
            # data_aggregator: exit 0 with JSON (graceful degradation)
            if valid:
                ok(f"{mod}.py (exit={code}, valid JSON - graceful)")
            else:
                fail(f"{mod}.py", f"exit={code}, valid_json={valid}, stderr={stderr[:120]}")
        elif code == 0 and valid:
            ok(f"{mod}.py (exit=0, valid JSON)")
        else:
            fail(f"{mod}.py", f"exit={code}, valid_json={valid}, stderr={stderr[:120]}")

    # API modules (expect exit 1 with JSON error when creds missing)
    for mod in API_MODULES:
        if mod == "wordpress_publisher":
            # wordpress_publisher uses argparse, needs a file arg
            code, stdout, stderr = run_module(mod, [fixture, "--json"])
        elif mod == "dataforseo":
            # dataforseo requires a keyword arg
            code, stdout, stderr = run_module(mod, ["podcast", "--json"])
        else:
            code, stdout, stderr = run_module(mod, ["--json"])
        # These should fail gracefully: exit 1 with JSON error OR stderr message
        valid_stdout, _ = is_valid_json(stdout)
        valid_stderr, _ = is_valid_json(stderr)
        if code != 0 and (valid_stdout or valid_stderr or "error" in stderr.lower() or "Error" in stdout):
            ok(f"{mod}.py (exit={code}, expected API error)")
        elif code == 0:
            # If creds happen to be configured, that's fine too
            ok(f"{mod}.py (exit=0, API configured)")
        else:
            fail(f"{mod}.py", f"exit={code}, no error info, stderr={stderr[:120]}")


# ── 3. Import Chain Tests ──────────────────────────────────────────────────

def test_import_chains():
    print("\n[3/8] Import Chain Tests")

    # Test 1: copywriting/scripts/ can import content_scorer
    scripts_dir = SKILLS_DIR / "copywriting" / "scripts"
    code1 = subprocess.run(
        [sys.executable, "-c", "from content_scorer import ContentScorer; print('OK')"],
        capture_output=True, text=True, cwd=str(scripts_dir)
    ).returncode
    if code1 == 0:
        ok("copywriting/scripts/ -> content_scorer import")
    else:
        fail("copywriting/scripts/ -> content_scorer import")

    # Test 2: data-pipeline/scripts/ can import data_aggregator
    scripts_dir = SKILLS_DIR / "data-pipeline" / "scripts"
    code2 = subprocess.run(
        [sys.executable, "-c", "from data_aggregator import DataAggregator; print('OK')"],
        capture_output=True, text=True, cwd=str(scripts_dir)
    ).returncode
    if code2 == 0:
        ok("data-pipeline/scripts/ -> data_aggregator import")
    else:
        fail("data-pipeline/scripts/ -> data_aggregator import")


# ── 4. Content Analysis Pipeline ───────────────────────────────────────────

def test_content_pipeline():
    print("\n[4/8] Content Analysis Pipeline")
    fixture = str(FIXTURE)

    # Test 1: readability_scorer has readability_metrics.flesch_reading_ease
    code, stdout, _ = run_module("readability_scorer", [fixture, "--json"])
    valid, data = is_valid_json(stdout)
    if (valid and isinstance(data, dict)
            and isinstance(data.get("readability_metrics", {}).get("flesch_reading_ease"), (int, float))):
        ok(f"readability_scorer: flesch_reading_ease = {data['readability_metrics']['flesch_reading_ease']}")
    else:
        fail("readability_scorer: missing readability_metrics.flesch_reading_ease")

    # Test 2: seo_quality_rater has overall_score 0-100
    code, stdout, _ = run_module("seo_quality_rater", [fixture, "--keyword", "podcast", "--json"])
    valid, data = is_valid_json(stdout)
    if valid and isinstance(data, dict):
        score = data.get("overall_score")
        if isinstance(score, (int, float)) and 0 <= score <= 100:
            ok(f"seo_quality_rater: overall_score = {score}")
        else:
            fail("seo_quality_rater: overall_score not 0-100", f"got {score}")
    else:
        fail("seo_quality_rater: invalid JSON")

    # Test 3: content_scorer has composite_score 0-100 and all 5 dimensions
    code, stdout, _ = run_module("content_scorer", [fixture, "--json"])
    valid, data = is_valid_json(stdout)
    if valid and isinstance(data, dict):
        composite = data.get("composite_score")
        dimensions = data.get("dimensions", {})
        expected_dims = {"humanity", "specificity", "structure_balance", "seo", "readability"}
        actual_dims = set(dimensions.keys()) if isinstance(dimensions, dict) else set()
        if (isinstance(composite, (int, float)) and 0 <= composite <= 100
                and expected_dims.issubset(actual_dims)):
            ok(f"content_scorer: composite_score = {composite}, all 5 dimensions present")
        else:
            fail("content_scorer: missing composite_score or dimensions",
                 f"composite={composite}, dims={actual_dims}")
    else:
        fail("content_scorer: invalid JSON")


# ── 5. Scrubber Pipeline ──────────────────────────────────────────────────

def test_scrubber():
    print("\n[5/8] Scrubber Pipeline")

    # Create temp file with known watermarks
    watermarked = (
        "Hello\u200b world\ufeff test\u202f content.\n"
        "This has em\u2014dashes and zero\u200cwidth chars.\n"
        "More\u2060 invisible\u00ad characters here.\n"
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(watermarked)
        tmp_path = f.name

    try:
        # Test 1: Watermark chars removed and em-dashes replaced
        code, stdout, stderr = run_module("content_scrubber", [tmp_path, "--json"])
        valid, stats = is_valid_json(stdout)
        if valid and isinstance(stats, dict):
            unicode_removed = stats.get("unicode_removed", 0)
            emdashes_replaced = stats.get("emdashes_replaced", 0)
            if unicode_removed > 0 or emdashes_replaced > 0:
                ok(f"scrubber: unicode_removed={unicode_removed}, emdashes_replaced={emdashes_replaced}")
            else:
                fail("scrubber: expected removals but got 0")
        else:
            fail("scrubber: invalid JSON output", f"exit={code}")

        # Test 2: Verify cleaned content has no watermark chars
        # Run with --in-place to clean the file, then check
        run_module("content_scrubber", [tmp_path, "--in-place", "--json"])
        with open(tmp_path, "r", encoding="utf-8") as f:
            cleaned = f.read()
        watermark_chars = {"\u200b", "\ufeff", "\u202f", "\u200c", "\u2060", "\u00ad"}
        remaining = [c for c in cleaned if c in watermark_chars]
        if not remaining:
            ok("scrubber: all watermark chars removed from output")
        else:
            fail("scrubber: watermark chars remain", f"count={len(remaining)}")

        # Test 3: Idempotency - run again, no further changes
        code2, stdout2, _ = run_module("content_scrubber", [tmp_path, "--json"])
        valid2, stats2 = is_valid_json(stdout2)
        if valid2 and isinstance(stats2, dict):
            if stats2.get("unicode_removed", 0) == 0 and stats2.get("emdashes_replaced", 0) == 0:
                ok("scrubber: idempotent (0 changes on re-run)")
            else:
                fail("scrubber: not idempotent",
                     f"unicode={stats2.get('unicode_removed')}, emdash={stats2.get('emdashes_replaced')}")
        else:
            fail("scrubber: idempotency check failed (invalid JSON)")
    finally:
        os.unlink(tmp_path)


# ── 6. SKILL.md Validation ─────────────────────────────────────────────────

def test_skill_frontmatter():
    print("\n[6/8] SKILL.md Validation")

    for skill_name in sorted(EXPECTED_SYMLINKS.keys()):
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        label = f"{skill_name}/SKILL.md"
        if not skill_md.exists():
            fail(label, "file missing")
            continue

        content = skill_md.read_text(encoding="utf-8")

        # Parse YAML frontmatter between --- markers
        fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            fail(label, "no YAML frontmatter")
            continue

        frontmatter = fm_match.group(1)

        # Extract name field
        name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
        name_val = name_match.group(1).strip() if name_match else None

        # Extract description field
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        desc_val = desc_match.group(1).strip() if desc_match else None

        if not name_val:
            fail(label, "missing 'name' field")
        elif name_val != skill_name:
            fail(label, f"name '{name_val}' != dir '{skill_name}'")
        elif not desc_val:
            fail(label, "missing 'description' field")
        else:
            ok(f"{label}: name={name_val}")


# ── 7. Command Path Verification ──────────────────────────────────────────

def test_command_paths():
    print("\n[7/8] Command Path Verification")

    if not COMMANDS_DIR.exists():
        fail("commands dir", "missing")
        return

    cmd_files = sorted(COMMANDS_DIR.glob("*.md"))
    if not cmd_files:
        fail("commands", "no .md files found")
        return

    # Regex to match python script references like: python3 path/to/script.py
    script_pattern = re.compile(r"python3?\s+([\w/.{}-]+\.py)")
    tested = 0

    for cmd_file in cmd_files:
        content = cmd_file.read_text(encoding="utf-8")
        matches = script_pattern.findall(content)

        for script_ref in matches:
            # Skip template variables like {baseDir}/scripts/...
            if "{" in script_ref:
                continue
            script_path = ROOT / script_ref
            label = f"{cmd_file.name} -> {script_ref}"
            if script_path.exists():
                ok(label)
            else:
                fail(label, "script not found")
            tested += 1

    if tested == 0:
        # No direct python paths found (all may use {baseDir} templates)
        # Verify commands exist and are non-empty instead
        for cmd_file in cmd_files:
            size = cmd_file.stat().st_size
            if size > 0:
                ok(f"{cmd_file.name} exists ({size} bytes)")
            else:
                fail(f"{cmd_file.name}", "empty file")


# ── 8. Agent File Verification ─────────────────────────────────────────────

EXPECTED_AGENTS = [
    "content-analyzer", "cro-analyst", "editor", "headline-generator",
    "internal-linker", "keyword-mapper", "landing-page-optimizer",
    "meta-creator", "performance", "seo-optimizer",
]


def test_agent_files():
    print("\n[8/8] Agent File Verification")

    for agent in EXPECTED_AGENTS:
        agent_file = AGENTS_DIR / f"{agent}.md"
        label = f"{agent}.md"
        if not agent_file.exists():
            fail(label, "missing")
        elif agent_file.stat().st_size == 0:
            fail(label, "empty")
        else:
            ok(f"{label} ({agent_file.stat().st_size} bytes)")


# ── Runner ─────────────────────────────────────────────────────────────────

def main():
    print("=== SEO Machine Integration Tests ===")

    # Verify fixture exists
    if not FIXTURE.exists():
        print(f"\nFATAL: Test fixture not found: {FIXTURE}")
        sys.exit(1)

    test_symlinks()
    test_module_cli()
    test_import_chains()
    test_content_pipeline()
    test_scrubber()
    test_skill_frontmatter()
    test_command_paths()
    test_agent_files()

    total = passed + failed
    print(f"\n=== Results: {passed}/{total} passed, {failed} failed ===")

    if errors:
        print(f"\nFailed tests:")
        for e in errors:
            print(f"  - {e}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
