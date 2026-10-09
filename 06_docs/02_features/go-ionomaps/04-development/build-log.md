# BUILD log — go-ionomaps v0.1.0

Up: [implementation plan](implementation-plan.md)

| Field | Value |
|---|---|
| Phase | BUILD, opened 2026-10-07 at the PLAN gate (watchpost D-139; D-48) |
| What this is | One row for each plan task as it is finished: the commit, the test first, and anything learned that the plan did not say |
| Order | G0 to G4 first, for watchpost's UAT-1 (watchpost D-151; D-49) |
| Gate for every row | `scripts/gate`, full, on go1.27.2; the module's floor is go 1.26.9 (watchpost D-152; D-50) |

## G0 — Foundations

| Task | Commit | The test first | Learned |
|---|---|---|---|
| G0.1 The gate and CI | this commit | `TestTheGateIsGreenOnAPassingTree`, `TestTheGateFailsOnWhatItCatches` (a planted vet error, unformatted file, failing test, and a docs lane with nothing staged, each failing and named), `TestTheGateRefusesTwoModes` | `scripts/gate` is a smaller go-tuiMaps gate: quick, docs and fuzz lanes, every fuzz target found and run, the pinned `govulncheck` at the floor, five cross-compiles, P10 where the harness is set up, and every run logged with the tree tested. `.github/workflows/gate.yml` runs the quick gate on each push and the full gate on dispatch, on linux/amd64 and arm64 |
| G0.2 No third-party data in the tree | this commit | `TestNoThirdPartyDataIsCommitted`: every file git knows of is scanned by content for a FastChar reply's three signatures (the station's location header, the column header with its confidence and qualifier columns, rows of soundings); each signature planted alone is caught, one example row is not | The first planted reply carried all three signatures, so the location check could be disabled and the test still passed (a hand mutant survived); each signature is now planted alone |
| G0.3 The NOTICE names every source | this commit | `TestTheNoticeNamesEverySource`, with a planted source missing from it | `internal/terms` holds the static list of sources and their run-time hosts (GIRO's `lgdc.uml.edu`, NOAA's `services.swpc.noaa.gov`; PyIRI, IGRF-14 and the ITU recommendations at build time only) and the committed datasets (none yet) |
| G0.4 Every exported function cites its source | this commit | `TestEveryExportedFunctionCitesItsSource`, with a planted uncited function | The first run also read the plan's spike, a nested module of evidence under `06_docs`; the check covers this module's own files |

**The order, honestly:** the tests were written before their code but first run after it. Each test plants the fault it exists to catch, and each guard was then disabled by hand, seen to fail its test, and restored by copy (four mutants, all killed after the G0.2 fix).

**P10 on the first full gate:** the invariant-density rule flagged the plan's spike (PLAN evidence, a nested module), `internal/terms` (a static list) and `internal/repocheck` (one real guard each). Each was ratified as an exemption (D-51) rather than padded; the ledger stays the harness's, and `06_docs/p10-ledger.md` is its tracked mirror, held by `TestTheP10MirrorMatchesTheLedger` and `TestEveryP10MirrorRowNamesCodeThatExists` (ported from go-tuiMaps).

## G1 — Types, terms, the fetcher

| Task | Commit | The test first | Learned |
|---|---|---|---|
| G1.1 `Snapshot`, `Hour`, `Field`, `Background` | this commit | `TestTheGridIsTwoDegrees`, `TestAGlobalFieldIsAValidTuimapsGrid`, `TestAFieldSaysWhenAndFromWhat` (`snapshot_test.go`): written and run first, they failed to compile on the missing types | **The grid is 180 by 90 cells, each value its cell's centre** (179°W, 89°N first): go-tuiMaps samples a grid as cells (`internal/render/field.go:48`), so outer edges at -180..180 and -90..90 mean cells, not edge points. `Field.CellCentre` refuses a cell off the grid rather than answer 0, 0. `NoData` is a bitset; an empty field marks every cell. The test's own error, asking an empty field's cell to have data, was fixed in the test |
| G1.2 `Fetcher`, `Response`, `Validators`, `New`, `Sources` | this commit | `TestTheLibraryOpensNoConnectionOfItsOwn` (no import of net, net/http, crypto/tls or os/exec outside tests; `New` refuses a nil fetcher and asks nothing), `TestEverySourceCarriesItsTerms`, `TestEveryRequestGoesToAnExportedHost` (every web address written in the code is on an exported host; a planted one is caught) | `Response` carries its own small header type, the rate headers and validators only (I-1). The counting-server half of R-5.1 comes with the first fetch (G2). **P10:** the bare-name recursion check took `Library.Sources` calling `terms.Sources` for recursion, so the internal list is `terms.All`; the density rule's 0.56 on the nine small functions was ratified as a root-package row (D-52 withdrawn by D-53: density rows are by package only) that `TestTheRootExemptionEndsAtUpdate` ends when `Library.Update` is declared (planted, caught). Five hand mutants, all killed |

## G2 — Parsers

| Task | Commit | The test first | Learned |
|---|---|---|---|
| G2.2 GloTEC GeoJSON, typed decode | this commit | `TestFoF2FromNmF2`, `TestAGridIsReadIntoItsCells`, `TestOutOfRangeCellsAreRejectedAndCounted`, `TestAChangedFormatIsAnError` (not JSON, no time, a future time, a point off the grid, a point missing, a point repeated; no error quotes the input), `FuzzGloTECDecode`, `BenchmarkGloTECDecode` (`internal/glotec`): written and run first, failing to compile | **GloTEC is 72 by 72 points at the centres of 5° by 2.5° cells** (from the dry run's saved grids, read locally; none committed, R-4.3: the tests build a synthetic grid). foF2 = 8.98e-6 √NmF2 MHz. The quality flag is carried per cell, never dropped. Bounds are A-1. **Typed decode:** 4.2 ms, 0.8 MB and 28 allocations a grid; slice coordinates had cost 10,397 allocations, so they are a fixed `[2]float64` (a short array reads as 0, 0, no cell centre). Two of the test's own cases were wrong at first (a text match that missed; one later added for a repeated point, after a hand mutant survived). P10 counts a guard only when its condition calls nothing and its body is one return, so the existing checks were phrased that way; nothing was added to reach the bar. Five hand mutants killed; 60 s of fuzzing clean |
