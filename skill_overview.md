# Skill Pipeline Registry

This registry documents the inputs, process logic, governing standards, and outputs for each skill in the Chwezi SDLC Documentation pipeline. It is formatted as an Engineering Interface Control Document to ensure compliance with ISO/IEC 15504 and IEEE 1002 taxonomy requirements.

## Path Interpretation

Repository-level pathing is canonicalized to `projects/<ProjectName>/...`.

- `projects/<ProjectName>/_context/` is the source of truth for project inputs.
- Table entries that still show `../project_context/` and `../output/` are legacy execution aliases preserved for compatibility with existing skill-local instructions.
- Read those aliases as references into the active project workspace, not as a separate repository architecture.

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-initialize-srs | User input, existing context, project anchors | Populate ../project_context/ with IEEE/ISO-driven templates, ensuring baseline artifacts and seeds exist | ISO/IEC 15504 – Process Assessment Framework; IEEE 1074 – Software Life Cycle Process | Seeded templates in ../project_context/ (vision.md, tech_stack.md, features.md, business_rules.md, quality_standards.md, glossary.md) |
| 02-context-engineering | ../project_context/vision.md, glossary.md | Synthesize Introduction, Purpose, and Definition sections guided by stakeholder vision and terminology | IEEE 830 Clause 5.1 – Introduction | ../output/SRS_Draft.md Section 1.0 (Purpose, Scope, Definitions) |
| 03-descriptive-modeling | ../project_context/tech_stack.md, features.md | Map environment, constraints, and capability descriptions, aligning system context with feature candidates | IEEE 830 Clause 5.2 – Overall Description | ../output/SRS_Draft.md Section 2.0 (Overall Description, System Overview) |
| 04-interface-specification | ../project_context/tech_stack.md | Conduct connectivity and interface audit versus infrastructure stack, documenting protocols and interoperability controls | IEEE 1233 – System Requirements Development; ISO/IEC 25051 – Software Product Quality Requirements | ../output/SRS_Draft.md Section 3.1 (External Interfaces) |
| 05-feature-decomposition | ../project_context/features.md | Break down functional capabilities into stimulus/response pairs with verifiable SHALL statements | IEEE 830 Clause 5.3.1 – Functional Requirements (Feature-Based) | ../output/SRS_Draft.md Section 3.2 (Functional Requirements) |
| 06-logic-modeling | ../project_context/business_rules.md | Formalize algorithms, formulas, and decision tables (LaTeX where appropriate), capturing logic invariants for requirements | IEEE 1016 – Standards for Software Design Descriptions (Logic Mapping) | ../output/SRS_Draft.md Sections 3.2.x (Data/Logic Details) |
| 07-attribute-mapping | ../project_context/quality_standards.md | Enforce NFR metrics, describing performance, security, reliability, and other quality attributes with traceable targets | ISO/IEC 25010 – Software Product Quality | ../output/SRS_Draft.md Sections 3.3–3.6 (Attribute-based Requirements) |
| 08-semantic-auditing | ../output/SRS_Draft.md (full draft) | Validate completeness, consistency, and traceability; generate audit report and requirements traceability matrix | IEEE 1012 – Verification & Validation | ../output/Traceability_Matrix.md and Audit_Report.md (plus updated SRS draft sections) |

## Phase 01: Strategic Vision

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 03-vision-statement | ../project_context/vision.md, stakeholders.md, glossary.md | Generate formal vision document with elevator pitch, product positioning (Geoffrey Moore template), value propositions, and SMART success criteria | IEEE 29148-2018 Sec 6.2 – Stakeholder Requirements Definition | ../output/Vision_Statement.md |
| 01-prd-generation | ../project_context/vision.md, features.md, stakeholders.md; optionally ../output/Vision_Statement.md | Generate Product Requirements Document with market context, SMART objectives, feature priority matrix (MoSCoW), and success metrics | IEEE 29148-2018; IEEE 1233-1998 – System Requirements Development | ../output/PRD.md |
| 02-business-case | ../project_context/vision.md, stakeholders.md; optionally ../output/PRD.md | Generate business case with cost-benefit analysis (NPV), ROI projection, risk assessment matrix, and go/no-go criteria | IEEE 1058-1998 – Software Project Management Plans | ../output/Business_Case.md |

### Phase 01 Outcome Discovery And Premium Positioning Additions

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 04-lean-canvas | vision.md, features.md, stakeholders.md, discovery evidence | Generate Lean Canvas, Impact Map, Hypothesis Board, discovery interview plan, and validation thresholds for uncertain products | IEEE 29148; Lean Customer Development; Impact Mapping | Lean_Canvas.md, impact map, hypothesis board |
| 07-premium-product-positioning | buyer/user context, pricing intent, proof assets, service model | Convert premium positioning into measurable product, UX, proof, support, adoption, governance, and service requirements | IEEE 29148; premium product strategy | Premium positioning requirements and quality gate |

## Phase 02: Agile Requirements Track

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-user-story-generation | ../project_context/vision.md, features.md, personas.md | Transform features into INVEST-compliant user stories with acceptance criteria, story points, and epic breakdown | IEEE 29148-2018 Sec 6.4; INVEST Criteria | ../output/user_stories.md, epic_breakdown.md, backlog_summary.md |
| 02-acceptance-criteria | ../output/user_stories.md; optionally ../project_context/quality_standards.md | Formalize Given-When-Then acceptance criteria per story with NFR criteria and testability validation | IEEE 29148-2018 Sec 6.4.5 – Requirements Specification | ../output/acceptance_criteria.md |
| 03-story-mapping | ../output/user_stories.md, epic_breakdown.md | Build Jeff Patton story maps with backbone activities, walking skeleton, and release slices | IEEE 29148-2018; Jeff Patton Story Mapping (2014) | ../output/story_map.md, story_map.mmd |
| 04-backlog-prioritization | ../output/user_stories.md, ../project_context/vision.md | Prioritize backlog using MoSCoW classification and WSJF scoring, allocate stories to sprints | IEEE 29148-2018 Sec 6.4.6; SAFe WSJF | ../output/prioritized_backlog.md, release_plan.md |

### Phase 02 Experience And Service Requirements Additions

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 11-experience-mapping-requirements | journey evidence, interviews, analytics, support logs, stakeholder register | Convert journey stages, touchpoints, pain points, evidence, and future-state opportunities into traceable SDLC requirements | IEEE 29148; ISO 9241-210; experience mapping | experience_mapping_requirements.md |
| 12-service-blueprint-requirements | service scenario, journey/process evidence, support model, operational actors | Convert frontstage/backstage actions, handoffs, evidence, service failures, and recovery into product, support, governance, and rollout requirements | IEEE 29148; ISO 9241-210; service design | service_blueprint_requirements.md |

## Phase 03: Design Documentation

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-high-level-design | ../output/SRS_Draft.md, ../project_context/tech_stack.md | Generate system architecture with component, deployment, and data flow diagrams (Mermaid), technology decisions, and traceability | IEEE 1016-2009 Sec 5 – Design Viewpoints | ../output/HLD.md |
| 02-low-level-design | ../output/HLD.md, SRS_Draft.md, ../project_context/business_rules.md | Decompose HLD into module specs with class, sequence, and state diagrams (Mermaid), algorithm formalization (LaTeX), error handling design | IEEE 1016-2009 Sec 6 – Design Elements | ../output/LLD.md |
| 03-api-specification | ../output/SRS_Draft.md, HLD.md, ../project_context/tech_stack.md | Generate REST API endpoint definitions, schemas, auth, error format, and machine-readable OpenAPI 3.1 YAML | OpenAPI 3.1.x; IEEE 29148-2018; RFC 9110; RFC 9457 | ../output/API_Specification.md, openapi.yaml |
| 04-database-design | ../output/SRS_Draft.md, HLD.md, ../project_context/business_rules.md, tech_stack.md | Generate ERD (Mermaid), normalized table definitions, indexing strategy, data dictionary, migration strategy. MANDATORY: mysql-best-practices for MySQL | IEEE 1016-2009 Sec 6.7; ISO/IEC 25010 | ../output/Database_Design.md, erd.mmd |

### Phase 03 Strategy And UX Content Additions

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 08-engineering-strategy-brief | PRD/SRS, tech stack, risks, constraints, current architecture, quality attributes | Produce engineering strategy diagnosis, guiding policies, coherent actions, operating mechanisms, ADR candidates, and SaaS assumptions | IEEE 1016; engineering strategy | Engineering_Strategy_Brief.md |
| 09-ux-content-and-form-specification | UX spec, SRS/user stories, personas, existing screens/forms, content evidence | Generate UX content, microcopy, form, validation, error-state, accessibility, and completion-metric requirements | ISO 9241-210; WCAG 2.1 AA | UX_Content_And_Form_Specification.md |

## Phase 04: Development Artifacts

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-technical-specification | ../output/SRS_Draft.md, HLD.md, LLD.md | Generate module-level technical specifications with interface contracts, data structures, algorithm details, and error handling design | IEEE 1016-2009; IEEE 830-1998 | ../output/Technical_Specification.md |
| 02-coding-guidelines | ../project_context/tech_stack.md, quality_standards.md | Generate coding standards document covering naming conventions, formatting, patterns, error handling, and code review criteria | IEEE 730 – Software Quality Assurance | ../output/Coding_Guidelines.md |
| 03-dev-environment-setup | ../project_context/tech_stack.md | Generate developer environment setup guide with toolchain installation, build configuration, local development workflow, and troubleshooting | IEEE 1074 – Software Life Cycle Process | ../output/Dev_Environment_Setup.md |
| 04-contribution-guide | ../project_context/tech_stack.md, vision.md | Generate contribution guidelines covering branching strategy, commit conventions, PR workflow, code review standards, and CI/CD integration | IEEE 1074 – Software Life Cycle Process | ../output/Contribution_Guide.md |

## Phase 05: Testing Documentation

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-test-strategy | ../project_context/quality_standards.md, tech_stack.md; ../output/SRS_Draft.md (optional) | Generate test strategy defining test levels, types, tools, environments, entry/exit criteria, and risk-based test prioritization | IEEE 829 Sec 6 – Test Strategy | ../output/Test_Strategy.md |
| 02-test-plan | ../output/Test_Strategy.md, SRS_Draft.md; ../project_context/features.md | Generate detailed test plan with test cases, traceability to requirements, test data requirements, schedule, and resource allocation | IEEE 829 Sec 7-8 – Test Plan | ../output/Test_Plan.md |
| 03-test-report | ../output/Test_Plan.md | Generate test execution report template with pass/fail summary, defect analysis, coverage metrics, and release recommendation | IEEE 829 Sec 9-10 – Test Report | ../output/Test_Report_Template.md |

## Phase 06: Deployment & Operations

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-deployment-guide | ../project_context/tech_stack.md; ../output/HLD.md (optional) | Generate step-by-step deployment procedures with pre/post-deployment checklists, rollback procedures, and environment-specific configurations | IEEE 1062 – Software Acquisition | ../output/Deployment_Guide.md |
| 02-runbook | ../output/Deployment_Guide.md (optional); ../project_context/tech_stack.md | Generate operational runbook with incident response procedures, escalation paths, health checks, and recovery playbooks per SRE practices | SRE Best Practices | ../output/Runbook.md |
| 03-monitoring-setup | ../project_context/tech_stack.md, quality_standards.md | Generate monitoring configuration guide with metrics definitions, alerting rules, dashboard specifications, and SLI/SLO targets | ISO/IEC 25010 – Software Product Quality | ../output/Monitoring_Setup.md |
| 04-infrastructure-docs | ../project_context/tech_stack.md; ../output/HLD.md (optional) | Generate infrastructure documentation with architecture diagrams (Mermaid), resource inventory, networking topology, and scaling policies | IEEE 1016-2009 – Software Design Descriptions | ../output/Infrastructure_Docs.md |

### Phase 06 Rollout And Support Additions

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 05-go-live-readiness | deployment guide, runbook, monitoring, test report, support/training evidence | Generate go-live readiness assessment, blocker register, launch control plan, and go/no-go recommendation | Operational readiness; transition governance | Go_Live_Readiness.md |
| 06-customer-adoption-and-support-plan | release scope, stakeholder roles, user docs, support model, known risks, service levels | Generate adoption, training, rollout communication, service desk, escalation, recovery, maintenance, and feedback-loop plan | Transition governance; service design | Customer_Adoption_And_Support_Plan.md |

## Phase 07: Agile Artifacts

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-sprint-planning | ../project_context/vision.md; ../output/prioritized_backlog.md, user_stories.md | Generate sprint planning template with sprint goal, team capacity calculation, selected backlog items, task breakdown, and risk tracking | Scrum Guide; IEEE 29148-2018 | ../output/Sprint_Planning_Template.md |
| 02-definition-of-done | ../project_context/quality_standards.md, tech_stack.md | Generate Definition of Done checklist covering code quality, testing, documentation, review, and deployment readiness at story, increment, and release levels | Scrum Guide | ../output/Definition_of_Done.md |
| 03-definition-of-ready | ../project_context/vision.md, features.md | Generate Definition of Ready checklist ensuring backlog items have acceptance criteria, sizing, dependency resolution, and design clarity before sprint commitment | Scrum Guide | ../output/Definition_of_Ready.md |
| 04-retrospective-template | ../project_context/vision.md | Generate sprint retrospective template with multiple facilitation formats (Start-Stop-Continue, 4Ls, Sailboat), action item tracking, and improvement metrics | Scrum Guide | ../output/Retrospective_Template.md |

## Phase 08: End-User Documentation

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-user-manual | ../project_context/vision.md, features.md; ../output/SRS_Draft.md (optional) | Generate comprehensive user manual with getting started guide, feature guides, role-based workflows, troubleshooting, and glossary | ISO 26514 – User Documentation | ../output/User_Manual.md |
| 02-installation-guide | ../project_context/tech_stack.md; ../output/Deployment_Guide.md (optional) | Generate step-by-step installation instructions with system requirements, prerequisites, configuration, verification, and common issues | ISO 26514 – User Documentation | ../output/Installation_Guide.md |
| 03-faq | ../project_context/vision.md, features.md; ../output/User_Manual.md (optional) | Generate structured FAQ organized by category with clear question-answer pairs and cross-references to detailed documentation | ISO 26514 – User Documentation | ../output/FAQ.md |
| 04-release-notes | ../project_context/vision.md; ../output/SRS_Draft.md (optional) | Generate release notes template with version tracking, new features, bug fixes, breaking changes, migration instructions, and known issues | IEEE 830-1998 | ../output/Release_Notes_Template.md |

## Phase 09: Governance & Compliance

| Skill ID & Name | Inputs | Process Logic | Governing Standard | Primary Output |
|-----------------|--------|----------------|-------------------|----------------|
| 01-traceability-matrix | ../output/SRS_Draft.md (required); HLD.md, LLD.md, user_stories.md (optional); ../project_context/vision.md | Generate requirements traceability matrix mapping every requirement to source, design element, test case, and implementation status with gap analysis | IEEE 1012-2016 – Verification & Validation | ../output/Traceability_Matrix.md |
| 02-audit-report | ../output/Traceability_Matrix.md, SRS_Draft.md (required); ../project_context/quality_standards.md | Generate V&V audit report assessing completeness, consistency, correctness with severity-rated findings and remediation recommendations | IEEE 1012-2016 – Verification & Validation | ../output/Audit_Report.md |
| 03-compliance-documentation | ../project_context/vision.md, quality_standards.md; ../output/SRS_Draft.md, HLD.md (optional) | Generate compliance documentation mapping requirements to applicable regulatory frameworks (GDPR, HIPAA, SOC2) with gap analysis and remediation roadmap | GDPR; HIPAA; SOC2 | ../output/Compliance_Docs.md |
| 04-risk-assessment | ../project_context/vision.md, quality_standards.md; ../output/SRS_Draft.md, HLD.md (optional) | Generate systematic risk assessment with probability/impact matrix, risk register, mitigation strategies, and monitoring plan per ISO 31000 framework | ISO 31000; IEEE 1012-2016 | ../output/Risk_Assessment.md |
| 28-anti-ai-slop | Any generated SRS/spec/doc/code draft; ../project_context/ | MANDATORY pre-ship gate: apply the seven universal anti-slop guardrails, the merged banned-vocabulary + IEEE-982.1 adjective list, and the SRS/spec avoidance block; promote unmet items to V&V fail tags | Merriam-Webster 2025 WOTY; Kommers et al. arXiv 2601.06060; this engine's Principle 7 | Ship/no-ship decision + ticked gate checklist + fail tags |
| 29-ai-slop-audit | Any artefact to evaluate (SRS, spec, requirement, doc, system, codebase) | AUTO-RUN on analyse/review/evaluate/audit/de-slop requests: layered automated + human-judgement audit, 0–100 genericness score, graded A–F report with evidence and concrete fixes mapped to V&V tags | Kommers et al. arXiv 2601.06060; Spracklen et al. USENIX Security 2025; Veracode; GitClear | Graded AI Slop Audit report |

## Verification Gateways

1. Each skill ingests the output of the preceding phase as its baseline artifact (e.g., Skill 02 uses the vision/glossary created by Skill 01). This ensures traceability of inputs back to original templates.
2. Skill 05 requires the Feature catalog generated by Skills 01–03; Skill 06 and Skill 07 enforce data/logic and quality attributes flowing from Skill 05 definitions.
3. Skill 08 performs the terminal verification gate: it reads the entire SRS draft produced by Skills 02–07, confirms compliance with the cited standards, and emits the traceability matrix plus audit report. Passing Skill 08 is mandatory before any new iteration of Skill 01 to preserve integrity across the pipeline.
4. Phase 01 (Strategic Vision) produces Vision_Statement.md and PRD.md that feed into Phase 02 as upstream context. Business_Case.md provides the go/no-go decision gate.
5. Phase 02 Agile track skills execute sequentially: user stories → acceptance criteria → story mapping → backlog prioritization. Each consumes the prior skill's output.
6. Phase 03 (Design Documentation) requires Phase 02 outputs (SRS_Draft.md or user_stories.md). HLD runs first; LLD, API Spec, and Database Design can run in parallel after HLD completes. Each design artifact traces back to SRS requirements.
7. Phase 04 (Development Artifacts) skills are independent and may run in any order after Phase 03 design docs are available.
8. Phase 05 (Testing Documentation) executes sequentially: test strategy → test plan → test report. Test strategy establishes the framework; test plan requires it as input.
9. Phase 06 (Deployment & Operations) skills are largely independent. Deployment guide typically runs first; runbook and monitoring can run in parallel after it.
10. Phase 07 (Agile Artifacts) skills are independent and may run in any order. Sprint planning typically references Phase 02 agile outputs (prioritized backlog, user stories).
11. Phase 08 (End-User Documentation) skills are independent. User manual and installation guide are typically generated first as they are most critical for end users.
12. Phase 09 (Governance & Compliance) is the terminal verification phase. Run 01-traceability-matrix first as it feeds the audit report. Skills 03 (compliance) and 04 (risk) are independent and can run in parallel after 01 and 02 complete.
