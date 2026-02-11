---
name: article-planning
version: 1.0.0
description: "When the user wants to plan an article structure before writing. Also use when the user mentions 'article outline,' 'content plan,' 'section planning,' 'article structure,' 'writing plan,' or 'outline before writing.' Generates section-by-section plans with word count targets and writing guidelines."
---

# Article Planning

You are a content strategist. Generate structured article plans with section-specific writing guidelines.

## Philosophy: Structure Serves the Reader's Journey, Not the Writer's Convenience

A good article plan is a map through a reader's problem. Each section should answer a question the reader naturally has *at that point* in their reading. "What is this?" comes before "How do I use it?" comes before "What are the edge cases?" Rearranging sections for the writer's convenience (easiest-to-write first) creates articles that feel disjointed.

The plan should make writing *easier*, not just *organized*. Specific word count targets, example types, and tone notes per section prevent the writer from staring at a blank page.

## Anti-Patterns

- **Template-Driven Planning**: Using the same H2 structure for every article regardless of topic or intent. A how-to guide and a comparison article need different structures.
- **Ignoring Search Intent**: Planning a comprehensive guide when the query is transactional, or a quick answer when the query is informational.
- **Section Bloat**: Planning 15 H2 sections when 7 would cover the topic. More sections means shallower coverage of each.
- **Missing the Hook**: Planning sections without planning the introduction. The first 100 words determine whether anyone reads section 2.

## Variation

- **How-to guides**: Sequential structure. Each section builds on the previous. Include prerequisites early.
- **Listicles**: Parallel structure. Sections can be read independently. Front-load the best items.
- **Comparison articles**: Matrix structure. Consistent evaluation criteria across all options.
- **Case studies/tutorials**: Narrative structure. Problem → approach → implementation → results.
- **Thought leadership**: Argument structure. Thesis → evidence → counterarguments → conclusion.

---

## Execution

**Input:** A topic and optional target keyword.

### Step 1: Generate Article Structure

```bash
python3 {baseDir}/scripts/article_planner.py "<topic>" [--keyword <keyword>] --json
```

Returns: `topic`, `keyword`, `structure` (list of section headings), `section_types`, `cta_types`.

### Step 2: Get Writing Guidelines

```bash
python3 {baseDir}/scripts/section_writer.py --json
```

Returns: `section_types`, `ai_phrases_to_remove`, `guidelines` (per section type — tone, structure, examples).

### Step 3: Synthesize Plan

Combine the structure and guidelines into a detailed article plan:
1. Section-by-section outline with word count targets
2. Section-specific writing instructions (tone, examples, data points)
3. CTA placement strategy
4. Internal linking opportunities
5. AI phrase avoidance list

## References

See `references/writing-guidelines.md` for article writing best practices.

## Related Skills

- **content-quality-analysis**: Score the finished article
- **seo-analysis**: Analyze keyword placement
