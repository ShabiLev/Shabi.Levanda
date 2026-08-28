from __future__ import annotations

import argparse
from pathlib import Path

from weasyprint import HTML


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the canonical ATS-readable portfolio CV PDF")
    parser.add_argument("--output", type=Path, default=ROOT / "assets" / "cv" / "Shabi-Levanda-CV-EN.pdf")
    args = parser.parse_args()
    source = ROOT / "assets" / "cv" / "Shabi-Levanda-CV-EN.html"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    HTML(filename=str(source), base_url=str(ROOT)).write_pdf(str(args.output))
    print(f"Generated {args.output.relative_to(ROOT)} with WeasyPrint")


if __name__ == "__main__":
    main()
