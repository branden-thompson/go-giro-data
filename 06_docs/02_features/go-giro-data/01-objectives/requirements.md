---
title: "go-giro-data — REQUIREMENTS"
date: 2026-10-06
phase: DISCOVER
sev: SEV-0
authority: HUM LEAD
status: "DRAFT — approved at the DISCOVER gate. Rows marked (path) wait for watchpost D-20's path ruling (B: GIRO-driven on a PyIRI port; D: derived from NOAA GloTEC) at DISCOVER exit."
---

# Requirements

Each row traces to the brief's G-R-n, a host requirement (GR-n, watchpost's brief) or a ruling.
**What, never how.** PLAN carries signatures only.

Each row's **Instrument** is a planned test name, a check or a metric. A planned name is a commitment
PLAN may rename, never drop.

## R-1 — Fields (G-R1, GR-1)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-1.1 | MUF(3000) and foF2 over the globe for a UTC hour, on a grid a go-tuiMaps host can hand in directly (outer edges -180..180, -90..90; no antimeridian crossing), 2° by default, 1° as an option | G-R1; compute (wave 1) | `TestAGlobalFieldIsAValidTuimapsGrid`, `TestTheGridStepIsTheHostsChoice` |
| R-1.2 | Every field carries the time it is valid for, the time it was computed, and its sources | G-R1, G-R4 | `TestAFieldSaysWhenAndFromWhat` |
| R-1.3 | MUF(3000) is derived from foF2 and M(3000)F2 by the published ITU-R P.533 method, checked against the recommendation's own worked values before use | wave 1 (P.533 equations rebuilt from a garbled extraction) | `TestMUFFollowsP533`, its values cited |

## R-2 — Readings at a point (GR-2; watchpost D-28, D-27)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-2.1 | foF2 and MUF(3000) at any point, from the field | D-28 (the readout), D-37 (the centre) | `TestAReadingAtAPointComesFromTheField` |
| R-2.2 | For a path between two points at an hour: whether each amateur band 160 m to 10 m is expected open, with the near-vertical case (short paths) answered from foF2 | GR-2; D-24, D-30 | `TestEachBandsStatusForAPath`, `TestShortPathsUseFoF2` |
| R-2.3 | The point and path calls serve one place or many, so a future shortlist (watchpost D-27) needs no new call | D-27 | `TestReadingsForManyPointsInOneCall` |

## R-3 — Fails out loud (G-R3, GR-3; G-M4)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-3.1 | An input that stops, goes stale or changes format yields an error or a stated age, never a silently old or empty field | G-M4 | `FuzzEveryInputParser`, `TestAStaleInputIsSaidStale`, the fault-injection table (G-M4) |
| R-3.2 | A partly covered field says which part is measured and which is background | G-M4 | `TestAFieldSaysWhereItIsMeasured` |

## R-4 — Terms travel with the data (G-R4, GR-4; G-M1)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-4.1 | Each source's name, terms and required citation are readable by the host, so it can credit them | G-M1 | `TestEverySourceCarriesItsTerms` (G-M1's list) |
| R-4.2 | The repository's README and NOTICE state every source's terms; the MIT code licence is stated not to relicense data | G-R4; D-2 | `TestTheNoticeNamesEverySource` |
| R-4.3 | No third-party data is committed until its provenance is ruled: no GIRO readings ever; coefficient tables only after a provenance ruling (PyIRI's CCIR/URSI tables state none) | D-2, D-31; wave 1 | `TestNoThirdPartyDataIsCommitted` (a tree scan against an allowed list) |

## R-5 — The host owns the network (G-R5, GR-5)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-5.1 | The library opens no network connection of its own; the host supplies the fetcher (User-Agent, allowed hosts, timeout) | GR-5; watchpost 0.18.0 HR-6's lesson | `TestTheLibraryOpensNoConnectionOfItsOwn` |
| R-5.2 | It asks only for what an update needs, at no more than the host's stated cadence | NFR-3 (watchpost) | `TestAnUpdateAsksOnlyWhatItNeeds` |
| R-5.3 | **Throttle behaviour (watchpost D-39):** live stations only, list refreshed at most daily; one update's requests in a burst of at most 40, at most hourly, at most 2 a minute sustained; a 429 stops the update and backs off 60 s doubling to 15 minutes; the last good field is kept with its age; a `Retry-After`, if ever sent, is honoured | watchpost D-38, D-39 | `TestAnUpdateNeverExceedsItsBurst`, `TestA429BacksOff`, `TestRetryAfterIsHonouredWhenSent` |

## R-6 — Reproducible (G-R6; G-M2)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-6.1 | From the recorded inputs for an hour, the same field is produced on another machine, within G-M2's target | G-M2 | `TestAFieldIsReproducedFromItsInputs` (a recorded-input golden, kept outside the tree if its data may not be committed) |

## R-7 — A reimplementation traceable to its sources (G-R8)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-7.1 | Every algorithm cites the published work it implements (paper, recommendation, or PyIRI under MIT with its notice kept) | G-R8 | a citation check over exported functions |
| R-7.2 | Nothing comes from `arodland/prop`, which has no licence, or from IRI's Fortran, whose licence grants no distribution | wave 1 | the provenance record in PLAN |
| R-7.3 | Sunspot numbers on SILSO's version-2 scale are converted to the version-1 scale (k = 0.6) the ITU coefficients use; foF2 is capped at R12 = 160 | wave 1 (P.1239) | `TestTheSunspotScaleIsConverted`, `TestFoF2IsCappedAt160` |

## R-8 — Bounded cost (G-R7, GR-6; G-G1)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-8.1 | One update's CPU and peak memory are measured and within G-G1's target; it recomputes only on new data | G-G1 | a benchmark, recorded |

## R-9 — The path's own requirements *(path)*

| # | Requirement | Applies if | Instrument |
|---|---|---|---|
| R-9.1 | A background model: PyIRI's method, ported (foF2 and M(3000)F2, whole globe, every hour) | B, and D where GloTEC has no observations | `TestTheBackgroundMatchesPyIRI` (against PyIRI's published outputs) |
| R-9.2 | An effective sunspot number fitted from measurements (Secan & Wilkinson 1997) | B | `TestTheEffectiveSunspotFit` |
| R-9.3 | Spatial assimilation of station residuals on the sphere with a valid kernel (Gneiting 2013) | B | `TestTheKernelIsValidOnTheSphere`, G-M3 |
| R-9.4 | foF2 and M(3000)F2 derived from GloTEC's NmF2 and hmF2 | D | `TestFoF2FromNmF2`, G-M3 |
| R-9.5 | GIRO readings at a schedule GIRO's limits allow, with confidence scores used | B | the request budget; `TestLowConfidenceReadingsAreDropped` |

## Metrics

G-M1 to G-M4 and G-G1 as ruled (watchpost D-12) in `problem-statement.md`. Targets are set in DISCOVER and
the PLAN-time dry run. G-M3's starting point from the literature is about 0.5 MHz RMS near stations and
1-2 MHz far from them, with climatology as the baseline (watchpost D-23).
