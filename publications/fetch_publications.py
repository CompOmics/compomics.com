"""
Fetch publications for CompOmics group members from ORCID and enrich via CrossRef.

A publication is kept when at least one author has a Ghent University or VIB
affiliation in CrossRef or OpenAlex, when neither source has affiliation data
for it, or when an iD in AFFILIATION_EXEMPT_ORCIDS is a group author.
Records that OpenAlex types as supplementary materials are skipped.

Dependencies: requests
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

TEAM_DIR = Path(__file__).parent.parent / "team"
EXTRA_ORCIDS_FILE = Path(__file__).parent / "extra_orcids.txt"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "publications.json"

ORCID_API = "https://pub.orcid.org/v3.0/{orcid}/works"
ORCID_PERSON_API = "https://pub.orcid.org/v3.0/{orcid}/person"
CROSSREF_API = "https://api.crossref.org/works/{doi}"
OPENALEX_API = "https://api.openalex.org/works"
CROSSREF_HEADERS = {
    "User-Agent": "CompOmics-website/1.0 (mailto:lennart.martens@UGent.be)"
}


ORCID_FIELD = re.compile(r"""\borcid:\s*['"](\d{4}-\d{4}-\d{4}-\d{3}[\dX])['"]""")
ORCID_LINE = re.compile(r"^\s*(\d{4}-\d{4}-\d{4}-\d{3}[\dX])\b")

LOCAL_AFFILIATION = re.compile(r"\b(ghent|gent|ugent|vib)\b|flanders institute for biotechnology", re.I)
# Group authors whose publications skip the affiliation check.
AFFILIATION_EXEMPT_ORCIDS = {"0000-0003-4277-658X"}  # Lennart Martens


def read_orcid_ids() -> list[str]:
    """Read the `orcid:` fields of the `memberData` entries in team/index.qmd,
    followed by the iDs listed in publications/extra_orcids.txt."""
    text = (TEAM_DIR / "index.qmd").read_text(encoding="utf-8")
    orcids = ORCID_FIELD.findall(text)
    if EXTRA_ORCIDS_FILE.exists():
        for line in EXTRA_ORCIDS_FILE.read_text(encoding="utf-8").splitlines():
            match = ORCID_LINE.match(line)
            if match:
                orcids.append(match.group(1))
    return list(dict.fromkeys(orcids))


def fetch_dois_for_orcid(orcid: str) -> list[str]:
    url = ORCID_API.format(orcid=orcid)
    resp = requests.get(url, headers={"Accept": "application/json"}, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    dois = []
    for group in data.get("group", []):
        for ext_id in group.get("external-ids", {}).get("external-id", []):
            if ext_id.get("external-id-type") == "doi":
                # some ORCID records hold stray text before the DOI, e.g. "34\n10.1186/..."
                tokens = ext_id.get("external-id-value", "").split()
                if tokens:
                    dois.append(tokens[-1].lower())
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
    affiliations = [aff.get("name", "") for a in authors_raw for aff in a.get("affiliation", [])]
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
        "affiliations": [aff for aff in affiliations if aff],
    }


def fetch_openalex_works(dois: list[str]) -> dict[str, dict]:
    """Map each DOI found in OpenAlex to its work `type` and the institution
    names and raw affiliation strings of all its authors (`affiliations`)."""
    result = {}
    for i in range(0, len(dois), 50):
        chunk = dois[i : i + 50]
        params = {"filter": "doi:" + "|".join(chunk), "per-page": 50, "select": "doi,type,authorships"}
        try:
            resp = requests.get(OPENALEX_API, params=params, headers=CROSSREF_HEADERS, timeout=60)
            resp.raise_for_status()
        except Exception as exc:
            print(f"  OpenAlex error for DOIs {i + 1}-{i + len(chunk)}: {exc}")
            continue
        for work in resp.json().get("results", []):
            doi = (work.get("doi") or "").lower().removeprefix("https://doi.org/")
            affiliations = []
            for authorship in work.get("authorships", []):
                affiliations += [inst.get("display_name") or "" for inst in authorship.get("institutions", [])]
                affiliations += authorship.get("raw_affiliation_strings") or []
            result[doi] = {"type": work.get("type"), "affiliations": [aff for aff in affiliations if aff]}
        time.sleep(0.2)
    return result


def passes_affiliation_check(affiliations: list[str], group_orcids: list[str]) -> bool:
    """True when an author has a local affiliation, when no affiliation data
    exists, or when a group author is in AFFILIATION_EXEMPT_ORCIDS."""
    if AFFILIATION_EXEMPT_ORCIDS.intersection(group_orcids) or not affiliations:
        return True
    return any(LOCAL_AFFILIATION.search(aff) for aff in affiliations)

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
        raise SystemExit("No ORCID IDs found. Add orcid: 'xxxx-xxxx-xxxx-xxxx' to the memberData entries in team/index.qmd.")

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
    print(f"\nFetching work types and affiliations for {len(all_dois)} DOI(s) from OpenAlex...")
    openalex_works = fetch_openalex_works(all_dois)

    print(f"\n{len(all_dois)} unique DOI(s) to resolve via CrossRef...")
    publications = []
    for i, doi in enumerate(all_dois, 1):
        print(f"  [{i}/{len(all_dois)}] {doi}")
        # OpenAlex lists a versioned DOI ("<doi>.v1") under its base DOI.
        openalex = openalex_works.get(doi) or openalex_works.get(re.sub(r"\.v\d+$", "", doi), {})
        if openalex.get("type") == "supplementary-materials":
            print("    Skipping: supplementary materials")
            continue
        meta = fetch_crossref_metadata(doi)
        if meta and meta.get("title") and meta.get("year"):
            group_orcids = validate_group_orcids(meta, doi_to_orcids[doi], orcid_names)
            if not group_orcids:
                print(f"    Skipping: no candidate ORCID matches actual authors ({meta['title']!r})")
                time.sleep(0.1)
                continue
            meta["affiliations"] += openalex.get("affiliations", [])
            meta["group_orcids"] = group_orcids
            publications.append(meta)
        time.sleep(0.1)

    before = len(publications)
    publications = deduplicate(publications)
    print(f"Deduplication removed {before - len(publications)} near-duplicate(s)")

    # Filter after deduplication so a preprint does not replace a dropped journal version.
    kept = []
    for pub in publications:
        if passes_affiliation_check(pub.pop("affiliations"), pub["group_orcids"]):
            kept.append(pub)
        else:
            print(f"  Skipping: no Ghent University or VIB affiliation ({pub['title']!r})")
    print(f"Affiliation check removed {len(publications) - len(kept)} publication(s)")
    publications = kept

    publications.sort(key=lambda p: (-(p["year"] or 0), p.get("title", "")))

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(publications, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(publications)} publications to {OUTPUT_FILE}")




if __name__ == "__main__":
    main()
