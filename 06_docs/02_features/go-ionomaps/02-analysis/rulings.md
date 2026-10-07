---
title: "go-ionomaps (formerly go-giro-data) — HUM LEAD rulings"
date: 2026-10-05
phase: DISCOVER (intake)
sev: SEV-0
authority: HUM LEAD
status: "LIVE — every ruling is written here the moment it is made."
---

# go-ionomaps (formerly go-giro-data) — rulings

Recorded verbatim. A correction to a ruling is a new row, never an edit of an old one.

go-ionomaps (named go-giro-data until watchpost D-56) is paired with watchpost 0.19.0 and go-tuiMaps v0.3.0. Rows written before the rename keep the old name. A decision that binds more than one
of the three is written in watchpost's log
(`watchpost/06_docs/02_features/propagation-overlays/02-analysis/rulings.md`, cited "watchpost D-n") and
restated here; this log holds go-giro-data's own.

| # | Date | Question | HUM LEAD verbatim | Ruling |
|---|---|---|---|---|
| D-0 | 2026-10-05 | Inherited from watchpost D-1, D-2, D-5 | see watchpost D-1, D-2, D-5 | A new project under the INIT of watchpost D-1: LEVEL-1, SEV-0, the full directive set, written in Go to integrate with watchpost and go-tuiMaps. Public, MIT for the code (watchpost D-2); no third-party data committed until its terms are ruled. `main` holds the scaffold; DISCOVER works on `feature/discover` (watchpost D-5). |
| D-1 | 2026-10-05 | Restates watchpost D-10 | see watchpost D-10 | go-giro-data has its own problem statement and metrics, alongside the host requirements watchpost's DISCOVER writes for it. |
| D-2 | 2026-10-05 | Restates watchpost D-11 | see watchpost D-11 | PS-G LOCKED, as written in `../01-objectives/problem-statement.md`. DISCOVER surveys the published sources; a source with open terms returns as a ruling. |
| D-3 | 2026-10-05 | Restates watchpost D-12 | see watchpost D-12 | Metrics G-M1 to G-M4 and guardrail G-G1; targets set in DISCOVER. |
| D-4 | 2026-10-05 | Restates watchpost D-16 | see watchpost D-16 | This project's brief APPROVED as presented; intake closed; DISCOVER opens. |
| D-5 | 2026-10-05 | Restates watchpost D-19 | see watchpost D-19 | PS-G amended to the claim the source survey supports; metrics unchanged. |
| D-6 | 2026-10-05 | Restates watchpost D-20 | see watchpost D-20 | Paths B (GIRO-driven reimplementation on a PyIRI port) and D (derived from NOAA GloTEC) go to wave 2; the path is ruled at DISCOVER exit on measurements. |
| D-7 | 2026-10-06 | Restates watchpost D-38, D-39 | see watchpost D-38, D-39 | GIRO's throttle measured in one sitting; the feature's throttle behaviour (burst of at most 40 an hour, at most 2 a minute sustained, back-off 60 s to 15 minutes on a 429, the last good field kept) binds every phase. |
| D-8 | 2026-10-06 | Restates watchpost D-40 | see watchpost D-40 | **Path: B on D.** GIRO station residuals assimilated over a GloTEC-derived background; a PyIRI-port climatology as the fallback; re-scored over more days in PLAN's dry run. |
| D-9 | 2026-10-06 | Restates watchpost D-41 | see watchpost D-41 | The computed field is treated as a substantially derivative product of GIRO's readings; full credit and citation; the NOTICE states the readings' non-commercial terms for library users; raw readings never redistributed. No contact with LGDC. |
| D-10 | 2026-10-06 | Restates watchpost D-42 | see watchpost D-42 | Pull: the host asks for updates; no goroutines or timers in the library; the library holds D-39's throttle and answers an early call from the last good field with its age and reason. |
| D-11 | 2026-10-06 | Restates watchpost D-43 | see watchpost D-43 | The fallback ships only NRL's spherical-harmonic refits (PyIRI, MIT), lineage stated; never the raw CCIR/URSI tables; the coefficients sit behind a swappable seam. |
| D-12 | 2026-10-06 | Restates watchpost D-47 | see watchpost D-47 | Both limits modelled: regular daytime absorption from the published method behind ITU-R P.533's absorption term; disturbance absorption from NOAA D-RAP after a terms check; every band status names the limit that closes it. |
| D-13 | 2026-10-06 | Restates watchpost D-49 | see watchpost D-49 | G-M2, G-M3 and G-G1's targets are set from PLAN's dry run, each by its own ruling, before PLAN exits. |
| D-14 | 2026-10-06 | Restates watchpost D-50 | see watchpost D-50 | Fields up to 24 h ahead, from the background carried forward with the current station corrections decaying toward climatology, labelled as forecasts with their age. |
| D-15 | 2026-10-06 | Restates watchpost D-51 | see watchpost D-51 | Seed list of live stations (metadata only), dropped after 3 dark days, one rotation probe per update, rotation above 40, no burst probe on a cold start. |
| D-16 | 2026-10-06 | Restates watchpost D-52 | see watchpost D-52 | G-M3 scores against held-out ionosondes only; the KC2G reference is removed. |
| D-17 | 2026-10-06 | Restates watchpost D-53 | see watchpost D-53 | No reopening of `arodland/prop`; papers and PyIRI only; per-function citations; a provenance table in PLAN; the record says truthfully that 0.18.0's research read it. |
| D-18 | 2026-10-06 | Restates watchpost D-54 | see watchpost D-54 | The library is renamed before v0.1.0; the name is its own ruling. |
| D-19 | 2026-10-06 | Restates watchpost D-56 | see watchpost D-56 | **Renamed `go-ionomaps`** (repository, module `github.com/branden-thompson/go-ionomaps`, feature folder). Earlier rows keep the old name as they were written. |
| D-20 | 2026-10-06 | Restates watchpost D-69 | see watchpost D-69 | G-M1 scored per layer: code and computed field free to build on; the live GIRO input non-commercial; a commercial user arranges their own access or runs on GloTEC and climatology alone; README and NOTICE say so. |
| D-21 | 2026-10-06 | Restates watchpost D-73 | see watchpost D-73 | "Open" means the reference circuit: SSB voice at 100 W with simple antennas, about +10 dB signal-to-noise in 2.5 kHz; below D-RAP's 1 dB frequency a band is "disturbed", not closed; the daytime-absorption limit is computed for this circuit. |
| D-22 | 2026-10-06 | Restates watchpost D-75 | see watchpost D-75 | Floors before the dry run: B on D must beat climatology on foF2 and MUF(3000), held out, in the US, else the library ships the GloTEC-and-climatology background alone; forecast error at +3 h and +12 h no worse than climatology, else hours ahead are cut. |
| D-23 | 2026-10-06 | Restates watchpost D-76, D-78 | see watchpost D-76, D-78 | The host asks only when its Propagation mode is opened (no background updates); the library gains the "best bands" and "your frequency" answers; no history is recorded and there is no backfill in 0.19.0. |
| D-24 | 2026-10-06 | Restates watchpost D-84 | see watchpost D-84 | DISCOVER exits; this library's requirements are APPROVED; PLAN opens with the dry run. |
| D-25 | 2026-10-07 | Restates watchpost D-87 | see watchpost D-87 | The rotation probe counts inside the burst of 40: with 40 or more live, an update polls 39 live stations and makes the probe; the live station left out goes first next update. No update makes more than 40 GIRO requests. |
| D-26 | 2026-10-07 | Restates watchpost D-88 | see watchpost D-88 | NOAA's space-weather scales (`products/noaa-scales.json`) are fetched with D-RAP when the host asks, with validators, and carried in the snapshot (R, S, G now and the three-day outlook); named, not modelled. |
