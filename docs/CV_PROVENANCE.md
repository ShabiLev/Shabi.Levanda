# CV Provenance and Privacy Review

## Authoritative source

The portfolio CV is derived from the intentionally public `ShabiLev/Shabi-Resume` repository, inspected on 2026-08-15. That repository's current tree contains only `index.html`; its referenced PDF does not exist.

The auditable CV source is:

`assets/cv/Shabi-Levanda-CV.html`

The downloadable artifact is:

`assets/cv/Shabi-Levanda-CV.pdf`

## Preserved facts

- Quality & Release Engineering leadership positioning
- AI & Agentic Systems Builder portfolio positioning
- 22+ years in high-tech
- 10+ years QA leadership
- 20% cycle-time improvement
- 40–50% defect / data error reduction
- career chronology for Cello, Terminal X, Cellebrite and Elbit
- Python Automation Full-Stack training at QA Experts College
- verified public email, LinkedIn and GitHub profiles

## Intentional exclusions

- phone number
- home address or location detail
- identity information
- QR code and unverified domain
- testimonials
- internal company, customer, tenant or production information
- private repository URLs or configuration

## Generation

The PDF is rendered from the repository-owned HTML source using Chromium:

```powershell
python -m http.server 8080 --bind 127.0.0.1
.\.venv\Scripts\playwright.exe pdf --paper-format A4 http://127.0.0.1:8080/assets/cv/Shabi-Levanda-CV.html assets/cv/Shabi-Levanda-CV.pdf
```

After regeneration, rerun the complete test suite. The gate uses `pypdf` to enforce one page, extract and privacy-scan the real PDF text, and verify that required sections remain intact. Rasterize and visually inspect the actual PDF before release; an HTML preview alone is insufficient.
