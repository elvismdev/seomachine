# Yoast SEO REST API Fields

## Fields Set by Publisher

| Field | Description | Source |
|-------|-------------|--------|
| `yoast_wpseo_title` | SEO title (meta title) | From draft frontmatter `meta_title` |
| `yoast_wpseo_metadesc` | Meta description | From draft frontmatter `meta_description` |
| `yoast_wpseo_focuskw` | Focus keyphrase | From draft frontmatter `target_keyword` |

## Draft Frontmatter Format

The publisher expects markdown files with YAML-style frontmatter:

```markdown
**Meta Title**: Your SEO Title Here
**Meta Description**: Your meta description here (150-160 chars)
**Target Keyword**: your target keyword

---

# Article Title

Content starts here...
```

## WordPress Block Format

Articles should use WordPress block format (HTML comments in Markdown) for proper rendering:
- `<!-- wp:heading -->` for headings
- `<!-- wp:paragraph -->` for paragraphs
- `<!-- wp:list -->` for lists

## Important Notes

- Posts are ALWAYS created as drafts (status: "draft")
- Never auto-publish — always review in WordPress editor first
- Categories and tags are assigned based on content analysis
