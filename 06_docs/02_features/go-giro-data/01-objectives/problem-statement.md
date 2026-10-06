---
title: "go-giro-data — problem statement"
date: 2026-10-05
phase: DISCOVER (intake)
sev: SEV-0
authority: HUM LEAD
status: "LOCKED (watchpost D-11); metrics ruled (watchpost D-12), targets set in DISCOVER"
---

# Problem statement

go-giro-data has a statement of its own (watchpost D-10), beside the host requirements watchpost's
DISCOVER writes for it. Its host's statements are PS-1 and PS-2, in
`watchpost/06_docs/02_features/propagation-overlays/01-objectives/problem-statement.md`.

## PS-G

> A developer who wants to show HF operators current ionospheric conditions has no source they are
> free to build on and able to check: the maps published today come with no licence or reuse terms, or
> for non-commercial use only, and none can be reproduced, so a program that shows them depends on
> someone else's service without permission, and goes blank or wrong without warning when that service
> changes.

| Criterion | |
|---|---|
| Bad outcome | depends on a service without permission; blank or wrong without warning |
| Affected humans | the developer; the HF operators who read the result, second |
| Tech agnostic | no technology named |
| Non-prescriptive | permission from KC2G, or a licensed source found in DISCOVER, answers it as well as our own computation |
| Verifiable | yes; "the maps published today" is a claim DISCOVER checks across KC2G, GIRO, Australia's Space Weather Services, NOAA SWPC and any others; a source with open terms returns as a ruling |

## Metrics (watchpost D-12)

Targets are set in DISCOVER.

| # | Name · symbol | Type | Definition | Measured in |
|---|---|---|---|---|
| G-M1 | Free to build on · F | compliance | every input the library reads, and every output it publishes, has recorded terms that permit the use; a test holds the list of sources and their terms | sources without permitting terms (target 0) |
| G-M2 | Reproducible · P | reproducibility | from the recorded inputs for one hour, another machine regenerates the same field | largest difference, MHz |
| G-M3 | Fidelity · Φ | accuracy | foF2 and MUF(3000) against ionosonde readings held out of the fit (leave-one-out); KC2G's grid for the same hours as a second reference | RMS error, MHz |
| G-M4 | Fails out loud · W | honesty | when an input stops, goes stale or changes format, the library returns an error or an age, never a silently old or empty field | share of injected faults reported (target 100%) |
| G-G1 | Compute cost · K | guardrail (watchpost issue #25) | CPU seconds and peak memory for one map update on a reference machine | CPU s; MB |

Anti-solution check:
- G-M1: KC2G's maps used with written permission pass, so the metric does not force a reimplementation.
- G-M2: PS-G's "able to check". A service nobody else can rerun fails.
- G-M3: a climatology that never changes fails. Held-out readings keep the fit from grading itself.
- G-M4: PS-G's "blank or wrong without warning".
