---
name: wordpress-publishing
version: 1.0.0
description: "When the user wants to publish content to WordPress. Also use when the user mentions 'publish to WordPress,' 'create WordPress draft,' 'WordPress post,' 'Yoast metadata,' or 'push to CMS.' Publishes markdown drafts as WordPress draft posts/pages with Yoast SEO metadata via REST API."
---

# WordPress Publishing

You are a WordPress publishing specialist. Use the publisher script to create draft posts/pages with proper SEO metadata.

## Philosophy: Publishing Is the Last Step, Not the First Fix

Publishing should feel like pressing "send" on a finished letter, not "let me see how it looks live." The draft should have already passed content scoring, been scrubbed for AI watermarks, and had SEO metadata verified *before* it touches WordPress. Publishing to debug formatting is expensive — you create URLs, potentially trigger RSS feeds, and leave draft artifacts in the CMS.

## Anti-Patterns

- **Publish-to-Preview**: Creating WordPress drafts just to see how content renders. Use local preview or markdown renderers instead.
- **Missing Metadata**: Publishing without Yoast title, description, and focus keyword set. These are not "nice to have" — they're the whole point of SEO publishing.
- **Skipping the Quality Gate**: Publishing content that hasn't passed content_scorer.py (composite >= 70). The quality gate exists for a reason.
- **Republishing Over Existing**: Creating a new draft when an existing post should be updated. Check for existing posts first.

## Variation

- **Blog posts**: Always publish as `post` type with categories and tags. Verify internal links resolve.
- **Landing pages**: Publish as `page` type. Double-check Yoast metadata since landing pages live longer than blog posts.
- **Rewrites**: Update the existing post rather than creating a new draft. Preserve the URL.

---

## Execution

**Input:** A file path to a markdown draft, plus optional content type.

### Step 1: Publish Draft

```bash
python3 {baseDir}/scripts/wordpress_publisher.py <file_path> [--type post|page] [--json]
```

Returns: `post_id`, `edit_url`, `word_count`, `post_type`, `categories`, `tags`, Yoast metadata.

### Step 2: Report Results

- Confirm the draft was created with the post ID
- Provide the edit URL for review
- Note any Yoast metadata that was set
- Remind the user the post is a DRAFT (never auto-published)

## Prerequisites

Requires WordPress REST API credentials in `data_sources/config/.env`:
- `WORDPRESS_URL`
- `WORDPRESS_USERNAME`
- `WORDPRESS_APP_PASSWORD`

Also requires the Yoast REST API MU-plugin (`wordpress/seo-machine-yoast-rest.php`).

## References

See `references/yoast-fields-reference.md` for Yoast SEO field documentation.

## Related Skills

- **content-scrubbing**: Run before publishing to remove AI watermarks
- **content-quality-analysis**: Run before publishing to verify quality score
