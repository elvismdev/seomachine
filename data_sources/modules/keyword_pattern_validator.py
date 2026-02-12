"""
Keyword Pattern Validator for Programmatic SEO
Validates keyword patterns, estimates page count, and flags content quality risks.
"""
import argparse
import json
import re
import sys
from typing import Dict, Any, List, Set, Tuple
from itertools import product


class KeywordPatternValidator:
    """Validate keyword patterns for programmatic SEO"""

    # Common pattern issues
    GENERIC_MODIFIERS = {
        "best", "top", "great", "good", "awesome", "amazing",
        "ultimate", "complete", "definitive"
    }

    def validate(
        self,
        pattern: str,
        variables: Dict[str, List[str]],
        expected_search_volume_per_page: int = 0
    ) -> Dict[str, Any]:
        """
        Validate a keyword pattern for programmatic SEO

        Args:
            pattern: Template pattern with variables (e.g., "{tool} vs {competitor}")
            variables: Dictionary mapping variable names to lists of values
            expected_search_volume_per_page: Minimum expected monthly searches per page

        Returns:
            Dictionary with validation results, warnings, and recommendations
        """
        if not pattern or not pattern.strip():
            return {
                "pattern": "",
                "valid": False,
                "quality_score": 0,
                "warnings": ["Pattern cannot be empty"],
                "recommendations": [],
                "details": {}
            }

        pattern = pattern.strip()

        # Extract variables from pattern
        pattern_variables = self._extract_variables(pattern)

        # Validate variables match pattern
        validation_errors = []
        missing_vars = pattern_variables - set(variables.keys())
        extra_vars = set(variables.keys()) - pattern_variables

        if missing_vars:
            validation_errors.append(
                f"Pattern references undefined variables: {', '.join(missing_vars)}"
            )
        if extra_vars:
            validation_errors.append(
                f"Unused variables provided: {', '.join(extra_vars)}"
            )

        if validation_errors:
            return {
                "pattern": pattern,
                "valid": False,
                "quality_score": 0,
                "warnings": validation_errors,
                "recommendations": ["Fix variable mismatches before proceeding"],
                "details": {
                    "pattern_variables": list(pattern_variables),
                    "provided_variables": list(variables.keys())
                }
            }

        # Calculate page count
        total_pages = self._calculate_page_count(variables)

        # Analyze pattern quality
        quality_score, quality_details = self._analyze_quality(
            pattern, variables, total_pages
        )

        # Check for risks
        warnings = self._identify_warnings(
            pattern, variables, total_pages, expected_search_volume_per_page
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            pattern, variables, total_pages, quality_details, warnings
        )

        # Sample pages
        sample_pages = self._generate_samples(pattern, variables, count=5)

        # Analyze uniqueness
        uniqueness_score, uniqueness_details = self._analyze_uniqueness(
            pattern, variables
        )

        return {
            "pattern": pattern,
            "valid": True,
            "quality_score": round(quality_score, 1),
            "total_pages": total_pages,
            "warnings": warnings,
            "recommendations": recommendations,
            "sample_pages": sample_pages,
            "details": {
                "pattern_variables": list(pattern_variables),
                "variable_counts": {k: len(v) for k, v in variables.items()},
                "quality_breakdown": quality_details,
                "uniqueness": uniqueness_details
            }
        }

    def _extract_variables(self, pattern: str) -> Set[str]:
        """Extract variable names from pattern"""
        return set(re.findall(r'\{(\w+)\}', pattern))

    def _calculate_page_count(self, variables: Dict[str, List[str]]) -> int:
        """Calculate total number of possible pages"""
        if not variables:
            return 0
        counts = [len(values) for values in variables.values()]
        total = 1
        for count in counts:
            total *= count
        return total

    def _analyze_quality(
        self,
        pattern: str,
        variables: Dict[str, List[str]],
        total_pages: int
    ) -> Tuple[float, Dict[str, Any]]:
        """Analyze pattern quality"""
        scores = []
        details = {}

        # 1. Specificity score (30%)
        specificity_score = self._score_specificity(pattern)
        scores.append(specificity_score * 0.30)
        details["specificity"] = specificity_score

        # 2. Search likelihood score (25%)
        search_likelihood = self._score_search_likelihood(pattern)
        scores.append(search_likelihood * 0.25)
        details["search_likelihood"] = search_likelihood

        # 3. Uniqueness score (20%)
        uniqueness_score = self._score_uniqueness_potential(pattern, variables)
        scores.append(uniqueness_score * 0.20)
        details["uniqueness_potential"] = uniqueness_score

        # 4. Scale appropriateness (15%)
        scale_score = self._score_scale(total_pages)
        scores.append(scale_score * 0.15)
        details["scale_appropriateness"] = scale_score

        # 5. Pattern complexity (10%)
        complexity_score = self._score_complexity(pattern, variables)
        scores.append(complexity_score * 0.10)
        details["pattern_complexity"] = complexity_score

        overall_score = sum(scores)

        return overall_score, details

    def _score_specificity(self, pattern: str) -> float:
        """Score how specific the pattern is"""
        score = 70  # Base score

        # Bonus for specific formats
        if "vs" in pattern.lower():
            score += 15
        if "for" in pattern.lower():
            score += 10
        if "in" in pattern.lower():
            score += 10

        # Penalty for generic modifiers
        pattern_lower = pattern.lower()
        for modifier in self.GENERIC_MODIFIERS:
            if modifier in pattern_lower:
                score -= 10
                break

        return max(0, min(100, score))

    def _score_search_likelihood(self, pattern: str) -> float:
        """Score likelihood people search this pattern"""
        score = 60  # Base score

        # Common search patterns
        common_patterns = [
            r"\{[^}]+\}\s+vs\s+\{[^}]+\}",  # X vs Y
            r"\{[^}]+\}\s+for\s+\{[^}]+\}",  # X for Y
            r"\{[^}]+\}\s+in\s+\{[^}]+\}",   # X in Y
            r"how\s+to",                      # How to X
            r"best\s+\{[^}]+\}",             # Best X
        ]

        for pattern_regex in common_patterns:
            if re.search(pattern_regex, pattern, re.IGNORECASE):
                score += 20
                break

        # Penalty for unnatural phrasing
        word_count = len(pattern.split())
        if word_count > 8:
            score -= 15

        return max(0, min(100, score))

    def _score_uniqueness_potential(
        self,
        pattern: str,
        variables: Dict[str, List[str]]
    ) -> float:
        """Score how unique generated pages will be"""
        score = 70  # Base score

        # Multiple variables = more uniqueness potential
        var_count = len(variables)
        if var_count >= 3:
            score += 20
        elif var_count == 2:
            score += 10

        # Check variable diversity
        avg_values_per_var = sum(len(v) for v in variables.values()) / max(var_count, 1)
        if avg_values_per_var >= 20:
            score += 10
        elif avg_values_per_var < 5:
            score -= 20

        return max(0, min(100, score))

    def _score_scale(self, total_pages: int) -> float:
        """Score appropriateness of scale"""
        if total_pages < 10:
            return 40  # Too few pages
        elif 10 <= total_pages <= 100:
            return 100  # Ideal for testing
        elif 100 < total_pages <= 1000:
            return 90  # Good scale
        elif 1000 < total_pages <= 5000:
            return 75  # Manageable
        elif 5000 < total_pages <= 10000:
            return 60  # Large but viable
        else:
            return 30  # Too many pages

    def _score_complexity(
        self,
        pattern: str,
        variables: Dict[str, List[str]]
    ) -> float:
        """Score pattern complexity"""
        score = 70  # Base score

        # Appropriate number of variables
        var_count = len(variables)
        if var_count == 2:
            score += 20
        elif var_count == 3:
            score += 15
        elif var_count > 4:
            score -= 20

        # Pattern has static text (context)
        static_text = re.sub(r'\{[^}]+\}', '', pattern).strip()
        if len(static_text) > 5:
            score += 10

        return max(0, min(100, score))

    def _identify_warnings(
        self,
        pattern: str,
        variables: Dict[str, List[str]],
        total_pages: int,
        expected_volume: int
    ) -> List[str]:
        """Identify potential issues"""
        warnings = []

        # Scale warnings
        if total_pages < 10:
            warnings.append(
                f"Only {total_pages} pages will be generated. Consider adding more variable values."
            )
        elif total_pages > 10000:
            warnings.append(
                f"{total_pages:,} pages is very large. Consider splitting into multiple patterns or reducing variable combinations."
            )

        # Thin content risk
        if total_pages > 1000:
            warnings.append(
                "Large page count increases thin content risk. Ensure each page has substantial unique content."
            )

        # Cannibalization risk
        if len(variables) == 1:
            warnings.append(
                "Single-variable pattern may cause keyword cannibalization. Consider adding context variables."
            )

        # Generic pattern warning
        pattern_lower = pattern.lower()
        generic_count = sum(1 for word in self.GENERIC_MODIFIERS if word in pattern_lower)
        if generic_count > 0:
            warnings.append(
                "Pattern contains generic modifiers (best/top/etc). These are competitive and may not match search intent."
            )

        # Search volume warning
        if expected_volume > 0 and total_pages > 0:
            avg_volume_per_page = expected_volume / total_pages
            if avg_volume_per_page < 10:
                warnings.append(
                    f"Average search volume per page would be ~{avg_volume_per_page:.0f}/month. Pages may not attract meaningful traffic."
                )

        # Variable value warnings
        for var_name, values in variables.items():
            unique_values = set(values)
            if len(unique_values) != len(values):
                warnings.append(
                    f"Variable '{var_name}' has duplicate values. This will create duplicate pages."
                )

        return warnings

    def _generate_recommendations(
        self,
        pattern: str,
        variables: Dict[str, List[str]],
        total_pages: int,
        quality_details: Dict[str, Any],
        warnings: List[str]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Scale recommendations
        if total_pages < 50:
            recommendations.append(
                "Small page count is good for testing. Validate search demand before expanding."
            )
        elif total_pages > 5000:
            recommendations.append(
                "Consider launching in phases: start with highest-value combinations, then expand based on performance."
            )

        # Quality improvements
        if quality_details["specificity"] < 70:
            recommendations.append(
                "Increase specificity by adding context (e.g., '{tool} vs {competitor} for {use_case}')."
            )

        if quality_details["search_likelihood"] < 70:
            recommendations.append(
                "Pattern may not match natural search queries. Research actual search terms users employ."
            )

        # Uniqueness recommendations
        if quality_details["uniqueness_potential"] < 60:
            recommendations.append(
                "Add more variables or diversify variable values to ensure page uniqueness."
            )

        # Content recommendations
        if total_pages > 100:
            recommendations.append(
                "Develop content templates with dynamic sections to differentiate pages beyond just keywords."
            )
            recommendations.append(
                "Plan for unique data, examples, or comparisons for each page to avoid thin content penalties."
            )

        # SEO recommendations
        if len(variables) >= 2:
            recommendations.append(
                "Create internal linking strategy to connect related pages and distribute authority."
            )

        if not recommendations:
            recommendations.append(
                "Pattern looks viable. Validate with keyword research and create 5-10 test pages before scaling."
            )

        return recommendations

    def _generate_samples(
        self,
        pattern: str,
        variables: Dict[str, List[str]],
        count: int = 5
    ) -> List[str]:
        """Generate sample pages from pattern"""
        samples = []
        var_names = list(variables.keys())

        if not var_names:
            return []

        # Get combinations
        var_values = [variables[name] for name in var_names]
        combinations = list(product(*var_values))

        # Limit to requested count
        sample_count = min(count, len(combinations))

        for i in range(sample_count):
            combo = combinations[i]
            page = pattern
            for var_name, value in zip(var_names, combo):
                page = page.replace(f"{{{var_name}}}", value)
            samples.append(page)

        return samples

    def _analyze_uniqueness(
        self,
        pattern: str,
        variables: Dict[str, List[str]]
    ) -> Tuple[float, Dict[str, Any]]:
        """Analyze how unique generated pages will be"""
        # Calculate entropy/diversity metrics
        var_counts = [len(values) for values in variables.values()]
        avg_diversity = sum(var_counts) / max(len(var_counts), 1)

        # Calculate potential unique combinations
        total_combinations = self._calculate_page_count(variables)

        # Uniqueness score based on variable diversity
        if avg_diversity >= 20:
            uniqueness_score = 100
        elif avg_diversity >= 10:
            uniqueness_score = 80
        elif avg_diversity >= 5:
            uniqueness_score = 60
        else:
            uniqueness_score = 40

        details = {
            "variable_count": len(variables),
            "avg_values_per_variable": round(avg_diversity, 1),
            "total_combinations": total_combinations,
            "uniqueness_score": uniqueness_score
        }

        return uniqueness_score, details


def validate_pattern(**kwargs) -> Dict[str, Any]:
    """Convenience function"""
    validator = KeywordPatternValidator()
    return validator.validate(**kwargs)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Keyword Pattern Validator for Programmatic SEO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic validation
  python3 keyword_pattern_validator.py --pattern "{tool} vs {competitor}" \\
    --variables '{"tool": ["Slack", "Teams"], "competitor": ["Zoom", "Discord"]}'

  # With search volume expectations
  python3 keyword_pattern_validator.py --pattern "{service} for {industry}" \\
    --variables '{"service": ["CRM", "ERP"], "industry": ["healthcare", "finance"]}' \\
    --expected-volume 1000 --json
        """
    )

    parser.add_argument(
        "--pattern",
        required=True,
        help="Keyword pattern template (e.g., '{tool} vs {competitor}')"
    )
    parser.add_argument(
        "--variables",
        required=True,
        help="JSON object mapping variable names to value lists"
    )
    parser.add_argument(
        "--expected-volume",
        type=int,
        default=0,
        help="Expected total monthly search volume across all pages"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    try:
        # Parse variables JSON
        variables = json.loads(args.variables)

        result = validate_pattern(
            pattern=args.pattern,
            variables=variables,
            expected_search_volume_per_page=args.expected_volume
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "=" * 60)
            print("Keyword Pattern Validator")
            print("=" * 60)

            print(f"\nPattern: {result['pattern']}")
            print(f"Valid: {result['valid']}")

            if result['valid']:
                print(f"\nQuality Score: {result['quality_score']}/100")
                print(f"Total Pages: {result['total_pages']:,}")

                print(f"\nQuality Breakdown:")
                for metric, score in result['details']['quality_breakdown'].items():
                    print(f"  {metric.replace('_', ' ').title()}: {score:.1f}/100")

                if result['sample_pages']:
                    print(f"\nSample Pages:")
                    for i, sample in enumerate(result['sample_pages'], 1):
                        print(f"  {i}. {sample}")

                if result['warnings']:
                    print(f"\nWarnings:")
                    for warning in result['warnings']:
                        print(f"  ⚠ {warning}")

                if result['recommendations']:
                    print(f"\nRecommendations:")
                    for rec in result['recommendations']:
                        print(f"  • {rec}")
            else:
                print(f"\nErrors:")
                for warning in result['warnings']:
                    print(f"  ✗ {warning}")

            print()

    except json.JSONDecodeError as e:
        print(f"Error parsing variables JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
