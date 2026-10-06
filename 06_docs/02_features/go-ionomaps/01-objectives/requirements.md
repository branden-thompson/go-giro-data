---
title: "go-ionomaps — REQUIREMENTS"
date: 2026-10-06
phase: DISCOVER
sev: SEV-0
authority: HUM LEAD
status: "DRAFT — for approval at the DISCOVER gate. The path is B on D (watchpost D-40): GIRO station residuals assimilated over a GloTEC-derived background, a PyIRI-port climatology as the fallback. Revised after the DISCOVER-exit red team, round 1 (watchpost 08-reports/red-team-discover.md)."
---

# Requirements

## What this gives the host (watchpost D-82)

- **Maps:** MUF(3000) and foF2 over the whole world for now and for each hour up to a day ahead, ready for a go-tuiMaps grid.
- **Answers:** for any place or path, each amateur HF band is called open, above the upper limit, absorbed, disturbed or no data, under a stated reference circuit. A frequency's reach is given as a skip zone and an area reached.
- **The host owns the network:** the library asks only when the host does, through the host's fetcher, under a throttle it keeps itself, and states every source's terms.

## How to read the rows

Each row traces to the brief's G-R-n, a host requirement (GR-n, watchpost's brief) or a ruling. Rulings are
watchpost's unless marked. **What, never how.** PLAN carries signatures only.

Each row's **Instrument** is a planned test name, a check or a metric. A planned name is a commitment PLAN
may rename, never drop.

## R-1 — Fields (G-R1, GR-1)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-1.1 | MUF(3000) and foF2 over the globe for a UTC hour, on a grid a go-tuiMaps host can hand in directly (outer edges -180..180, -90..90; no antimeridian crossing), 2° by default, 1° as an option. MUF(3000) is foF2 × M(3000)F2 by definition | G-R1 | `TestAGlobalFieldIsAValidTuimapsGrid`, `TestTheGridStepIsTheHostsChoice` |
| R-1.2 | Every field carries the time it is valid for, the time it was computed, and its sources | G-R1, G-R4 | `TestAFieldSaysWhenAndFromWhat` |
| R-1.3 | **Hours ahead (D-50):** fields for each hour up to 24 h ahead, from the background carried forward with the current station corrections decaying toward climatology; each labelled a forecast, with the time it was made. **Floor (D-75):** forecast error at +3 h and +12 h no worse than climatology, or hours ahead are cut from 0.19.0 | D-50, D-75 | `TestForecastHoursDecayTowardClimatology`, `TestAForecastSaysItIsOne`; the forecast metric (D-75) in the dry run |

## R-2 — Readings at a point and along a path (GR-2; D-27, D-28, D-37, D-47)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-2.1 | foF2 and MUF(3000) at any point, from the field | D-28, D-37 | `TestAReadingAtAPointComesFromTheField` |
| R-2.2 | For a path between two points at an hour, each amateur band 160 m to 10 m gets a status (R-2.6) under **the reference circuit: SSB voice at 100 W with simple antennas, about +10 dB signal-to-noise in 2.5 kHz** (D-73); short paths (near-vertical) take their upper limit from foF2 | GR-2; D-24, D-73 | `TestEachBandsStatusForAPath`, `TestShortPathsUseFoF2` |
| R-2.3 | The point and path calls serve one place or many, so a future shortlist (D-27) needs no new call | D-27 | `TestReadingsForManyPointsInOneCall` |
| R-2.4 | **The lower limit (D-47):** regular daytime D-layer absorption for each band and path, from the published method behind ITU-R P.533's absorption term (solar zenith angle, frequency, solar activity), implemented from the method, never copied text or tables | D-47 | `TestDaytimeAbsorptionClosesTheLowBands`, its worked values cited |
| R-2.5 | Disturbance absorption (flares, polar-cap events) from NOAA SWPC's D-RAP (`text/drap_global_frequencies.txt`, public domain), fetched when the host asks (D-76); a band below D-RAP's 1 dB frequency is **disturbed**, a named degraded state, not closed (D-73) | D-47, D-73, D-76 | `TestADisturbanceMarksTheBandsItCovers` |
| R-2.6 | Each band's status is one of: open (between the limits), above the upper limit, absorbed, disturbed, or no data, and names the limit that decided it | D-47, D-73; AX-F | `TestEveryStatusNamesItsLimit` |
| R-2.8 | **Best bands for an area (D-76):** for the near-vertical area around a point (within a radius the host gives) and for a path, each band's status now and the hours today it is expected open | D-74, D-76 | `TestBestBandsForAnArea`, `TestTheDaysOpenHours` |
| R-2.9 | **A frequency's reach (D-76):** for a frequency, an origin and an hour, the skip zone and the area reached under the reference circuit, as a field a go-tuiMaps host draws (reached or not, on the generic host ramp, go-tuiMaps L-2.2), with the limit that bounds it | D-76 | `TestAFrequencysReachIsAField`, `TestTheSkipZoneIsReturned` |
| R-2.7 | MUF for paths other than 3000 km follows the published ITU-R P.533 method, its equations checked against the recommendation's own worked values before use (wave 1 rebuilt them from a garbled extraction) | wave 1; CQ-C2 | `TestPathMUFFollowsP533`, its values cited |

## R-3 — Fails out loud, and trusts no input (G-R3, GR-3; G-M4)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-3.1 | An input that stops, goes stale or changes format yields an error or a stated age, never a silently old or empty field | G-M4 | `FuzzEveryInputParser`, `TestAStaleInputIsSaidStale`, the fault-injection table (G-M4) |
| R-3.2 | A partly covered field says which part is measured and which is background | G-M4 | `TestAFieldSaysWhereItIsMeasured` |
| R-3.3 | **Physical ranges (IS-3):** foF2, hmF2, NmF2, M(3000)F2, confidence scores, coordinates and times are checked against physical bounds (no time in the future or outside the asked window); counts of stations and grid cells are capped; rejected values are counted and reported; **no NaN or Inf ever leaves the library**; station codes match `^[A-Z0-9]{5}$` and reach URLs only through `url.Values` | IS-3 | `FuzzNoNaNOrInfLeavesTheLibrary`, `TestOutOfRangeReadingsAreRejectedAndCounted`, `TestStationCodesAreChecked` |
| R-3.4 | **The requester's IP (IS-2):** GIRO's replies carry the requester's IP in a header line; header and comment lines are dropped before parsing; no error quotes input text; nothing the library returns or stores holds a reply's raw text | IS-2 | `TestReplyHeadersNeverLeaveTheParser`, `TestErrorsNeverQuoteInput` |

## R-4 — Terms travel with the data (G-R4, GR-4; G-M1)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-4.1 | Each source's name, terms and required citation are readable by the host, from a static list (never text parsed from replies), so it can credit them | G-M1; IS-3 | `TestEverySourceCarriesItsTerms` (G-M1's list) |
| R-4.2 | The README and NOTICE state every source's terms; the MIT code licence does not relicense data; **the live GIRO input is for non-commercial use** (GIRO: "only for educational and non-commercial research purposes"), so a commercial user arranges their own access or runs on the GloTEC and climatology background alone; a computed field is treated as a substantially derivative product (D-41, D-69) | G-R4; D-2, D-41, D-69 | `TestTheNoticeNamesEverySource` |
| R-4.3 | No third-party data is committed except as ruled: no GIRO readings ever; of coefficient tables, only NRL's spherical-harmonic refits from PyIRI (MIT; Forsythe et al. 2024; their CCIR/URSI lineage stated in the NOTICE), never the raw CCIR/URSI tables (D-43). The check scans **file content** (a FastChar header, URSI codes beside confidence columns), not only an allowed list; a change to the allowed list needs a ruling | D-31, D-43; CQ-V3 | `TestNoThirdPartyDataIsCommitted` |
| R-4.4 | **The coefficients sit behind a swappable seam** (D-43): the climatology reads its tables through one interface, so they can be removed or replaced without touching the rest | D-43 | `TestTheClimatologyRunsOnAnySuppliedTables` |

## R-5 — The host owns the network (G-R5, GR-5)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-5.1 | The library opens no network connection of its own; the host supplies the fetcher (User-Agent, timeout). **The fetcher must not retry a 429** and must hand the library each response's status and headers, so the library alone decides a back-off (watchpost's httpx retries a 429 by default, `platform/httpx/httpx.go:926-928`) | GR-5; IS-1, CQ-T1, PF-F1 | `TestTheLibraryOpensNoConnectionOfItsOwn`, `TestA429IsSeenByTheLibraryNotRetried` (a counting fake server) |
| R-5.2 | An update asks only for what it needs: from GIRO, only the readings since the last one held (not the whole day again) | PF-F2 | `TestAnUpdateAsksOnlySinceTheLastReading` |
| R-5.3 | **Throttle behaviour (D-39):** one update's GIRO requests in a burst of at most 40, at most hourly, at most 2 a minute sustained; a 429 stops the update and backs off 60 s doubling to 15 minutes; the last good field is kept with its age; a `Retry-After`, if ever sent, is honoured. NOAA grids at most 6 an hour. Updates happen only when the host asks (D-76). With 40 live stations, a rotation probe would make 41: how the cap and the probe share an update is a PLAN question | D-38, D-39, D-76 | `TestAnUpdateNeverExceedsItsBurst`, `TestA429BacksOff`, `TestRetryAfterIsHonouredWhenSent` |
| R-5.4 | **Pull (D-42):** the host asks for an update; the library starts no goroutines or timers; it holds the throttle state, and an update asked too soon is answered from the last good field with its age and the reason | D-42 | `TestTheLibraryStartsNoGoroutines`, `TestAnEarlyUpdateAnswersFromTheLastField` (a fake clock) |
| R-5.5 | **The live-station list (D-51):** a shipped seed list (codes and positions only); a station dropped after 3 days with no data; one not-live station probed per update, in rotation; above 40 live, polled in rotation, those left out asked first next time; a cold start never probes in a burst | D-51 | `TestAColdStartUsesTheSeedWithoutABurst`, `TestADarkStationIsDroppedAfterThreeDays`, `TestOneProbePerUpdate`, `TestAboveFortyStationsRotate` |
| R-5.6 | **One owner of the throttle per process (PF-F8):** a library object is safe for concurrent use and merges overlapping updates into one; a host with several callers (watchpost's readout, Propagation mode and recorder) shares one object and one computed field | PF-F8 | `TestOverlappingUpdatesMergeIntoOne`, `go test -race` |

## R-6 — Reproducible (G-R6; G-M2)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-6.1 | From the same inputs for an hour, the same field is produced on another machine, within G-M2's target. In CI the inputs are **synthetic and committed**; real inputs are re-fetched under the throttle in the dry run, never kept in the tree, and the dry run fails if they are missing | G-M2; CQ-V2, DQ-F11 | `TestAFieldIsReproducedFromItsInputs` (synthetic golden); the dry run's real-input check |

## R-7 — A reimplementation traceable to its sources (G-R8; D-53)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-7.1 | Every exported function cites the published work it implements (paper, recommendation, or PyIRI under MIT with its notice kept) | G-R8; D-53 | a citation check over exported functions |
| R-7.2 | `arodland/prop` (no licence) is never opened again; it was read through the GitHub API in 0.18.0's research and no code was copied. Nothing comes from IRI's Fortran, whose licence grants no distribution. PLAN carries a provenance table, one row per component with its source | D-53; wave 1 | the provenance table in PLAN |
| R-7.3 | Sunspot numbers on SILSO's version-2 scale are converted to the version-1 scale (k = 0.6) the ITU coefficients use; foF2 is capped at R12 = 160 | wave 1 (P.1239) | `TestTheSunspotScaleIsConverted`, `TestFoF2IsCappedAt160` |

## R-8 — Bounded cost (G-R7, GR-6; G-G1)

| # | Requirement | Source | Instrument |
|---|---|---|---|
| R-8.1 | One update's CPU and peak memory are measured and within G-G1's target (set by the dry run, D-49); it recomputes only on new data | G-G1; D-49 | a benchmark, recorded |
| R-8.2 | GeoJSON is decoded into typed structures, not generic maps (measured once by the round-1 Performance reviewer on an Apple M5 Pro, one GloTEC grid: 5.1 ms and 0.74 MB against 10.5 ms, 7.6 MB and 192k allocations; re-measured in PLAN) | PF (3) | `BenchmarkGloTECDecode` |

## R-9 — The path's own requirements (B on D, D-40)

| # | Requirement | Role | Instrument |
|---|---|---|---|
| R-9.1 | A climatology: PyIRI's method, ported (foF2 and M(3000)F2, whole globe, every hour), on the coefficients D-43 ships | the fallback when GloTEC is missing or stale. (The D-23 baseline is an offline measurement and needs no port, CQ-C1) | `TestTheFallbackMatchesPyIRI` (against PyIRI's published outputs) |
| R-9.2 | Spatial assimilation on the sphere with a valid kernel (Gneiting 2013) of station residuals (ionosonde minus background) **for both foF2 and M(3000)F2**, so MUF(3000) gains from the stations as foF2 does (B on D's MUF error is dominated by M(3000)F2: 3.97 MHz against GloTEC's 4.02, 3.22 with measured M(3000)F2; CQ-E2) | the assimilation | `TestTheKernelIsValidOnTheSphere`, G-M3 for foF2 and MUF(3000) |
| R-9.3 | foF2 and M(3000)F2 derived from GloTEC's NmF2 and hmF2 | the background | `TestFoF2FromNmF2`, G-M3 |
| R-9.4 | GIRO readings under D-39's throttle, with confidence scores used | the assimilation's input | `TestLowConfidenceReadingsAreDropped` |

**Moved to a PLAN question (CQ-N1):** an effective sunspot number fitted from measurements (Secan & Wilkinson
1997), if the dry run shows it improves the fallback.

## Non-functional requirements

| # | Requirement | Source | Instrument |
|---|---|---|---|
| NFR-1 | A gate of the library's own (tests with `-race`, vet, format, fuzz, P10) from the first Go code, and **a pinned `govulncheck` from the first dependency** | GC-5; IS-8 | the gate |

## What PLAN's dry run must measure (REFLECT L1; D-49)

- **MUF(3000) leave-one-station-out** for B on D, not only foF2.
- **The US stations' scores, and signed bias by distance.** The < 500 km bin was seven European stations; both backgrounds read high.
- **The NRL refits D-43 ships**, scored, with the F10.7 rule written down (the published figures used 100; 103 moves the climatology's RMS from 1.38 to 1.47).
- **GloTEC's availability** (how often the fallback runs) and its archive's reach (D-62's backfill).
- **The forecast hours' accuracy** (R-1.3).
- **D-RAP's file** size and format.
- Every target D-49 left to the dry run, each ruled.

## Metrics

G-M1 to G-M4 and G-G1, as ruled (D-12; G-M3 without KC2G, D-52). G-M1 is scored per layer (D-69). **Floors
set before the dry run (D-75):** B on D beats climatology on foF2 and MUF(3000) in the US, else the GloTEC and
climatology background ships alone; the forecast is no worse than climatology, else hours ahead are cut.
Other targets are set from PLAN's dry run, each by its own ruling (D-49). The literature's starting point for G-M3 is
about 0.5 MHz RMS near stations and 1-2 MHz far from them, with climatology as the baseline (D-23).

The prototype scores that chose the path were foF2 RMS 1.00 MHz overall and 0.37 MHz within 500 km of a
station, held out, on 2026-10-05 (`02-analysis/evidence/`). **Their limits:**
- one day;
- one F10.7;
- untuned kernels;
- the < 500 km bin is seven European stations;
- by station, held out: the mainland-US stations 0.51-0.81 MHz (AL945, EG931, IF843, MHJ45), the Pacific stations 1.2-1.8 (EA653, LL721, WA619, GU513), `evidence/subsets.py`;
- foF2 mainly: B on D's MUF(3000) scored 3.97 MHz against GloTEC's 4.02 (`subsets.py`), dominated by M(3000)F2.
