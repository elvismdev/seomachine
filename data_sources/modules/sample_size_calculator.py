"""
Sample Size Calculator for A/B Testing
Calculates required sample size, test duration, and statistical parameters.
"""
import argparse
import json
import math
import sys
from typing import Dict, Any, Optional


class SampleSizeCalculator:
    """Calculate sample sizes for A/B tests"""

    def calculate(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        confidence_level: float = 0.95,
        power: float = 0.80,
        daily_traffic: Optional[int] = None,
        variants: int = 2
    ) -> Dict[str, Any]:
        """
        Calculate required sample size per variant

        Args:
            baseline_rate: Current conversion rate (e.g., 0.03 for 3%)
            minimum_detectable_effect: Relative change to detect (e.g., 0.10 for 10% lift)
            confidence_level: Statistical confidence (default: 0.95)
            power: Statistical power (default: 0.80)
            daily_traffic: Daily traffic for duration calculation
            variants: Number of variants including control (default: 2)

        Returns:
            Dictionary with sample size calculation results
        """
        # Validate inputs
        if not 0 < baseline_rate < 1:
            raise ValueError("Baseline rate must be between 0 and 1")
        if minimum_detectable_effect <= 0:
            raise ValueError("Minimum detectable effect must be positive")
        if not 0.8 <= confidence_level < 1:
            raise ValueError("Confidence level typically between 0.8 and 0.99")
        if not 0.5 <= power < 1:
            raise ValueError("Power typically between 0.5 and 0.99")
        if variants < 2:
            raise ValueError("Must have at least 2 variants (control + treatment)")

        alpha = 1 - confidence_level

        # Z-scores for common values
        z_alpha = self._z_score(1 - alpha / 2)
        z_beta = self._z_score(power)

        # Calculate effect size
        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_detectable_effect)

        # Ensure p2 is valid probability
        if p2 >= 1:
            p2 = 0.99

        # Sample size formula for two-proportion z-test
        p_bar = (p1 + p2) / 2
        numerator = (
            z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) +
            z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
        ) ** 2
        denominator = (p2 - p1) ** 2

        sample_per_variant = math.ceil(numerator / denominator)
        total_sample = sample_per_variant * variants

        # Calculate duration if daily traffic provided
        duration_days = None
        traffic_per_variant = None
        if daily_traffic and daily_traffic > 0:
            traffic_per_variant = daily_traffic // variants
            duration_days = math.ceil(sample_per_variant / traffic_per_variant)

        result = {
            "baseline_rate": round(baseline_rate, 4),
            "minimum_detectable_effect": f"{round(minimum_detectable_effect * 100, 1)}%",
            "expected_new_rate": round(p2, 4),
            "absolute_lift": round(p2 - p1, 4),
            "confidence_level": f"{round(confidence_level * 100)}%",
            "statistical_power": f"{round(power * 100)}%",
            "variants": variants,
            "sample_per_variant": sample_per_variant,
            "total_sample_needed": total_sample,
            "daily_traffic": daily_traffic,
            "traffic_per_variant_per_day": traffic_per_variant,
            "duration_days": duration_days,
            "parameters": {
                "alpha": round(alpha, 4),
                "z_alpha": round(z_alpha, 4),
                "z_beta": round(z_beta, 4)
            },
            "recommendations": []
        }

        # Add recommendations
        recommendations = []

        if duration_days:
            if duration_days < 7:
                recommendations.append(
                    "Test duration is very short. Consider a smaller MDE for more reliable results."
                )
            elif duration_days > 90:
                recommendations.append(
                    f"Test would take {duration_days} days. Consider increasing MDE or focusing on higher-traffic pages."
                )

            if duration_days < 14:
                recommendations.append(
                    "Run for at least 14 days to account for weekly patterns regardless of sample size."
                )

            if duration_days >= 7 and duration_days <= 28:
                recommendations.append(
                    "Good test duration. Balances statistical validity with practical timeline."
                )

        if minimum_detectable_effect < 0.05:
            recommendations.append(
                "MDE below 5% requires very large samples. Ensure this precision is necessary."
            )
        elif minimum_detectable_effect >= 0.20:
            recommendations.append(
                "MDE of 20%+ is quite large. You might be able to detect smaller improvements with a reasonable sample size."
            )

        if baseline_rate < 0.01:
            recommendations.append(
                "Low baseline rate means high variance. Consider a larger MDE or longer test."
            )

        if baseline_rate > 0.30:
            recommendations.append(
                "High baseline rate. Improvements may be harder to achieve but easier to detect."
            )

        if variants > 2:
            recommendations.append(
                f"Testing {variants} variants increases required sample size. Consider prioritizing top 2-3 variants."
            )

        if sample_per_variant < 100:
            recommendations.append(
                "Very small sample size. Results may be noisy even if statistically significant."
            )

        result["recommendations"] = recommendations

        return result

    def _z_score(self, p: float) -> float:
        """
        Approximate z-score using rational approximation (Abramowitz and Stegun)

        Args:
            p: Probability (cumulative distribution function value)

        Returns:
            Z-score corresponding to probability p
        """
        if p <= 0 or p >= 1:
            return 0
        if p < 0.5:
            return -self._z_score(1 - p)

        t = math.sqrt(-2 * math.log(1 - p))
        c0, c1, c2 = 2.515517, 0.802853, 0.010328
        d1, d2, d3 = 1.432788, 0.189269, 0.001308

        return t - (c0 + c1 * t + c2 * t * t) / (
            1 + d1 * t + d2 * t * t + d3 * t * t * t
        )


def calculate_sample_size(**kwargs) -> Dict[str, Any]:
    """Convenience function for sample size calculation"""
    calculator = SampleSizeCalculator()
    return calculator.calculate(**kwargs)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="A/B Test Sample Size Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate sample size for 3% baseline, 10% relative lift
  python3 sample_size_calculator.py --baseline 0.03 --mde 0.10

  # Include daily traffic to estimate duration
  python3 sample_size_calculator.py --baseline 0.05 --mde 0.15 --traffic 1000

  # Test with 3 variants (A/B/C)
  python3 sample_size_calculator.py --baseline 0.02 --mde 0.20 --variants 3 --json
        """
    )

    parser.add_argument(
        "--baseline",
        type=float,
        required=True,
        help="Current conversion rate (e.g., 0.03 for 3%%)"
    )
    parser.add_argument(
        "--mde",
        type=float,
        required=True,
        help="Minimum detectable effect as relative change (e.g., 0.10 for 10%% lift)"
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.95,
        help="Confidence level (default: 0.95)"
    )
    parser.add_argument(
        "--power",
        type=float,
        default=0.80,
        help="Statistical power (default: 0.80)"
    )
    parser.add_argument(
        "--traffic",
        type=int,
        default=None,
        help="Daily traffic to calculate test duration"
    )
    parser.add_argument(
        "--variants",
        type=int,
        default=2,
        help="Number of variants including control (default: 2)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    try:
        result = calculate_sample_size(
            baseline_rate=args.baseline,
            minimum_detectable_effect=args.mde,
            confidence_level=args.confidence,
            power=args.power,
            daily_traffic=args.traffic,
            variants=args.variants
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "=" * 50)
            print("A/B Test Sample Size Calculator")
            print("=" * 50)
            print(f"\nTest Parameters:")
            print(f"  Baseline rate: {result['baseline_rate']}")
            print(f"  Minimum detectable effect: {result['minimum_detectable_effect']}")
            print(f"  Expected new rate: {result['expected_new_rate']}")
            print(f"  Absolute lift: {result['absolute_lift']}")
            print(f"  Confidence level: {result['confidence_level']}")
            print(f"  Statistical power: {result['statistical_power']}")
            print(f"  Number of variants: {result['variants']}")

            print(f"\nSample Size Requirements:")
            print(f"  Per variant: {result['sample_per_variant']:,}")
            print(f"  Total needed: {result['total_sample_needed']:,}")

            if result['duration_days']:
                print(f"\nTimeline:")
                print(f"  Daily traffic: {result['daily_traffic']:,}")
                print(f"  Traffic per variant/day: {result['traffic_per_variant_per_day']:,}")
                print(f"  Estimated duration: {result['duration_days']} days")

            if result['recommendations']:
                print(f"\nRecommendations:")
                for rec in result['recommendations']:
                    print(f"  • {rec}")

            print()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
