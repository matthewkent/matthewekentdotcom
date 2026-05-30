# matthewekent.com

A static recipe website served from S3 at `www.matthewekent.com`. Built with a Python CLI tool that generates HTML from Markdown recipes.

## CLI tool

```bash
uv sync                          # install dependencies (first time)
uv run python tool.py generate   # build output/ from recipes/
uv run python tool.py publish    # upload output/ to S3
```

Always run `generate` before `publish`. Inspect `output/` locally before publishing.

## Recipes

Recipe source files live in `recipes/*.md`. Each filename is the URL slug and should be stable (changing the filename changes the URL).

**Frontmatter fields:**
- `title` (required)
- `source` (optional) — attribution
- `yield` (optional) — e.g. "1 loaf", "8 pieces"

**Required sections:** `## Ingredients`, `## Method`
**Optional section:** `## Notes`

Use `###` sub-headers under Ingredients only for recipes with multiple distinct components (crust + filling, brine + glaze, etc.).

Use `/new-recipe` to create a new recipe from pasted text.

## Generated output

`output/` is gitignored — it's always regeneratable by running `generate`. Do not commit it.

## S3

Bucket: `www.matthewekent.com`
Credentials: standard boto3 chain (`~/.aws/credentials` or environment variables)

## Design

No JavaScript. Text and CSS only. The stylesheet is `static/style.css` and templates are in `templates/`.
