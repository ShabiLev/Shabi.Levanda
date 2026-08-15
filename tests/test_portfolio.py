from __future__ import annotations

from urllib.parse import urljoin, urlparse

import pytest
from axe_playwright_python.sync_playwright import Axe


EXPECTED_PUBLIC_PROJECTS = {
    "flowproof": "https://github.com/ShabiLev/flowproof-ai-release-gate",
    "agentic-platform": "https://github.com/ShabiLev/agentic-engineering-platform",
    "ai-academy": "https://github.com/ShabiLev/Shabi-s-AI-Academy",
    "release-command-center": "https://github.com/ShabiLev/QA_Release_Command_Center_Kit",
    "playwright-framework": "https://github.com/ShabiLev/quality-engineering-playwright-framework",
    "data-quality": "https://github.com/ShabiLev/multi-tenant-data-quality-pipeline",
}
VIEWPORTS = [
    (320, 800),
    (360, 800),
    (375, 812),
    (390, 844),
    (430, 900),
    (768, 900),
    (1024, 900),
    (1280, 720),
    (1440, 900),
]


@pytest.mark.browser
def test_homepage_identity_and_executive_information_architecture(loaded_page):
    page = loaded_page
    assert page.title() == "Shabi Levanda | Quality & Release Engineering Leader | AI Systems Builder"
    assert page.get_by_role("heading", name="Shabi Levanda", exact=True).count() == 1
    assert page.locator(".hero-role").get_by_text("Quality & Release Engineering Leader", exact=False).is_visible()
    assert page.locator(".hero-role").get_by_text("AI & Agentic Systems Builder", exact=False).is_visible()
    assert page.get_by_text("turn engineering work into verified, releasable outcomes", exact=False).is_visible()
    assert page.locator("main > section").count() == 7
    assert page.locator("h1").count() == 1
    assert page.locator("header").count() == 1
    assert page.locator("main").count() == 1
    assert page.locator("footer").count() == 1
    assert page.get_by_role("navigation", name="Primary navigation").count() == 1


@pytest.mark.browser
def test_hebrew_homepage_is_authored_rtl_and_matches_information_architecture(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto(f"{portfolio_base_url}/he/", wait_until="networkidle")
    assert page.locator("html").get_attribute("lang") == "he"
    assert page.locator("html").get_attribute("dir") == "rtl"
    assert page.get_by_role("heading", name="שבי לבנדה", exact=True).count() == 1
    assert page.locator(".hero-role").get_by_text("Quality & Release Engineering Leader", exact=False).is_visible()
    assert page.get_by_text("תוצר של AI אינו הוכחה שהעבודה הושלמה", exact=False).is_visible()
    assert page.locator(".hero-actions").get_by_text("CV באנגלית", exact=False).is_visible()
    assert page.locator("main > section").count() == 7
    assert page.locator("h1").count() == 1
    page.close()


@pytest.mark.browser
@pytest.mark.parametrize(
    "path,current_lang,target_href",
    [("/", "en", "he/"), ("/he/", "he", "../index.html")],
)
def test_language_switch_is_reciprocal_and_exposes_current_language(
    browser, portfolio_base_url, path, current_lang, target_href
):
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(f"{portfolio_base_url}{path}", wait_until="networkidle")
    switcher = page.locator(".language-switch").first
    assert switcher.is_visible()
    assert switcher.locator(f'a[lang="{current_lang}"][aria-current="page"]').count() == 1
    assert page.locator(f'a[href="{target_href}"]').count() >= 1
    page.close()


@pytest.mark.browser
def test_ai_engineering_story_has_four_verified_capabilities_and_compact_flow(loaded_page):
    section = loaded_page.locator("#ai-engineering")
    assert section.locator(".ai-capabilities article").count() == 4
    for heading in ("Prompt Engineering", "Context Engineering", "Agentic Engineering", "Evaluation & Governance"):
        assert section.get_by_role("heading", name=heading, exact=True).count() == 1
    assert section.locator(".ai-flow li").count() == 8
    assert section.get_by_text("AI output is not evidence of completion", exact=False).is_visible()


@pytest.mark.browser
def test_featured_and_more_project_hierarchy_and_links(loaded_page):
    page = loaded_page
    featured = page.locator(".featured-card")
    more = page.locator(".project-card")
    assert featured.count() == 3
    assert more.count() == 4
    assert page.locator(".featured-flowproof").count() == 1

    hrefs = set(page.locator("a[href]").evaluate_all("links => links.map(link => link.href)"))
    for expected_url in EXPECTED_PUBLIC_PROJECTS.values():
        assert expected_url in hrefs

    cwl_card = page.get_by_role("article").filter(has_text="CWL Office")
    assert cwl_card.get_by_role("link", name="View Case Study").get_attribute("href") == "projects/cwl-office/"
    assert cwl_card.locator('a[href*="github.com/ShabiLev/CWL-Office"]').count() == 0
    assert cwl_card.get_by_text("Private Source · Active Engineering", exact=True).is_visible()


@pytest.mark.browser
def test_internal_anchors_resolve_and_navigation_scrolls(loaded_page):
    page = loaded_page
    hrefs = page.locator('a[href^="#"]').evaluate_all("links => links.map(link => link.getAttribute('href'))")
    for href in hrefs:
        assert href != "#"
        assert page.locator(href).count() == 1, f"Missing anchor target: {href}"
    page.get_by_role("navigation", name="Primary navigation").get_by_role("link", name="Work").click()
    assert page.evaluate("location.hash") == "#work"
    page.wait_for_function("Math.abs(document.querySelector('#work').getBoundingClientRect().top) < 110")


@pytest.mark.browser
def test_cv_download_is_real_and_available_from_required_locations(loaded_page, portfolio_base_url):
    page = loaded_page
    expected_path = "assets/cv/Shabi-Levanda-CV-EN.pdf"
    assert page.locator(".header-cv").get_attribute("href") == expected_path
    assert page.locator(".hero-actions").get_by_role("link", name="Download CV", exact=False).get_attribute("href") == expected_path
    assert page.locator("#contact").get_by_role("link", name="Download CV", exact=False).get_attribute("href") == expected_path
    assert page.locator(f'a[href="{expected_path}"][download]').count() >= 3

    response = page.request.get(urljoin(f"{portfolio_base_url}/", expected_path))
    assert response.status == 200
    assert response.headers.get("content-type") == "application/pdf"
    assert len(response.body()) > 50_000


@pytest.mark.browser
def test_hebrew_cv_actions_use_the_approved_english_artifact(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(f"{portfolio_base_url}/he/", wait_until="networkidle")
    expected_path = "../assets/cv/Shabi-Levanda-CV-EN.pdf"
    assert page.locator(f'a[href="{expected_path}"][download]').count() >= 3
    assert page.get_by_role("link", name="הורדת קורות החיים באנגלית", exact=True).first.is_visible()
    page.close()


@pytest.mark.browser
def test_cwl_case_study_is_public_safe_and_functional(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    response = page.goto(f"{portfolio_base_url}/projects/cwl-office/", wait_until="networkidle")
    assert response and response.status == 200
    assert page.title() == "CWL Office Case Study | Shabi Levanda"
    assert page.get_by_role("heading", name="CWL Office", exact=True).count() == 1
    assert page.get_by_text("Confidentiality boundary", exact=True).is_visible()
    assert page.get_by_text("No production data or internal configuration", exact=False).is_visible()
    assert page.locator('a[href*="github.com/ShabiLev/CWL-Office"]').count() == 0
    assert page.locator("main section[id]").count() == 7
    page.close()


@pytest.mark.browser
def test_hebrew_cwl_case_study_is_rtl_public_safe_and_functional(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    response = page.goto(f"{portfolio_base_url}/he/projects/cwl-office/", wait_until="networkidle")
    assert response and response.status == 200
    assert page.locator("html").get_attribute("lang") == "he"
    assert page.locator("html").get_attribute("dir") == "rtl"
    assert page.get_by_role("heading", name="CWL Office", exact=True).count() == 1
    assert page.get_by_text("מה נשאר מחוץ לעמוד", exact=True).is_visible()
    assert page.locator('a[href*="github.com/ShabiLev/CWL-Office"]').count() == 0
    assert page.locator("main section[id]").count() == 7
    page.close()


@pytest.mark.browser
def test_cwl_mobile_header_and_section_navigation_remain_visible(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(f"{portfolio_base_url}/projects/cwl-office/", wait_until="networkidle")

    cv_link = page.locator(".header-cv")
    assert cv_link.is_visible()
    assert cv_link.get_attribute("href") == "../../assets/cv/Shabi-Levanda-CV-EN.pdf"

    viewport_width = page.evaluate("window.innerWidth")
    for link in page.locator(".case-study-nav a").all():
        box = link.bounding_box()
        assert box is not None
        assert box["x"] >= 0
        assert box["x"] + box["width"] <= viewport_width

    page.close()


@pytest.mark.browser
def test_hebrew_cwl_mobile_cv_label_and_vertical_flow_direction(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(f"{portfolio_base_url}/he/projects/cwl-office/", wait_until="networkidle")

    cv_link = page.locator(".header-cv")
    assert cv_link.is_visible()
    assert cv_link.get_attribute("aria-label") == "הורדת קורות החיים באנגלית"
    assert {"CV", "EN"}.issubset(set(cv_link.inner_text().split()))

    arrow_content = page.locator(".architecture-flow div").first.evaluate(
        "element => getComputedStyle(element, '::after').content"
    )
    assert "↓" in arrow_content
    page.close()


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

    labelled_links = page.locator("a[aria-label]").evaluate_all(
        "links => links.map(link => link.getAttribute('aria-label'))"
    )
    assert all(labelled_links)
    assert len(labelled_links) == len(set(labelled_links))


@pytest.mark.browser
def test_mobile_navigation_keyboard_escape_and_scroll_lock(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(portfolio_base_url, wait_until="networkidle")
    toggle = page.locator("[data-menu-toggle]")
    assert toggle.get_attribute("aria-label") == "Open navigation menu"
    toggle.focus()
    page.keyboard.press("Enter")
    assert toggle.get_attribute("aria-expanded") == "true"
    assert page.get_by_role("navigation", name="Mobile navigation").is_visible()
    assert "menu-open" in (page.locator("body").get_attribute("class") or "")
    page.keyboard.press("Escape")
    assert toggle.get_attribute("aria-expanded") == "false"
    assert "menu-open" not in (page.locator("body").get_attribute("class") or "")
    assert page.evaluate("document.activeElement === document.querySelector('[data-menu-toggle]')")
    page.close()


@pytest.mark.browser
def test_hebrew_mobile_navigation_keyboard_escape_focus_and_rtl_order(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(f"{portfolio_base_url}/he/", wait_until="networkidle")
    toggle = page.locator("[data-menu-toggle]")
    assert toggle.get_attribute("aria-label") == "פתיחת תפריט הניווט"
    toggle.focus()
    page.keyboard.press("Enter")
    assert toggle.get_attribute("aria-expanded") == "true"
    assert page.get_by_role("navigation", name="ניווט במובייל").is_visible()
    first_link = page.locator("[data-mobile-nav] a").first
    first_link.focus()
    assert first_link.inner_text() == "פרויקטים נבחרים"
    page.keyboard.press("Escape")
    assert toggle.get_attribute("aria-expanded") == "false"
    assert page.evaluate("document.activeElement === document.querySelector('[data-menu-toggle]')")
    page.close()


@pytest.mark.browser
def test_mobile_navigation_resets_when_resized_to_desktop(browser, portfolio_base_url):
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(portfolio_base_url, wait_until="networkidle")
    toggle = page.locator("[data-menu-toggle]")
    toggle.click()
    page.set_viewport_size({"width": 1200, "height": 900})
    page.wait_for_function(
        """() => {
          const toggle = document.querySelector('[data-menu-toggle]');
          return toggle?.getAttribute('aria-expanded') === 'false'
            && !document.body.classList.contains('menu-open');
        }"""
    )
    assert toggle.get_attribute("aria-expanded") == "false"
    assert "menu-open" not in (page.locator("body").get_attribute("class") or "")
    assert page.evaluate("document.body.scrollHeight > document.documentElement.clientHeight")
    page.close()


@pytest.mark.browser
@pytest.mark.parametrize("path", ["/", "/he/", "/projects/cwl-office/", "/he/projects/cwl-office/"])
@pytest.mark.parametrize("viewport", [{"width": 1440, "height": 900}, {"width": 390, "height": 844}])
def test_wcag_22_axe_has_no_violations(browser, portfolio_base_url, path, viewport):
    page = browser.new_page(viewport=viewport)
    page.goto(f"{portfolio_base_url}{path}", wait_until="networkidle")
    results = Axe().run(
        page,
        options={
            "runOnly": {
                "type": "tag",
                "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"],
            },
            "resultTypes": ["violations"],
        },
    )
    assert results.violations_count == 0, results.generate_report()
    page.close()


@pytest.mark.browser
@pytest.mark.parametrize("path", ["/", "/he/"])
def test_reduced_motion_and_400_percent_equivalent_reflow(browser, portfolio_base_url, path):
    context = browser.new_context(
        viewport={"width": 320, "height": 800},
        reduced_motion="reduce",
    )
    page = context.new_page()
    page.goto(f"{portfolio_base_url}{path}", wait_until="networkidle")
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    assert page.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == "auto"
    assert page.locator("#contact").is_visible()
    context.close()


@pytest.mark.browser
@pytest.mark.parametrize("path", ["/", "/he/", "/projects/cwl-office/", "/he/projects/cwl-office/"])
@pytest.mark.parametrize("width,height", VIEWPORTS)
def test_bilingual_route_matrix_has_no_overflow_or_runtime_errors(
    browser, portfolio_base_url, path, width, height
):
    page = browser.new_page(viewport={"width": width, "height": height})
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(f"{portfolio_base_url}{path}", wait_until="networkidle")
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    assert page.locator("h1").is_visible()
    assert not errors
    page.close()


@pytest.mark.browser
@pytest.mark.parametrize("path", ["/", "/he/"])
@pytest.mark.parametrize("viewport,max_gap", [({"width": 1440, "height": 900}, 210), ({"width": 390, "height": 844}, 150)])
def test_top_level_section_rhythm_has_no_viewport_sized_blank_region(
    browser, portfolio_base_url, path, viewport, max_gap
):
    page = browser.new_page(viewport=viewport)
    page.goto(f"{portfolio_base_url}{path}", wait_until="networkidle")
    gaps = page.evaluate(
        """() => {
          const sections = [...document.querySelectorAll('main > section')];
          const boxes = sections.map(section => section.querySelector(':scope > .shell').getBoundingClientRect());
          return boxes.slice(0, -1).map((box, index) => Math.round(boxes[index + 1].top - box.bottom));
        }"""
    )
    assert len(gaps) == 6
    assert min(gaps) >= 70
    assert max(gaps) <= max_gap, gaps
    page.close()


@pytest.mark.browser
def test_local_resources_load_without_http_errors(loaded_page):
    failures = []
    loaded_page.on("response", lambda response: failures.append(response.url) if response.status >= 400 else None)
    loaded_page.reload(wait_until="networkidle")
    assert not failures
    for src in loaded_page.locator("link[href], script[src], img[src]").evaluate_all(
        "nodes => nodes.map(node => node.href || node.src)"
    ):
        parsed = urlparse(src)
        if parsed.hostname in {"127.0.0.1", "localhost"}:
            assert parsed.path
