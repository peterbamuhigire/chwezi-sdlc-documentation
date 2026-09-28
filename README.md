# SRS Skills Engine

The SRS Skills Engine is a portable library for requirements and software-lifecycle documentation, organised into nine numbered phases. Its 159 active skills help teams turn documented project context into standards-informed PRDs, business cases, requirements specifications, design records, acceptance criteria, test plans, release evidence, operational handoffs, and governance artefacts. Phase outputs are recorded in project files for downstream review and traceability; missing stakeholder decisions or project evidence remain open questions rather than invented requirements.

It is for product owners, business analysts, software architects, delivery teams, testers, operators, and governance or compliance reviewers. The workflows support waterfall, agile, and hybrid documentation needs and provide domain overlays; they help teams define, verify, and hand off work but do not replace engineering execution or specialist legal and compliance review.

## Installation

For Claude Code, install the native plugin:

```text
/plugin marketplace add https://github.com/peterbamuhigire/srs-skills
/plugin install srs@chwezi-srs
```

Or clone the repository and run its installer (Node.js 18 or later):

```sh
git clone https://github.com/peterbamuhigire/srs-skills
cd srs-skills
./install.sh --scope project       # macOS, Linux, or Git Bash
.\install.ps1 --scope project      # Windows PowerShell
```

## Skills

| Phase | Skills | Coverage |
|---|---:|---|
| `01-strategic-vision` | 13 | Product vision, PRDs, business cases, product framing, and scoping |
| `02-requirements-engineering` | 41 | Elicitation, analysis, requirements specifications, models, traceability, and agile/hybrid flows |
| `03-design-documentation` | 18 | Architecture, API, UX, infrastructure, and domain-specific design records |
| `04-development-artifacts` | 6 | Development guidance and implementation-facing specifications |
| `05-testing-documentation` | 10 | Test strategies, acceptance, verification, and AI evaluation plans |
| `06-deployment-operations` | 23 | Release readiness, deployment, monitoring, incident response, and operations documentation |
| `07-agile-artifacts` | 5 | Agile team agreements, completion criteria, retrospectives, and experiments |
| `08-end-user-documentation` | 9 | Onboarding, customer success, user guidance, and sales enablement |
| `09-governance-compliance` | 34 | Reviews, traceability, privacy and responsible-AI records, compliance documentation, and improvement |

## References

- [SRS Skills Engine repository](https://github.com/peterbamuhigire/srs-skills) — capability inventory and public source repository; checked against [`AGENTS.md`](AGENTS.md), [`rules/common/core.md`](rules/common/core.md), [`rules/common/phase-handoff.md`](rules/common/phase-handoff.md), and the nine phase directories.
- No external books or standards documents were consulted for this README.
