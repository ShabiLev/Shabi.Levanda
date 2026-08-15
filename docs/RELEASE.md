# Release Process

## Version

Stage 13.1 prepares portfolio version `v1.1.0`. A tag or GitHub Release must not be created until the source pull request is approved and merged.

## Required gates

- factual-source and current-repository review
- desktop, laptop, tablet, mobile and 320px browser review
- navigation, selected work, more projects and all CTAs
- CWL Office confidentiality review
- CV provenance, download and visual review
- project and case-study URL audit
- automated and manual accessibility review
- complete automated test suite
- Lighthouse performance/accessibility/best-practices/SEO review
- recursive placeholder, secret and public-safety scans
- independent QA and UI/UX review
- exact-head pull-request CI

## CV release boundary

The v1.1 CV is generated from `assets/cv/Shabi-Levanda-CV.html` and published at `assets/cv/Shabi-Levanda-CV.pdf`. It contains only facts and contact channels already intentionally public in the authoritative `Shabi-Resume/index.html` source. The legacy PDF is not reused.

See [CV provenance](CV_PROVENANCE.md).

## Source release flow

1. Validate and independently review `feature/landing-page-v1.1`.
2. Push the feature branch and open a draft pull request to `main`.
3. Confirm every required check against the exact head SHA.
4. Resolve findings and rerun the complete gate.
5. Obtain human approval before merging.
6. Pull clean `main` and run post-merge verification.
7. Create `v1.1.0` only after the approved source merge.

## Deployment boundary

`Shabi.Levanda` is the canonical source repository. `ShabiLev.github.io` remains a possible production deployment target. Cross-repository deployment is outside Stage 13.1 and requires a separate approved workflow.

## Rollback and monitoring

The last known-good source release is `v1.0.0`. If post-merge source verification fails, revert through a new reviewed pull request. Any future deployment must retain its previous deployed SHA and verify HTTP availability, Hero identity, navigation, project links, CWL case study, CV download, responsive layout, accessibility, console errors and unexpected network requests.
