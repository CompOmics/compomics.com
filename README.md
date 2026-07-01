# CompOmics Website

Source for the CompOmics research group website, built with [Quarto](https://quarto.org).

## Local preview

```bash
quarto preview
```

## Build

```bash
quarto render
```

Output is written to `_site/`.

## Deployment

Pushes to `main` automatically deploy to GitHub Pages via the workflow in `.github/workflows/deploy.yml`.

In your GitHub repo settings: **Settings → Pages → Source → GitHub Actions**.

## Structure

```
_quarto.yml          # site config, navbar, theme
index.qmd            # home page
publications.qmd     # publications list
research/
  index.qmd          # research overview
  research.scss      # research page styles
tools/
  index.qmd          # tools listing (auto-generated)
  example-tool.qmd   # one file per tool
team/
  index.qmd          # team listing (auto-generated)
  jane-doe.qmd       # one file per person
news/
  index.qmd          # news listing (auto-generated)
  posts/             # one .qmd per news item
assets/
  compomics.scss     # custom theme
```
