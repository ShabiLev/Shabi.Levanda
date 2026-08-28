# Portfolio V2 evidence audit

Reviewed: 2026-08-28

| Capability | Current site/CV evidence | Gap found | V2 action |
|---|---|---|---|
| QA leadership | Verified roles, chronology, team leadership and approved impact figures | None; risk of dilution | Retained as the professional foundation |
| Release governance | Career bullets, FlowProof and QA Release Command Center | Positioned separately from data/AI | Integrated into delivery-engineering positioning |
| Automation | Python mobile automation and public Playwright/Pytest work | Tool list lacked a coherent operating purpose | Framed as engineering productivity and repeatable verification |
| SQL Server / T-SQL | Approved CV context and operational SQL knowledge source | Generic `SQL` only | Added operational investigation, reconciliation and reporting purpose |
| MongoDB | CWL Office and multi-tenant pipeline evidence | Underrepresented in CV | Added schema-aware, tenant-aware and validation language |
| Metabase / BI | Parameterized operational reporting evidence | Absent | Added Metabase and engineering decision-support framing |
| Data automation | Python export, filtering, provenance and reconciliation evidence | Absent | Added generalized public-safe capability wording |
| Applied AI | Public projects and central Conductor operating model | Category sounded narrower than the actual method | Renamed to Applied AI & Agentic Engineering; added human decision gate |

## Publication exclusions

The V2 public claim registry intentionally excludes formal titles such as Data Engineer,
BI Developer, Data Scientist, ML Researcher and AI Researcher. MySQL, Jenkins, specific
Appium ownership and dashboard ownership remain unpublished until stronger evidence is
available. No customer data, production identifiers, credentials or private endpoints are
used in V2 copy.

## Source-of-truth boundary

`data/verified-profile.json` is the canonical registry for public positioning, four pillars,
competency families, impact sources and publication exclusions. The authored English site
and CV source must contain its critical invariants. `scripts/verify_profile_sync.py` enforces
that contract, while `scripts/generate_cv_pdf.py` produces the committed PDF derivative.
