from __future__ import annotations

import json
import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "data" / "verified-profile.json"
SITE_PATH = ROOT / "index.html"
CV_HTML_PATH = ROOT / "assets" / "cv" / "Shabi-Levanda-CV-EN.html"
CV_PDF_PATH = ROOT / "assets" / "cv" / "Shabi-Levanda-CV-EN.pdf"


def visible_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))).strip().casefold()


def main() -> int:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    site = visible_text(SITE_PATH)
    cv = visible_text(CV_HTML_PATH)
    required = [
        profile["positioning"]["headline"],
        *[pillar["name"] for pillar in profile["pillars"]],
        "SQL Server",
        "MongoDB",
        "Metabase",
        "Reconciliation",
        "Context engineering",
        "Independent QA",
    ]
    errors: list[str] = []
    for phrase in required:
        for label, content in (("site", site), ("CV source", cv)):
            if phrase.casefold() not in content:
                errors.append(f"{label} is missing canonical phrase: {phrase}")
    for excluded in profile["publicationRules"]["excludedTitles"]:
        if excluded.casefold() in site or excluded.casefold() in cv:
            errors.append(f"unsupported formal title is public: {excluded}")
    if not CV_PDF_PATH.is_file():
        errors.append("generated CV PDF is missing")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Profile synchronization PASS ({len(required)} canonical invariants, 2 authored surfaces, PDF present)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
