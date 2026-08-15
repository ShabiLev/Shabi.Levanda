# Stage 13.1 RC2 verification evidence

Evidence recorded on 2026-08-15 for `feature/landing-page-v1.1`. Pull request #2 is the authoritative record for the final exact-head CI SHA and run URL.

## Automated gate

| Check | Command | Result |
| --- | --- | --- |
| Portfolio suite | `.\.venv\Scripts\python.exe -m pytest -q` | PASS — 160 tests |
| Project adapter | `.\.venv\Scripts\shabi.exe validate` | PASS |
| Whitespace | `git diff --check` | PASS; line-ending warnings only |
| Signature scan | `rg` for private-key, credential, MongoDB URI, phone and local-user-path signatures, excluding Git, the virtual environment, test results and binary assets | PASS — no matches |

The pytest suite exercises all four authored routes in real Chromium: English and Hebrew landing pages plus both CWL Office case studies. Coverage includes axe WCAG 2.2 A/AA, `lang`/`dir` and reciprocal `hreflang`, Hebrew UI leakage, keyboard menus and focus restoration, reduced motion, CV delivery and extracted-PDF privacy, exact two-page CV integrity, local assets, console/resource failures and responsive reflow.

## Responsive, RTL and browser review

English and Hebrew landing pages were rendered and screenshot-reviewed at 360, 390, 768, 1024, 1280 and 1440 CSS pixels. Automated coverage additionally includes 320, 375 and 430 pixels and both CWL routes. No route produced document-level horizontal overflow, clipped CTAs, console errors or failed local resources.

Measured landing content-to-content gaps are identical in LTR and RTL:

- desktop 1440px: 173–195px across all six transitions;
- mobile 390px: 94–126px across all six transitions.

Keyboard review in both languages confirmed that the menu opens with Enter, exposes the localized close label, closes with Escape and restores focus to the toggle. The automated suite also verifies the visible skip link, focus transfer to `main-content`, focus styling and `scroll-behavior: auto` under reduced-motion emulation.

Reviewed release captures:

- [English landing — desktop](evidence/landing-en-desktop.jpg)
- [English landing — mobile](evidence/landing-en-mobile.jpg)
- [Hebrew landing — desktop RTL](evidence/landing-he-desktop.jpg)
- [Hebrew landing — mobile RTL](evidence/landing-he-mobile.jpg)
- [English CWL Office case study](evidence/cwl-en.jpg)
- [Hebrew CWL Office case study](evidence/cwl-he.jpg)
- [Hebrew CWL Office case study — mobile RTL](evidence/cwl-he-mobile.jpg)

## HEBREW EDITORIAL REVIEW

- **Strings reviewed:** every visible string in `/he/index.html` and `/he/projects/cwl-office/`, including metadata and OpenGraph copy, navigation, buttons, project cards, experience and AI sections, footer text, image alternatives, privacy language and ARIA labels.
- **Corrections made:** rewrote literal translations into natural Israeli technology Hebrew; clarified the English CV CTA; replaced hybrid Hero and CWL sentences; corrected mixed-direction punctuation and line order with scoped `bdi`; prevented `Multi‑Tenant` from splitting; added unique contextual names to repeated project links; and standardized public/private-source language without adding facts.
- **Terminology decisions:** retained established terms where they are clearer to Israeli engineering readers, including `Quality Engineering`, `Release`, `Prompt Engineering`, `Context Engineering`, `Agentic Engineering`, `AI`, `Production`, `Multi‑Tenant`, `Read-only`, `Repository` and `Case Study`; used natural Hebrew explanations around them rather than mechanical noun-for-noun translation. Engineering evidence is described as verification results, test outputs or findings according to context, not automatically as legalistic "ראיות".
- **Remaining concerns:** only optional Low polish remains: one repeated form of "מוגדר", one use of "בדיקות Responsive", two legacy ASCII hyphen forms in the experience section, an older but accurate Twitter summary and the phrase "כתובות Production" in the CWL confidentiality boundary. The independent editor confirmed that none is unnatural enough to block release, changes professional meaning or creates a BiDi defect.
- **Result:** **GO** from the separate native-Hebrew senior technology editor after remediation and a second read-only review of the frozen source plus exact-current desktop/mobile screenshots. No Critical, High or Medium editorial findings remain.

## CV artifact

The English CV is generated from the repository-owned HTML source. The final PDF is 83,780 bytes and exactly two intentional A4 pages. `pypdf` extracts and privacy-scans each page; page 1 contains Cello and Terminal X, while page 2 contains Cellebrite, Elbit, selected engineering projects, governed AI engineering, technology, professional development, languages, service and the `02 / 02` footer. PyMuPDF measures 125.6pt bottom clearance on page 1 and 20.6pt on page 2, above the enforced 18pt safe-area minimum.

Both actual PDF pages were rasterized after final generation and visually inspected. Titles, sections and footers are visible and unclipped:

- [CV page 1](evidence/cv-en-page-1.png)
- [CV page 2](evidence/cv-en-page-2.png)

The requested `SHABI LEVANDA(1).docx` was not found. Provenance, the inspected fallback source hash, accepted facts and excluded private/unsupported content are recorded in [CV provenance](CV_PROVENANCE.md). A Hebrew PDF remains an explicit follow-up; every Hebrew CV action clearly identifies and downloads the verified English artifact.

## Lighthouse

Lighthouse 13.4.1 ran against a repository-owned local HTTP server in headless Chromium.

| Route | Performance | Accessibility | Best Practices | SEO |
| --- | ---: | ---: | ---: | ---: |
| `/` | 100 | 100 | 100 | 92 |
| `/he/` | 100 | 100 | 100 | 92 |
| `/projects/cwl-office/` | 100 | 100 | 100 | 91 |
| `/he/projects/cwl-office/` | 100 | 100 | 100 | 91 |

SEO is intentionally below 100 because Stage 13.1 has no approved production URL and therefore does not publish speculative canonical URLs. These are local artifact results, not production-deployment evidence.

## External-link audit

The 2026-08-15 live audit returned HTTP 200 for the GitHub profile and every linked public repository and supporting case-study/document target. LinkedIn returned its expected automation-blocking HTTP 999; the URL matches the approved public source. No live-demo URL is claimed, and CWL Office has no private or future-`main` repository link.

## Privacy and factual boundaries

- Both CWL pages exclude private repository URLs, customer or tenant identities, database/collection names, connection information, production screenshots and internal configuration.
- The CV and site exclude the source phone number, local source paths and stronger metrics found only in an older document.
- Superseded one-page CV files were removed; the gate rejects common local and international Israeli mobile-number formats across deployable text and extracted PDF content.
- AI wording is constrained to supported prompt contracts, scoped context, bounded specialist orchestration, deterministic evaluation, independent QA, evidence and accountable release gates. It does not claim autonomous production agents, RAG/memory, model tuning, formal certification or regulatory compliance.
- FlowProof links to the actual public `flowproof-ai-release-gate` repository and does not present the local v2.2.0 release candidate as public-main truth.
- No analytics, trackers, cookies, environment files or third-party runtime assets were added.

## Independent review

Independent UI/UX/RTL, Hebrew editorial, factual/AI, privacy and Senior QA re-reviews all issued GO after their findings were remediated. Senior QA independently confirmed 20.624pt page-2 footer clearance and 35 blank raster rows below the final content. The PR source gate may issue GO only while GitHub Actions is successful on its exact current head.

## Remaining boundaries

- Manual screen-reader and physical-device testing were not performed.
- A professionally reviewed Hebrew PDF was not produced; the Hebrew site intentionally links to the English CV.
- Production deployment, canonical production metadata and post-deployment smoke evidence are outside Stage 13.1.
- No merge, tag or release is authorized by this evidence. Tag `v1.1.0` must wait for approved merge and post-merge verification.
