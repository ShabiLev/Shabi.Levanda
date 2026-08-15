# Stage 13.1 verification evidence

Evidence recorded on 2026-08-15 for `feature/landing-page-v1.1`. Exact-head CI evidence is added to the pull request after the branch is pushed.

## Automated gate

| Check | Command | Result |
| --- | --- | --- |
| Portfolio suite | `.\.venv\Scripts\python.exe -m pytest -q` | PASS — 80 tests |
| Project adapter | `.\.venv\Scripts\shabi.exe validate` | PASS |
| Whitespace | `git diff --check` | PASS; line-ending warnings only |
| Signature scan | `rg` over the repository, excluding Git, the virtual environment and binary assets | PASS — no credential, private-key, MongoDB URI or local-user-path signatures |

The pytest suite includes real Chromium coverage for the landing page and CWL Office case study, axe WCAG 2.2 A/AA checks, keyboard/menu behavior, CV delivery, extracted-PDF privacy checks, one-page/section-integrity validation, local links, console errors, resource responses and responsive reflow.

## Responsive and browser review

Both routes were inspected at 320, 375, 390, 430, 768, 1024, 1280 and 1440 CSS pixels. The checks found no document-level horizontal overflow, clipped CTAs, console errors or failed local resources.

Manual keyboard review confirmed:

- the skip link becomes visible and moves focus to `main-content`;
- all sampled interactive elements show a 3px solid focus indicator;
- the mobile menu opens from the keyboard;
- Escape closes the menu and restores focus to the menu button;
- reduced-motion emulation computes `scroll-behavior: auto`;
- CWL section navigation wraps on mobile and every link remains visible;
- the CWL mobile header retains a compact CV action.

Reviewed captures:

- [Landing page — 1440px](evidence/landing-desktop-1440.jpg)
- [Landing page — 390px](evidence/landing-mobile-390.jpg)
- [CWL Office case study — 1280px](evidence/cwl-case-study-desktop-1280.jpg)
- [CWL Office case study — 390px](evidence/cwl-case-study-mobile-390.jpg)

## Lighthouse

Lighthouse 13.4.1 ran against the repository-owned local server in headless Chromium.

| Route | Performance | Accessibility | Best Practices | SEO | FCP | LCP | CLS | TBT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `/` | 100 | 100 | 100 | 100 | 0.9s | 1.8s | 0 | 0ms |
| `/projects/cwl-office/` | 100 | 100 | 100 | 100 | 0.9s | 1.1s | 0 | 0ms |

These are local artifact results, not production-deployment evidence.

## External-link audit

`curl.exe` followed redirects and returned HTTP 200 for all 12 public repository and supporting-document targets used by the portfolio:

- FlowProof repository and architecture
- Agentic Engineering Platform repository and portfolio case study
- QA Release Command Center repository and portfolio case study
- Shabi's AI Academy repository and portfolio case study
- Quality Engineering Playwright Framework repository and case study
- Multi-Tenant Data Quality Pipeline repository and case study

No live-demo URL is claimed. CWL Office has no public repository link.

## Privacy and factual review

- The CWL Office page contains no private repository URL, code, customer or tenant identity, database name, connection information, production screenshot or internal configuration.
- The CV was generated from an auditable HTML source using intentionally public career facts and contact channels. The legacy phone-bearing PDF was not reused.
- The generated PDF was rasterized and visually inspected as the actual one-page artifact; all sections and the privacy footer are visible without a split or clipping.
- The portrait is the exact public image embedded in the authoritative resume landing page; no synthetic replacement was created.
- FlowProof copy reflects the public repository and does not present the local v2.2.0 release candidate as a public release.
- No analytics, trackers, cookies, environment files or third-party runtime assets were added.

## Independent review

The independent UI/UX and accessibility reviewer issued GO with no Critical, High or Medium findings. Two Low observations—mobile CWL navigation discoverability and cross-page CV consistency—were remediated with wrapping navigation, a compact mobile CV action and a browser regression test.

Independent QA/security/privacy findings and the exact-head CI outcome are recorded in the pull request release gate.

## Remaining boundaries

- Manual screen-reader and physical-device testing were not performed.
- Production deployment is outside Stage 13.1; canonical production metadata and post-deployment smoke evidence remain intentionally absent.
- Tag `v1.1.0` must not be created until an approved merge and post-merge verification.
