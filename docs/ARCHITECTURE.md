# Architecture

## Decision

The portfolio uses plain HTML, CSS and JavaScript. The content is a single-page static document with stable fragment navigation and no runtime data dependency.

```text
Browser
  -> index.html (content and semantics)
  -> styles.css (responsive presentation)
  -> script.js (mobile navigation and small progressive enhancements)
  -> assets/ (repository-owned static assets)
```

## Quality architecture

```text
Repository-owned HTTP target
  -> pytest + Playwright browser checks
  -> responsive and keyboard checks
  -> placeholder and public-safety scans
  -> GitHub Actions quality gate
  -> independent review
  -> source release decision
```

Tests start an ephemeral local server by default. CI starts the same static target explicitly and supplies `PORTFOLIO_BASE_URL`, so no test depends on public websites being available.

## Boundaries

- `Shabi.Levanda` is the canonical source.
- `ShabiLev.github.io` is an optional deployment target and is not modified by this stage.
- Public repositories are factual references, not runtime dependencies.
- The central agent platform remains external; this repository contains only `.shabi/project.yaml` as its project adapter.

## Accessibility and resilience

The document uses native landmarks, a single `h1`, ordered headings, native links and buttons, visible focus, a skip link and reduced-motion support. Navigation remains usable without JavaScript on desktop; JavaScript adds an accessible compact-menu interaction on small screens.
