# Release Process

## Version

Stage 13 prepares portfolio version `v1.0.0`. A tag or release must not be created until the source pull request is approved and merged.

## Required gates

- implementation and factual-source review
- desktop, laptop, tablet, mobile and small-mobile browser review
- navigation and all six projects
- project and case-study URL review
- accessibility basics and keyboard behavior
- complete automated test suite
- placeholder and public-safety scans
- independent maintainability, security/privacy and credibility review
- exact-head pull-request CI

## Known release blocker

No privacy-approved CV PDF is available. The existing public PDF contains a personal phone number and a malformed LinkedIn target, so it is not copied. The portfolio links to the public resume source and marks PDF download as pending approval. A future PDF must be reviewed before being added under `assets/resume/Shabi-Levanda-CV.pdf`.

## Source release flow

1. Validate and independently review `feature/portfolio-v1`.
2. Push the feature branch and open a draft pull request to `main`.
3. Confirm every required check against the exact head SHA.
4. Resolve findings and rerun the complete gate.
5. Obtain human approval before merging.
6. Create `v1.0.0` only after the approved source merge.

## Deployment boundary

`Shabi.Levanda` is the canonical source repository. `ShabiLev.github.io` is only a possible production deployment target. Cross-repository deployment is outside this stage and requires a separate approved workflow.

## Rollback and monitoring

Before deployment, retain the last known-good deployment SHA. Rollback means redeploying that exact artifact. Post-release checks must cover HTTP availability, title and hero identity, navigation, all project links, responsive layout, console errors and the absence of unexpected tracking requests.
