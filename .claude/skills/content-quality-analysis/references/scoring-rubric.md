# Content Quality Scoring Rubric

## Composite Score (0-100, Threshold: 70)

### Dimension Weights

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Humanity/Voice | 30% | Human tone, personality, conversational devices, absence of AI phrases |
| Specificity | 25% | Concrete examples, real numbers, named entities vs vague generalizations |
| Structure Balance | 20% | Prose-to-list ratio (target 40-70% prose, not all bullet points) |
| SEO Compliance | 15% | Keyword density, meta tags, heading structure, internal links |
| Readability | 10% | Flesch Reading Ease (target 60-70), sentence rhythm, paragraph length |

### Score Interpretation

| Range | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Exceptional — ready for publication |
| 80-89 | B | Strong — minor polish recommended |
| 70-79 | C | Passing — meets quality threshold |
| 60-69 | D | Below threshold — needs revision |
| <60 | F | Significant issues — major rewrite needed |

### Humanity/Voice (30%)

**Penalized patterns (AI phrases):**
- "In today's digital/modern/fast-paced..."
- "When it comes to..."
- "It's important to note/remember/understand..."
- "Let's dive in/into..."
- "Furthermore", "Moreover", "Additionally"
- "In order to", "Due to the fact that"
- "At the end of the day"

**Rewarded patterns:**
- Contractions (you're, it's, don't)
- Questions to the reader
- First/second person pronouns
- Specific opinions and personality
- Informal transitions

### Specificity (25%)

**Strong signals:**
- Named companies, people, products
- Specific numbers and percentages
- Real-world examples with context
- "For example," followed by a concrete case

**Weak signals:**
- Vague quantifiers ("many", "several", "various")
- Generic advice without examples
- Abstract claims without evidence

### Structure Balance (20%)

**Target:** 40-70% prose ratio (not all lists, not a wall of text)

**Scoring:**
- Prose ratio 50-65%: Full points
- Prose ratio 40-50% or 65-70%: Minor deduction
- Prose ratio <40% (too many lists): Major deduction
- Prose ratio >70% (wall of text): Moderate deduction

### Readability (10%)

**Targets:**
- Flesch Reading Ease: 60-70 (professional but accessible)
- Flesch-Kincaid Grade: 8-10 (high school level)
- Passive voice: <15% of sentences
- Average sentence length: 15-20 words
- Paragraph length: 2-4 sentences

**Sentence rhythm:**
- Statistical standard deviation of sentence lengths should show variety
- Monotonous sections (many same-length sentences in a row) are penalized

## Pipeline Context

This scorer is the quality gate in the `/write` command pipeline:
1. Article saved to `drafts/`
2. `/scrub` removes AI watermarks
3. `content_scorer.py` evaluates quality (this step)
4. If < 70: auto-revise top fixes, re-score (max 2 iterations)
5. If still < 70 after 2 iterations: route to `review-required/`
6. If >= 70: run 5 optimization agents
