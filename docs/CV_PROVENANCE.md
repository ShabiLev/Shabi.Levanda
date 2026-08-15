# CV Provenance and Privacy Review

## Authoritative sources

The requested `SHABI LEVANDA(1).docx` was not present anywhere under the user profile. The safest available historical substitute was inspected in full:

`Shabi_Levanda_Resume_Updated.docx` — modified 2026-01-01, SHA-256 `f6c04f0cb0262e67dd6655e10aa326d6f2da16b3909fdb702f768f049ac30365`.

The source document is not copied into the public repository. Public portfolio repositories and the existing approved resume landing page provide current engineering/project corroboration.

Repository-owned source and artifact:

- `assets/cv/Shabi-Levanda-CV-EN.html`
- `assets/cv/Shabi-Levanda-CV-EN.pdf`

The superseded one-page `Shabi-Levanda-CV.html` and `.pdf` artifacts were removed from the deployable tree so stale `22+` copy cannot remain reachable at a legacy path.

## Preserved facts

- more than 20 years in high-tech and 10+ years in QA leadership
- Cello (formerly Cellopark), Terminal X, Cellebrite and Elbit chronology
- 20% development-cycle reduction and 40–50% defect/data-error reduction
- team leadership, mentoring, hands-on testing, Agile, release quality and system engineering
- Jira, Xray, Confluence, SQL, MongoDB, Python, automation and test documentation
- Python Automation Full-Stack training, Hebrew/English languages and Police Patrol volunteering
- verified public email, LinkedIn and GitHub profiles
- current Prompt, Context and Agentic Engineering capability, supported by public engineering repositories

Claims found only in a stronger older DOCX—24+/13+, additional 30%/40% metrics and Acting Program Manager—were not used.

## Intentional exclusions

- phone number and QR/vCard data
- the historical source DOCX
- military-service dates, employee locations and testimonials
- home/location, identity or family information
- internal company, customer, tenant or production information
- private repository URLs or configuration

## Generation and gate

```powershell
$cvPath = (Resolve-Path assets\cv\Shabi-Levanda-CV-EN.html).Path
$cvUri = [System.Uri]::new($cvPath).AbsoluteUri
.\.venv\Scripts\playwright.exe pdf --paper-format A4 $cvUri assets\cv\Shabi-Levanda-CV-EN.pdf
.\.venv\Scripts\python.exe -m pytest -q
```

The automated gate uses `pypdf` to enforce exactly two pages, extract and privacy-scan the real PDF text, verify page-specific roles and assert that required ending content is present. PyMuPDF geometry additionally enforces at least 18 points of bottom clearance on every page. Both actual PDF pages must also be rasterized and visually inspected at 100% before release.

## Hebrew CV boundary

The Hebrew website is complete in RC2. A Hebrew PDF was not generated because this pass did not include an independently reviewed professional Hebrew CV translation. Publishing a weak automated translation would be lower quality than linking the verified English artifact. `Shabi-Levanda-CV-HE.pdf` remains an explicit follow-up.
