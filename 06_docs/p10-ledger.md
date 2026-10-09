<!-- GENERATED from the local P10 ledger by `go test -run TestTheP10MirrorMatchesTheLedger -update-p10-mirror .` - do not edit by hand. -->

# P10 exemption ledger - the tracked mirror

**Every row here was RATIFIED by the HUM LEAD, never self-issued** (D-51). The ledger the P10 check reads
is the harness's and is not tracked, so this mirror is how a clone reproduces "P10 clean": each row is an
exemption the HUM LEAD approved, with the reason as ratified. A row is added by ratifying it with the HUM
LEAD, writing it to the ledger and regenerating this file; `TestTheP10MirrorMatchesTheLedger` fails while
the two differ, and `TestEveryP10MirrorRowNamesCodeThatExists` while a row names code that is gone.

**3 rows.**

| File | Symbol | Rule | Ratified | Reason |
|---|---|---|---|---|
| `06_docs/02_features/go-ionomaps/02-analysis/evidence/plan-dry-run/spike` | `package` | P10-05-INVARIANT-DENSITY | 2026-10-09 | The plan's spike: a nested module of PLAN evidence (the answers' cost at 2 degrees), committed at PLAN and never part of the library or built by it. P10 skips nested modules otherwise and counts this one only for density. RATIFIED by HUM LEAD 2026-10-09 (D-51: "Ratify all three"). Removable if the evidence moves out of the repository. |
| `internal/terms` | `package` | P10-05-INVARIANT-DENSITY | 2026-10-09 | A static list: Sources() and Datasets() return fixed values, never text parsed from replies (R-4.1), so there is nothing to check at run time. Their content is held by TestTheNoticeNamesEverySource and, from G1, TestEverySourceCarriesItsTerms. RATIFIED by HUM LEAD 2026-10-09 (D-51). Removable if the package gains functions that take input. |
| `internal/repocheck` | `package` | P10-05-INVARIANT-DENSITY | 2026-10-09 | The repository's own checks: the data scan and the NOTICE check, each with one meaningful guard (empty content holds nothing; a check over no sources is refused); a second would only pad. Each is held by a test that plants the fault it catches, and each guard was mutated by hand and caught. RATIFIED by HUM LEAD 2026-10-09 (D-51). Removable if the package gains functions with more to check. |
