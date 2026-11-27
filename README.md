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
research/
  index.qmd          # research overview
  research.scss      # research page styles
publications/
  index.qmd          # publications list (searchable, filterable by year)
  publications.scss  # publications page styles
  fetch_publications.py  # pulls DOIs from ORCID, enriches via CrossRef, keeps Ghent/VIB work
  extra_orcids.txt   # ORCID iDs fetched in addition to the team's
tools/
  index.qmd          # tools + community projects (searchable/filterable)
  tools.yml          # tool data, one entry per tool
  community.yml      # community project data
  tools-grid.ejs     # card template for both grids
  tools.scss         # tools page styles
team/
  index.qmd          # team cards and memberData (profiles, ORCID iDs)
  network.qmd        # affiliated members, collaborators and alumni
news/
  index.qmd          # news listing (auto-generated)
  posts/             # one .qmd per news item
assets/
  compomics.scss     # custom theme
```

The visual design system (colours, type, components, rules) is described in `DESIGN.md`.

## Team changes

Team data lives in `team/index.qmd`: one card (`data-member="<key>"`) and one `memberData` entry (`title`, `orcid`, `role`, profile text) per person, with the photo at `assets/images/<key>.jpg`. The publication fetch, author highlighting and the person filter on the publications page read the current members from `memberData`.

Adding a member:

1. Add the photo, the card in the right section and the `memberData` entry, including `orcid`.

When a member leaves:

1. Remove the card and the `memberData` entry from `team/index.qmd`.
2. Add the ORCID iD to `publications/extra_orcids.txt` to keep their publications listed.
3. Add the person to `team/network.qmd`.
4. Remove their key from the `devs` lists in `tools/tools.yml` and `tools/community.yml`, or keep it to show them as a developer without a team profile.

`scripts/check-team-data.js` runs before every render. It blocks the build when `memberData` has a syntax error or a card has no entry, and prints notes for members without an ORCID iD and for tool developers without a team profile.
