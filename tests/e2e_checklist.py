#!/usr/bin/env python3
"""
SEO Machine E2E Test Checklist

Interactive guide for manually testing every Claude Code command and skill.
Run this script, then follow the prompts to exercise each workflow.

Each test tells you exactly what to run and what to verify in the output.
Results are logged to tests/e2e_results.log with timestamps.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = Path(__file__).resolve().parent / "e2e_results.log"

results = {"passed": [], "failed": [], "skipped": []}


def log(msg):
    """Print and log to file."""
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def header(title):
    log(f"\n{'='*60}")
    log(f"  {title}")
    log(f"{'='*60}")


def ask_result(test_id, description, command, checks):
    """Present a test case and ask for pass/fail/skip."""
    log(f"\n--- Test {test_id} ---")
    log(f"  {description}")
    log(f"\n  RUN:")
    log(f"    {command}")
    log(f"\n  VERIFY:")
    for check in checks:
        log(f"    [ ] {check}")

    while True:
        try:
            answer = input(f"\n  Result? [p]ass / [f]ail / [s]kip / [q]uit: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = "q"

        if answer in ("p", "pass"):
            results["passed"].append(test_id)
            log(f"  >> PASS")
            return "pass"
        elif answer in ("f", "fail"):
            note = input("  Failure note (optional): ").strip()
            results["failed"].append((test_id, note))
            log(f"  >> FAIL: {note}")
            return "fail"
        elif answer in ("s", "skip"):
            results["skipped"].append(test_id)
            log(f"  >> SKIP")
            return "skip"
        elif answer in ("q", "quit"):
            return "quit"
        else:
            print("  Enter p, f, s, or q")


def main():
    log(f"\n{'#'*60}")
    log(f"  SEO Machine E2E Test Checklist")
    log(f"  Started: {datetime.now().isoformat()}")
    log(f"  Root: {ROOT}")
    log(f"{'#'*60}")

    print("\nThis checklist guides you through testing every Claude Code")
    print("command and skill. Run each command in a separate Claude Code")
    print("session and verify the output matches expectations.\n")
    print("Tests are grouped by workflow. You can skip any test or quit")
    print("at any time. Results are saved to tests/e2e_results.log.\n")

    test_topic = "podcast advertising ROI"
    test_keyword = "podcast advertising"
    draft_file = f"drafts/podcast-advertising-roi-{datetime.now().strftime('%Y-%m-%d')}.md"

    # ── Phase 1: Research ──────────────────────────────────────────────

    header("PHASE 1: Research Commands")

    r = ask_result(
        "R1", "Research command generates a brief",
        f'/research "{test_topic}"',
        [
            f"Creates file in research/ (e.g. brief-podcast-advertising-roi-*.md)",
            "Brief contains: keyword analysis, competitor review, content angle",
            "References context/brand-voice.md and context/target-keywords.md",
            "Brief has sections: Overview, Keywords, Competitors, Content Angle",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "R2", "SERP research for a keyword",
        f'/research-serp "{test_keyword}"',
        [
            "Output includes SERP analysis for the keyword",
            "Lists top-ranking pages with titles and URLs",
            "Identifies content gaps and opportunities",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "R3", "Topic cluster research",
        "/research-topics",
        [
            "Generates topic clusters from existing content/keywords",
            "Groups related topics with hub-and-spoke structure",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "R4", "Trending topics research",
        "/research-trending",
        [
            "Identifies trending topics in your industry",
            "Provides actionable content recommendations",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "R5", "Content gap analysis",
        "/research-gaps",
        [
            "Identifies content gaps vs competitors",
            "Lists keywords competitors rank for that you don't",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "R6", "Performance-based research",
        "/research-performance",
        [
            "Uses analytics data to find content opportunities",
            "Gracefully handles missing API credentials",
        ]
    )
    if r == "quit": return finish()

    # ── Phase 2: Content Creation ──────────────────────────────────────

    header("PHASE 2: Content Creation Pipeline")

    r = ask_result(
        "W1", "Write command creates article with full pipeline",
        f'/write "{test_topic}"',
        [
            f"Creates draft file in drafts/ with date suffix",
            "Scrubber runs automatically (no Unicode watermarks in output)",
            "Content scorer runs (shows composite score in output)",
            "If score >= 70: 5 optimization agents run",
            "If score < 70: revision loop runs (max 2 iterations)",
            "Final article has: title, meta description, H2/H3 structure",
            "Article references brand voice and includes internal links",
            "Word count is substantial (1500+ words for a real topic)",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "W2", "Article command (simplified creation)",
        '/article "best podcast microphones 2025"',
        [
            "Creates article in drafts/",
            "Full pipeline runs (scrub, score, optimize)",
            "Output is a complete, publishable article",
        ]
    )
    if r == "quit": return finish()

    # ── Phase 3: Content Processing ────────────────────────────────────

    header("PHASE 3: Content Processing Commands")

    r = ask_result(
        "P1", "Scrub command is idempotent",
        f"/scrub {draft_file}",
        [
            "Reports 0 changes (since /write already scrubbed)",
            "File content is unchanged",
            "No Unicode watermark characters in output",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "P2", "Optimize command adds SEO polish",
        f"/optimize {draft_file}",
        [
            "Runs SEO optimization pass on the file",
            "Improves keyword placement, meta tags, structure",
            "Does not break existing content or introduce AI phrases",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "P3", "Analyze-existing command audits content",
        f"/analyze-existing {draft_file}",
        [
            "Generates a content health audit",
            "Includes readability scores, SEO metrics, recommendations",
            "Saves audit to audits/ directory",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "P4", "Rewrite command updates existing content",
        f'/rewrite "{test_topic}"',
        [
            "Creates updated version in rewrites/",
            "Preserves key SEO elements from original",
            "Improves content based on current best practices",
        ]
    )
    if r == "quit": return finish()

    # ── Phase 4: Analytics & Strategy ──────────────────────────────────

    header("PHASE 4: Analytics & Strategy")

    r = ask_result(
        "A1", "Performance review uses analytics data",
        "/performance-review",
        [
            "Attempts to pull GA4/GSC/DataForSEO data",
            "Gracefully handles missing credentials with clear message",
            "If credentials present: generates data-driven priorities",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "A2", "Priorities command generates content matrix",
        "/priorities",
        [
            "Creates prioritized content plan",
            "Uses opportunity scoring factors",
            "Output has priority levels: CRITICAL, HIGH, MEDIUM, LOW",
        ]
    )
    if r == "quit": return finish()

    # ── Phase 5: Landing Pages ─────────────────────────────────────────

    header("PHASE 5: Landing Page Commands")

    r = ask_result(
        "L1", "Landing page research",
        '/landing-research "podcast hosting platform"',
        [
            "Researches landing page strategy for the topic",
            "Includes CRO recommendations and competitor analysis",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "L2", "Landing page write",
        '/landing-write "podcast hosting platform"',
        [
            "Creates landing page in landing-pages/",
            "Includes above-fold content, CTAs, trust signals",
            "Runs CRO analysis automatically",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "L3", "Landing page audit",
        "/landing-audit landing-pages/podcast-hosting-platform-*.md",
        [
            "Generates CRO audit of the landing page",
            "Includes above-fold analysis, CTA effectiveness, trust signals",
            "Provides specific improvement recommendations",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "L4", "Landing page competitor analysis",
        '/landing-competitor "https://example.com/pricing"',
        [
            "Analyzes a competitor landing page",
            "Extracts CRO patterns, messaging, trust signals",
        ]
    )
    if r == "quit": return finish()

    # ── Phase 6: Publishing ────────────────────────────────────────────

    header("PHASE 6: WordPress Publishing")

    r = ask_result(
        "PB1", "Publish draft to WordPress (requires credentials)",
        f"/publish-draft {draft_file}",
        [
            "If WordPress credentials configured:",
            "  Creates draft post (never auto-publishes)",
            "  Sets Yoast SEO meta (title, description, focus keyphrase)",
            "  Returns edit URL for the draft",
            "If no credentials: clear error message about missing config",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "PB2", "Landing page publish",
        "/landing-publish landing-pages/podcast-hosting-platform-*.md",
        [
            "Publishes landing page as WordPress page (not post)",
            "Same credential requirements as publish-draft",
        ]
    )
    if r == "quit": return finish()

    # ── Phase 7: Orchestration Skills ──────────────────────────────────

    header("PHASE 7: Orchestration Skills (deterministic + LLM)")

    r = ask_result(
        "S1", "Content quality analysis skill",
        f"/content-quality-analysis {draft_file}",
        [
            "Runs content_scorer.py, readability_scorer.py, engagement_analyzer.py",
            "Shows composite score (0-100) with 5 dimension breakdown",
            "LLM interprets results with strategic recommendations",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S2", "SEO analysis skill",
        f'/seo-analysis {draft_file} --keyword "{test_keyword}"',
        [
            "Runs keyword_analyzer.py, seo_quality_rater.py, search_intent_analyzer.py",
            "Shows keyword density, TF-IDF clusters, intent classification",
            "LLM provides optimization strategy",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S3", "Content scrubbing skill",
        f"/content-scrubbing {draft_file}",
        [
            "Runs content_scrubber.py",
            "Reports Unicode removals and em-dash replacements",
            "Should be idempotent if file was already scrubbed",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S4", "SEO audit skill",
        f"/seo-audit {draft_file}",
        [
            "Runs seo_quality_rater.py deterministic scoring",
            "Provides overall SEO score (0-100) with category breakdowns",
            "LLM interprets with actionable audit findings",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S5", "Copywriting skill",
        f"/copywriting {draft_file}",
        [
            "Runs content_scorer.py for quality scoring",
            "Evaluates voice, specificity, structure, readability",
            "LLM provides copywriting improvement recommendations",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S6", "Page CRO skill",
        f"/page-cro landing-pages/podcast-hosting-platform-*.md",
        [
            "Runs cro_checker.py and landing_page_scorer.py",
            "Checks conversion optimization elements",
            "LLM provides CRO improvement recommendations",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S7", "Form CRO skill",
        f"/form-cro landing-pages/podcast-hosting-platform-*.md",
        [
            "Runs cta_analyzer.py on the page",
            "Analyzes CTA effectiveness and form optimization",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S8", "Landing page analysis skill",
        f"/landing-page-analysis landing-pages/podcast-hosting-platform-*.md",
        [
            "Runs full CRO suite: above_fold, cta, trust_signal, cro_checker, landing_page_scorer",
            "Comprehensive landing page audit with scores",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S9", "Data pipeline skill",
        "/data-pipeline",
        [
            "Runs data_aggregator.py (combines GA4 + GSC + DataForSEO)",
            "Gracefully handles missing credentials",
            "Shows available data or clear messages about missing sources",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S10", "Analytics tracking skill",
        "/analytics-tracking",
        [
            "Runs data_aggregator.py for analytics overview",
            "Gracefully degrades without API credentials",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S11", "Opportunity scoring skill",
        f'/opportunity-scoring "{test_keyword}"',
        [
            "Runs opportunity_scorer.py and competitor_gap_analyzer.py",
            "Produces priority-ranked keyword opportunities",
            "Shows score breakdown by factor",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S12", "Content comparison skill",
        f'/content-comparison {draft_file} --keyword "{test_keyword}"',
        [
            "Runs content_length_comparator.py",
            "Compares word count against SERP top 10",
            "Shows whether content is above/below benchmark",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S13", "Article planning skill",
        f'/article-planning "{test_topic}"',
        [
            "Runs article_planner.py and section_writer.py",
            "Generates article structure with sections and guidelines",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S14", "WordPress publishing skill",
        f"/wordpress-publishing {draft_file}",
        [
            "Runs wordpress_publisher.py",
            "If credentials: publishes as draft, returns edit URL",
            "If no credentials: clear error message",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "S15", "Landing performance skill",
        '/landing-performance "/pricing"',
        [
            "Runs landing_performance.py for page analytics",
            "Shows traffic, conversion, engagement metrics (if data available)",
            "Gracefully handles missing data sources",
        ]
    )
    if r == "quit": return finish()

    # ── Phase 8: Marketing Skills (non-orchestration) ──────────────────

    header("PHASE 8: Marketing Skills (LLM-only, spot check)")

    r = ask_result(
        "M1", "Email sequence skill",
        "/email-sequence",
        [
            "Generates email sequence strategy",
            "Includes subject lines, send cadence, segmentation",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "M2", "Social content skill",
        f"/social-content {draft_file}",
        [
            "Generates social media content from the article",
            "Includes posts for multiple platforms",
        ]
    )
    if r == "quit": return finish()

    r = ask_result(
        "M3", "Competitor alternatives skill",
        "/competitor-alternatives",
        [
            "Generates competitor comparison content",
            "Uses context/competitor-analysis.md for data",
        ]
    )
    if r == "quit": return finish()

    finish()


def finish():
    """Print final results and exit."""
    header("RESULTS")

    total = len(results["passed"]) + len(results["failed"]) + len(results["skipped"])

    log(f"\n  Passed:  {len(results['passed'])}/{total}")
    log(f"  Failed:  {len(results['failed'])}/{total}")
    log(f"  Skipped: {len(results['skipped'])}/{total}")

    if results["failed"]:
        log(f"\n  Failed tests:")
        for test_id, note in results["failed"]:
            log(f"    {test_id}: {note or '(no note)'}")

    if results["skipped"]:
        log(f"\n  Skipped: {', '.join(results['skipped'])}")

    log(f"\n  Completed: {datetime.now().isoformat()}")
    log(f"  Log saved: {LOG_FILE}")

    # Save structured results
    results_file = LOG_FILE.with_suffix(".json")
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": {
                "passed": results["passed"],
                "failed": [{"test": t, "note": n} for t, n in results["failed"]],
                "skipped": results["skipped"],
            },
            "totals": {
                "passed": len(results["passed"]),
                "failed": len(results["failed"]),
                "skipped": len(results["skipped"]),
                "total": total,
            }
        }, f, indent=2)
    log(f"  JSON saved: {results_file}")

    sys.exit(1 if results["failed"] else 0)


if __name__ == "__main__":
    main()
