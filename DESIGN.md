---
name: CompOmics
description: Website of the CompOmics computational proteomics group at Ghent University and VIB.
colors:
  logo-blue: "#276ba6"
  logo-red: "#c4362a"
  paper: "#f3f6f9"
  card-white: "#ffffff"
  panel-blue-grey: "#e7edf3"
  line: "#d9e1e9"
  line-soft: "#e6ecf1"
  ink: "#1c232b"
  ink-soft: "#36404b"
  muted: "#5b6673"
  navy-900: "#0f1a26"
  navy-800: "#18232f"
  navy-700: "#233142"
  on-navy: "#e8edf2"
  on-navy-muted: "#9fb0c2"
  line-prediction: "#276ba6"
  line-identification: "#d63729"
  line-metaproteomics: "#1f8a70"
  line-fair: "#c08a1e"
  line-reprocessing: "#6b4fa0"
  line-neutral: "#6b7785"
  line-identification-text: "#c4362a"
  line-metaproteomics-text: "#1b7a63"
  line-fair-text: "#8a6210"
  line-neutral-text: "#5b6673"
typography:
  hero:
    fontFamily: "Bricolage Grotesque, system-ui, sans-serif"
    fontSize: "clamp(4rem, 14vw, 9rem)"
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: "-0.015em"
  display:
    fontFamily: "Bricolage Grotesque, system-ui, sans-serif"
    fontSize: "clamp(2.5rem, 5vw, 3.5rem)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Bricolage Grotesque, system-ui, sans-serif"
    fontSize: "1.75rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Bricolage Grotesque, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 700
    lineHeight: 1.25
  body:
    fontFamily: "Source Sans 3, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  lead:
    fontFamily: "Source Sans 3, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Source Sans 3, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.4
  data:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
rounded:
  badge: "0.4rem"
  control: "0.5rem"
  card: "0.6rem"
  panel: "1rem"
  round: "50%"
components:
  button-primary:
    backgroundColor: "{colors.logo-blue}"
    textColor: "{colors.card-white}"
    rounded: "{rounded.control}"
    padding: "0.85rem 1.5rem"
  chip:
    backgroundColor: "{colors.card-white}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.control}"
    padding: "0.4rem 0.9rem"
  chip-active:
    backgroundColor: "{colors.logo-blue}"
    textColor: "{colors.card-white}"
    rounded: "{rounded.control}"
  input-search:
    backgroundColor: "{colors.card-white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0.6rem 2.2rem 0.6rem 2.4rem"
  badge-line:
    textColor: "{colors.line-identification-text}"
    rounded: "{rounded.badge}"
    padding: "0.2rem 0.55rem"
  card:
    backgroundColor: "{colors.card-white}"
    rounded: "{rounded.card}"
    padding: "1.35rem 1.4rem 1.1rem"
  panel-navy:
    backgroundColor: "{colors.navy-800}"
    textColor: "{colors.on-navy}"
    rounded: "{rounded.panel}"
  footer:
    backgroundColor: "{colors.navy-900}"
    textColor: "{colors.on-navy-muted}"
---

# Design System: CompOmics

## Overview

**Creative North Star: "The group photo and the spectrum"**

The site has two signatures, and everything else stays quiet around them. The first is the group itself: the homepage is a sequence of real group photos under an ink navy overlay, from a posed picture to a silly one, and the team page opens on the same photo. The second is the language of mass spectrometry: the research page draws the five research lines as the b-ion ladder of the peptide AIMFR, and those five colours are the only categorical colours on the site.

Content pages are calm and readable: a pale logo-blue page, white cards, dark blue-grey text, Bricolage Grotesque headings and Source Sans 3 body text. The homepage and every dark surface use the same ink navy, so the dark homepage and the light content pages read as one site. Colour carries meaning (a research line, a link, an active state) and is never decoration.

The site deliberately avoids the common generated-site look: no small uppercase labels above headings, no gradient text, no glow, no cards that lift on hover, no monospace used as a "technical" costume.

**Key Characteristics:**
- Real photos of the group as the main imagery; no stock or illustration.
- Five research-line colours used consistently on every page.
- One ink navy for every dark surface: homepage, team panel, footer, dark mode.
- Sentence case everywhere; headings carry themselves without labels.
- Flat surfaces with a light border; shadows only where a surface sits over a photo or opens on demand.

## Colors

A pale blue-grey page with white cards, logo blue for actions, and five research-line colours that always mean the same thing.

### Primary
- **Logo Blue** (`logo-blue`): links, buttons, focus rings, the active filter chip, and the analyte prediction line. In dark mode it lifts to `#6aaee6`.

### Secondary
- **Logo Red** (`logo-red`, fill `#d63729`): the identification line, and hover or active states. Not used as decoration. In dark mode `#ef7a6d`.

### Tertiary: research lines
Each line has a fill colour (bars, spectrum peaks, dots, card top borders, badge tints) and a text colour that passes 4.5:1 on the page and on white cards. In dark mode both use one lifted value.
- **Analyte prediction** (`line-prediction`): tool category Prediction.
- **Identification** (`line-identification`, text `line-identification-text`): tool category Identification.
- **Metaproteomics** (`line-metaproteomics`, text `line-metaproteomics-text`): tool category Metaproteomics.
- **FAIR & AI-ready data** (`line-fair`, text `line-fair-text`): tool category Support.
- **Reprocessing** (`line-reprocessing`): tool category Interpretation.
- **Neutral** (`line-neutral`, text `line-neutral-text`): community projects and courses that span several lines.

Dark-mode values: prediction `#6aaee6`, identification `#ef7a6d`, metaproteomics `#4cc3a2`, FAIR `#e0b04d`, reprocessing `#a78bdb`, neutral `#8e9cab`.

### Neutral
- **Paper** (`paper`): page background in light mode.
- **Card White** (`card-white`): cards, inputs, chips, panels.
- **Panel Blue-Grey** (`panel-blue-grey`): pressed or deeper surfaces, tag backgrounds such as "Preprint".
- **Line** (`line`, `line-soft`): borders and dividers.
- **Ink** (`ink`): headings and strong text. **Ink Soft** (`ink-soft`): body text. **Muted** (`muted`): secondary text, at least 5:1 on the page.
- **Ink Navy** (`navy-900`, `navy-800`, `navy-700`): every dark surface. 900 is the base (homepage, footer, dark-mode page), 800 is a raised surface on dark (homepage tiles and location card, team profile panel, dark-mode cards), 700 is a border on dark. Text on navy uses `on-navy` and `on-navy-muted`.

### Named Rules
**The One Meaning Rule.** A research-line colour only ever marks that research line. Links and buttons use logo blue, states use logo red, everything else is neutral.

**The One Navy Rule.** Every dark surface uses the navy scale. No near-black (`#111`, `#0f1217`) or separate dark blues.

**The Token Rule.** Colours come from the SCSS tokens in `assets/compomics-light.scss` and `assets/compomics-dark.scss` (`$rl-*`, `$navy-*`, `$paper*`, `$ink*`) or their CSS custom properties (`--rl-*`, `--navy-*`). No new hex values in page files.

## Typography

**Display Font:** Bricolage Grotesque (with system-ui)
**Body Font:** Source Sans 3 (with system-ui)
**Data Font:** JetBrains Mono, only for code and measured values such as m/z in the research spectrum

**Character:** a confident grotesque for headings next to a plain, highly readable humanist sans for text.

### Hierarchy
- **Hero** (700, `clamp(4rem, 14vw, 9rem)`, 0.95): the CompOmics word mark on the homepage only.
- **Display** (700, `clamp(2.5rem, 5vw, 3.5rem)`, 1.05): page titles (Research, Tools, Team, Publications, Tutorials) and homepage scene headlines (larger clamp).
- **Headline** (700, 1.75rem, 1.15): section titles, year headings, team section headings.
- **Title** (700, 1.25rem, 1.25): tool names, card titles; tutorial titles at 1.375rem weight 600.
- **Lead** (400, 1.25rem, 1.6): the intro paragraph under a page title, max 60 to 68ch.
- **Body** (400, 1rem, 1.6 to 1.7): text, max about 72ch.
- **Label** (600, 0.875rem or 0.8125rem): counts, dates, badges, chips, meta. Sentence case.

The type scale is fixed in `assets/compomics.scss` (`$fs-xs` 0.8125rem to `$fs-display`); use those tokens for every font size.

### Named Rules
**The No Label Rule.** No small uppercase or letter-spaced label above a heading, and no uppercase labels at all. The heading says what the section is.

**The Honest Mono Rule.** Monospace is for code and measured data only, never for counts, chips or captions.

## Layout

Content pages use the Quarto content column (about 850px of text width) with full-width page headers: title, a lead paragraph, then the toolbar or content. The homepage is a stack of full-viewport scenes (`min-height: 100vh`, content max 1120px) over fixed photo frames.

Grids: tool cards in 3 columns, 2 below 900px, 1 below 576px; team portraits in 5 columns from 860px. Lists (publications, tutorials) are full-width rows separated by thin lines; tutorials use a narrow date column (9.5rem) on the left.

Text is left-aligned; never justified. More space above a heading than below it.

## Elevation & Depth

Content pages are flat: white surfaces on the pale page, separated by a 1px line. Shadows appear in three places only.

### Shadow Vocabulary
- **Card rest** (`box-shadow: 0 1px 2px rgba(20, 40, 60, 0.05)`): tool cards at rest.
- **Card hover** (`box-shadow: 0 8px 24px rgba(20, 40, 60, 0.10)`): tool cards on hover, with a border tint; no movement.
- **Over photo** (`box-shadow: 0 14px 36px rgba(0, 0, 0, 0.35)`): homepage tiles and location card, which sit on the photo and use a translucent Navy 800 with a backdrop blur for legibility.
- **Panel** (`box-shadow: 0 16px 40px rgba(0, 0, 0, 0.22)`): the team profile panel.

### Named Rules
**The Still Card Rule.** Cards never move on hover. Hover changes border colour, shadow or text colour only.

## Shapes

Gently rounded rectangles with a clear step per size: badges `0.4rem`, buttons, inputs and chips `0.5rem`, cards and tiles `0.6rem` (tool cards square their top corners under the 3px colour bar), panels `1rem`. Portraits and avatars are circles. No pill-shaped buttons.

## Components

### Buttons
- **Shape:** gently rounded (`0.5rem`).
- **Primary:** logo blue fill, white text, weight 700, `0.85rem 1.5rem`. On the homepage they sit over the photo.
- **Hover / Focus:** slightly darker fill, no lift; focus shows a 2px logo-blue ring.
- **Outline:** "Get directions" uses a 1px border and text in the on-navy red.

### Chips (filters)
- **Style:** white background, 1px line border, label type; tool category chips carry a dot in the line colour.
- **State:** the active chip is filled with the line's text colour (logo blue for "All") with white text, or navy text in dark mode.

### Badges and tags
- **Research-line badge:** 12% tint of the line colour, 1px border at 35%, text in the line text colour, sentence case.
- **Neutral tag:** "Preprint" uses `panel-blue-grey` with muted text.

### Cards / Containers
- **Corner Style:** `0.6rem`, top corners `0.25rem` under a 3px top border in the research-line colour.
- **Background:** card white; Navy 800 in dark mode.
- **Shadow Strategy:** see Card rest and Card hover.
- **Internal Padding:** `1.35rem 1.4rem 1.1rem`; a footer row separated by a soft line holds avatars and links.

### Inputs / Fields
- **Style:** white field, 1px line border, `0.5rem` radius, search icon on the left, clear button on the right.
- **Focus:** logo-blue border and a 3px logo-blue ring at 18%.

### Navigation
- **Navbar:** logo left, Source Sans 3 links at 1rem; active and hover in logo blue. Transparent over the homepage photo.
- **Footer:** Navy 900 band with the white logo, the address and the GitHub link.

### Research spectrum (signature)
The five research lines drawn as a mass spectrum with an intensity axis, an m/z axis, grey minor peaks and five coloured peaks at the b-ion masses of AIMFR, with the residue ladder annotated in monospace. The peaks rise once on page load; reduced motion shows them at full height. Section headings on the research page repeat a single peak in the line colour.

### Homepage scenes (signature)
Full-viewport scenes over fixed group photos that cross-fade on scroll from posed to silly. Text sits on the photo in white with a soft text shadow; tiles and the location card are translucent Navy 800.

## Do's and Don'ts

### Do:
- **Do** use the `$rl-*` tokens or `--rl-*` variables whenever something belongs to a research line, and the `-text` variant for text.
- **Do** use the navy scale for any new dark surface.
- **Do** keep headings in Bricolage Grotesque at weight 700 and text in Source Sans 3.
- **Do** write labels, badges and headings in sentence case.
- **Do** check contrast: 4.5:1 for text, 3:1 for large text and graphics.
- **Do** respect `prefers-reduced-motion` for any animation.
- **Do** use real photos of the group and real tool logos.

### Don't:
- **Don't** add small uppercase labels above headings, or uppercase labels anywhere.
- **Don't** use gradient text, glows, or decorative gradient washes.
- **Don't** make cards lift or slide on hover, or animate cards in one by one.
- **Don't** add a coloured side border thicker than 1px to cards, list items or callouts. Exceptions: the 2px rule on block quotes and the grey step rail on the course page, which marks a real sequence.
- **Don't** use monospace for anything that is not code or measured data.
- **Don't** introduce a new accent colour or a second dark colour outside the tokens.
- **Don't** use warm cream backgrounds, pill buttons or em dashes in copy.
