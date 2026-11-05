# AI Assistant Use Section (optional)

Parent skill: [02-coding-guidelines](../SKILL.md). Load this reference when the project's `Coding_Guidelines.md` shall state how the team uses artificial intelligence (AI) coding assistants: tools that suggest, generate, explain or edit code inside the team's own repository.

The section is optional. It adds one section to the document, numbered 9, after the Code Review Checklist. It defines what the guidelines shall say. The community development engine owns how to write instruction files, review AI-generated changes and configure an assistant (see section 7).

## 1. When this section applies

| Request | Action |
|---|---|
| A team asks for coding guidelines that include rules for its own use of AI coding assistants | Add section 9 using this reference. |
| Code in the product calls a model, builds prompts, runs retrieval or executes agent tools | Apply [ai-coding-guidelines-addendum.md](ai-coding-guidelines-addendum.md). Do not add section 9 for that reason alone. |
| The document is the coding guidelines of an AI-agent product (tool schemas, reversibility, blast-radius caps, idempotency, timeouts, approval gates) | Route to `05-ai-agent-coding-guidelines-addendum`. Do not add section 9 for that reason alone. |
| The team uses no assistant and plans none | Omit section 9. Record "not applicable: no assistant in use" in the decision and gap register. |
| It is unknown whether the team uses an assistant | Stop this branch. Record `[CONTEXT-GAP: assistant use]` with the owner who can answer. |

A team can need both section 9 and the addendum, for example a team that builds an AI feature and also uses an assistant to write it. The two cover different subjects: section 9 governs the people writing code, the addendum governs the code that runs.

## 2. Required content

Section 9 shall contain eight elements, in this order, each under its own heading numbered 9.1 to 9.8. Each rule inside an element shall be written as a stimulus and a response ("When a change includes assistant-generated code that touches authentication, the reviewer shall ..."), name a role, not a person, and carry a verification method.

| ID | Element | Required content | Source in the project | Acceptance condition |
|---|---|---|---|---|
| AU-1 | Encouraged uses and ownership | Uses the team welcomes (for example test planning, documentation drafts, code explanation, refactoring suggestions, migration help, comparing alternatives), each with the check the developer makes against existing behaviour. A sentence that the developer who submits a change owns every line in it. | Team decision, recorded with its owner | At least one use is listed with its check. The ownership sentence names the submitter role. |
| AU-2 | Uses that need extra review | Each use that needs a second reader, the reviewer role and what the reviewer checks. | Risk register, high-level design | Every listed use names a reviewer role and a review step. |
| AU-3 | Output not accepted without human approval | Each category of output that needs named approval before merge, and the approver role. | Security requirements, risk decisions | Every category names an approver role. An empty list states "none" with the owner's decision. |
| AU-4 | Architecture rules the assistant cannot know | Where business logic, data access and validation live; which layers may depend on which; which imports cross no boundary; how errors are represented; permitted and discouraged patterns; the dependency policy. | High-level design, low-level design, architecture decision records | Every rule cites the artefact it comes from and names the check that enforces it (a lint rule, an import-boundary check or a review item). |
| AU-5 | Testing expectations for assisted changes | Minimum tests per change type and how test independence is kept: a test is shown to fail when the behaviour is wrong, and is not derived only from the implementation under test. | Test strategy | Minimum tests are stated per change type. The independence rule is stated. |
| AU-6 | Security requirements that always apply | A pointer to section 7 (Security Practices), and the classes of data that shall not be sent to an assistant (secrets, personal data, tenant data). | Data classification, section 7 | Each class of data maps to the project's data classification, or the gap is recorded. |
| AU-7 | Disclosure and review of assisted work | What the author states in the change description (assistant involved, which parts, what was verified) and what the reviewer checks. | Contribution guide, pull request template | The record location is named, and the reviewer's check is a numbered step. |
| AU-8 | Instruction files | Each file the assistants read, its repository path, the owner role, the change control, the review trigger, and which document wins when the file and `Coding_Guidelines.md` differ. | Repository layout, owner decision | Every file has a path, an owner role and a review step. The precedence rule is stated. |

Keep the first version short. A section that nobody reads cannot be applied, so write each element as a short list of rules and put the detail in the artefact the rule cites.

## 3. What the section shall not contain

- Statements about what a particular assistant product can do or which file name it reads. Those facts change; name the files the team uses and cite the tool's own documentation read on a dated day if a claim is needed.
- Rules the team has not decided. Record an undecided rule in the decision and gap register with its owner; do not draft a default.
- Per-developer prompts. Shared prompts that the team has agreed belong in the instruction files (AU-8), under change control.

## 4. Applying the checklist by hand

No automated document-conformance check exists for coding guidelines. The check is a reviewer's reading, so state it as `not assessed` by tools and record the reviewer.

1. For each element AU-1 to AU-8, find its heading in section 9. If the heading is absent, the element is FAIL.
2. Read the acceptance condition in the table in section 2. Mark PASS only when the text satisfies every part of it. Quote the line that satisfies it.
3. Mark FAIL when any part is missing, and name the missing part.
4. Section 9 passes when all eight elements are PASS. Any FAIL returns the draft to its owner with the failing element and the missing part.

## 5. Worked example A (passes)

Fictional project: Harbour Tracker, a multi-tenant shipment tracking web application (TypeScript, PostgreSQL). The excerpt shows each element in short form.

```markdown
## 9. AI Assistant Use
Version 1.2 | Owner: Engineering lead | Reviewed with section 8

### 9.1 Encouraged uses and ownership (AU-1)
- Developers may use an assistant to draft test plans, explain unfamiliar modules and propose refactorings. The developer compares each proposal with the module's current behaviour, using its existing tests, before accepting it.
- The developer who opens a pull request owns every line in it, including lines an assistant wrote.

### 9.2 Uses that need extra review (AU-2)
- When an assistant proposes a database migration, the data reviewer shall run it on a copy of the staging data and confirm the row counts before merge.

### 9.3 Output not accepted without human approval (AU-3)
- Authentication, authorisation and tenant-scoping code: approver is the security lead.
- Cryptography and secret handling: approver is the security lead.

### 9.4 Architecture rules the assistant cannot know (AU-4)
- R1. Business logic lives in `src/domain`; request handlers call it and contain none (ADR-004). Check: lint rule `no-logic-in-handlers`.
- R2. Every query carries the tenant identifier from the session, never from request input (ADR-007). Check: review item T-2 and the tenant-isolation test suite.
- R3. `src/ui` imports nothing from `src/data` (HLD section 4.2). Check: import-boundary rule in the build.

### 9.5 Testing expectations for assisted changes (AU-5)
- Every change to `src/domain` includes a unit test for each new branch. The reviewer confirms each new test fails when the changed line is reverted. A test generated from the implementation alone does not count.

### 9.6 Security requirements that always apply (AU-6)
- Section 7 applies in full.
- Secrets, customer shipment records and personal data (classes S1, S2 and P1 in the data classification) shall not be pasted into an assistant.

### 9.7 Disclosure and review of assisted work (AU-7)
- The author completes the "Assistant involvement" field of the pull request template: tool, files touched, what was verified.
- Reviewer step 5 of the review checklist: confirm the field is complete and sample one assisted function by reading it line by line.

### 9.8 Instruction files (AU-8)
- `AGENTS.md` in the repository root. Owner: Engineering lead. Changes go through a pull request reviewed by two engineers, as for this document. Review trigger: any change to R1 to R3 or to the data classification.
- Precedence: when `AGENTS.md` and this document differ, this document wins and `AGENTS.md` is corrected in the same pull request.
```

Applying the checklist:

| ID | Quoted evidence | Verdict |
|---|---|---|
| AU-1 | 9.1: "compares each proposal with the module's current behaviour"; "owns every line in it" (submitter role: developer who opens the pull request) | PASS |
| AU-2 | 9.2: data reviewer runs the migration on a staging copy and confirms row counts | PASS |
| AU-3 | 9.3: both categories name the security lead | PASS |
| AU-4 | 9.4: R1 to R3 each cite ADR-004, ADR-007 or HLD 4.2 and name a check | PASS |
| AU-5 | 9.5: tests per `src/domain` change; revert-and-fail check; implementation-only tests excluded | PASS |
| AU-6 | 9.6: pointer to section 7; classes S1, S2, P1 mapped to the data classification | PASS |
| AU-7 | 9.7: pull request field named; reviewer step 5 | PASS |
| AU-8 | 9.8: path, owner, two-engineer review, trigger and precedence all present | PASS |

Result: 8 of 8 PASS. Section 9 is accepted.

## 6. Worked example B (fails)

Example B repeats 9.1 to 9.7 of example A unchanged and replaces 9.8 with:

```markdown
### 9.8 Instruction files (AU-8)
- Assistants read the repository instructions and follow them.
```

| ID | Quoted evidence | Verdict |
|---|---|---|
| AU-1 to AU-7 | Same text as example A | PASS |
| AU-8 | 9.8: "Assistants read the repository instructions and follow them." Missing: no file is named, so there is no path; no owner role; no change control or review trigger; no precedence rule. Four of the four required parts are absent. | FAIL |

Result: 7 of 8 PASS, 1 FAIL. Section 9 is returned to its owner with this note: "AU-8 lacks the file name and path, owner role, review step and precedence rule." The document is not released until AU-8 passes.

Both examples were applied by hand when this reference was written. They are synthetic; they describe no real project.

## 7. Where the how lives

The community development engine, resolved through the engine-routing table, owns the procedures this section points to. Read the skill before writing the matching element.

| Element | Community development engine skill | What it owns |
|---|---|---|
| AU-7, AU-5 | `sdlc-meta/ai-assisted-development`, its AI-generated code review gate | How a reviewer checks an AI-generated change before merge |
| AU-8 | `sdlc-meta/doc-architect` | How to generate and maintain layered `AGENTS.md` project guidance |
| AU-1, AU-3, AU-6 | `ai/coding-agent-optimization` | Device-level assistant configuration, context, delegation and permissions |

This reference does not restate those procedures. If a procedure changes there, section 9 keeps pointing at the owner and its acceptance conditions stay as defined in section 2.

## 8. Decision and gap register entries

Record in the document's decision and gap register: the assistants and files in scope (AU-8), each rule the team deferred, each approver role the owner has not yet named, and the reviewer and date of the hand-applied checklist. Mark any element that needs evidence the team has not produced as `not assessed`, with its owner.

## 9. Degraded mode

If the project sources named in the table are unavailable, produce the section headings with the required parts listed as gaps, mark each element FAIL for the checklist, and hand the draft back with the gap register. Do not write a default rule to fill a gap.
