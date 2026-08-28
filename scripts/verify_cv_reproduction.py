from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader


def normalized_pages(path: Path) -> list[str]:
    return [re.sub(r"\s+", " ", page.extract_text() or "").strip() for page in PdfReader(path).pages]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare committed and regenerated CV semantics")
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    args = parser.parse_args()
    expected = normalized_pages(args.expected)
    actual = normalized_pages(args.actual)
    if expected != actual:
        raise SystemExit("CV reproduction FAIL: page count or extracted text differs")
    print(f"CV reproduction PASS ({len(actual)} pages, identical extracted text)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
