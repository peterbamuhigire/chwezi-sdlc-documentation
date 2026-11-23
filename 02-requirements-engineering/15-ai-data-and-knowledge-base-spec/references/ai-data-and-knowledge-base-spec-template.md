# AI Data and Knowledge-Base Spec Template

## 1. Source Inventory

| Source ID | Name | Type | Owner | Classification | Volume | Refresh |
|-----------|------|------|-------|----------------|--------|---------|
| DS-001 | Customer document uploads | object store | Product | confidential (per-tenant) | 100 GB/tenant median | continuous |
| DS-002 | Customer CRM sync | API | Product | PII (per-tenant) | 10k records/tenant | hourly |
| DS-003 | Public regulatory corpus | curated repo | Legal | public | 5 GB | weekly |
| DS-004 | Conversation logs | log store | Platform | confidential (per-tenant) | streaming | continuous |
| DS-005 | Internal knowledge wiki | wiki | Eng/Support | internal-shared | 200 MB | daily |

## 2. Per-Source Scope

| Source | Scope | Licence / opt-out posture |
|--------|-------|----------------------------|
| DS-001 | per-tenant | tenant retains rights; we hold processor licence |
| DS-002 | per-tenant | tenant retains rights |
| DS-003 | shared | open licence; opt-out not applicable |
| DS-004 | per-tenant | tenant retains rights |
| DS-005 | shared internal | not exposed to tenants |

## 3. Ingestion Pipelines

| Source | Mode | Schedule | Transform | Chunk | Embedding | Index segmentation |
|--------|------|----------|-----------|-------|-----------|---------------------|
| DS-001 | push | continuous | OCR + dedupe | 800 tok / 100 overlap | embedding-v3 | per-tenant namespace + metadata filter |
| DS-002 | pull | hourly | entity normalisation | 500 tok | embedding-v3 | per-tenant namespace |
| DS-003 | pull | weekly | parse + dedupe | 1200 tok | embedding-v3 | shared namespace |
| DS-004 | streaming | continuous | redact / hash PII | n/a | n/a (raw log) | per-tenant partition |
| DS-005 | pull | daily | parse | 1000 tok | embedding-v3 | internal namespace |

## 4. SLA and Freshness

| Source | Ingestion SLA | Freshness target | Stale behaviour |
|--------|----------------|--------------------|------------------|
| DS-001 | <= 5 min upload-to-retrievable | <= 5 min | feature shows "indexing in progress" |
| DS-002 | hourly | <= 1 h | retrieval may lag last hour |
| DS-003 | weekly | <= 7 d | n/a |
| DS-004 | streaming | < 60 s | log gap alarm |
| DS-005 | daily | <= 24 h | n/a |

## 5. Retention and Lineage

| Source | Retention | Lineage record |
|--------|-----------|------------------|
| DS-001 | life of contract + 30 d delete on offboarding | doc id, version, ingest time, model, prompt version |
| DS-002 | life of contract + 30 d | record id, version, ingest time |
| DS-003 | indefinite (public) | snapshot id, ingest time |
| DS-004 | 90 d hot, 13 mo cold, then delete | prompt-hash, model, prompt-registry tag, retrieval-set id |
| DS-005 | life of product | wiki id, version |

Lineage queries shall return: input doc-id, retrieval rank, prompt-registry tag, model + version, output id, user, tenant, timestamp.

## 6. Training-Data Exclusion

| Source | Provider general training | Our fine-tunes | Our embedding model | Evidence |
|--------|-----------------------------|-----------------|----------------------|----------|
| DS-001 | excluded | excluded | excluded | contract Art. X; gateway endpoint `no-train`; audit Q-2026-1 |
| DS-002 | excluded | excluded | excluded | as above |
| DS-003 | n/a | allowed | allowed | open licence |
| DS-004 | excluded | excluded | excluded | as above |
| DS-005 | excluded | optional | optional | internal-only |

## 7. Cross-Tenant Controls for Embeddings and Logs

- Per-tenant namespace in the vector store; metadata filter is defence-in-depth only, never the sole isolation.
- Per-tenant conversation-log partition; tenant-id required claim on every read.
- Retrieval prompts include `tenant_id` as a guarded claim; cross-tenant retrieval prohibited at the gateway.
- Enterprise tier: per-tenant KMS key for embeddings + logs; key rotation every 365 d.
- Audit: monthly cross-tenant retrieval test shall return zero hits across tenants.

## 8. Traceability

| Source | AI FRs served | Eval IDs | Red-team IDs |
|--------|----------------|----------|---------------|
| DS-001 | AI-FR-003 | EVAL-ANL-300 | RT-ANL-80, RT-S-LEAK-* |
| DS-002 | AI-FR-002 | EVAL-COMP-150 | RT-COMP-60 |
| DS-003 | AI-FR-003 | EVAL-ANL-300 | -- |
| DS-004 | observability | -- | RT-S-LEAK-* |
| DS-005 | AI-FR-002 (style) | EVAL-COMP-150 | -- |

## Worked example · K1 ticket data and K2 maintenance corpus

**Requirement** FR-K1-01. **Snapshot** tickets-v1. **Permitted use** offline synthetic dispatch evaluation. At dispatch the model can use the ticket text and ID. Adjudicated labels become available afterwards. Record both event time and label time. The proposed Support Operations Lead must confirm adjudication ownership. No production ticket is included.

The table uses synthetic day numbers. Freeze training at the end of day 3 and evaluation at the end of day 6. Assign whole threads by their first eligible event. A later event in a training thread stays out of the temporal holdout. Within a thread keep the earliest equivalent text after comparing normalized text. Preserve the raw text and ID for inspection.

| Row | Thread | Event day | Label day | Use permission | Rule and disposition |
|---|---|---:|---:|---|---|
| T1 | alpha | 1 | 2 | granted | Train. Earliest original example |
| T2 | alpha | 2 | 2 | granted | Duplicate of T1 after whitespace normalization. Exclude |
| T3 | beta | 3 | 5 | granted | Label arrived after the training cutoff. Quarantine for this training snapshot |
| T4 | gamma | 4 | 5 | granted | Held out. Contains the test-only identifier AX-9 |
| T5 | delta | 5 | 6 | unknown | Quarantine until permission is established |
| T6 | alpha | 5 | 5 | granted | Cross-cutoff event in training thread. Exclude from training and holdout |
| T7 | epsilon | 6 | pending | granted | Predict-only. Exclude from labeled outcome denominator |

Fit the vocabulary on T1 only. AX-9 must remain absent from the fitted vocabulary. Drop the future closure-code field even where it is populated. Freeze the prediction and label tables separately. A pending label or an unknown use permission affects its own row. T4 remains eligible for the separate held-out check. Keep model calibration examples in separate groups from this holdout.

For K2 use corpus **atlas-v2** and access class **Atlas maintenance, tenant A**. P2 revision 2 is effective and eligible. P1 revision 1 has been withdrawn, P3 is tenant B only, and P4 is a permitted but unrelated document. On withdrawal, remove P1 from the index, snippets and answer cache, then query using both old and new wording. Record the index revision and eligible IDs before evaluating the answer. If the caller has access only to an unrelated entry, return no supported answer. Keep the input record and withdrawal receipt under their corpus owner.
