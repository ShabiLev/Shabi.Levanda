from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DEPLOYABLE_EXTENSIONS = {".html", ".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf", ".md"}
RELEASE_FILES = sorted(
    [path for path in ROOT.iterdir() if path.is_file() and path.suffix.casefold() in DEPLOYABLE_EXTENSIONS]
    + [path for path in (ROOT / "assets").rglob("*") if path.is_file() and path.suffix.casefold() in DEPLOYABLE_EXTENSIONS]
    + [path for path in (ROOT / "docs").rglob("*") if path.is_file() and path.suffix.casefold() in DEPLOYABLE_EXTENSIONS]
)
FORBIDDEN_PLACEHOLDERS = (
    "TODO", "Lorem ipsum", "you@example.com", "+972-52-000-0000", "G-XXXXXXX", "paste your", "example text",
)
PUBLIC_SAFETY_PATTERNS = {
    "MongoDB cloud connection string": re.compile(r"mongodb\+srv", re.I),
    "private key material": re.compile(r"BEGIN PRIVATE KEY", re.I),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{12,}"),
    "GitHub fine-grained token": re.compile(r"github_pat_[A-Za-z0-9_]{10,}"),
    "GitHub classic token": re.compile(r"ghp_[A-Za-z0-9]{10,}"),
    "bearer credential": re.compile(r"Bearer\s+[A-Za-z0-9._~-]{12,}", re.I),
    "credential assignment": re.compile(r"(?:password|secret)\s*=", re.I),
    "local Windows identity": re.compile(r"ShabiLevanda-Cello", re.I),
}


@pytest.mark.static
@pytest.mark.parametrize("path", RELEASE_FILES, ids=lambda path: path.name)
def test_release_assets_have_no_placeholders(path: Path):
    content = path.read_bytes().decode("utf-8", errors="ignore")
    for placeholder in FORBIDDEN_PLACEHOLDERS:
        assert placeholder.casefold() not in content.casefold(), f"Forbidden placeholder in {path.name}: {placeholder}"


@pytest.mark.static
@pytest.mark.parametrize("path", RELEASE_FILES, ids=lambda path: path.name)
def test_release_assets_are_public_safe(path: Path):
    content = path.read_bytes().decode("utf-8", errors="ignore")
    for label, pattern in PUBLIC_SAFETY_PATTERNS.items():
        assert not pattern.search(content), f"Potential {label} in {path.name}"


@pytest.mark.static
def test_only_expected_release_assets_are_referenced():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'href="styles.css"' in html
    assert 'src="script.js"' in html
    assert 'href="assets/favicon.svg"' in html
    assert "http://" not in html
    assert "rel=\"canonical\"" not in html

    local_references = re.findall(r'(?:href|src)="([^"#]+)"', html)
    release_paths = {path.resolve() for path in RELEASE_FILES}
    for reference in local_references:
        if reference.startswith(("https://", "mailto:")):
            continue
        assert (ROOT / reference).resolve() in release_paths, f"Unscanned deploy asset: {reference}"


@pytest.mark.static
def test_verified_contact_allowlist():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'href="https://www.linkedin.com/in/shabi-levanda/"' in html
    assert 'href="mailto:shabi231@gmail.com"' in html
    assert "tel:" not in html
