"""Shared scoring utilities used across multiple analysis modules."""


def get_grade(score: float) -> str:
    """Convert a 0-100 score to a letter grade.

    Used by: seo_quality_rater, readability_scorer, cro_checker,
    above_fold_analyzer, trust_signal_analyzer, landing_page_scorer,
    content_scorer.
    """
    if score >= 90:
        return "A (Excellent)"
    elif score >= 80:
        return "B (Good)"
    elif score >= 70:
        return "C (Average)"
    elif score >= 60:
        return "D (Needs Work)"
    else:
        return "F (Poor)"
