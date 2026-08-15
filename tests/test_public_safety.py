from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import pytest
import pymupdf
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEPLOYABLE_EXTENSIONS = {
    ".html",
    ".css",
    ".js",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".pdf",
    ".md",
    ".txt",
}
SOURCE_ROOTS = [ROOT, ROOT / "assets", ROOT / "docs", ROOT / "projects"]
EXCLUDED_DIRECTORIES = {".git", ".venv", ".pytest_cache", "test-results", "tests"}
RELEASE_FILES = sorted(
    {
        path.resolve()
        for source_root in SOURCE_ROOTS
        if source_root.exists()
        for path in source_root.rglob("*")
        if path.is_file()
        and path.suffix.casefold() in DEPLOYABLE_EXTENSIONS
        and not any(part in EXCLUDED_DIRECTORIES for part in path.parts)
    }
)
FORBIDDEN_PLACEHOLDERS = (
    "TODO",
    "Lorem ipsum",
    "you@example.com",
    "+972-52-000-0000",
    "G-XXXXXXX",
    "paste your",
    "example text",
    "PDF coming soon",
    "pending approval",
)
PUBLIC_SAFETY_PATTERNS = {
    "MongoDB cloud connection string": re.compile(r"mongodb\+srv", re.I),
    "private key material": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY", re.I),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{12,}"),
    "GitHub fine-grained token": re.compile(r"github_pat_[A-Za-z0-9_]{10,}"),
    "GitHub classic token": re.compile(r"ghp_[A-Za-z0-9]{10,}"),
    "bearer credential": re.compile(r"Bearer\s+[A-Za-z0-9._~-]{12,}", re.I),
    "credential assignment": re.compile(r"(?:password|secret)\s*=", re.I),
    "local Windows identity": re.compile(r"ShabiLevanda-Cello", re.I),
    "Israeli mobile phone number": re.compile(r"(?:\+972[-\s]?|0)5\d(?:[-\s]?\d){7}"),
    "private CWL repository URL": re.compile(r"github\.com/ShabiLev/CWL-Office", re.I),
}


def release_content(path: Path) -> str:
    if path.suffix.casefold() == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    return path.read_bytes().decode("utf-8", errors="ignore")


@pytest.mark.static
@pytest.mark.parametrize("path", RELEASE_FILES, ids=lambda path: str(path.relative_to(ROOT)))
def test_release_assets_have_no_placeholders(path: Path):
    content = release_content(path)
    for placeholder in FORBIDDEN_PLACEHOLDERS:
        assert placeholder.casefold() not in content.casefold(), f"Forbidden placeholder in {path}: {placeholder}"


@pytest.mark.static
@pytest.mark.parametrize("path", RELEASE_FILES, ids=lambda path: str(path.relative_to(ROOT)))
def test_release_assets_are_public_safe(path: Path):
    content = release_content(path)
    for label, pattern in PUBLIC_SAFETY_PATTERNS.items():
        assert not pattern.search(content), f"Potential {label} in {path}"


@pytest.mark.static
def test_required_binary_assets_exist_and_are_nontrivial():
    expected_sizes = {
        ROOT / "assets" / "shabi-levanda-portrait.jpg": 50_000,
        ROOT / "assets" / "og-image.png": 20_000,
        ROOT / "assets" / "cv" / "Shabi-Levanda-CV-EN.pdf": 70_000,
    }
    for path, minimum_size in expected_sizes.items():
        assert path.is_file(), f"Missing release asset: {path.relative_to(ROOT)}"
        assert path.stat().st_size > minimum_size, f"Release asset is unexpectedly small: {path.relative_to(ROOT)}"


@pytest.mark.static
def test_legacy_cv_artifacts_are_not_deployable():
    assert not (ROOT / "assets" / "cv" / "Shabi-Levanda-CV.html").exists()
    assert not (ROOT / "assets" / "cv" / "Shabi-Levanda-CV.pdf").exists()


@pytest.mark.static
@pytest.mark.parametrize(
    "phone",
    ["054-9999720", "054 999 9720", "0549999720", "+972-54-9999720", "+972 54 999 9720"],
)
def test_israeli_mobile_phone_variants_are_rejected(phone):
    assert PUBLIC_SAFETY_PATTERNS["Israeli mobile phone number"].search(phone)


@pytest.mark.static
def test_english_cv_pdf_is_exactly_two_complete_pages():
    pdf_path = ROOT / "assets" / "cv" / "Shabi-Levanda-CV-EN.pdf"
    reader = PdfReader(pdf_path)
    assert len(reader.pages) == 2, "The RC2 English CV must render as exactly two intentional A4 pages"

    page_text = [(page.extract_text() or "").casefold() for page in reader.pages]
    assert "cello" in page_text[0] and "terminal x" in page_text[0]
    assert "cellebrite" in page_text[1] and "elbit systems" in page_text[1]
    text = "\n".join(page_text)
    for expected in (
        "Quality & Release Engineering Leader",
        "Selected impact",
        "Selected engineering projects",
        "AI & agentic engineering",
        "Professional development",
        "02 / 02",
    ):
        assert expected.casefold() in text, f"Missing or clipped CV section: {expected}"

    document = pymupdf.open(pdf_path)
    minimum_bottom_clearance_points = 18
    for page_number, page in enumerate(document, start=1):
        content_bottom = max(block[3] for block in page.get_text("blocks") if block[4].strip())
        clearance = page.rect.height - content_bottom
        assert clearance >= minimum_bottom_clearance_points, (
            f"CV page {page_number} has only {clearance:.1f}pt bottom clearance; "
            f"expected at least {minimum_bottom_clearance_points}pt"
        )


@pytest.mark.static
@pytest.mark.parametrize(
    "html_path",
    [path for path in RELEASE_FILES if path.suffix.casefold() == ".html"],
    ids=lambda path: str(path.relative_to(ROOT)),
)
def test_all_local_html_references_resolve_and_are_scanned(html_path: Path):
    html = html_path.read_text(encoding="utf-8")
    local_references = re.findall(r'(?:href|src)="([^"#]+)"', html)
    release_paths = set(RELEASE_FILES)

    for reference in local_references:
        parsed = urlparse(reference)
        if parsed.scheme in {"https", "mailto"}:
            continue
        assert parsed.scheme != "http", f"Insecure reference in {html_path}: {reference}"

        clean_path = unquote(parsed.path)
        if clean_path.startswith("/"):
            target = ROOT / clean_path.lstrip("/")
        else:
            target = html_path.parent / clean_path
        target = target.resolve()
        if target.is_dir() or clean_path.endswith("/"):
            target = target / "index.html"

        assert target.is_file(), f"Broken local reference in {html_path}: {reference}"
        assert target.resolve() in release_paths, f"Unscanned deploy asset in {html_path}: {reference}"


@pytest.mark.static
def test_metadata_and_verified_contact_allowlist():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'name="description"' in html
    assert 'property="og:title"' in html
    assert 'property="og:description"' in html
    assert 'property="og:image"' in html
    assert 'name="twitter:card"' in html
    assert 'href="https://www.linkedin.com/in/shabi-levanda/"' in html
    assert 'href="mailto:shabi231@gmail.com"' in html
    assert "tel:" not in html
    assert 'rel="canonical"' not in html


@pytest.mark.static
@pytest.mark.parametrize(
    "relative_path,language,direction",
    [
        ("index.html", "en", "ltr"),
        ("he/index.html", "he", "rtl"),
        ("projects/cwl-office/index.html", "en", "ltr"),
        ("he/projects/cwl-office/index.html", "he", "rtl"),
    ],
)
def test_bilingual_routes_have_language_direction_and_hreflang_metadata(relative_path, language, direction):
    html = (ROOT / relative_path).read_text(encoding="utf-8")
    assert f'<html lang="{language}" dir="{direction}">' in html
    assert 'hreflang="en"' in html
    assert 'hreflang="he"' in html
    assert 'hreflang="x-default"' in html
    assert 'property="og:locale"' in html
    assert 'rel="canonical"' not in html


@pytest.mark.static
@pytest.mark.parametrize("relative_path", ["he/index.html", "he/projects/cwl-office/index.html"])
def test_hebrew_routes_do_not_leak_english_interface_copy(relative_path):
    html = (ROOT / relative_path).read_text(encoding="utf-8")
    for untranslated_label in (
        "Selected work",
        "More engineering work",
        "About & leadership",
        "Experience & impact",
        "Download CV",
        "View Project",
        "Return to selected work",
    ):
        assert untranslated_label not in html


@pytest.mark.static
def test_cwl_case_study_contains_only_the_public_boundary():
    html = (ROOT / "projects" / "cwl-office" / "index.html").read_text(encoding="utf-8")
    assert "Private Source" in html
    assert "Sanitized Case Study" in html
    assert "tenant names" in html
    assert "production URLs" in html
    assert "github.com/ShabiLev/CWL-Office" not in html
    assert "mongodb+srv" not in html.casefold()
    assert "screenshot" in html.casefold()

    hebrew_html = (ROOT / "he" / "projects" / "cwl-office" / "index.html").read_text(encoding="utf-8")
    assert "גבול הסודיות" in hebrew_html
    assert "github.com/ShabiLev/CWL-Office" not in hebrew_html
    assert "mongodb+srv" not in hebrew_html.casefold()
