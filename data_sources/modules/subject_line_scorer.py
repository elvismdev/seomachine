"""
Email Subject Line Scorer
Scores subject lines against best practices for deliverability, engagement, and conversion.
"""
import argparse
import json
import re
import sys
from typing import Dict, Any, List, Tuple


class SubjectLineScorer:
    """Score email subject lines against best practices"""

    # Power words categorized by psychological trigger
    POWER_WORDS = {
        "urgency": [
            "now", "today", "hurry", "fast", "quick", "limited", "ending", "expires",
            "deadline", "urgent", "immediately", "last chance", "final", "hours", "minutes"
        ],
        "curiosity": [
            "secret", "discover", "reveal", "unlock", "hidden", "surprising", "shocking",
            "insider", "exclusive", "behind", "truth", "learn", "find out", "what", "how", "why"
        ],
        "benefit": [
            "free", "save", "profit", "gain", "bonus", "gift", "win", "reward", "increase",
            "improve", "boost", "grow", "maximize", "results", "success", "easy", "simple"
        ],
        "social_proof": [
            "proven", "tested", "certified", "guaranteed", "trusted", "popular", "trending",
            "bestselling", "award", "recommended", "expert", "professional"
        ]
    }

    # Spam trigger words and patterns
    SPAM_TRIGGERS = [
        "viagra", "cialis", "casino", "lottery", "winner", "congratulations",
        "act now", "click here", "buy now", "order now", "limited time",
        "guarantee", "no obligation", "risk free", "100%", "$$$",
        "dear friend", "this is not spam", "unsubscribe"
    ]

    # Personalization indicators
    PERSONALIZATION_PATTERNS = [
        r"\{{\s*\w+\s*\}}",  # {{name}}
        r"\[\s*\w+\s*\]",    # [name]
        r"%\w+%",             # %name%
    ]

    PERSONALIZATION_WORDS = [
        "you", "your", "you're", "yours"
    ]

    def score(self, subject_line: str) -> Dict[str, Any]:
        """
        Score an email subject line

        Args:
            subject_line: The subject line text to score

        Returns:
            Dictionary with overall score, component scores, and recommendations
        """
        if not subject_line or not subject_line.strip():
            return {
                "subject_line": "",
                "overall_score": 0,
                "length_score": 0,
                "power_word_score": 0,
                "clarity_score": 0,
                "personalization_score": 0,
                "spam_risk_score": 0,
                "suggestions": ["Subject line cannot be empty"],
                "alternatives": [],
                "details": {}
            }

        subject_line = subject_line.strip()
        lower_subject = subject_line.lower()

        # Calculate individual scores
        length_score, length_details = self._score_length(subject_line)
        power_score, power_details = self._score_power_words(lower_subject)
        clarity_score, clarity_details = self._score_clarity(subject_line)
        personalization_score, personalization_details = self._score_personalization(subject_line)
        spam_score, spam_details = self._score_spam_risk(subject_line)

        # Weighted overall score
        overall_score = (
            length_score * 0.25 +
            power_score * 0.20 +
            clarity_score * 0.25 +
            personalization_score * 0.15 +
            spam_score * 0.15
        )

        # Generate suggestions
        suggestions = self._generate_suggestions(
            subject_line, length_details, power_details,
            clarity_details, personalization_details, spam_details
        )

        # Generate alternatives
        alternatives = self._generate_alternatives(
            subject_line, length_details, power_details, clarity_details
        )

        return {
            "subject_line": subject_line,
            "overall_score": round(overall_score, 1),
            "length_score": round(length_score, 1),
            "power_word_score": round(power_score, 1),
            "clarity_score": round(clarity_score, 1),
            "personalization_score": round(personalization_score, 1),
            "spam_risk_score": round(spam_score, 1),
            "suggestions": suggestions,
            "alternatives": alternatives,
            "details": {
                "length": length_details,
                "power_words": power_details,
                "clarity": clarity_details,
                "personalization": personalization_details,
                "spam_risk": spam_details
            }
        }

    def _score_length(self, subject: str) -> Tuple[float, Dict[str, Any]]:
        """Score based on length (optimal: 30-50 chars for mobile)"""
        length = len(subject)
        char_count = length
        word_count = len(subject.split())

        # Optimal range: 30-50 characters
        if 30 <= length <= 50:
            score = 100
            assessment = "optimal"
        elif 20 <= length < 30:
            score = 80
            assessment = "good_short"
        elif 50 < length <= 60:
            score = 75
            assessment = "good_long"
        elif length < 20:
            score = 50
            assessment = "too_short"
        else:  # > 60
            score = 40
            assessment = "too_long"

        return score, {
            "char_count": char_count,
            "word_count": word_count,
            "assessment": assessment,
            "optimal_range": "30-50 characters"
        }

    def _score_power_words(self, lower_subject: str) -> Tuple[float, Dict[str, Any]]:
        """Score based on presence of power words"""
        found_words = {}
        total_power_words = 0

        for category, words in self.POWER_WORDS.items():
            category_words = []
            for word in words:
                if word in lower_subject:
                    category_words.append(word)
                    total_power_words += 1
            if category_words:
                found_words[category] = category_words

        # Score based on power word presence
        if total_power_words == 0:
            score = 40
            assessment = "none"
        elif total_power_words == 1:
            score = 70
            assessment = "minimal"
        elif total_power_words <= 3:
            score = 100
            assessment = "optimal"
        else:
            score = 60
            assessment = "excessive"

        return score, {
            "found_words": found_words,
            "total_count": total_power_words,
            "assessment": assessment
        }

    def _score_clarity(self, subject: str) -> Tuple[float, Dict[str, Any]]:
        """Score based on clarity (first 3 words should convey value)"""
        words = subject.split()
        if len(words) == 0:
            return 0, {"assessment": "empty", "first_three_words": ""}

        first_three = " ".join(words[:3])
        first_word = words[0].lower()

        score = 70  # Base score

        # Positive signals
        if any(word in first_three.lower() for word in ["how", "why", "what", "get", "save", "learn"]):
            score += 15

        # Question format
        if subject.strip().endswith("?"):
            score += 10

        # Starts with action verb
        action_verbs = ["get", "learn", "discover", "unlock", "boost", "save", "improve"]
        if first_word in action_verbs:
            score += 10

        # Negative signals
        if first_word in ["the", "a", "an"]:
            score -= 10

        # Contains numbers (specificity)
        if re.search(r'\d+', first_three):
            score += 5

        score = max(0, min(100, score))

        return score, {
            "first_three_words": first_three,
            "has_question": subject.strip().endswith("?"),
            "has_numbers": bool(re.search(r'\d+', subject)),
            "assessment": "clear" if score >= 70 else "unclear"
        }

    def _score_personalization(self, subject: str) -> Tuple[float, Dict[str, Any]]:
        """Score based on personalization elements"""
        lower_subject = subject.lower()
        has_merge_tag = False
        has_personal_words = False

        # Check for merge tags
        for pattern in self.PERSONALIZATION_PATTERNS:
            if re.search(pattern, subject):
                has_merge_tag = True
                break

        # Check for personal words
        words = lower_subject.split()
        personal_words_found = [w for w in self.PERSONALIZATION_WORDS if w in words]
        if personal_words_found:
            has_personal_words = True

        if has_merge_tag and has_personal_words:
            score = 100
            assessment = "highly_personalized"
        elif has_merge_tag or has_personal_words:
            score = 70
            assessment = "personalized"
        else:
            score = 40
            assessment = "generic"

        return score, {
            "has_merge_tag": has_merge_tag,
            "has_personal_words": has_personal_words,
            "personal_words_found": personal_words_found,
            "assessment": assessment
        }

    def _score_spam_risk(self, subject: str) -> Tuple[float, Dict[str, Any]]:
        """Score spam risk (higher score = lower risk)"""
        lower_subject = subject.lower()
        spam_flags = []

        # Check for spam trigger words
        for trigger in self.SPAM_TRIGGERS:
            if trigger in lower_subject:
                spam_flags.append(f"spam_word: {trigger}")

        # Check for excessive capitalization
        if len(subject) > 0:
            caps_ratio = sum(1 for c in subject if c.isupper()) / len(subject)
            if caps_ratio > 0.5:
                spam_flags.append("excessive_caps")

        # Check for excessive punctuation
        exclamation_count = subject.count("!")
        if exclamation_count > 1:
            spam_flags.append(f"excessive_exclamation: {exclamation_count}")

        # Check for all caps words
        words = subject.split()
        all_caps_words = [w for w in words if len(w) > 1 and w.isupper()]
        if all_caps_words:
            spam_flags.append(f"all_caps_words: {', '.join(all_caps_words)}")

        # Calculate score (inverse of risk)
        if len(spam_flags) == 0:
            score = 100
            risk = "low"
        elif len(spam_flags) <= 2:
            score = 60
            risk = "medium"
        else:
            score = 20
            risk = "high"

        return score, {
            "spam_flags": spam_flags,
            "flag_count": len(spam_flags),
            "risk_level": risk
        }

    def _generate_suggestions(
        self, subject: str, length_details: Dict,
        power_details: Dict, clarity_details: Dict,
        personalization_details: Dict, spam_details: Dict
    ) -> List[str]:
        """Generate actionable suggestions"""
        suggestions = []

        # Length suggestions
        if length_details["assessment"] == "too_short":
            suggestions.append(f"Subject line is only {length_details['char_count']} characters. Add more context (aim for 30-50).")
        elif length_details["assessment"] == "too_long":
            suggestions.append(f"Subject line is {length_details['char_count']} characters. Shorten to 30-50 for better mobile visibility.")

        # Power word suggestions
        if power_details["assessment"] == "none":
            suggestions.append("Add power words to increase engagement (e.g., 'discover', 'exclusive', 'quick').")
        elif power_details["assessment"] == "excessive":
            suggestions.append("Too many power words can seem spammy. Limit to 1-3 per subject line.")

        # Clarity suggestions
        if not clarity_details["has_numbers"]:
            suggestions.append("Consider adding numbers for specificity (e.g., '5 tips' instead of 'tips').")
        if clarity_details["assessment"] == "unclear":
            suggestions.append("Lead with value or an action verb to clarify the benefit.")

        # Personalization suggestions
        if personalization_details["assessment"] == "generic":
            suggestions.append("Add personalization with 'you/your' or merge tags like {{name}}.")

        # Spam suggestions
        if spam_details["risk_level"] in ["medium", "high"]:
            for flag in spam_details["spam_flags"]:
                if "excessive_caps" in flag:
                    suggestions.append("Reduce ALL CAPS to avoid spam filters.")
                elif "excessive_exclamation" in flag:
                    suggestions.append("Limit exclamation marks to one (or none).")
                elif "spam_word" in flag:
                    word = flag.split(": ")[1]
                    suggestions.append(f"Remove spam trigger word: '{word}'")

        if not suggestions:
            suggestions.append("Subject line looks strong. Test variations to optimize performance.")

        return suggestions

    def _generate_alternatives(
        self, subject: str, length_details: Dict,
        power_details: Dict, clarity_details: Dict
    ) -> List[str]:
        """Generate alternative subject line variants"""
        alternatives = []

        # Variant 1: Add curiosity/question
        if not subject.endswith("?"):
            question_variant = self._make_question_variant(subject)
            if question_variant:
                alternatives.append(question_variant)

        # Variant 2: Add personalization
        if "you" not in subject.lower():
            personal_variant = self._make_personal_variant(subject)
            if personal_variant:
                alternatives.append(personal_variant)

        # Variant 3: Add specificity/numbers
        if not re.search(r'\d+', subject):
            numeric_variant = self._make_numeric_variant(subject)
            if numeric_variant:
                alternatives.append(numeric_variant)

        return alternatives[:3]  # Return max 3

    def _make_question_variant(self, subject: str) -> str:
        """Convert to question format"""
        lower = subject.lower()
        if lower.startswith("how to"):
            return subject.replace("How to", "How can you", 1).replace("how to", "how can you", 1) + "?"
        elif "learn" in lower:
            return subject.replace("Learn", "Want to learn", 1).replace("learn", "want to learn", 1) + "?"
        else:
            return f"Want to know: {subject}?"

    def _make_personal_variant(self, subject: str) -> str:
        """Add personalization"""
        if subject[0].isupper():
            return f"Your {subject[0].lower()}{subject[1:]}"
        return f"Your {subject}"

    def _make_numeric_variant(self, subject: str) -> str:
        """Add numbers for specificity"""
        lower = subject.lower()
        if "tips" in lower or "ways" in lower or "ideas" in lower:
            return re.sub(
                r'\b(tips|ways|ideas|strategies)\b',
                r'5 \1',
                subject,
                flags=re.IGNORECASE,
                count=1
            )
        return f"5 insights: {subject}"


def score_subject_line(subject_line: str) -> Dict[str, Any]:
    """Convenience function"""
    scorer = SubjectLineScorer()
    return scorer.score(subject_line)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Email Subject Line Scorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 subject_line_scorer.py "Quick tips to boost your SEO"
  python3 subject_line_scorer.py "{{name}}, your exclusive offer expires today" --json
        """
    )

    parser.add_argument(
        "subject_line",
        nargs="?",
        help="Subject line to score"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    # Handle interactive mode if no subject provided
    if not args.subject_line:
        if sys.stdin.isatty():
            print("Enter subject line to score:")
            subject_line = input("> ").strip()
        else:
            subject_line = sys.stdin.read().strip()
    else:
        subject_line = args.subject_line

    try:
        result = score_subject_line(subject_line)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "=" * 60)
            print("Email Subject Line Scorer")
            print("=" * 60)
            print(f"\nSubject: {result['subject_line']}")
            print(f"\nOverall Score: {result['overall_score']}/100")

            print(f"\nComponent Scores:")
            print(f"  Length: {result['length_score']}/100 ({result['details']['length']['char_count']} chars)")
            print(f"  Power Words: {result['power_word_score']}/100")
            print(f"  Clarity: {result['clarity_score']}/100")
            print(f"  Personalization: {result['personalization_score']}/100")
            print(f"  Spam Risk: {result['spam_risk_score']}/100 ({result['details']['spam_risk']['risk_level']} risk)")

            if result['suggestions']:
                print(f"\nSuggestions:")
                for suggestion in result['suggestions']:
                    print(f"  • {suggestion}")

            if result['alternatives']:
                print(f"\nAlternative Variants:")
                for i, alt in enumerate(result['alternatives'], 1):
                    print(f"  {i}. {alt}")

            print()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
