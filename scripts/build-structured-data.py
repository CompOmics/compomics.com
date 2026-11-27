"""Quarto pre-render step: write schema.org JSON-LD for the home, team and tools
pages to _jsonld/, from team/team.yml and tools/tools.yml.

Tools with `comingSoon: true` are left out.
"""

import json
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_jsonld"

site = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))["website"]
SITE = site["site-url"].rstrip("/")
ORG_ID = f"{SITE}/#organization"
ORG_REF = {"@type": "ResearchOrganization", "@id": ORG_ID, "name": "CompOmics"}


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1])


def slug(name):
    """Anchor id of a tool card; matches tools/tools-grid.ejs."""
    return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", name).lower()).strip("-")


def absolute(url, page_dir):
    if re.match(r"https?://", url):
        return url
    parts = [p for p in f"{page_dir}/{url}".split("/") if p not in ("", ".")]
    path = []
    for p in parts:
        if p == "..":
            path.pop()
        else:
            path.append(p)
    return f"{SITE}/{'/'.join(path)}"


def write(name, data):
    OUT.mkdir(exist_ok=True)
    body = json.dumps({"@context": "https://schema.org", **data}, ensure_ascii=False, indent=2)
    body = body.replace("</", "<\\/")
    (OUT / f"{name}.html").write_text(
        f'<script type="application/ld+json">\n{body}\n</script>\n', encoding="utf-8"
    )


# ── Home: the organisation ──────────────────────────────────────────────────
write("home", {
    **ORG_REF,
    "url": f"{SITE}/",
    "logo": f"{SITE}/assets/images/CompOmics_logo.png",
    "description": front_matter(ROOT / "index.qmd")["description"],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Technologiepark 75",
        "postalCode": "9052",
        "addressLocality": "Gent-Zwijnaarde",
        "addressCountry": "BE",
    },
    "parentOrganization": {
        "@type": "ResearchOrganization",
        "name": "VIB-UGent Center for Medical Biotechnology",
        "sameAs": "https://ror.org/04hbttm44",
        "parentOrganization": [
            {"@type": "CollegeOrUniversity", "name": "Ghent University", "sameAs": "https://ror.org/00cv9y106"},
            {"@type": "ResearchOrganization", "name": "VIB", "sameAs": "https://ror.org/03xrhmk39"},
        ],
    },
    "sameAs": ["https://github.com/compomics"],
})

# ── Team: one Person per member ─────────────────────────────────────────────
team = yaml.safe_load((ROOT / "team" / "team.yml").read_text(encoding="utf-8"))
people = {}
for group in team:
    for m in group["members"]:
        person = {
            "@type": "Person",
            "@id": f"{SITE}/team/#member-{m['key']}",
            "name": m["name"],
        }
        if m.get("orcid"):
            person["sameAs"] = f"https://orcid.org/{m['orcid']}"
        people[m["key"]] = person

write("team", {"@graph": [
    {
        **people[m["key"]],
        "jobTitle": m.get("role"),
        "image": f"{SITE}/assets/images/{m['key']}.jpg",
        "memberOf": ORG_REF,
    }
    for group in team for m in group["members"]
]})

# ── Tools: one SoftwareApplication per released tool ────────────────────────
tools = yaml.safe_load((ROOT / "tools" / "tools.yml").read_text(encoding="utf-8"))
apps = []
for t in tools:
    if t.get("comingSoon"):
        continue
    links = {k: absolute(v, "tools") for k, v in (t.get("links") or {}).items()}
    url = links.get("web") or links.get("docs") or links.get("github")
    app = {
        "@type": ["SoftwareApplication", "SoftwareSourceCode"] if "github" in links else "SoftwareApplication",
        "@id": f"{SITE}/tools/#{slug(t['name'])}",
        "name": t["name"],
        "description": t["desc"],
        "url": url,
        "isAccessibleForFree": True,
        "publisher": ORG_REF,
    }
    if "github" in links:
        app["codeRepository"] = links["github"]
    same = [links[k] for k in ("github", "pypi", "bioconda", "web", "api") if k in links and links[k] != url]
    if same:
        app["sameAs"] = same
    help_ = [links[k] for k in ("docs", "tutorial") if k in links]
    if help_:
        app["softwareHelp"] = [{"@type": "CreativeWork", "url": h} for h in help_]
    if "paper" in links:
        app["citation"] = {"@type": "ScholarlyArticle", "url": links["paper"]}
    authors = [people[d] for d in t.get("devs") or [] if d in people]
    if authors:
        app["author"] = authors
    apps.append(app)

write("tools", {"@graph": apps})
