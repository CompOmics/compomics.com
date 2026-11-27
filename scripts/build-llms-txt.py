"""Quarto post-render step: write llms.txt (https://llmstxt.org) to the site
output, from page front matter, team/team.yml, tools/tools.yml,
tools/community.yml and the tutorial posts.

Tools with `comingSoon: true` are left out.
"""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
config = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))
SITE = config["website"]["site-url"].rstrip("/")
OUT = ROOT / config["project"].get("output-dir", "_site")

PAGES = ["research", "tools", "team", "publications", "tutorials"]


def front_matter(path):
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or []


def tool_line(t):
    links = t.get("links") or {}
    repo = links.get("github") if re.match(r"https://github\.com/[^/]+/[^/]+", links.get("github", "")) else None
    url = repo or links.get("docs") or links.get("web") or links.get("github")
    if not url:
        return None
    return f"- [{t['name']}]({url}): {t['desc']}"


team = load(ROOT / "team" / "team.yml")
leaders = [m["name"] for g in team if g["section"] == "Group leader" for m in g["members"]]

lines = [
    "# CompOmics",
    "",
    f"> {front_matter(ROOT / 'index.qmd')['description']}",
    "",
    "CompOmics is the computational proteomics group of the VIB-UGent Center for Medical "
    "Biotechnology, part of Ghent University and VIB, in Ghent, Belgium."
    + (f" Group leader: {', '.join(leaders)}." if leaders else ""),
    "",
    "## Pages",
    "",
]
for page in PAGES:
    fm = front_matter(ROOT / page / "index.qmd")
    lines.append(f"- [{fm['title']}]({SITE}/{page}/): {fm.get('description', '')}".rstrip(": "))

lines += ["", "## Tools", ""]
lines += [l for t in load(ROOT / "tools" / "tools.yml") if not t.get("comingSoon") and (l := tool_line(t))]

lines += ["", "## Community projects", "", "Community initiatives CompOmics contributes to.", ""]
lines += [l for t in load(ROOT / "tools" / "community.yml") if (l := tool_line(t))]

lines += ["", "## Tutorials", ""]
for post in sorted((ROOT / "tutorials" / "posts").glob("*.qmd")):
    fm = front_matter(post)
    if fm.get("draft"):
        continue
    url = f"{SITE}/tutorials/posts/{post.stem}.html"
    lines.append(f"- [{fm['title']}]({url}): {fm.get('description', '')}".rstrip(": "))

OUT.mkdir(exist_ok=True)
(OUT / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
