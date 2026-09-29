# UX Requirements Foundations

Parent skill: [05-ux-specification](../SKILL.md). Also loaded by
`01-prd-generation` (sections 2 and 3), `03-vision-statement` (section 3),
`04-lean-canvas` (section 7) and `07-premium-product-positioning` (section 4).
Load it when a PRD, vision, canvas or UX specification must turn user-experience
intent into declared scope, evidence-backed personas and verifiable UX
requirements. Visual design, typography, motion and render proof belong to
the `chwezi-design-engine` engine; this reference states what the experience
must achieve and how that is verified.

## 1. Declare the experience scope

Every PRD, vision and UX specification states which scope it targets:

| Scope | Covers | Typical evidence |
|---|---|---|
| Single interaction | One product or channel, one task (file a claim, pay a school fee) | Task success, time on task, error rate |
| Journey | Several channels over time toward one goal (SMS reminder, web sign-in, USSD payment) | Journey completion, drop-off per step, channel hand-off failures |
| Relationship | The whole customer life cycle with the organisation | Retention, repeat use, complaints, service-level adherence |

Decision rule: when the client expects relationship-level change and the team
is scoped for a single interaction, stop and re-scope before requirements are
written. Mismatched scope is the most common source of disputed "scope creep".

## 2. Persona and actor discipline

1. Choose one primary persona per release. The design must at least work for
   every secondary persona; a design tuned to a secondary persona is not
   allowed to break the primary one.
2. Each persona states: role and main tasks, goals, context (device,
   connectivity, language, literacy, physical environment), pain points,
   constraints, and one quotable problem statement drawn from research.
3. Mark the evidence source for every attribute (interview ID, analytics,
   support log). Unevidenced attributes are hypotheses and are labelled so.
4. Do not record ethnicity, photographs or other attributes that do not
   change a design decision; they invite stereotype, not insight.
5. Use the persona to refuse feature creep: a request that serves "somebody"
   but not the primary persona needs a separate justification.
6. Never average users into one composite; averaged personas satisfy nobody.

A PRD without validated research input is marked `speculative` and its
personas are treated as hypotheses to be tested in the first milestone.

## 3. Strategy-statement filter

Reject a product or UX strategy statement, and return to discovery, when it
is any of the following:

- a feature list or a single "killer idea" with no validated user problem;
- a plan that claims to need no further customer feedback;
- a string of trend words ("AI-powered super-app for everyone");
- a motivational or greeting-card line ("deliver excellence and delight");
- an expert assertion with no evidence, or a risky assumption not yet tested;
- a vision the organisation cannot resource or operate;
- a fixed destination statement ("be the Uber of X") with no operational
  meaning.

A usable strategy names the target segment, the validated problem, the value
proposition that differs from current alternatives, and the evidence that
users will change behaviour for it. It is revisited as evidence arrives.

## 4. UX outcome launch gate and process maturity

Premium positioning requires all five outcomes to be evidenced before launch;
a single failed outcome blocks the premium claim.

| Outcome | Verifiable measure (set thresholds per project) |
|---|---|
| Useful | Top tasks of the primary persona covered; each traced to a research finding |
| Easy to learn | First-task success without coaching, for example at least 80% of 5 to 8 representative participants |
| Efficient | Time on task for top tasks against a recorded baseline or competitor benchmark |
| Satisfying | Post-task or standardised questionnaire score agreed before testing |
| Accessible | WCAG 2.2 Level AA conformance evidence for web content, plus platform accessibility checks for native apps |

Process maturity for premium claims: the team must evidence problem
definition, stakeholder and user research, success criteria, personas,
journeys, information architecture, task flows, prototypes, expert review and
usability testing with real users. Cosmetic styling without research, flows
or testing is not premium UX regardless of visual polish.

## 5. Cognitive-load requirements

Treat these as design heuristics that generate testable requirements, not as
fixed numeric laws:

- Recognition over recall: offer choices, recent items and defaults rather
  than asking users to remember codes or earlier values.
- Chunk long identifiers for display and entry (for example a 10-digit phone
  number shown as 3-3-4) and accept pasted input with or without separators.
- Keep each form step to one decision theme; save progress automatically and
  offer a clear route back after interruption (a call, a lost connection).
- Close tasks frequently with explicit confirmation so users can release what
  they were holding in mind.
- Provide accelerators (shortcuts, saved templates) for expert users without
  removing the visible path for novices.

Write the requirement as the observable outcome, for example: "A cashier
interrupted mid-sale shall be able to resume the sale with all entered lines
intact after signing back in within 30 minutes."

## 6. Affordance review for primary actions

Walk every primary action through four checks; failure at any check is a
design defect to fix before launch:

1. **Present:** the control exists in the state where the user needs it, and
   defaults, modes and consequences are shown.
2. **Perceivable:** it is rendered, not occluded, not lost among competing
   elements.
3. **Recognisable:** it sits where the user looks for it and stands out by
   contrast, size and grouping; status messages are not hidden at screen edges.
4. **Understandable:** the label and any icon state the action in the user's
   words and meet contrast and text-size requirements.

## 7. Business-model blocks the UX strategy must evidence

When a Lean Canvas or Business Model Canvas is produced, customer segments
and value propositions must carry research evidence, not hypotheses alone.
The other blocks (channels, customer relationships, revenue streams, key
resources, key activities, key partnerships, cost structure) are checked for
consistency with the declared experience scope in section 1.

## Quality gate

- Scope declared; persona attributes evidenced or labelled as hypotheses.
- Strategy statement passes section 3.
- Each of the five outcomes has a measure, threshold and planned test.
- Cognitive-load and affordance findings are written as testable requirements.
- Visual and interaction design handed to `chwezi-design-engine`; render,
  device and accessibility proof recorded as `NOT_ASSESSED` until performed.

## Sources and currentness

Independent synthesis informed by: Levy, *UX Strategy*; Branson, UX/UI design
guidance drawing on Hartson and Pyla's cognitive-affordance model; Deacon, UX
and UI strategy; Osterwalder and Pigneur, *Business Model Generation*; an
enterprise UX practice guide for financial services. No source text,
catalogues or examples are reproduced.

Evidence/currentness (accessed 2026-09-24):
- WCAG 2.2 is the current W3C Recommendation (latest dated 12 December 2024);
  WCAG 3.0 is not a Recommendation (w3.org/TR/WCAG22). Earlier guidance citing
  WCAG 2.1 AA is superseded here.
- US Section 508 and ADA obligations are jurisdiction-specific and were not
  re-verified: `NOT_ASSESSED`; cite only when the project's jurisdiction
  requires them.
- The "7 plus or minus 2" working-memory figure is not used as a numeric cap;
  later research places working-memory capacity nearer 3 to 5 chunks
  (Cowan, 2001), so limits must be validated by usability testing.
- Participant counts and satisfaction thresholds in section 4 are examples to
  be set per project, not standards.
