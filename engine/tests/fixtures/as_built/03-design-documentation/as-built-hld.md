---
phase: '03'
generated_from_commit: "0000000000000000000000000000000000000000"
source_repository: ../missing-garage-erp
---
# As-Built High-Level Design — Garage ERP (fixture)

Invoice numbers are allocated from the `invoice_sequences` table inside the posting transaction. [AS-BUILT]

Job cards are created by `JobCardController::store`, which calls the parts reservation service. [AS-BUILT]

The nightly job `cron/close_day.php` posts the day's takings to the ledger. [AS-BUILT]

Credit notes appear unused since March 2023. [VERIFY: confirm with the finance lead whether credit notes are raised outside the system]

The `discount_rules` table has two readers with different rounding. [VERIFY: confirm which rounding the business intends]

The marker convention itself (`[AS-BUILT]`, `[VERIFY: reason]`) is not a live marker when quoted in code.
