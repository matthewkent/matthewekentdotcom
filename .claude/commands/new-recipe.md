Transform pasted or provided recipe text into the canonical Markdown format used by this site, then save it to the recipes/ directory.

## Canonical format

```markdown
---
title: Recipe Title
sources:
  - https://... (optional)
yield: How much it makes (optional)
---

## Ingredients

### Component Name (use ### sub-headers only if there are multiple distinct components)
- ingredient

## Method

1. Step one.
2. Step two.

## Notes

Optional tips, variations, or notes. (Omit this section entirely if there's nothing to say.)
```

## Instructions

1. If the user has not yet pasted the recipe text, ask them to paste it now.

2. Parse the raw text and extract:
   - **Title** — the recipe name
   - **Sources** — any "adapted from", "via", or credit lines. Use a `sources` list of URLs. Omit the field entirely if there's no source. Multiple sources are supported.
   - **Yield/servings** — how much it makes (optional)
   - **Ingredients** — group into `###` sub-sections only if the recipe has clearly distinct components (e.g. crust + filling, or brine + glaze). Use a flat list if it's a single component.
   - **Method steps** — number them. If the original has prose paragraphs rather than numbered steps, break them into logical steps.
   - **Notes** — any tips, variations, or commentary. Omit the section if there are none.

3. Infer a kebab-case filename from the title (e.g. "Chocolate Chip Cookies" → `chocolate-chip-cookies.md`).

4. Show the user the complete formatted Markdown and the proposed filename. Ask them to confirm before saving.

5. Once confirmed, save the file to `recipes/<filename>.md`.

**Important:** Do not invent, add, or change any ingredients or steps. If the source text is ambiguous — missing quantities, unclear steps, uncertain section breaks — ask the user to clarify rather than guessing.
