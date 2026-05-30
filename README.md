# matthewekent.com

Personal baking recipe website, served as static HTML from S3 at [matthewekent.com](https://matthewekent.com).

## Setup

```bash
uv sync
```

## Commands

**Generate site**
```bash
uv run python tool.py generate
```
Builds HTML and CSS from `recipes/` into `output/`.

**Preview locally**
```bash
uv run python -m http.server 8000 --directory output
```
Then open [http://localhost:8000](http://localhost:8000).

**Publish to S3**
```bash
uv run python tool.py publish
```
Uploads `output/` to S3 and invalidates the CloudFront cache. Run `generate` first.

**Add a recipe**
```
/new-recipe
```
Paste unformatted recipe text and Claude will convert it to the canonical Markdown format.
