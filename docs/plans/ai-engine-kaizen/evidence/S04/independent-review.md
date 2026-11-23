# S04 acceptance walkthrough

Tested revision: d56eefac9899ceba9623b826211ebcaf99451886

Walked the public importer through distinct event IDs, duplicate and conflicting payloads, legacy rows, an interrupted write and concurrent delivery. The ticket-only deduplication proposal fails the E8 case. Removing either the retry row or the legacy row caused the walkthrough check to reject the work order. The independent software reviewer owns the oracle; D07/E05 execute it and C04 reconciles both results. Checked the G1 tuple, mismatched adapter rejection, operator, replay ID and expected G1 response. PASS for the specification; actual deployment and public importer runs remain assigned to engineering.
