from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from weasyprint import HTML


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the canonical ATS-readable portfolio CV PDF")
    parser.add_argument("--output", type=Path, default=ROOT / "assets" / "cv" / "Shabi-Levanda-CV-EN.pdf")
    args = parser.parse_args()
    source = ROOT / "assets" / "cv" / "Shabi-Levanda-CV-EN.html"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    engine = "Chromium"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.goto(source.as_uri(), wait_until="networkidle")
            page.pdf(
                path=str(args.output),
                format="A4",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                prefer_css_page_size=True,
            )
            browser.close()
    except PlaywrightError:
        engine = "WeasyPrint fallback"
        HTML(filename=str(source), base_url=str(ROOT)).write_pdf(str(args.output))
    print(f"Generated {args.output.relative_to(ROOT)} with {engine}")


if __name__ == "__main__":
    main()
