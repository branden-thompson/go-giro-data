# go-ionomaps

Ionospheric maps for Go programs: maximum usable frequency (MUF) and the F2 layer's critical
frequency (foF2), as fields a terminal map can draw, with each amateur band's status between its upper
limit (MUF, foF2) and its lower limit (D-layer absorption).

**Status: in discovery.** No code yet. The design is recorded in `06_docs/02_features/go-ionomaps/`.

## How it works (planned)

Station readings from the Global Ionospheric Radio Observatory (GIRO) are assimilated over a background
derived from NOAA SWPC's GloTEC, with a climatology (a Go port of NASA's PyIRI method) as the fallback.
The host supplies the network; the library opens no connection of its own.

## Licence and data terms

The code is MIT (see `LICENSE`). The licence covers the code only and does not relicense any data.
Sources and their terms are in `NOTICE`. In short:
- **GIRO's live readings are for non-commercial use.** GIRO offers them "only for educational and
  non-commercial research purposes". A commercial user needs their own arrangement with GIRO, or runs on
  the GloTEC and climatology background alone.
- No GIRO data is in this repository, and none ever will be.

Research for the design fetched GIRO and NOAA data under GIRO's and NOAA's terms; that data was kept outside
this repository.
