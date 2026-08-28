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

## Mandatory capability evidence matrix

| Capability | Current website | Current CV | Evidence | Gap | Action |
|---|---|---|---|---|---|
| QA leadership | Strong | Strong | Approved roles, chronology, leadership bullets and impact | None | Retain as foundation |
| Release management | Strong project framing | Present | Career release validation; FlowProof; release command center | Positioning, not historical title | Keep as capability; preserve actual job titles |
| Automation | Public projects | Strong | Python mobile automation; Playwright/Pytest framework | Purpose was fragmented | Frame as repeatable engineering productivity |
| Python | Project cards | Present | Automation framework, training and data workflows | Not a historical developer title | Retain as hands-on capability |
| Selenium | Project-adjacent | Present | Approved professional training | Limited public project depth | Keep in competencies only |
| Playwright | Strong | Present | Public framework and this repository's browser suite | Recent/project capability | Retain |
| Appium | Absent | Removed from V2 | Generic prior CV tool list only; no artifact-level proof | **UNVERIFIED — DO NOT PUBLISH** | Exclude until primary evidence is available |
| API | Present in work framing | Present | REST/Postman training and Cello/Terminal X environments | Lightly described | Keep naturally under automation/investigation |
| SQL | New dedicated pillar | Stronger | SQL Server/T-SQL operational investigation knowledge and approved CV context | Was generic | Publish generalized, purpose-led wording |
| MongoDB | CWL and pipeline evidence | Stronger | Multi-tenant workspace, aggregation/schema and export workflows | Underrepresented | Publish generalized schema/tenant/reconciliation wording |
| BI | New engineering analytics pillar | Present | Operational reports, KPI and decision-support work | No formal BI title | Publish only as engineering analytics capability |
| Metabase | Present | Present | Parameterized operational reporting evidence | Previously absent | Add as reporting tool, not formal job title |
| Dashboards | General decision-support language | Absent as ownership claim | Reporting/KPI context without named owned dashboard artifact | **UNVERIFIED — DO NOT PUBLISH** as dashboard ownership | Use operational reporting/visibility wording only |
| Data investigation | Present | Present | SQL/Mongo production and defect investigation context | Previously generic | Make purpose explicit |
| Reconciliation | Present | Present | SQL controls and multi-tenant source/export count validation | Previously absent in CV | Retain |
| CI/CD | Present | Present | Portfolio CI and training/project evidence | Broad enterprise ownership not proved | Keep as capability only |
| GitHub Actions | Repository evidence | Present | `.github/workflows/portfolio-ci.yml` and public project workflows | None | Retain |
| Jenkins | Absent | Absent | Profile mention without current repository/CV provenance | **UNVERIFIED — DO NOT PUBLISH** | Exclude until primary evidence is available |
| AI | Major differentiator | Major section | Public AI projects and central operating model | Needed safer category | Use Applied AI, never AI research/model training |
| Prompt engineering | Dedicated capability | Present | Structured prompt contracts and project work | None | Retain |
| Context engineering | Dedicated capability | Present | Repository-aware scoping, constraints and handoffs | None | Retain |
| Agents | Dedicated capability | Present | Central specialist-agent platform and public references | Must avoid autonomy hype | Describe bounded specialist roles |
| Orchestration | Dedicated flow | Present | Conductor-led execution graph and quality gates | None | Retain with human boundaries |
| AI governance | Dedicated capability | Present | Independent QA, deterministic checks, evidence and human gates | None | Retain |
| Project/product execution | Demonstrated by selected work | Present through projects | Public repositories and AI-assisted execution methodology | Not a historical Product Manager title | Publish only as applied execution capability |

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
