# Quality Gate

## Automated gate

```powershell
python -m pytest
```

Coverage includes:

- homepage identity and semantic landmarks
- exactly six project cards and exact repository URLs
- resolvable internal anchors and navigation behavior
- truthful resume state
- keyboard entry and external-link hardening
- WCAG A/AA axe scans on desktop and mobile
- 400% zoom-equivalent reflow at 320 CSS pixels
- mobile navigation with keyboard and Escape behavior
- horizontal-overflow checks at 1440×900, 1280×720, 768×900, 390×844 and 360×800
- browser console and local HTTP errors
- placeholder detection in release assets
- credential-like and local-identity public-safety patterns

The suite intentionally does not request third-party project URLs. Their existence and factual content are reviewed separately so CI remains deterministic.

## Manual gate

Review the actual browser at all five target sizes and record visual hierarchy, content density, navigation, focus visibility, project stacking, touch targets, workflow adaptation, contact and resume behavior, console errors, readable contrast and zoom behavior.

Automated checks do not replace manual accessibility expert review, screen-reader coverage or production deployment verification.

## Release decision

A gate without executable or review evidence is not a pass. CI must correspond to the exact pull-request head. Failed checks must be fixed and rerun; thresholds and scope must not be weakened to manufacture success.
