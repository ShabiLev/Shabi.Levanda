# Quality Gate

## Automated gate

```powershell
python -m pytest
```

Coverage includes:

- executive identity, semantic landmarks and seven-section information architecture
- three featured projects and four smaller public showcases
- exact public project links and private CWL link boundary
- functional English and Hebrew CWL Office case-study routes
- authored Hebrew RTL landing content, reciprocal language controls and hreflang metadata
- natural Israeli technology terminology, rejected literal-translation phrases, English-CV clarity and non-breaking mixed-direction terms
- real CV download from Header, Hero and Contact
- skip-link focus, external-link hardening and accessible labels
- mobile menu keyboard operation, Escape, scroll lock and resize reset
- axe WCAG 2.0/2.1/2.2 A/AA scans on all four language/content routes
- reduced-motion behavior and 320px / 400%-equivalent reflow
- responsive widths at 320, 360, 375, 390, 430, 768, 1024, 1280 and 1440
- computed top-level content-gap assertions preventing viewport-sized blank regions
- browser console, page error and local resource checks
- recursive placeholder, credential, phone, local-path and private-CWL-URL scans
- local-link resolution across every deployable HTML file
- minimum binary-size checks for portrait, social image and PDF
- real PDF text extraction, privacy scanning, exact two-page count, page-specific section-integrity checks and an 18pt minimum bottom safe area

The deterministic CI suite does not request third-party URLs. External repository and case-study availability is audited separately and recorded with the release evidence.

## Manual gate

Review all four routes in real Chromium at the responsive matrix above. Record:

- first-screen identity and CTA hierarchy
- portrait treatment and project hierarchy
- keyboard order, focus visibility, Escape and menu focus restoration
- touch-target usability and absence of clipping/overlap
- natural scrolling and reduced-motion behavior
- CWL confidentiality and absence of private links/data
- CV visual output and download response
- authored Hebrew quality, mixed-direction text, RTL focus/navigation order and bilingual consistency
- separate native-Hebrew senior technology editorial approval after the final copy is frozen
- console/network errors

Run Lighthouse against the repository-owned server and record Performance, Accessibility, Best Practices and SEO scores.

Automated checks do not replace manual screen-reader or physical-device coverage; any gap must remain explicit.

## Release decision

A gate without executable or review evidence is not a pass. CI must correspond to the exact pull-request head. Failed checks must be fixed and rerun; thresholds and scope must not be weakened to manufacture success.
