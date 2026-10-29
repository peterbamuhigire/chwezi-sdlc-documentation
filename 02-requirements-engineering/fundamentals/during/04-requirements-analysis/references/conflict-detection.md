# Conflict Detection Reference Guide

**Purpose:** Identify and resolve conflicts between requirements using systematic detection algorithms and structured resolution strategies.

**Standards:** IEEE 29148-2018 Section 6.5, Wiegers Practice 8

---

## 1. Conflict Types

### 1.1 Contradiction

Two requirements specify mutually exclusive behaviors for the same stimulus or entity.

**Detection Signal:** Requirements that reference the same system element but prescribe incompatible actions or states.

**Example:**
- FR-012: "The system shall lock a user account after 3 failed login attempts."
- FR-045: "The system shall never lock a user account automatically."

These cannot coexist. One must be modified or removed.

### 1.2 Redundancy

Two or more requirements specify the same behavior using different wording, creating maintenance burden and potential divergence during updates.

**Detection Signal:** Requirements with high semantic similarity that reference the same entities and actions.

**Example:**
- FR-020: "The system shall send an email notification when an order is placed."
- FR-087: "The system shall notify the customer via email upon order submission."

These are functionally identical. Merge into a single requirement.

### 1.3 Subsumption

One requirement is a strict subset of another, meaning satisfying the broader requirement automatically satisfies the narrower one.

**Detection Signal:** A specific requirement whose scope falls entirely within a more general requirement.

**Example:**
- FR-030: "The system shall validate all form inputs before submission."
- FR-031: "The system shall validate the email field format before form submission."

FR-031 is subsumed by FR-030. Retain the general requirement and remove the specific one, or retain the specific one for explicit test traceability.

### 1.4 Boundary Conflict

Two requirements define overlapping or contradictory numeric ranges, thresholds, or constraints that cannot simultaneously be satisfied.

**Detection Signal:** Requirements that reference the same measurable attribute with incompatible bounds.

**Example:**
- NFR-005: "The system shall respond to API requests within 200ms at the 95th percentile."
- NFR-012: "The system shall encrypt all API payloads using AES-256-GCM before transmission."

The encryption overhead may make the 200ms target infeasible. This is a boundary conflict between performance and security constraints.

---

## 2. Detection Algorithm

Before comparing drafted requirements, reconcile the material statements in
the elicitation sources through the project's
`_registry/source-reconciliation.yaml`. Map each statement to a requirement or
an explicit ambiguity record; keep contradictory alternatives unresolved until
an authorised owner decides. The `scripts/validate_source_reconciliation.py`
check verifies record completeness and cross-links. It does not find omitted
source statements or judge semantic contradictions automatically; retain the
analyst's evidence and independent review in the conflict report.

### Step 1: Build a Requirements Cross-Reference Matrix

Create a matrix where each requirement is cross-referenced against every other requirement sharing at least one common entity, attribute, or system element.

| Req ID | Entity     | Attribute    | Action       |
|--------|------------|--------------|--------------|
| FR-012 | UserAccount| lockStatus   | lock         |
| FR-045 | UserAccount| lockStatus   | prevent_lock |

### Step 2: Apply Conflict Heuristics

For each pair of requirements sharing a common element:

1. **Same entity + same attribute + different action** = Potential Contradiction
2. **Same entity + same action + same outcome** = Potential Redundancy
3. **Same entity + broader scope contains narrower scope** = Potential Subsumption
4. **Same attribute + overlapping numeric ranges** = Potential Boundary Conflict

### Step 3: Classify and Confirm

For each potential conflict:
- Review the full requirement text in context
- Confirm or dismiss the conflict
- Assign a severity: Critical (blocks implementation), Major (requires stakeholder decision), Minor (documentation cleanup)

### Step 4: Document Findings

Record each confirmed conflict in the Conflict Detection Report with:
- Conflicting requirement identifiers
- Conflict type
- Severity
- Recommended resolution
- Escalation path

---

## 3. Resolution Strategies

### 3.1 Merge Strategy

**Applies to:** Redundancy, Subsumption

Combine the conflicting requirements into a single, comprehensive requirement that captures the full intent. Retire the merged requirements and update all traceability links.

**Process:**
1. Identify the requirement with the broadest scope
2. Incorporate any unique details from the narrower requirement
3. Assign the merged requirement a new or retained identifier
4. Update traceability matrix to redirect all links

### 3.2 Stakeholder Arbitration

**Applies to:** Contradiction, Boundary Conflict

When two requirements reflect competing stakeholder interests, escalate to the designated decision authority.

**Process:**
1. Present both requirements with full context to the arbitrator
2. Document the business impact of choosing each alternative
3. Record the decision with rationale and the name of the decision-maker
4. Update the losing requirement with a reference to the arbitration record

### 3.3 Constraint Relaxation

**Applies to:** Boundary Conflict

When two constraints are individually valid but collectively infeasible, negotiate relaxation of one or both constraints.

**Process:**
1. Quantify the gap between the conflicting thresholds
2. Propose relaxed values that satisfy both constraints within acceptable tolerance
3. Validate the relaxed values with stakeholders and technical leads
4. Document the original and relaxed values with justification

### 3.4 Deferral

**Applies to:** Any conflict type when information is insufficient

When a conflict cannot be resolved with available information, defer the conflicting requirements to a future analysis cycle.

**Process:**
1. Tag both requirements with `[DEFERRED-CONFLICT]`
2. Document what information is needed to resolve the conflict
3. Assign an owner and a target resolution date
4. Exclude deferred requirements from the current baseline

---

## 4. Escalation Paths

| Conflict Severity | First Escalation         | Second Escalation       | Final Authority         |
|--------------------|--------------------------|-------------------------|-------------------------|
| Critical           | Project Manager          | Steering Committee      | Executive Sponsor       |
| Major              | Business Analyst Lead    | Project Manager         | Product Owner           |
| Minor              | Requirements Author      | Peer Reviewer           | Business Analyst Lead   |

---

## 5. Conflict Detection Checklist

- [ ] Cross-reference matrix built for all requirements sharing common entities
- [ ] All four conflict heuristics applied to every requirement pair
- [ ] Each potential conflict confirmed or dismissed with evidence
- [ ] Severity assigned to every confirmed conflict
- [ ] Resolution strategy selected and documented for every conflict
- [ ] Escalation path identified for unresolved conflicts
- [ ] Traceability links updated after merge or removal

---

**Last Updated:** 2026-03-07
