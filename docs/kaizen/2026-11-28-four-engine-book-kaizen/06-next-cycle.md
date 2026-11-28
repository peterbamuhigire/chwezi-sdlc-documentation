# Next cycle

The repository maintainer should re-audit by 2026-12-28 or at the next routing, platform, packaging or recovery-contract change. This takes over from the November 29 check after the November 28 [source refresh](standards-source-register.md).

1. Replay the [second-wave recovery cases](03-experiment-log.md#second-wave-recovery-replay) using the deployment guide prompt. Confirm that a compatible rollback still proceeds and that a same-count loss or repeated queue effect blocks writer resumption.
2. Re-verify each of the four platform claims against its primary source. Run `python scripts/validate_source_register.py --today 2026-12-28`. Without a newer register, the same check dated `2026-12-29` must fail on the four overdue claims.
3. Recheck the Windows failures in the [validator ledger](04-validation-record.md) after changes to the relevant managed runtime or environment. Run the packaging check in a clean checkout and keep the populated-checkout result available separately.

Live operator acceptance, production migration, live-model routing, hosted installation, authenticated account behavior, comparative model cost and the full Linux kernel suite remain `NOT_ASSESSED`. The [Linux recheck](04-validation-record.md#linux-recheck) covers the engine, source and clean-package contracts. Historical standards mappings and project decisions remain with their designated owners.
