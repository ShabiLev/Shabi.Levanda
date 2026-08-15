# Architecture

## Decision

The portfolio remains a dependency-light static site: semantic HTML, a shared responsive design system and a small progressive-enhancement script. Stage 13.1 adds one public-safe case-study route without introducing a runtime framework.

```text
Browser
  -> index.html (seven-section executive landing page)
  -> projects/cwl-office/index.html (sanitized case study)
  -> styles.css (shared tokens and responsive presentation)
  -> script.js (header and accessible mobile navigation)
  -> assets/
       -> portrait and social image
       -> cv/Shabi-Levanda-CV.html (auditable source)
       -> cv/Shabi-Levanda-CV.pdf (download artifact)
```

## Information architecture

The landing page has seven top-level content sections:

1. Hero
2. Selected Work
3. More Projects
4. About & Leadership
5. Experience & Impact
6. Governed AI Engineering
7. Contact

The header and footer frame these sections. Deep technical detail stays in public repository documentation or the dedicated CWL Office case study.

## Quality architecture

```text
Repository-owned HTTP target
  -> pytest + Playwright browser checks
  -> axe WCAG A/AA checks on both routes
  -> eight-width responsive matrix and 320px reflow
  -> CV, resource and internal-link verification
  -> recursive public-safety scan
  -> Lighthouse and manual keyboard/visual review
  -> independent QA, UI/UX and privacy review
  -> GitHub Actions exact-head gate
```

Tests start an ephemeral local server by default. CI starts the same static target explicitly and supplies `PORTFOLIO_BASE_URL`.

## Security and privacy boundaries

- `Shabi.Levanda` is the canonical public source repository.
- CWL Office source, configuration, tenant data and production topology remain private.
- The CWL case study uses conceptual architecture and contains no screenshots or data samples.
- The downloadable CV is generated from an auditable HTML source using only intentionally public facts and contact channels.
- The private central agent platform remains external; this repository contains only the minimal `.shabi/project.yaml` adapter.
- No analytics, trackers, cookies, runtime CDN assets or external fonts are used.

## Accessibility and resilience

Both routes use native landmarks, one `h1`, ordered headings, native links and buttons, visible focus, a skip link and reduced-motion support. The mobile menu has explicit expanded state, Escape handling, scroll locking, focus restoration and desktop-breakpoint reset.
