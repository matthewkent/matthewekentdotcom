#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

import boto3
import click
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).parent
RECIPES_DIR = REPO_ROOT / "recipes"
TEMPLATES_DIR = REPO_ROOT / "templates"
STATIC_DIR = REPO_ROOT / "static"
OUTPUT_DIR = REPO_ROOT / "output"
S3_BUCKET = "www.matthewekent.com"
CLOUDFRONT_DISTRIBUTION_ID = "E361KYL0SNEF3J"

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css",
}


def load_recipes():
    recipes = []
    for path in sorted(RECIPES_DIR.glob("*.md")):
        post = frontmatter.load(path)
        recipes.append({
            "slug": path.stem,
            "title": post["title"],
            "sources": (
                post.get("sources")
                or ([{"name": post["source"], "url": post.get("source_url")}] if post.get("source") else [])
            ),
            "yield": post.get("yield"),
            "content_html": markdown.markdown(post.content, extensions=["extra"]),
            "url": f"/recipes/{path.stem}/",
        })
    return sorted(recipes, key=lambda r: r["title"].lower())


@click.group()
def cli():
    pass


@cli.command()
def generate():
    """Generate static site assets into output/."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()
    (OUTPUT_DIR / "recipes").mkdir()

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
    recipes = load_recipes()

    recipe_tmpl = env.get_template("recipe.html")
    for recipe in recipes:
        dest = OUTPUT_DIR / "recipes" / recipe["slug"]
        dest.mkdir()
        (dest / "index.html").write_text(recipe_tmpl.render(recipe=recipe), encoding="utf-8")

    index_tmpl = env.get_template("index.html")
    (OUTPUT_DIR / "index.html").write_text(index_tmpl.render(recipes=recipes), encoding="utf-8")

    shutil.copy(STATIC_DIR / "style.css", OUTPUT_DIR / "style.css")

    click.echo(f"Generated {len(recipes)} recipes → output/")


@cli.command()
def publish():
    """Publish generated assets to S3."""
    if not OUTPUT_DIR.exists() or not any(OUTPUT_DIR.iterdir()):
        raise click.ClickException("output/ is empty — run 'generate' first")

    s3 = boto3.client("s3")
    count = 0

    for local_path in OUTPUT_DIR.rglob("*"):
        if not local_path.is_file():
            continue
        key = str(local_path.relative_to(OUTPUT_DIR))
        content_type = CONTENT_TYPES.get(local_path.suffix, "application/octet-stream")
        s3.upload_file(
            str(local_path),
            S3_BUCKET,
            key,
            ExtraArgs={
                "ContentType": content_type,
                "CacheControl": "max-age=3600",
            },
        )
        click.echo(f"  {key}")
        count += 1

    click.echo(f"Published {count} files to s3://{S3_BUCKET}")

    cf = boto3.client("cloudfront")
    cf.create_invalidation(
        DistributionId=CLOUDFRONT_DISTRIBUTION_ID,
        InvalidationBatch={
            "Paths": {"Quantity": 1, "Items": ["/*"]},
            "CallerReference": str(count),
        },
    )
    click.echo("Invalidated CloudFront cache")


if __name__ == "__main__":
    cli()
