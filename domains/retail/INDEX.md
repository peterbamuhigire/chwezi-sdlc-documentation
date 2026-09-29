# Domain: Retail

## Profile

| Property | Value |
|---|---|
| **Regulatory Bodies** | FTC, PCI SSC, data protection authorities, consumer protection authorities, tax/fiscal-device authorities where applicable |
| **Key Standards** | PCI-DSS v4.0, GDPR/CCPA or local data protection law, WCAG 2.2 AA, consumer protection law, tax/fiscal-device rules where applicable |
| **Risk Level** | Medium to high: payment data, consumer personal data, inventory value, refunds, promotions, shrink, cash/POS settlement, and supplier funding |
| **Audit Requirement** | PCI-DSS scope review, payment/fiscal-device evidence, inventory and POS reconciliation, refund/discount approval evidence |
| **Data Classification** | Cardholder data, consumer PII, order history, loyalty data, inventory quantities/value, promotion and pricing rules, payment settlement data |

## Default Feature Modules

- Product Catalog & Inventory
- Point of Sale
- E-commerce & Orders
- Customer Loyalty
- Pricing, Promotions & Markdowns
- Omnichannel Fulfilment & Returns
- Store Operations, Labour & Audits
- Vendor Funding, Private Label & Space Productivity
- KPI Dashboard & Weekly Business Review

## Auto-Injected Requirements

See `references/nfr-defaults.md` for the full list of `[DOMAIN-DEFAULT]` requirements injected into new retail projects at scaffold time.

Key injected areas:

- **NFR:** PCI-DSS card data protection, checkout performance, consumer data rights, inventory accuracy, product data quality, retail event auditability, dashboard freshness.
- **FR:** Cookie consent management, consumer data export/deletion, payment tokenization, price and promotion governance, returns disposition, store task evidence, shrink incident capture.
- **Interfaces:** Payment gateway APIs, inventory management system sync, loyalty platform integration, POS, ERP/general ledger, warehouse management system, third-party logistics, tax/fiscal device, supplier funding register, analytics warehouse.

## Retail SRS Routing

When a project brief includes retail, omnichannel, e-commerce, POS, store operations, merchandising, pricing, promotions, markdowns, loyalty, CRM, fulfilment, returns, shrink, planograms, vendor funding, private label, or retail dashboards, load:

1. `02-requirements-engineering/retail-operating-model-srs/SKILL.md`
2. `domains/retail/references/retail-operating-model.md`
3. `domains/retail/references/finance-control-gates.md`
4. The relevant feature files listed below

If the project touches inventory value, refunds, markdowns, discounts, vendor funding, POS/cash/card/mobile-money settlement, gift cards, loyalty liabilities, shrink, stock counts, or management reporting, also route to the finance engine at `chwezi-accounting-doctrine`.

## References

- [regulations.md](references/regulations.md) - PCI-DSS, GDPR/CCPA, FTC Act, ADA Title III.
- [architecture-patterns.md](references/architecture-patterns.md) - payment tokenization, inventory sync, cart/checkout, returns, multi-channel.
- [security-baseline.md](references/security-baseline.md) - PCI scope minimization, tokenization, 3D Secure, fraud scoring, consent management.
- [nfr-defaults.md](references/nfr-defaults.md) - default non-functional requirements for injection.
- [retail-operating-model.md](references/retail-operating-model.md) - shared retail capability spine, entities, workflows, and diagnostics.
- [finance-control-gates.md](references/finance-control-gates.md) - accounting, reconciliation, and control gates for retail software.

## Feature Reference

- [product-catalog.md](features/product-catalog.md)
- [point-of-sale.md](features/point-of-sale.md)
- [ecommerce-orders.md](features/ecommerce-orders.md)
- [customer-loyalty.md](features/customer-loyalty.md)
- [pricing-promotions-markdowns.md](features/pricing-promotions-markdowns.md)
- [omnichannel-fulfilment-returns.md](features/omnichannel-fulfilment-returns.md)
- [store-operations-labour.md](features/store-operations-labour.md)
- [vendor-private-label-space.md](features/vendor-private-label-space.md)
- [retail-kpi-wbr.md](features/retail-kpi-wbr.md)

## Evidence Basis

This retail expansion is based on the internal digital-research project `umbrex-retail-playbooks-engine-enhancement`, which extracted 20 public Umbrex retail playbooks and converted them into engine implementation recommendations. Treat Umbrex pages as primary publisher evidence for the corpus structure and topics, not as independent proof of market statistics, legal requirements, or accounting treatment.
