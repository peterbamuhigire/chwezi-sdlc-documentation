# Domain-Specific Elicitation Checklists

## Purpose

This reference provides domain-specific checklists that supplement general elicitation techniques. Each checklist ensures that critical domain requirements -- particularly regulatory, integration, and safety concerns -- are not missed during elicitation. These checklists hook into the existing `skills/` directory domain skills for deeper coverage.

## Reference Standard

- IEEE 29148-2018 Section 6.3: Domain-specific elicitation
- Laplante Ch.4: Domain analysis

## Usage

1. Identify the project domain from `vision.md` and `features.md`
2. Select the matching checklist below (one or more may apply)
3. For each checklist item, record: Addressed (Yes/No/Partial), Source, and Notes
4. Items marked "No" or "Partial" shall generate follow-up elicitation tasks

## Healthcare Domain Checklist

**Applicable when**: The system handles patient data, clinical workflows, or integrates with healthcare systems.

**Related skill**: `skills/` healthcare-specific skills (if available)

| # | Category | Checklist Item | Addressed | Source | Notes |
|---|----------|----------------|-----------|--------|-------|
| HC-01 | HIPAA | The system shall implement access controls for Protected Health Information (PHI) | | | |
| HC-02 | HIPAA | The system shall maintain an audit trail of all PHI access and modifications | | | |
| HC-03 | HIPAA | The system shall encrypt PHI at rest and in transit (AES-256 minimum) | | | |
| HC-04 | HIPAA | The system shall support role-based access with minimum necessary privilege | | | |
| HC-05 | HIPAA | The system shall implement breach notification procedures | | | |
| HC-06 | HL7/FHIR | The system shall define which HL7 message types it sends and receives | | | |
| HC-07 | HL7/FHIR | The system shall support FHIR R4 resources for interoperability | | | |
| HC-08 | HL7/FHIR | The system shall handle HL7 acknowledgment (ACK/NAK) messages | | | |
| HC-09 | Clinical | The system shall define clinical decision support rules with evidence sources | | | |
| HC-10 | Clinical | The system shall support medication interaction checking | | | |
| HC-11 | Patient Safety | The system shall implement patient identification verification (two-identifier rule) | | | |
| HC-12 | Patient Safety | The system shall log all clinical actions with timestamps and user attribution | | | |

## SaaS Domain Checklist

**Applicable when**: The system is a multi-tenant cloud application with subscription-based access.

**Related skill**: `skills/saas/multi-tenant-saas-architecture`, `skills/saas/modular-saas-architecture` (Chwezi Dev Engine)

| # | Category | Checklist Item | Addressed | Source | Notes |
|---|----------|----------------|-----------|--------|-------|
| SA-01 | Multi-Tenancy | The system shall isolate tenant data (shared DB with tenant ID, schema-per-tenant, or DB-per-tenant) | | | |
| SA-02 | Multi-Tenancy | The system shall prevent cross-tenant data leakage in all queries and APIs | | | |
| SA-03 | Multi-Tenancy | The system shall support tenant-specific configuration and branding | | | |
| SA-04 | Billing | The system shall define subscription tiers with feature differentiation | | | |
| SA-05 | Billing | The system shall track usage metrics for metered billing | | | |
| SA-06 | Billing | The system shall handle subscription lifecycle (trial, active, suspended, cancelled) | | | |
| SA-07 | API | The system shall define API rate limiting per tenant and tier | | | |
| SA-08 | API | The system shall version APIs and define deprecation policy | | | |
| SA-09 | SLA | The system shall define uptime SLA targets (e.g., 99.9%) | | | |
| SA-10 | SLA | The system shall define data backup and recovery RPO/RTO targets | | | |
| SA-11 | Onboarding | The system shall support self-service tenant provisioning | | | |
| SA-12 | Onboarding | The system shall define data migration paths for new tenants | | | |

## POS (Point of Sale) Domain Checklist

**Applicable when**: The system processes sales transactions, handles payments, or manages inventory at the point of sale.

**Related skill**: `finance-ui-pattern-library`, `inventory-costing-and-stock-accounting` (Chwezi accounting engine; resolve it through the engine-routing table)

| # | Category | Checklist Item | Addressed | Source | Notes |
|---|----------|----------------|-----------|--------|-------|
| POS-01 | Payment | The system shall define supported payment methods (cash, card, mobile, voucher) | | | |
| POS-02 | Payment | The system shall comply with PCI-DSS for card payment processing | | | |
| POS-03 | Payment | The system shall handle payment gateway timeout and retry logic | | | |
| POS-04 | Payment | The system shall support split payments and partial refunds | | | |
| POS-05 | Inventory | The system shall synchronize inventory in real-time across terminals | | | |
| POS-06 | Inventory | The system shall define stock threshold alerts and reorder triggers | | | |
| POS-07 | Offline | The system shall operate in offline mode when network connectivity is lost | | | |
| POS-08 | Offline | The system shall synchronize offline transactions when connectivity is restored | | | |
| POS-09 | Hardware | The system shall define supported hardware peripherals (receipt printer, barcode scanner, cash drawer, card reader) | | | |
| POS-10 | Reporting | The system shall generate end-of-day (Z-report) and shift reports (X-report) | | | |
| POS-11 | Tax | The system shall calculate applicable taxes based on jurisdiction and product category | | | |
| POS-12 | Tax | The system shall generate tax-compliant receipts with required legal information | | | |

## GIS (Geographic Information Systems) Domain Checklist

**Applicable when**: The system handles spatial data, map rendering, or geographic analysis.

**Related skill**: `skills/gis/gis-platform-engineering` (Chwezi Dev Engine)

| # | Category | Checklist Item | Addressed | Source | Notes |
|---|----------|----------------|-----------|--------|-------|
| GIS-01 | Spatial Data | The system shall define supported coordinate reference systems (CRS/EPSG codes) | | | |
| GIS-02 | Spatial Data | The system shall define supported geometry types (point, line, polygon, multi-*) | | | |
| GIS-03 | Spatial Data | The system shall define spatial data import/export formats (GeoJSON, Shapefile, KML, GeoTIFF) | | | |
| GIS-04 | Projections | The system shall handle coordinate transformation between projections | | | |
| GIS-05 | Projections | The system shall define the default map projection for display | | | |
| GIS-06 | Map Rendering | The system shall define base map tile sources and zoom level ranges | | | |
| GIS-07 | Map Rendering | The system shall define maximum feature count per map view for performance | | | |
| GIS-08 | Map Rendering | The system shall implement tile caching strategy (client-side, server-side, CDN) | | | |
| GIS-09 | Spatial Query | The system shall define supported spatial operations (intersect, buffer, union, within) | | | |
| GIS-10 | Spatial Query | The system shall define spatial index strategy for query performance | | | |
| GIS-11 | Data Volume | The system shall define maximum dataset size and handling for large vector/raster data | | | |
| GIS-12 | Data Volume | The system shall implement data simplification for display at low zoom levels | | | |

## Cross-Domain Concerns

These items apply to all domains and shall be checked regardless of the primary domain:

| # | Category | Checklist Item | Addressed | Source | Notes |
|---|----------|----------------|-----------|--------|-------|
| CD-01 | Security | The system shall define authentication and authorization requirements | | | |
| CD-02 | Security | The system shall define data encryption requirements (at rest, in transit) | | | |
| CD-03 | Privacy | The system shall define data retention and deletion policies | | | |
| CD-04 | Privacy | The system shall handle user consent for data collection (GDPR, CCPA if applicable) | | | |
| CD-05 | Accessibility | The system shall define WCAG 2.2 compliance level (A, AA, or AAA) | | | |
| CD-06 | Localization | The system shall define supported languages and locales | | | |
| CD-07 | Integration | The system shall define all external system integrations and API contracts | | | |
| CD-08 | Performance | The system shall define response time, throughput, and concurrency targets | | | |

## Checklist Completion Recording

After completing the applicable checklists, summarize in the elicitation log:

```
## Domain Checklist Results

**Domain(s) Assessed**: [Healthcare / SaaS / POS / GIS]
**Date**: [Current Date]

| Checklist | Total Items | Addressed | Partial | Not Addressed | Coverage |
|-----------|-------------|-----------|---------|---------------|----------|
| Healthcare | 12 | 8 | 2 | 2 | 67% |
| Cross-Domain | 8 | 6 | 1 | 1 | 75% |

**Follow-up Required**:
- [HC-09]: Clinical decision support rules -- schedule SME interview
- [HC-10]: Medication interaction checking -- requires regulatory clarification
- [CD-04]: GDPR consent -- awaiting legal review
```
