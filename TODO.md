
# To Do

- [x] Add tutorials button to landing page (Robbe)
- [x] Extend research vision text, remove tool names (Arthur)
- [x] Add Ralf to Rusteomics (Robbe)
- [x] Add MZPEAK to community projects (Robbe)
- [x] Add E. coli atlas to tools or community projects (ask Caro) (Robbe)
- [] Let everyone provide comments on their team entry (ask next week)
- [x] Weekly updated author lists (Arthur) -> montly updates now?
- [x] Eugene Kolker???? (Robbe)
- [x] Former collaborators and alumni (Xuxa)
- [x] Check colorscheme linkedin embedding (Robbe)
- [x] Update tutorial links with tools (Robbe)
- [x] Maybe change jupyter notebook color? (Robbe)
- [x] Website deployment issue to have a python environment (Arthur)
- [x] Unify the overall view of each separate part of the website. 


## Deploy to www.compomics.com (after site checked)
- [] Add root `CNAME` file containing `www.compomics.com` + list it under project resources in `_quarto.yml`
- [] Set `site-url: https://www.compomics.com` in `_quarto.yml`
- [] GitHub repo Settings → Pages: set custom domain `www.compomics.com`, then enable Enforce HTTPS
- [] DNS at registrar: `www` CNAME → `compomics.github.io`; apex `compomics.com` → GitHub Pages A records (185.199.108-111.153)
- [] Flip DNS last (cuts over from old site, no fast rollback)

## Todo after deployment

- [] Modernise the classic "Bioinformatics for Proteomics" tutorial (`tutorials/posts/2026-06-01-bioinformatics-for-proteomics.qmd`). Ported as-is with 2014-era materials linked from Google Drive; deprecation warning kept in place until done. TODO: replace deprecated PRIDE XML with mzIdentML/mzTab (needs editing the module 3 slide decks, not just the page text); refresh slides/screenshots to current tool UIs; rehost slides + exercise resources off Google Drive; decide combined page vs per-module split; optionally write the missing MS1 (4.3) and targeted (4.4) quantification sections; update the functional-analysis module (module 2 pins no tools). Tool versions already bumped (PeptideShaker 3.0.11, SearchGUI 4.3.15). (Arthur)