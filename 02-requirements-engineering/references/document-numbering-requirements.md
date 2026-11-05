# Document Numbering Requirements Standard (Phase 02-05 cross-cutting reference)

Reusable requirement block for the numbers a system prints on the documents it issues: invoices,
receipts, credit notes, bills, kitchen tickets, orders, purchase orders, goods receipts, stock
transfers, adjustments, counts, expenses, deposits, withdrawals, journal entries, payroll runs and
every other record a person issues, prints, sends or quotes as evidence of a transaction or stock
event. Each requirement has an ID, statement, rationale and verification method. Drop the block into
the SRS, then carry its design obligations and test cases into Phases 03 and 05.

Consumers: `waterfall/05-feature-decomposition` (Section 3.2), `waterfall/07-attribute-mapping`
(Sections 3.3-3.6), `fundamentals/during/09-business-rules-analysis`,
`03-design-documentation/10-saas-multi-tenancy-architecture-spec`, `03-design-documentation/04-database-design`,
`03-design-documentation/03-api-specification`, `03-design-documentation/02-low-level-design`,
`05-testing-documentation/02-test-plan` and `agile/02-acceptance-criteria`.

## 1. When the block applies

| Condition | Action |
|---|---|
| The system is multi-tenant SaaS and issues any user-facing document number | Include the block by default. Every multi-tenant SRS carries a "Document Numbering" feature in Section 3.2 and the NFRs in Sections 3.3-3.6. |
| Single-tenant system that issues document numbers | Include the block with "tenant" read as "operating entity". |
| A consultant wants to omit the block from a multi-tenant SRS | Record a waiver through `09-governance-compliance/08-waiver-management` naming the approver and the reason. Silent omission is a `[TRACE-GAP]`. |
| A fiscal authority issues its own number (for example a fiscal document number) | Store it in a separate field. It never replaces or consumes the system's own series. Fiscal numbering rules are outside this block and stay `NOT_ASSESSED` until verified through the Digital Research Engine. |

Out of scope: master-data codes (customer, supplier, product, batch codes) and deterministic report
runs (one per day). The document type register (section 3) records each exclusion and its reason.

## 2. Terms to add to `_context/glossary.md`

| Term | Definition |
|---|---|
| Document number | The identifier a person sees, prints, quotes and searches for. It is distinct from the record's internal surrogate key. |
| Document type | A class of document that owns one series, for example sales invoice or goods receipt note. |
| Series | The ordered set of numbers issued for one document type in one tenant. |
| Issue event | The state change that makes a document official (finalised, posted, sent, approved, settled or dispatched). The number is assigned at this event. |
| Void | A status that cancels an issued document while keeping its number in the series. |
| Gap | A counter value between the seed point and the current counter that no document of that type in that tenant holds. |
| Clash | A candidate number that is already held by an existing document of the same type in the same tenant. |
| Provisional tag | A short reference shown on a document created offline. It is visibly not a document number. |
| Idempotency key | A client-supplied key that identifies one create request, so a replay returns the original result. |

## 3. Inputs to elicit: the document type register

Collect one row per document type before writing the requirements. A missing column is a
`[CONTEXT-GAP: document type register]`; do not invent formats or issue events.

| Column | Content | Missing behaviour |
|---|---|---|
| Type key | Stable machine name, never renamed | Stop; the series cannot be specified |
| Label | Plain-language name used in messages | Use the business term from the glossary |
| Issue event | The state change that assigns the number | `[CONTEXT-GAP]`; ask the document owner |
| Format | Prefix, optional date label, padded counter, for example `PO-{n:6}` | Propose `PREFIX-{n:6}` and mark it for owner approval |
| Volume class | Very high (per sale or ticket), high (daily operations) or lower | Default to lower; flag for confirmation |
| Scope | Tenant series or platform series | Tenant |
| Existing numbers | Brownfield only: current format, highest number, known duplicates | `[CONTEXT-GAP]` blocks the migration requirements |
| External numbers | Supplier, import or fiscal numbers held alongside | None |

## 4. Where each part lands in the SRS

| SRS section | Content from this block |
|---|---|
| 1.3 Definitions | The terms in section 2 |
| 2.4 Constraints | DC-DOCNUM items, each citing its source (owner rule, regulation or architecture decision) |
| 2.5 Assumptions | The document type register status and any unconfirmed issue events |
| 3.2.N Document Numbering (cross-cutting feature) | FR-DOCNUM items, each with an inline Given-When-Then stub |
| 3.3 Performance | NFR-DOCNUM-005 to NFR-DOCNUM-007 |
| 3.4 Design Constraints | DC-DOCNUM items |
| 3.5 Reliability and Security | NFR-DOCNUM-001 to NFR-DOCNUM-004, CTRL-DOCNUM items |
| 3.6 Other Requirements (transition) | NFR-DOCMIG items for systems that already hold numbers |

## 5. Functional requirements

Numbers below 100 are the base set. Projects add type-specific rows from 101 upward.

### 5.1 One series per tenant and document type

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| **FR-DOCNUM-001** | The system shall keep one number series for each combination of tenant and document type listed in the document type register. | A shared counter lets one tenant's activity or another type consume numbers, which leaves gaps a client cannot explain. | Test: issue documents of two types in two tenants; each of the four series starts at its seed plus 1 and is consecutive. |
| **FR-DOCNUM-002** | The system shall assign each newly issued document the next counter value after the highest counter value already held in that series. | Contiguity is the property auditors and clients check. | Test: TC-DOCNUM-001 and TC-DOCNUM-002. |
| **FR-DOCNUM-003** | The system shall not reset a series at a year, month, period, branch or location boundary. | A reset produces repeated counters and breaks the gap check. | Test: issue documents either side of a year end; the counter continues. |
| **FR-DOCNUM-004** | Where a format carries a date or period label, the system shall derive the label from the document's own date and keep the counter continuous across label changes. | The label helps people read the number; the counter carries the order. | Test: TC-DOCNUM-011. |
| **FR-DOCNUM-005** | The system shall keep the document number separate from the record's internal surrogate key and shall not derive one from the other. | Surrogate keys are shared across tenants and skip values on failed inserts. | Inspection of the data design; test that two tenants' first documents both show counter 1. |
| **FR-DOCNUM-006** | The system shall ignore any document number supplied by a client application, import file or request body on create, except fields declared as external references. | Only the server can guarantee contiguity and uniqueness. | Test: TC-DOCNUM-014. |

### 5.2 Number at issue, void instead of delete

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| **FR-DOCNUM-010** | The system shall assign a document number at the document type's issue event and shall not assign one while the document is a draft. | Discarded drafts would otherwise leave gaps or fill the series with voids. | Test: create a draft; it shows no number; issue it; it shows the next number. |
| **FR-DOCNUM-011** | The system shall allow a draft without a number to be deleted without affecting any series. | Users must be able to abandon unfinished work. | Test: TC-DOCNUM-005. |
| **FR-DOCNUM-012** | When a user attempts to delete a document that holds a number, the system shall refuse the deletion and offer the void action, naming the document and its number. | A deleted numbered document is an unexplained gap and a lost audit record. | Test: attempt the delete; the record remains and the message names the void action. |
| **FR-DOCNUM-013** | When an authorised user voids a numbered document, the system shall keep its number, record the actor, time and reason, and keep the document in the series. | The void is evidence; hiding it defeats the gap check. | Test: TC-DOCNUM-004. |
| **FR-DOCNUM-014** | The system shall show voided documents in document lists and reports with a void marker and the void reason. | Readers must see why a number has no live document. | Demonstration on the list and report screens; inspection of the printed report. |
| **FR-DOCNUM-015** | If saving a document fails or is rolled back after a number was proposed for it, the system shall issue that same number to the next document of that type in that tenant. | A failed save must not burn a number. | Test: TC-DOCNUM-003. |

### 5.3 Clash handling

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| **FR-DOCNUM-020** | Before a series issues its first number, the system shall set its starting point past the highest existing number of that type and format in that tenant. | Existing documents keep their numbers and the series continues after them. | Test: seed a tenant holding `GRN-00041`; the next number is `GRN-00042`. |
| **FR-DOCNUM-021** | When the next candidate number is already held by a document of the same type in the same tenant, the system shall step past it and issue the next free number. | Numbers written by imports, legacy code or manual repairs must not cause duplicates or failures. | Test: TC-DOCNUM-007. |
| **FR-DOCNUM-022** | The system shall reject a second document with the same number, type and tenant at the data store. | The final backstop against any writer that bypasses the allocator. | Inspection of the schema; test: TC-DOCNUM-008. |
| **FR-DOCNUM-023** | When a save is rejected because its number already exists, the system shall roll back the save, retry it once with a newly allocated number and, if the retry also fails, tell the user in plain language that nothing was saved. | The user never sees a duplicate, a gap or a technical error. | Test: TC-DOCNUM-008. |
| **FR-DOCNUM-024** | The system shall record each step past a clashing number with tenant, document type and the numbers involved. | A rising clash count shows a writer outside the allocator. | Inspection of the audit log after TC-DOCNUM-007. |

### 5.4 Platform, credit note and external numbers

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| **FR-DOCNUM-030** | The system shall number the platform operator's own invoices and credit notes to tenants from platform-wide series that do not consume any tenant's series. | Subscription billing must not leave gaps in a tenant's sales invoices. | Test: TC-DOCNUM-015. |
| **FR-DOCNUM-031** | The system shall number credit notes from their own series, separate from invoices. | Mixing them breaks the contiguity of both. | Test: issue invoice, credit note, invoice; the invoice series has no gap. |
| **FR-DOCNUM-032** | The system shall store supplier, imported and fiscal-authority numbers in fields separate from the system's document number, and shall not let them consume or reset a series. | External numbers follow rules the system does not control. | Test: TC-DOCNUM-016. |

### 5.5 Replays, offline clients and tenancy

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| **FR-DOCNUM-040** | When a create request is replayed with an idempotency key already used for a document of that tenant, the system shall return the original document and its original number and shall not allocate another number. | Network retries must not create duplicates or gaps. | Test: TC-DOCNUM-006. |
| **FR-DOCNUM-041** | The system shall keep the idempotency key with the document for the life of the document. | A short-lived key cache lets a late replay create a second document. | Test: replay after the cache retention period; the original number returns. |
| **FR-DOCNUM-042** | The system shall reject an API request to create a numbered document that carries no idempotency key, with an error that names the missing key. | A made-up fallback key cannot detect a replay. | Test: send the create without a key; the response is a client error naming the key. |
| **FR-DOCNUM-043** | While a document created offline has not been confirmed by the server, the client shall show a provisional tag that is visibly marked as not a document number. | An offline client cannot know the next number. | Demonstration on the offline client; inspection of the screen text. |
| **FR-DOCNUM-044** | When the server confirms an offline document, the client shall replace the provisional tag with the server's number in every list, detail view and reprint. | One document must carry one number everywhere. | Test: TC-DOCNUM-013. |
| **FR-DOCNUM-045** | If an unconfirmed offline document is printed or shared, the output shall state that it is not yet confirmed and show the provisional tag in place of a number. | A provisional tag must never be mistaken for an official number. | Inspection of the printed sample. |
| **FR-DOCNUM-046** | The system shall take the tenant for every allocation from the authenticated context, never from the request body. | Prevents a caller from consuming another tenant's series. | Test: send another tenant's id in the body; the caller's own series advances. |
| **FR-DOCNUM-047** | The system shall not reveal another tenant's numbers, counts or series positions in any message, response or report. | Series position is commercial information. | Security test of error responses and the gap report. |

## 6. Non-functional requirements

Thresholds marked *default* come from the reference implementation plan. Replace each with the
project's measured peak and record the source; an unmeasured peak is a `[CONTEXT-GAP]`.

| ID | Requirement | Threshold | Verification |
|---|---|---|---|
| **NFR-DOCNUM-001** | Every committed series shall be contiguous above its seed point. | 0 gaps and 0 duplicates in the nightly report | Gap report; TC-DOCNUM-001 |
| **NFR-DOCNUM-002** | Series capacity shall cover decades of use by the largest tenant. | At least 10^18 values per series; a formatted number is at most 40 characters | Analysis plus TC-DOCNUM-018 |
| **NFR-DOCNUM-003** | A counter shall grow past its padding without error. | `PO-999999` is followed by `PO-1000000`, which is found, parsed and gap-checked | TC-DOCNUM-012 |
| **NFR-DOCNUM-004** | Lists and reports shall order documents by issue timestamp and then internal key, never by the number text alone. | 0 list or report queries ordered by the number column alone | Inspection and static check |
| **NFR-DOCNUM-005** | Allocation shall not become the bottleneck at peak issue rate. | *Default:* p95 wait for the series lock at most 50 ms with at least 40 parallel issuers in one tenant, and at least 200 committed documents per second per tenant | Load test TC-DOCNUM-017 |
| **NFR-DOCNUM-006** | Clash and replay lookups shall stay constant as volume grows. | *Default:* p95 at most 5 ms with 10 million documents of one type in one tenant | Volume test TC-DOCNUM-018 |
| **NFR-DOCNUM-007** | The gap report shall be incremental. | *Default:* one day's increment checked in at most 60 s at the volume above; a full re-scan runs only on manual request | Volume test TC-DOCNUM-018 |

### 6.1 Transition requirements for systems that already hold numbers

| ID | Requirement | Threshold | Verification |
|---|---|---|---|
| **NFR-DOCMIG-001** | The change shall leave every historical document number, amount, status and date unchanged. | Checksums of these columns per tenant identical before and after | TC-DOCNUM-009 |
| **NFR-DOCMIG-002** | Every series shall be seeded before the new numbering is switched on for its document type. | 0 types switched on without a seed record | Inspection of the seed log |
| **NFR-DOCMIG-003** | A document type that changes format shall start a new series key and keep the old counter unchanged. | 0 counters lowered | Inspection; TC-DOCNUM-010 |
| **NFR-DOCMIG-004** | A uniqueness rule shall be added only where no duplicates exist; existing duplicates shall be reported, left untouched and shall not stop the rollout. | 0 migration aborts caused by one tenant's data | Migration test on a fixture with duplicates |
| **NFR-DOCMIG-005** | Each document type shall have its own switch that returns it to the previous numbering, and switching back on shall reseed the series past every number written meanwhile. | Rollback of one type takes effect without a deployment | TC-DOCNUM-019 |
| **NFR-DOCMIG-006** | Every migration step shall be repeatable without changing the result. | Second run is a no-op | TC-DOCNUM-010 |
| **NFR-DOCMIG-007** | Documents issued before the change shall remain findable by their old numbers in search, screens and links. | 100% of a sampled set of old numbers resolve | Search test on a production copy |
| **NFR-DOCMIG-008** | Interfaces used by existing clients shall only gain fields; no field shall be removed or renamed. | Previous client release passes its contract tests against the new server | Contract test |
| **NFR-DOCMIG-009** | The full migration shall be rehearsed on a restored production copy before production switch-on. | Checksums identical, gap report empty, no new error type, NFR-DOCNUM-005 met | Rehearsal record |

## 7. Design constraints and controls

Place DC items in SRS 2.4 and 3.4 with their source. Under gate G5 of the
[final requirements quality gate](final-requirements-quality-gate.md), each DC item stays in the SRS
only because a decision owner mandated it. Cite the owner rule or ADR.

| ID | Constraint or control | Verification |
|---|---|---|
| **DC-DOCNUM-001** | One allocator component shall issue every document number; no other code path may build one. Counting rows, taking the maximum, random values, surrogate-key values and client values are not allocation methods. | Code inspection; CTRL-DOCNUM-001 |
| **DC-DOCNUM-002** | The number shall be allocated inside the transaction that saves the document, as late as possible in that transaction. | Design review; TC-DOCNUM-003 |
| **DC-DOCNUM-003** | Counters shall be 64-bit unsigned integers; document number columns, and every column that copies a number, shall hold at least 40 characters. | Schema test |
| **DC-DOCNUM-004** | Document numbers shall travel as strings in every interface. | Contract test; JSON numbers lose integer precision above 2^53 in common parsers (RFC 8259, section 6) |
| **DC-DOCNUM-005** | When one transaction needs several numbers, it shall lock series in a fixed published order, and a deadlock or lock timeout shall retry the whole transaction at most 3 times. | Design review; lock-order test |
| **CTRL-DOCNUM-001** | A continuous-integration check shall fail any new number-building code outside the allocator; its baseline count may only fall. | CI run record |
| **CTRL-DOCNUM-002** | A schema test shall confirm a uniqueness rule on (tenant, number) for every registered number column, with each recorded exception listed. | Test run record |
| **CTRL-DOCNUM-003** | A nightly report shall list gaps, duplicates and numbers above the counter for every series and alert the platform team. | Report sample and alert record |
| **CTRL-DOCNUM-004** | A continuous-integration check shall fail any delete of a numbered document type that is not limited to rows without a number. | CI run record |

## 8. Design-document obligations

| Document | Must specify |
|---|---|
| HLD and Multi-Tenancy Architecture Spec | The allocator as a named component, the document type register as its single source, platform versus tenant series, the offline provisional-tag flow, and the gap report as an operational signal |
| LLD | Allocation algorithm (lock the series row, seed when absent, probe for clashes, write the counter), retry wrapper, lock order across series, the issue-event method per type, and the void and delete-refusal paths |
| Database Design | Counter table keyed on (tenant, type); nullable number column while draft; uniqueness on (tenant, number) per numbered table; durable idempotency-key column with uniqueness on (tenant, key); column widths from DC-DOCNUM-003; numbering audit table (seed, clash skip, reseed, gap, duplicate) |
| API Specification | `document_number` (string or null) and `number_status` (`draft`, `issued`, `void`) on every numbered resource; idempotency key required on numbered creates; client-sent numbers ignored; replay returns the stored number |
| Test Plan | The test cases in section 10, mapped to the FR, NFR, DC and CTRL IDs |

## 9. Acceptance criteria (Given-When-Then)

- **Given** a tenant whose last issued invoice is counter 41, **When** a cashier issues an invoice, **Then** the invoice shows counter 42.
- **Given** a save that allocated counter 42 and then failed, **When** the next invoice is issued, **Then** it shows counter 42.
- **Given** an issued invoice with counter 42, **When** an authorised user voids it, **Then** the list shows counter 42 with a void marker and reason, and the next invoice shows counter 43.
- **Given** a draft order with no number, **When** the user deletes it, **Then** the next issued order shows the counter after the last issued order.
- **Given** a create request that returned counter 42, **When** the same request is replayed with the same idempotency key, **Then** the response carries the same document and counter 42.
- **Given** historical documents before migration, **When** the migration and switch-on complete, **Then** the checksum of every historical number, amount, status and date matches the pre-migration checksum.

## 10. Test case catalogue

Map each case into the project test plan with project data. "Contiguous" means the committed set
equals the integers from seed plus 1 to the counter value, with no duplicate.

| ID | Case | Expected result | Covers |
|---|---|---|---|
| **TC-DOCNUM-001** | 8 parallel issuers each issue 500 documents of one type in one tenant, each in its own transaction | Committed set contiguous; 0 duplicates; p95 lock wait recorded | FR-DOCNUM-002, NFR-DOCNUM-001 |
| **TC-DOCNUM-002** | As TC-DOCNUM-001 with 10% of transactions rolled back at random | Committed set contiguous; 0 duplicates | FR-DOCNUM-015, NFR-DOCNUM-001 |
| **TC-DOCNUM-003** | Allocate in a transaction, roll it back, issue again | Second issue returns the same number | FR-DOCNUM-015, DC-DOCNUM-002 |
| **TC-DOCNUM-004** | Void an issued document, then issue another | Void keeps its number and appears in lists and reports; next number follows on | FR-DOCNUM-013, FR-DOCNUM-014 |
| **TC-DOCNUM-005** | Create a draft, delete it, issue a document | No number consumed; series contiguous | FR-DOCNUM-010, FR-DOCNUM-011 |
| **TC-DOCNUM-006** | Replay a create with the same idempotency key, once immediately and once after the key cache period | Same document and number both times; counter unchanged | FR-DOCNUM-040, FR-DOCNUM-041 |
| **TC-DOCNUM-007** | Insert the next candidate number directly, then issue | Allocator steps past it; skip recorded; series has no gap | FR-DOCNUM-021, FR-DOCNUM-024 |
| **TC-DOCNUM-008** | A second connection inserts the candidate between clash check and insert | Save retries once and succeeds with the next number; on a second clash the user sees a plain-language "nothing was saved" message | FR-DOCNUM-022, FR-DOCNUM-023 |
| **TC-DOCNUM-009** | Run the migration on a production copy | Historical checksums identical | NFR-DOCMIG-001 |
| **TC-DOCNUM-010** | Run every migration twice on a fixture with duplicates, blank numbers, imports and legacy formats | Second run is a no-op; no counter lowered; no existing number changed | NFR-DOCMIG-003, NFR-DOCMIG-006 |
| **TC-DOCNUM-011** | Issue labelled numbers either side of a month and a year boundary | Label changes; counter continues | FR-DOCNUM-003, FR-DOCNUM-004 |
| **TC-DOCNUM-012** | Issue at the padding limit | Number widens; search, parse and gap report still work | NFR-DOCNUM-003 |
| **TC-DOCNUM-013** | Create offline, sync, reprint | Provisional tag before sync; server number everywhere after sync | FR-DOCNUM-043, FR-DOCNUM-044 |
| **TC-DOCNUM-014** | Send a create with a client-chosen number | Server's number wins | FR-DOCNUM-006 |
| **TC-DOCNUM-015** | Issue a platform invoice to a tenant between two tenant invoices | Tenant invoice series has no gap | FR-DOCNUM-030 |
| **TC-DOCNUM-016** | Import documents carrying their own numbers, then issue | Imports do not consume the counter; the allocator steps past any clash | FR-DOCNUM-032 |
| **TC-DOCNUM-017** | Load test at the project's measured peak, at least 40 parallel issuers | NFR-DOCNUM-005 thresholds met | NFR-DOCNUM-005 |
| **TC-DOCNUM-018** | Volume fixture of 10 million documents in one tenant; counter at its maximum value minus 1 | NFR-DOCNUM-006 and -007 met; the maximum fits 40 characters; the next allocation fails safely with a message | NFR-DOCNUM-002, -006, -007 |
| **TC-DOCNUM-019** | Switch one type off, issue through the old path, switch it on | Series reseeded past the numbers written meanwhile; 0 duplicates | NFR-DOCMIG-005 |
| **TC-DOCNUM-020** | Remove a number from a committed series in a test copy and run the gap report | Gap reported and alert raised | CTRL-DOCNUM-003 |

## 11. Review checklist

- [ ] The document type register exists, with an issue event and format for every type, and every exclusion has a reason.
- [ ] Section 3.2 has a Document Numbering feature carrying FR-DOCNUM-001 to FR-DOCNUM-047, or a recorded waiver for each omitted item.
- [ ] Every default threshold in section 6 has been replaced by a measured or owner-approved value.
- [ ] Brownfield systems carry the NFR-DOCMIG items and a rehearsal plan.
- [ ] The design documents in section 8 cover their obligations.
- [ ] Every FR, NFR, DC and CTRL item traces to at least one TC-DOCNUM case in the test plan.

## Evidence/currentness

Accessed 2026-11-05. Source: the owner's standing rule of 5 November 2026 for all multi-tenant
SaaS systems, and the reference implementation plan in the Maduuka repository
(`docs/plans/numbering/`: decisions, architecture, production rollout, verification and capacity
documents), read on 2026-11-05. Default thresholds in sections 6 and 10 are that plan's lab gates;
they are not industry benchmarks. The RFC 8259 integer-precision note is stable protocol text.
No tax-authority, fiscal-device or accounting-standard rule is asserted; those remain
`NOT_ASSESSED` until verified through the Digital Research Engine. Review date: 2027-05-05.
