# Shabi Levanda Engineering Portfolio

Canonical source for Shabi Levanda's engineering-leadership portfolio.

> Building reliable software delivery systems where AI speed meets engineering discipline.

The portfolio positions Shabi as a **Quality & Release Engineering Leader** and **AI & Agentic Systems Builder**. It presents only claims supported by public repositories and makes evidence, constraints and release readiness visible.

## Architecture

The site is intentionally static and dependency-light:

- semantic `index.html`
- responsive `styles.css`
- small progressive-enhancement `script.js`
- Python, pytest and Playwright quality gate
- GitHub Actions CI against a repository-owned local server

No runtime framework, analytics, cookies, tracking or third-party fonts are used.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --requirement requirements-dev.txt
python -m playwright install chromium
python -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080/`.

## Testing

In a second terminal with the virtual environment active:

```powershell
python -m pytest
```

The suite owns a deterministic local server when `PORTFOLIO_BASE_URL` is not set. It verifies identity, all six projects, expected repository and supporting-document hrefs, navigation, anchors, resume truthfulness, semantic landmarks, axe accessibility, keyboard behavior, mobile navigation, five responsive viewports, 400% reflow equivalence, overflow, local resource loading, placeholder detection and public-safety patterns. External URL availability is reviewed separately so CI does not depend on third-party uptime.

## CI

`.github/workflows/portfolio-ci.yml` runs on pull requests and pushes to `main`. It installs pinned Python dependencies and Chromium, starts the local target, performs a health check and runs the complete quality gate.

## Source and deployment separation

- `Shabi.Levanda`: canonical source repository.
- `ShabiLev.github.io`: optional future production deployment target.

This release does not write to or deploy across repositories. Deployment requires separate approval after the source release is accepted.

## Security and privacy

- Public project claims are sourced from public GitHub documentation.
- No analytics, tracking, cookies, credentials, customer data or private repository content.
- Release assets are scanned for placeholder and credential-like patterns.
- The existing CV PDF is not copied because privacy review found a personal phone number and a malformed LinkedIn link. The site documents this release blocker honestly.
- External links opened in a new tab use `noopener noreferrer`.

## Contribution and release workflow

1. Work on a non-default feature branch.
2. Run `python -m pytest` and complete manual browser review.
3. Update `CHANGELOG.md` and release evidence.
4. Open a draft pull request to `main`.
5. Require green exact-head CI and independent review.
6. Merge only after all gates pass; verify the deployed artifact separately.

See [architecture](docs/ARCHITECTURE.md), [portfolio strategy](docs/PORTFOLIO_STRATEGY.md), [quality gate](docs/QUALITY_GATE.md) and [release process](docs/RELEASE.md).
