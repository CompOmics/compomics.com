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
  index.qmd          # team page
  team.yml           # team data (profiles, ORCID iDs), one entry per person
  team-grid.ejs      # card and profile template
  network.qmd        # affiliated members, collaborators and alumni
news/
  index.qmd          # news listing (auto-generated)
  posts/             # one .qmd per news item
assets/
  compomics.scss     # custom theme
```

The visual design system (colours, type, components, rules) is described in `DESIGN.md`.

Structured data (schema.org JSON-LD) for the home, team and tools pages is generated from `team/team.yml` and `tools/tools.yml` by `scripts/build-structured-data.py` on every render. `scripts/build-llms-txt.py` writes `llms.txt` from the same data, the page descriptions and the tutorial posts. Tools marked `comingSoon` are left out of both.

## Team changes

Team data lives in `team/team.yml`: one entry per person (`key`, `name`, `orcid`, `role`, profile text) in its section, with the photo at `assets/images/<key>.jpg`. The publication fetch, author highlighting and the person filter on the publications page read the current members from `team.yml`.

Adding a member:

1. Add the photo and the entry in the right section of `team/team.yml`, including `orcid`.

When a member leaves:

1. Remove the entry from `team/team.yml`.
2. Add the ORCID iD to `publications/extra_orcids.txt` to keep their publications listed.
3. Add the person to `team/network.qmd`.
4. Remove their key from the `devs` lists in `tools/tools.yml` and `tools/community.yml`, or keep it to show them as a developer without a team profile.

`scripts/check-team-data.py` runs before every render. It blocks the build when `team.yml` cannot be read or an entry has no `key` or `name`, and prints notes for members without an ORCID iD and for tool developers without a team profile.
