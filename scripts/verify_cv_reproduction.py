from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader


def normalized_pages(path: Path) -> list[str]:
    return [re.sub(r"\s+", " ", page.extract_text() or "").strip() for page in PdfReader(path).pages]


REQUIRED_MARKERS = (
    "Quality, Release & Applied AI Engineering Leader",
    "Professional summary",
    "Recent leadership experience",
    "Earlier experience",
    "Selected engineering projects",
    "Applied AI & Agentic Engineering",
    "Core competencies",
    "SQL Server",
    "MongoDB",
    "Metabase",
    "02 / 02",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare committed and regenerated CV semantics")
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    args = parser.parse_args()
    expected = normalized_pages(args.expected)
    actual = normalized_pages(args.actual)
    if len(expected) != 2 or len(actual) != 2:
        raise SystemExit("CV reproduction FAIL: expected exactly two pages")
    for marker in REQUIRED_MARKERS:
        for label, pages in (("committed", expected), ("regenerated", actual)):
            if marker.casefold() not in " ".join(pages).casefold():
                raise SystemExit(f"CV reproduction FAIL: {label} PDF is missing {marker!r}")
    print(f"CV reproduction PASS (2 pages, {len(REQUIRED_MARKERS)} semantic invariants)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
