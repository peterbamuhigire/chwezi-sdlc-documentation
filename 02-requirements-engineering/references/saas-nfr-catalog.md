# SaaS NFR Catalog (Phase 02 cross-cutting reference)

Reusable non-functional-requirement library for multi-tenant SaaS. Every NFR has: ID, statement, measurable threshold, verification method, source standard. Drop into Phase 02 `quality_standards.md` or directly into Section 3.x of the SRS.

## 1. Tenant Isolation NFRs

| ID | Statement | Threshold | Verification | Source |
|----|-----------|-----------|--------------|--------|
| NFR-ISO-001 | Cross-tenant data access SHALL be 0 in penetration test. | 0 cross-tenant rows accessible | Quarterly red-team test | SOC 2 CC6 |
| NFR-ISO-002 | Every API request SHALL be rejected if tenant_id claim absent or invalid. | 100% rejection in fuzz test | Automated negative-path test | Golding Ch.2 |
| NFR-ISO-003 | Tenant-scoped queries SHALL include `WHERE tenant_id = ?` enforced at repository layer. | 100% of repository methods use tenant filter | Static analysis lint rule + code review | Golding Ch.10 |
| NFR-ISO-004 | Tenant logs SHALL be tagged with tenant_id and SHALL NOT be accessible cross-tenant. | 0 cross-tenant log records visible | Log-access audit | SOC 2 CC6 |
| NFR-ISO-005 | Per-tenant KMS keys (for Enterprise tier) SHALL encrypt at-rest data. | 1 key per tenant, rotation 12 mo | KMS audit | NIST 800-57 |

## 2. Noisy-Neighbor NFRs

| ID | Statement | Threshold | Verification | Source |
|----|-----------|-----------|--------------|--------|
| NFR-NN-001 | A tenant exceeding tier quota SHALL be throttled, not allowed to degrade peers. | P95 cross-tenant latency interference ≤ 10 ms during stress test | Multi-tenant load test | Golding Ch.3 |
| NFR-NN-002 | Per-tier rate-limit SHALL be enforced at API gateway. | Bronze 100 rps, Silver 500, Gold 2000, Enterprise unlimited | Synthetic gateway test | Tier doc |
| NFR-NN-003 | Compute pool SHALL reject a tenant consuming > 25% of pool capacity. | Rejection within 1 s of breach | Load test | Golding Ch.3 |
| NFR-NN-004 | Storage queries from one tenant SHALL NOT consume > 10% of DB connections. | Per-tenant connection pool limit | Connection-pool metrics | DB config |

## 3. Blast-Radius NFRs

| ID | Statement | Threshold | Verification | Source |
|----|-----------|-----------|--------------|--------|
| NFR-BR-001 | P0 fault in any single pod SHALL affect ≤ 10% of tenants. | ≤ 10% tenant impact | Chaos test (kill pod) | SRE BR-001 |
| NFR-BR-002 | Region-wide failure SHALL not affect tenants in other regions. | 0 cross-region impact | Region-failover test | Golding Ch.3 |
| NFR-BR-003 | Schema migration on shared DB SHALL be backward-compatible for one release. | Old + new schema serve traffic during deploy | Migration drill | Golding Ch.9 |

## 4. Per-Tenant Cost Attribution NFRs

| ID | Statement | Threshold | Verification |
|----|-----------|-----------|--------------|
| NFR-COST-001 | Every billable resource SHALL emit a meter event with tenant_id, tier, region. | 100% of priced resources instrumented | Audit of metering catalogue |
| NFR-COST-002 | Daily per-tenant cost report SHALL be produced. | Available by 08:00 local next day | Dashboard SLI |
| NFR-COST-003 | Per-tenant gross-margin SHALL be visible on FinOps dashboard. | Refreshed daily | FinOps review |

## 5. Tenant Lifecycle NFRs

| ID | Statement | Threshold | Verification |
|----|-----------|-----------|--------------|
| NFR-LCY-001 | Self-serve tenant provisioning SHALL complete within 5 minutes. | P95 ≤ 5 min | Synthetic signup |
| NFR-LCY-002 | Tier change SHALL propagate to all services within 10 minutes. | P95 ≤ 10 min | Synthetic upgrade |
| NFR-LCY-003 | Customer-initiated data export SHALL be available within 30 days (GDPR Art.20). | 100% within 30 d | DSAR queue SLA |
| NFR-LCY-004 | Hard-delete SHALL produce a verified destruction certificate. | 100% of hard-deletes certified | Audit |
| NFR-LCY-005 | Legal-hold SHALL block hard-delete with no override at runtime. | 100% blocking | Legal-hold drill |

## 6. Identity / Tenant-Context NFRs

| ID | Statement | Threshold | Verification |
|----|-----------|-----------|--------------|
| NFR-IDN-001 | Tenant-context tokens SHALL expire within 1 hour for non-SSO sessions. | TTL ≤ 1 h | Token policy |
| NFR-IDN-002 | Cross-tenant impersonation by support staff SHALL be audit-logged with reason. | 100% audited | Audit log review |
| NFR-IDN-003 | Federated SSO (SAML/OIDC) SHALL be available on Enterprise tier. | Available | Enterprise checklist |

## 7. Observability per Tenant

| ID | Statement | Threshold | Verification |
|----|-----------|-----------|--------------|
| NFR-OBS-001 | Every log line for tenant-scoped operations SHALL carry tenant_id. | 100% | Log audit |
| NFR-OBS-002 | Per-tenant dashboards SHALL be available to CSMs. | Available + < 5 s load | UX test |
| NFR-OBS-003 | Per-tenant alerts (e.g. unusual error rate) SHALL be routed to the assigned CSM. | Routed within 5 min | Synthetic alarm |

## 8. SaaS-specific Availability NFRs

| ID | Statement | Threshold | Verification |
|----|-----------|-----------|--------------|
| NFR-AVL-001 | Per-tier availability SHALL meet tier SLO. | See SLO doc | Monthly review |
| NFR-AVL-002 | Control plane SHALL meet ≥ 99.95% availability. | 99.95% | Control-plane SLI |
| NFR-AVL-003 | Application-plane single-tenant failure SHALL NOT propagate to control plane. | 0 propagation | Chaos test |

## 9. Data Residency NFRs

| ID | Statement | Threshold | Verification |
|----|-----------|-----------|--------------|
| NFR-RES-001 | EU-tenant data SHALL remain in EU regions. | 0 cross-region writes | Region audit |
| NFR-RES-002 | Region selection SHALL be set at provisioning and SHALL NOT change without a documented migration. | 0 silent migrations | Audit |

## 10. Pricing / Quota Enforcement NFRs

| ID | Statement | Threshold | Verification |
|----|-----------|-----------|--------------|
| NFR-PRC-001 | Feature gates SHALL be evaluated using tier in tenant-context, not in client. | 100% server-side | Client-tamper test |
| NFR-PRC-002 | Soft-limit breach SHALL emit a warning event; hard-limit breach SHALL throttle. | per quota table | Synthetic quota test |
| NFR-PRC-003 | Quota counts SHALL be visible to the tenant admin in real time. | < 1 min lag | UX test |

## 11. Document Numbering NFRs

Every multi-tenant SaaS that issues user-facing document numbers (invoices, receipts, credit notes, orders, stock and money documents, journals, payroll runs) carries the contiguous-numbering block: one series per tenant and document type, never reset, allocated at issue inside the save, voided not deleted, replay-safe, sized for decades. Take the FR, NFR, DC, CTRL and transition (NFR-DOCMIG) items and the test cases from [Document numbering requirements](document-numbering-requirements.md); do not restate them here.

## Usage in Phase 02

Drop relevant NFRs into Section 3 of the SRS. Each project picks the rows applicable, customises thresholds, and traces them to the per-tier SLO doc and the Multi-Tenancy Architecture Spec.
