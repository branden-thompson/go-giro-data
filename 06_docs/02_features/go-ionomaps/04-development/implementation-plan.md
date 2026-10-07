---
title: "go-ionomaps v0.1.0 — IMPLEMENTATION PLAN"
date: 2026-10-06
phase: PLAN
sev: SEV-0
authority: HUM LEAD
status: "DRAFT for the PLAN gate. No code: signatures, shapes, test descriptions, file paths and order only (watchpost 0.18.0 D-13)."
---

# Implementation plan

**Goal.** Build `requirements.md` (approved at watchpost D-84), test-first, so that watchpost 0.19.0 can pin
a release candidate in its BUILD and ship on v0.1.0 (watchpost D-3).

**Tech stack.**
- Go 1.25.13, no cgo, the standard library only, unless a dependency is ruled.
- PyIRI (MIT) is ported, not imported.
- A pinned `govulncheck` from the first dependency (NFR-1).

**Every task follows the same order** (watchpost's):
1. Write the named test and watch it fail for the named reason.
2. Make the change.
3. Run the gate.
4. Mutation check: disable what the test protects, watch it fail, restore by copy.

## Where code lives

| Path | Holds |
|---|---|
| `ionomaps.go`, `snapshot.go`, `answers.go` | the public surface (watchpost architecture, "go-ionomaps' shape") |
| `internal/throttle/` | D-39's budget, back-off and early answers (R-5.3, R-5.4) |
| `internal/stations/` | the seed list and rotation (R-5.5); `stations.tsv`, codes and positions only |
| `internal/giro/`, `internal/glotec/`, `internal/drap/`, `internal/scales/` | requests and parsing for each source (R-3.3, R-3.4, R-8.2, R-2.10) |
| `internal/climatology/` | the PyIRI port over `Tables` (R-9.1, R-4.4) |
| `internal/climatology/tables/` | NRL's refits, converted (R-4.3: the only third-party data allowed) |
| `internal/assimilate/` | the Gaussian process (R-9.2) |
| `internal/limits/` | P.533 path MUF, daytime absorption, D-RAP (R-2.4 to R-2.7) |
| `internal/forecast/` | hours ahead (R-1.3) |
| `internal/terms/` | sources, terms and citations (R-4.1) |
| `tools/tables/` | the build-time converter for the refits |
| `testdata/` | synthetic inputs only; **no GIRO data** (R-4.3) |
| `scripts/gate`, `.github/workflows/gate.yml` | the gate (NFR-1), modelled on go-tuiMaps' |

## Work packages

| WP | What | Requirements | Needs |
|---|---|---|---|
| G0 | Foundations: the gate, CI, the third-party-data scan, the NOTICE test, the citation check | NFR-1, R-4.2, R-4.3, R-7.1 | — |
| G1 | Public types, terms, the fetcher contract | R-1.2, R-4.1, R-5.1 | G0 |
| G2 | Parsers: GIRO, GloTEC, D-RAP, the scales, with fuzzers and physical ranges | R-3.1 to R-3.4, R-8.2, R-2.10 | G1 |
| G3 | The climatology: the PyIRI port, the tables seam, the refits | R-9.1, R-4.4, R-7.3 | G1 |
| G4 | The background: GloTEC fields, the fallback named | R-9.3, R-3.2 | G2, G3 |
| G5 | Assimilation of foF2 and M(3000)F2 | R-9.2, R-9.4 | G4 |
| G6 | Limits and statuses: path MUF, absorption, disturbed | R-2.2, R-2.4 to R-2.7 | G5 |
| G7 | Answers: bands, path, reach, many points | R-2.1, R-2.3, R-2.8, R-2.9 | G6 |
| G8 | Forecast hours and their floor | R-1.3 | G5, G3 |
| G9 | Throttle, stations, update, concurrency | R-5.2 to R-5.6 | G2 |
| G10 | Reproducibility, fault injection, benchmarks, the G-M3 instrument | R-6.1, G-M2, G-M3, G-M4, R-8.1 | G7, G8, G9 |

## G0 — Foundations

| # | Task | Test first |
|---|---|---|
| G0.1 | The gate: tests with `-race`, `go vet`, `gofmt -l`, fuzz smoke, P10, pinned `govulncheck`; a docs lane for Markdown-only changes | the gate fails on a planted vet error, an unformatted file and an empty change (a gate that cannot fail is refused, watchpost REFLECT L7) |
| G0.2 | No third-party data in the tree: a content scan (a FastChar header, URSI codes beside confidence columns) and an allowed list | `TestNoThirdPartyDataIsCommitted` fails on a planted FastChar reply |
| G0.3 | The NOTICE names every source in `internal/terms` | `TestTheNoticeNamesEverySource` fails when a source is added without its NOTICE entry |
| G0.4 | Every exported function cites its source | a citation check fails on an exported function with no "Source:" line |

## G1 — Types, terms, the fetcher

| # | Task | Shape | Test first |
|---|---|---|---|
| G1.1 | `Snapshot`, `Hour`, `Field`, `Source`, `Background` | as watchpost's architecture shows | `TestAFieldSaysWhenAndFromWhat` |
| G1.2 | `Fetcher`, `Response`, `Validators` | `Fetch(ctx, url, Validators) (Response, error)` | `TestTheLibraryOpensNoConnectionOfItsOwn` (a fetcher that counts; no `net` import in the module outside tests) |

## G2 — Parsers

| # | Task | Test first |
|---|---|---|
| G2.1 | GIRO FastChar text: header and comment lines dropped first; rows parsed; ranges checked | `TestReplyHeadersNeverLeaveTheParser`, `TestOutOfRangeReadingsAreRejectedAndCounted`, `FuzzGIROParser` |
| G2.2 | GloTEC GeoJSON, typed decode | `BenchmarkGloTECDecode`, `FuzzGloTECDecode`, `TestFoF2FromNmF2` |
| G2.3 | D-RAP table | `FuzzDRAPParser`, `TestDRAPGridIsTwoByFour` (from the measured file's layout) |
| G2.4 | Station codes `^[A-Z0-9]{5}$`, through `url.Values` | `TestStationCodesAreChecked` |
| G2.5 | NOAA's scales feed: levels 0 to 5 checked, outlook days and probabilities, unset when missing (D-88) | `FuzzScalesParser`, `TestTheScalesAreCarriedInTheSnapshot`, `TestMissingScalesAreUnsetNotZero` |

## G3 — The climatology

| # | Task | Test first |
|---|---|---|
| G3.1 | `Tables` and the port of PyIRI's evaluation (spherical harmonics in modip, Fourier in local time) | `TestTheFallbackMatchesPyIRI` against values produced by PyIRI 0.1.7 (MIT) at fixed inputs, committed as a small golden |
| G3.2 | The refits converter (`tools/tables`) and the converted tables | `TestTheConvertedTablesRoundTrip` |
| G3.3 | Sunspot scale and the R12 cap | `TestTheSunspotScaleIsConverted`, `TestFoF2IsCappedAt160` |
| G3.4 | Any tables through the seam | `TestTheClimatologyRunsOnAnySuppliedTables` |

## G4 to G8 — The science

| # | Task | Test first |
|---|---|---|
| G4.1 | GloTEC background; climatology when GloTEC is missing, named | `TestTheFallbackIsUsedAndNamed` |
| G5.1 | The GP on the sphere for foF2 and M(3000)F2 residuals; kernel valid on the sphere | `TestTheKernelIsValidOnTheSphere` (positive-definite on random station sets), `TestAResidualAtAStationIsRecovered` |
| G6.1 | P.533 path MUF | `TestPathMUFFollowsP533` against the recommendation's worked values |
| G6.2 | Daytime absorption for the reference circuit | `TestDaytimeAbsorptionClosesTheLowBands` (80 m absorbed at local noon, open at night, mid-latitude) |
| G6.3 | D-RAP disturbed | `TestADisturbanceMarksTheBandsItCovers` |
| G6.4 | Statuses naming their limit | `TestEveryStatusNamesItsLimit` |
| G7.1 | `Bands`, `Path`, `Reach`, many points in one call | `TestBestBandsForAnArea`, `TestTheDaysOpenHours`, `TestAFrequencysReachIsAField`, `TestTheSkipZoneIsReturned`, `TestReadingsForManyPointsInOneCall` |
| G8.1 | Forecast hours | `TestForecastHoursDecayTowardClimatology`, `TestAForecastSaysItIsOne` |

## G9 — Throttle, stations, update

| # | Task | Test first |
|---|---|---|
| G9.1 | The burst cap, the hourly limit, 2 a minute, the back-off, `Retry-After` honoured | `TestAnUpdateNeverExceedsItsBurst`, `TestA429BacksOff`, `TestRetryAfterIsHonouredWhenSent` (a fake clock and a counting fetcher) |
| G9.2 | Early answers from the last good snapshot | `TestAnEarlyUpdateAnswersFromTheLastField` |
| G9.3 | The seed, the dark-station drop, one probe inside the 40 (D-87), rotation at 40 or more live | `TestAColdStartUsesTheSeedWithoutABurst`, `TestADarkStationIsDroppedAfterThreeDays`, `TestOneProbePerUpdate`, `TestTheProbeCountsInsideTheBurst` (40 live: 39 polled, 1 probe), `TestAboveFortyStationsRotate` |
| G9.4 | Readings only since the last held | `TestAnUpdateAsksOnlySinceTheLastReading` |
| G9.5 | Concurrent callers merged; no goroutines of its own | `TestOverlappingUpdatesMergeIntoOne`, `TestTheLibraryStartsNoGoroutines`, the race detector |

## G10 — Instruments

| # | Task | Test first |
|---|---|---|
| G10.1 | Reproducibility on synthetic inputs (G-M2) | `TestAFieldIsReproducedFromItsInputs` |
| G10.2 | Fault injection: every input stopped, stale, truncated, reformatted (G-M4) | the fault table, each case reported, never a silent field |
| G10.3 | Cost per update (G-G1) | a benchmark at 2° and 1°, recorded |
| G10.4 | The G-M3 instrument: leave-one-station-out over recorded inputs kept outside the tree, failing when they are missing | the Go replica of the dry run's `loo_hybrid.py` agrees with it on the dry run's data |

## Release

- v0.1.0 release candidates are tagged as G10 lands.
- watchpost pins each candidate in its BUILD.
- v0.1.0 is tagged when watchpost's REVIEW is satisfied, as go-tuiMaps v0.2.0 was.
