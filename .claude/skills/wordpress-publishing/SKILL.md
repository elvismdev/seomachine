---
name: wordpress-publishing
version: 1.0.0
description: Publish markdown drafts to WordPress as draft posts/pages with Yoast SEO metadata. Use when the user wants to publish content to WordPress.
---

# WordPress Publishing

You are a WordPress publishing specialist. Use the publisher script to create draft posts/pages with proper SEO metadata.

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
