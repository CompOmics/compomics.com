"""
Fetch publications for CompOmics group members from ORCID and enrich via CrossRef.

Dependencies: requests, PyYAML
Usage: python publications/fetch_publications.py
Output: data/publications.json

To update the publications page:
  1. python publications/fetch_publications.py
  2. quarto render publications/index.qmd
"""

import json
import re
import string
import time
from difflib import SequenceMatcher
from pathlib import Path

import requests
import yaml

TEAM_DIR = Path(__file__).parent.parent / "team"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "publications.json"

ORCID_API = "https://pub.orcid.org/v3.0/{orcid}/works"
ORCID_PERSON_API = "https://pub.orcid.org/v3.0/{orcid}/person"
CROSSREF_API = "https://api.crossref.org/works/{doi}"
CROSSREF_HEADERS = {
    "User-Agent": "CompOmics-website/1.0 (mailto:lennart.martens@UGent.be)"
}


def read_orcid_ids() -> list[str]:
    orcids = []
    for path in TEAM_DIR.glob("*.qmd"):
        if path.name == "index.qmd":
            continue
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?\n)---", text, re.DOTALL)
        if not match:
            continue
        fm = yaml.safe_load(match.group(1))
        orcid = (fm or {}).get("orcid", "")
        if orcid:
            orcid = orcid.strip().rstrip("/")
            orcid = orcid.split("orcid.org/")[-1]
            if orcid:
                orcids.append(orcid)
    return orcids


def fetch_dois_for_orcid(orcid: str) -> list[str]:
    url = ORCID_API.format(orcid=orcid)
    resp = requests.get(url, headers={"Accept": "application/json"}, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    dois = []
    for group in data.get("group", []):
        for ext_id in group.get("external-ids", {}).get("external-id", []):
            if ext_id.get("external-id-type") == "doi":
                doi = ext_id.get("external-id-value", "").strip().lower()
                if doi:
                    dois.append(doi)
                break
    return dois


def fetch_orcid_name(orcid: str) -> str:
    """Fetch the display name associated with an ORCID iD."""
    url = ORCID_PERSON_API.format(orcid=orcid)
    resp = requests.get(url, headers={"Accept": "application/json"}, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    name = data.get("name") or {}
    given = (name.get("given-names") or {}).get("value", "")
    family = (name.get("family-name") or {}).get("value", "")
    return f"{given} {family}".strip()


def normalize_orcid(raw: str) -> str:
    """Extract bare XXXX-XXXX-XXXX-XXXX from a full ORCID URL or bare ID."""
    return raw.strip().rstrip("/").split("orcid.org/")[-1]


def fetch_crossref_metadata(doi: str) -> dict | None:
    url = CROSSREF_API.format(doi=doi)
    try:
        resp = requests.get(url, headers=CROSSREF_HEADERS, timeout=20)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        msg = resp.json().get("message", {})
    except Exception as exc:
        print(f"  CrossRef error for {doi}: {exc}")
        return None

    titles = msg.get("title", [])
    title = titles[0] if titles else ""

    authors_raw = msg.get("author", [])
    authors = []
    author_orcids = []
    for a in authors_raw:
        given = a.get("given", "")
        family = a.get("family", "")
        name = f"{given} {family}".strip() if given else family
        if name:
            authors.append(name)
            raw_orcid = a.get("ORCID", "")
            author_orcids.append(normalize_orcid(raw_orcid) if raw_orcid else None)

    container = msg.get("container-title", [])
    journal = container[0] if container else ""

    pub_date = msg.get("published", msg.get("published-print", msg.get("published-online", {})))
    date_parts = pub_date.get("date-parts", [[None]])
    year = date_parts[0][0] if date_parts and date_parts[0] else None

    return {
        "doi": doi,
        "title": title,
        "authors": authors,
        "author_orcids": author_orcids,
        "journal": journal,
        "year": year,
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "pages": msg.get("page", ""),
    }

NAME_SIMILARITY_THRESHOLD = 0.7

# CrossRef author metadata is sometimes truncated or omits collaborator-style
# bylines (e.g. HUPO working group credits), which would otherwise cause
# validate_group_orcids() to falsely drop a genuine group co-authorship.
# Pairs below were manually confirmed against PubMed/publisher pages, and are
# trusted even though the CrossRef author list doesn't show the match.
MANUALLY_VERIFIED_ORCID_DOIS = {
    ("0000-0003-4277-658X", "10.1002/pmic.201190020"),  # Quality Control in Proteomics
    ("0000-0003-4277-658X", "10.1038/nmeth.1333"),  # HUPO test sample study (collaborator credit)
    ("0000-0003-4277-658X", "10.1093/nar/gkj138"),  # PRIDE (CrossRef only lists first author)
}


def _name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def validate_group_orcids(meta: dict, candidate_orcids: set[str], orcid_names: dict[str, str]) -> list[str]:
    """Keep only ORCIDs of members who genuinely appear in the paper's author list.

    An ORCID's presence in a member's ORCID "works" record is not proof they
    authored the paper: ORCID entries can be added by automated sources (e.g.
    Europe PMC) and can be wrong. Cross-check against the paper's real authors
    (from CrossRef) either by matching author_orcids directly or by fuzzy name match.
    """
    author_orcids = set(meta.get("author_orcids") or [])
    authors = meta.get("authors") or []
    doi = meta.get("doi", "")
    valid = []
    for orcid in candidate_orcids:
        if orcid in author_orcids or (orcid, doi) in MANUALLY_VERIFIED_ORCID_DOIS:
            valid.append(orcid)
            continue
        name = orcid_names.get(orcid, "")
        if name and any(_name_similarity(name, author) >= NAME_SIMILARITY_THRESHOLD for author in authors):
            valid.append(orcid)
    return sorted(valid)


SIMILARITY_THRESHOLD = 0.9


def _normalize_title(title: str) -> str:
    """Lowercase and strip punctuation for similarity comparison."""
    return title.lower().translate(str.maketrans("", "", string.punctuation)).split()


def _title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _normalize_title(a), _normalize_title(b)).ratio()


def _publication_quality(pub: dict) -> int:
    """Higher is better: prefer published articles over preprints."""
    score = 0
    if pub.get("journal"):
        score += 2
    if pub.get("volume"):
        score += 1
    if pub.get("pages"):
        score += 1
    return score


def deduplicate(publications: list[dict]) -> list[dict]:
    """Remove near-duplicate entries (preprint + published version of same paper).
    When two titles exceed the similarity threshold, the higher-quality entry is kept."""
    kept: list[dict] = []
    for pub in publications:
        matched = False
        for i, existing in enumerate(kept):
            if _title_similarity(pub["title"], existing["title"]) >= SIMILARITY_THRESHOLD:
                # Replace the existing entry if the new one is higher quality
                if _publication_quality(pub) > _publication_quality(existing):
                    # Merge group_orcids so neither loses authorship tracking
                    merged = sorted(set(pub.get("group_orcids", [])) | set(existing.get("group_orcids", [])))
                    pub["group_orcids"] = merged
                    kept[i] = pub
                matched = True
                break
        if not matched:
            kept.append(pub)
    return kept


def main():
    orcids = read_orcid_ids()
    if not orcids:
        print('No ORCID IDs found. Add orcid: "xxxx-xxxx-xxxx-xxxx" to team/*.qmd files.')
        return

    print(f"Found {len(orcids)} ORCID ID(s): {', '.join(orcids)}")

    doi_to_orcids: dict[str, set[str]] = {}
    for orcid in orcids:
        print(f"Fetching works for ORCID {orcid}...")
        try:
            dois = fetch_dois_for_orcid(orcid)
            print(f"  {len(dois)} DOI(s) found")
            for doi in dois:
                doi_to_orcids.setdefault(doi, set()).add(orcid)
        except Exception as exc:
            print(f"  Error: {exc}")
        time.sleep(0.2)

    print("Fetching member names for authorship validation...")
    orcid_names = {}
    for orcid in orcids:
        try:
            orcid_names[orcid] = fetch_orcid_name(orcid)
        except Exception as exc:
            print(f"  Error fetching name for {orcid}: {exc}")
        time.sleep(0.2)

    all_dois = sorted(doi_to_orcids)
    print(f"\n{len(all_dois)} unique DOI(s) to resolve via CrossRef...")
    publications = []
    for i, doi in enumerate(all_dois, 1):
        print(f"  [{i}/{len(all_dois)}] {doi}")
        meta = fetch_crossref_metadata(doi)
        if meta and meta.get("title") and meta.get("year"):
            group_orcids = validate_group_orcids(meta, doi_to_orcids[doi], orcid_names)
            if not group_orcids:
                print(f"    Skipping: no candidate ORCID matches actual authors ({meta['title']!r})")
                time.sleep(0.1)
                continue
            meta["group_orcids"] = group_orcids
            publications.append(meta)
        time.sleep(0.1)

    before = len(publications)
    publications = deduplicate(publications)
    print(f"Deduplication removed {before - len(publications)} near-duplicate(s)")

    publications.sort(key=lambda p: (-(p["year"] or 0), p.get("title", "")))

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(publications, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(publications)} publications to {OUTPUT_FILE}")




if __name__ == "__main__":
    main()
