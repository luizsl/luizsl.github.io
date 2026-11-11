#!/usr/bin/env python3
"""Refresh data/metrics.json from OpenAlex.

OpenAlex is used because it resolves an author through ORCID, needs no API key, and
publishes the summary statistics the Publications page displays. NASA ADS is the
authoritative source in astronomy and additionally reports read counts, but its API
requires a personal token and some of its fields are not exposed without it; see the
README for how to switch once a token exists.

Run locally with:  python3 tools/update_metrics.py
"""

from __future__ import annotations

import json
import pathlib
import sys
import urllib.error
import urllib.request
from datetime import date

ORCID = "0000-0003-3490-9063"
ENDPOINT = f"https://api.openalex.org/authors/https://orcid.org/{ORCID}"
OUTPUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "metrics.json"
MAILTO = "luiz.sl@outlook.com"  # OpenAlex "polite pool" contact


def fetch_author() -> dict:
    request = urllib.request.Request(
        ENDPOINT,
        headers={
            "User-Agent": f"luizsl.github.io metrics job (mailto:{MAILTO})",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def build(author: dict) -> dict:
    stats = author.get("summary_stats") or {}
    orcid = (author.get("orcid") or "").rsplit("/", 1)[-1]

    if orcid != ORCID:
        raise SystemExit(f"OpenAlex returned ORCID {orcid!r}, expected {ORCID!r}")

    payload = {
        "source": "openalex",
        "source_label": "OpenAlex",
        "updated": date.today().isoformat(),
        "publications": author.get("works_count"),
        "citations": author.get("cited_by_count"),
        "h_index": stats.get("h_index"),
        "i10_index": stats.get("i10_index"),
        # OpenAlex has no read counts; the ADS job can fill this in later.
        "reads": None,
    }

    for key in ("publications", "citations", "h_index"):
        if not isinstance(payload[key], int):
            raise SystemExit(f"OpenAlex field {key!r} missing or not an integer")

    return payload


def main() -> int:
    try:
        author = fetch_author()
    except urllib.error.URLError as error:
        print(f"OpenAlex request failed: {error}", file=sys.stderr)
        return 1

    payload = build(author)
    previous = json.loads(OUTPUT.read_text()) if OUTPUT.exists() else {}
    comparable = {k: v for k, v in previous.items() if k != "updated"}

    if comparable == {k: v for k, v in payload.items() if k != "updated"}:
        # Keep the old date so the weekly job does not produce empty commits.
        payload["updated"] = previous.get("updated", payload["updated"])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
