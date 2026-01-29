#!/usr/bin/env python3
"""
Fetch missing DOI links for publications.json using Crossref, then update the JSON in-place.

Usage:
  python tools/fetch_dois.py
  # or specify a custom file:
  python tools/fetch_dois.py assets/data/publications.json

Notes:
- Requires internet access and the `requests` package:
    pip install requests
- Crossref etiquette suggests including a User-Agent with contact info.
  Please edit USER_AGENT below with your email.
"""
from __future__ import annotations
import json
import re
import sys
import time
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List

try:
    import requests
except ImportError:
    print("Missing dependency: requests. Install with: pip install requests")
    raise

USER_AGENT = "theory-chem-group-site/1.0 (mailto:YOUR_EMAIL_HERE)"

TITLE_RE = re.compile(r".*,\s*(.*?)\.\s*[A-Z]")  # greedy up to the title's ending period


def extract_title_and_first_author(citation: str) -> Tuple[str, str]:
    """Best-effort extraction from the citation string in hudp.txt style."""
    c = re.sub(r"^\s*\d+\.\s*", "", citation).strip()
    first_author = c.split(",")[0].strip()
    last_name = (first_author.split()[-1] if first_author else "").strip(".")
    m = TITLE_RE.match(c)
    title = m.group(1).strip() if m else ""
    return title, last_name


def title_similarity(a: str, b: str) -> float:
    """Very small, dependency-free similarity: token Jaccard."""
    ta = set(re.findall(r"[A-Za-z0-9]+", a.lower()))
    tb = set(re.findall(r"[A-Za-z0-9]+", b.lower()))
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def crossref_lookup(title: str, author_last: str, year: Optional[int] = None) -> Optional[str]:
    """Return DOI string if found, else None."""
    if not title:
        return None
    params = {
        "query.title": title,
        "rows": 5,
    }
    if author_last:
        params["query.author"] = author_last
    if year:
        params["filter"] = f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31"

    headers = {"User-Agent": USER_AGENT}
    url = "https://api.crossref.org/works"
    r = requests.get(url, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    items = data.get("message", {}).get("items", []) or []
    best = None
    best_score = 0.0
    for it in items:
        it_title = (it.get("title") or [""])[0]
        score = title_similarity(title, it_title)
        if score > best_score:
            best_score = score
            best = it
    if best and best_score >= 0.55:
        return best.get("DOI")
    return None


def main() -> int:
    json_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets/data/publications.json")
    if not json_path.exists():
        print(f"Not found: {json_path}")
        return 2

    pubs: List[Dict[str, Any]] = json.loads(json_path.read_text(encoding="utf-8"))
    updated = 0
    missing = 0

    for i, p in enumerate(pubs, start=1):
        if p.get("url"):
            continue
        missing += 1

        citation = p.get("citation", "")
        title, last = extract_title_and_first_author(citation)
        year = p.get("year")
        try:
            doi = crossref_lookup(title, last, year)
        except Exception as e:
            print(f"[{i:02d}] ERROR: {e}")
            doi = None

        if doi:
            p["url"] = f"https://doi.org/{doi}"
            updated += 1
            print(f"[{i:02d}] OK  {doi}  | {title[:80]}")
        else:
            print(f"[{i:02d}] MISS      | {title[:80]}")
        time.sleep(1.0)  # be polite to Crossref

    json_path.write_text(json.dumps(pubs, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nDone. Updated {updated} missing links. Still missing {missing - updated}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
