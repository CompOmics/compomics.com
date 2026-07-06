
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