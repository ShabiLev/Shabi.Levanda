from __future__ import annotations

from urllib.parse import urlparse

import pytest
from axe_playwright_python.sync_playwright import Axe


EXPECTED_PROJECTS = {
    "flowproof": "https://github.com/ShabiLev/flowproof-ai-release-gate",
    "agentic-platform": "https://github.com/ShabiLev/agentic-engineering-platform",
    "ai-academy": "https://github.com/ShabiLev/Shabi-s-AI-Academy",
    "release-command-center": "https://github.com/ShabiLev/QA_Release_Command_Center_Kit",
    "playwright-framework": "https://github.com/ShabiLev/quality-engineering-playwright-framework",
    "data-quality": "https://github.com/ShabiLev/multi-tenant-data-quality-pipeline",
}
EXPECTED_SUPPORTING_DOCS = {
    "flowproof": "https://github.com/ShabiLev/flowproof-ai-release-gate/blob/main/docs/ARCHITECTURE.md",
    "agentic-platform": "https://github.com/ShabiLev/agentic-engineering-platform/blob/main/docs/PORTFOLIO_CASE_STUDY.md",
    "ai-academy": "https://github.com/ShabiLev/Shabi-s-AI-Academy/blob/main/docs/portfolio/CASE_STUDY.md",
    "release-command-center": "https://github.com/ShabiLev/QA_Release_Command_Center_Kit/blob/main/docs/portfolio/CASE_STUDY.md",
    "playwright-framework": "https://github.com/ShabiLev/quality-engineering-playwright-framework/blob/main/docs/PORTFOLIO_CASE_STUDY.md",
    "data-quality": "https://github.com/ShabiLev/multi-tenant-data-quality-pipeline/blob/main/docs/PORTFOLIO_CASE_STUDY.md",
}


@pytest.mark.browser
def test_homepage_identity_and_semantics(loaded_page):
    page = loaded_page
    assert page.title() == "Shabi Levanda | Quality Engineering, Release Engineering & AI Systems"
    assert page.get_by_role("heading", name="Shabi Levanda", exact=True).count() == 1
    assert page.get_by_text("Building reliable software delivery systems where", exact=False).is_visible()
    assert page.locator("h1").count() == 1
    assert page.locator("header").count() == 1
    assert page.locator("main").count() == 1
    assert page.locator("footer").count() == 1
    assert page.get_by_role("navigation", name="Primary navigation").count() == 1


@pytest.mark.browser
def test_six_projects_and_public_repository_links(loaded_page):
    cards = loaded_page.locator("[data-project]")
    assert cards.count() == 6
    for project_id, expected_url in EXPECTED_PROJECTS.items():
        card = loaded_page.locator(f'[data-project="{project_id}"]')
        assert card.count() == 1
        urls = card.locator("a").evaluate_all("links => links.map(link => link.href)")
        assert expected_url in urls
        assert EXPECTED_SUPPORTING_DOCS[project_id] in urls


@pytest.mark.browser
def test_internal_anchors_resolve_and_navigation_scrolls(loaded_page):
    page = loaded_page
    hrefs = page.locator('a[href^="#"]').evaluate_all("links => links.map(link => link.getAttribute('href'))")
    for href in hrefs:
        assert href != "#"
        assert page.locator(href).count() == 1, f"Missing anchor target: {href}"
    page.get_by_role("link", name="Work", exact=True).click()
    assert page.evaluate("location.hash") == "#work"
    page.wait_for_function("Math.abs(document.querySelector('#work').getBoundingClientRect().top) < 100")


@pytest.mark.browser
def test_resume_state_is_truthful(loaded_page):
    resume = loaded_page.locator("#resume")
    source_link = resume.get_by_role("link", name="View public resume source", exact=False)
    assert source_link.get_attribute("href") == "https://github.com/ShabiLev/Shabi-Resume"
    assert resume.locator(".resume-status").get_by_text("PDF download pending approval").is_visible()
    assert resume.locator('[aria-disabled="true"]').count() == 0
    assert resume.locator('a[download]').count() == 0


@pytest.mark.browser
def test_keyboard_entry_and_external_link_hardening(loaded_page):
    page = loaded_page
    page.locator("body").press("Tab")
    assert page.evaluate("document.activeElement.getAttribute('href')") == "#main-content"
    page.keyboard.press("Enter")
    assert page.evaluate("document.activeElement.id") == "main-content"
    external_links = page.locator('a[target="_blank"]')
    for index in range(external_links.count()):
        rel = external_links.nth(index).get_attribute("rel") or ""
        assert {"noopener", "noreferrer"}.issubset(set(rel.split()))

    project_link_names = page.locator("[data-project] a").evaluate_all(
        "links => links.map(link => link.getAttribute('aria-label'))"
    )
    assert all(project_link_names)
    assert len(project_link_names) == len(set(project_link_names))


@pytest.mark.browser
def test_mobile_navigation_keyboard_and_escape(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(portfolio_base_url, wait_until="networkidle")
    toggle = page.locator(".menu-toggle")
    assert toggle.get_by_text("Open navigation").count() == 1
    toggle.focus()
    page.keyboard.press("Enter")
    assert toggle.get_attribute("aria-expanded") == "true"
    assert page.get_by_role("navigation", name="Primary navigation").is_visible()
    page.keyboard.press("Escape")
    assert toggle.get_attribute("aria-expanded") == "false"
    assert page.evaluate("document.activeElement === document.querySelector('.menu-toggle')")
    page.close()


@pytest.mark.browser
def test_mobile_navigation_resets_when_resized_to_desktop(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(portfolio_base_url, wait_until="networkidle")
    toggle = page.locator(".menu-toggle")
    toggle.click()
    assert page.locator("body").get_attribute("class") == "menu-open"
    page.set_viewport_size({"width": 768, "height": 900})
    assert toggle.get_attribute("aria-expanded") == "false"
    assert "menu-open" not in (page.locator("body").get_attribute("class") or "")
    assert page.evaluate("document.body.scrollHeight > document.documentElement.clientHeight")
    page.close()


@pytest.mark.browser
@pytest.mark.parametrize("viewport", [{"width": 1440, "height": 900}, {"width": 390, "height": 844}])
def test_wcag_axe_has_no_violations(browser, portfolio_base_url, viewport):
    page = browser.new_page(viewport=viewport)
    page.goto(portfolio_base_url, wait_until="networkidle")
    results = Axe().run(
        page,
        options={
            "runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]},
            "resultTypes": ["violations"],
        },
    )
    assert results.violations_count == 0, results.generate_report()
    page.close()


@pytest.mark.browser
def test_400_percent_equivalent_reflow(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 320, "height": 800})
    page.goto(portfolio_base_url, wait_until="networkidle")
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    assert page.locator("#contact").is_visible()
    page.close()


@pytest.mark.browser
@pytest.mark.parametrize("width,height", [(1440, 900), (1280, 720), (768, 900), (390, 844), (360, 800)])
def test_responsive_viewports_have_no_horizontal_overflow(browser, portfolio_base_url, width, height):
    page = browser.new_page(viewport={"width": width, "height": height})
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.goto(portfolio_base_url, wait_until="networkidle")
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    assert page.locator("#top h1").is_visible()
    assert page.locator('[data-project="data-quality"]').is_visible()
    assert not errors
    page.close()


@pytest.mark.browser
def test_local_resources_load_without_http_errors(loaded_page):
    failures = []
    loaded_page.on("response", lambda response: failures.append(response.url) if response.status >= 400 else None)
    loaded_page.reload(wait_until="networkidle")
    assert not failures
    for src in loaded_page.locator("link[href], script[src]").evaluate_all(
        "nodes => nodes.map(node => node.href || node.src)"
    ):
        parsed = urlparse(src)
        if parsed.hostname in {"127.0.0.1", "localhost"}:
            assert parsed.path
