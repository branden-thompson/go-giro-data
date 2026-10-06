# Evidence behind watchpost D-38 to D-40

The scripts and request log behind watchpost 0.19.0's wave 2
(`watchpost/06_docs/02_features/propagation-overlays/02-analysis/wave2-findings.md`), kept so the path
ruling (D-40) can be re-run. **No GIRO or NOAA data is committed** (GIRO: CC BY-NC-SA 4.0; watchpost D-41,
this library's R-4.3). Re-running needs the data re-fetched under the throttle (watchpost D-39).

| File | What |
|---|---|
| `burst.py` | the one-sitting fetch (D-38): every station in GIRO's form list for one day, then 24 GloTEC grids; stops on the first denial and probes recovery. Needs the form page saved as `../scaled.html` |
| `burst_rest.py` | the two passes run by hand after `burst.py` stopped, which went past D-38 (the agent's error E-1) |
| `day.sh` | a five-a-day plan under D-18; **never run** (D-38 replaced it) |
| `pairs.py` | ionosonde vs GloTEC-derived vs PyIRI climatology, at grid times; F10.7 = 100 by default |
| `loo.py` | path B (stations on climatology), leave-one-station-out |
| `loo_hybrid.py` | path B on D (stations on GloTEC), leave-one-station-out |
| `requests-2026-10-05.jsonl` | every request of the one-sitting run: time, URL, status, bytes, seconds, response headers (no reply bodies; GIRO's replies carry the requester's IP and are not kept) |

**Environment.** Python 3.9 with PyIRI 0.0.4 (MIT), CCIR coefficients; the release 3.9 installs. The
coefficients scored here are PyIRI's raw CCIR tables, not the NRL refits go-ionomaps will ship (watchpost
D-43); the dry run scores those.

**Reproducing the published numbers.** `pairs.py burst-2026-10-05 100` gives 566 pairs from 28 stations;
then `loo.py 2026-10-05` and `loo_hybrid.py 2026-10-05`. Three blind reviewers reproduced every figure this
way.

**Their limits, beside every quote of them:**
- one day;
- one F10.7;
- untuned kernels, chosen on the day they were scored;
- the under-500-km bin is seven European stations;
- the four US stations are all more than 1000 km from another;
- foF2 only (the MUF(3000) score for B on D is the dry run's).
