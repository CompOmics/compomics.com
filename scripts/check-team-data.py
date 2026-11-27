"""Quarto pre-render check of team/team.yml.

Blocks the build when team.yml cannot be read, or a member has no key or name
or a duplicate key. Prints notes for members without an ORCID iD and for tool
developers without a team entry.

Run manually with: python scripts/check-team-data.py
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def fail(msg):
    print(f"\n[check-team-data] BUILD BLOCKED\n{msg}\n", file=sys.stderr)
    sys.exit(1)


try:
    team = yaml.safe_load((ROOT / "team" / "team.yml").read_text(encoding="utf-8"))
except (OSError, yaml.YAMLError) as e:
    fail(f"Cannot read team/team.yml:\n{e}")

if not isinstance(team, list):
    fail("team/team.yml must be a list of sections.")

members = []
for group in team:
    if not isinstance(group, dict) or not group.get("section") or not isinstance(group.get("members"), list):
        fail(f"Every section in team/team.yml needs `section` and `members`: {group!r:.80}")
    members += group["members"]

problems = [m for m in members if not isinstance(m, dict) or not m.get("key") or not m.get("name")]
if problems:
    fail("These team.yml entries are missing `key` or `name`:\n" + "\n".join(f"    - {m!r:.80}" for m in problems))

keys = [m["key"] for m in members]
duplicates = sorted({k for k in keys if keys.count(k) > 1})
if duplicates:
    fail(f"Duplicate keys in team/team.yml: {', '.join(duplicates)}")

no_orcid = [m["key"] for m in members if not m.get("orcid")]
if no_orcid:
    print(f"[check-team-data] note: no orcid (publications not fetched): {', '.join(no_orcid)}")

devs = []
for name in ("tools.yml", "community.yml"):
    path = ROOT / "tools" / name
    if path.exists():
        for tool in yaml.safe_load(path.read_text(encoding="utf-8")) or []:
            devs += tool.get("devs") or []
unknown = [d for d in dict.fromkeys(devs) if d not in keys]
if unknown:
    print(f"[check-team-data] note: tool developers not in team.yml (no team profile): {', '.join(unknown)}")

print(f"[check-team-data] OK: {len(members)} members.")
