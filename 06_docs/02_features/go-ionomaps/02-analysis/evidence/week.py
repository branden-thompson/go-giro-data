"""PLAN's dry run, scored (watchpost FR-10.6): a week of GIRO soundings against GloTEC, the climatologies
and B on D, for foF2 and MUF(3000), held out.

Usage: week.py DIR DSI
  DIR  holds dry_fetch.py's output: fc_*.txt (GIRO) and glotec_*.geojson (NOAA, 3-hourly)
  DSI  NOAA SWPC's text/daily-solar-indices.txt (F10.7 by day)

Method:
- A sounding is paired with a grid when within 10 minutes of the grid's time and its confidence score is
  at least 70 (or 999, manual).
- GloTEC: foF2 = 8.98e-6 sqrt(NmF2); M(3000)F2 = 1490 / (hmF2 + 176) (Shimazaki 1955, first order).
  MUF(3000) = foF2 x M(3000)F2 for every method.
- Climatology: PyIRI 0.1.7 (MIT). main_library on the raw CCIR or URSI tables, and sh_library on the
  spherical-harmonic refits (watchpost D-43). Two F10.7 rules: the day's observed value, and the mean of the
  30 days before it.
- B on D: the station residuals of foF2 and of M(3000)F2 (sounding minus GloTEC), each predicted at the
  held-out station by a Gaussian process on the other stations at the same grid time. Kernel: exponential
  in great-circle distance (positive definite on the sphere, Gneiting 2013). B on C is the same over the
  climatology.
- Kernel length and noise are tuned on the first three days and scored on the rest (and reported on all).
- Forecast at +3 h and +12 h, issued at each grid time from B on D held out:
    clim(t+h) + (BD(t) - clim(t)) exp(-h/tau)
  tau tuned on the first three days; scored against climatology (watchpost D-75's floor). Also "yesterday":
  B on D at t+h-24 h, held out.

Exits 1 when it finds no grid, no station or no pair, so an empty run never reads as a result.
"""
import bisect, glob, json, math, re, sys, warnings
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np
import PyIRI
import PyIRI.main_library as ml
import PyIRI.sh_library as sh

warnings.filterwarnings("ignore")
D, DSI = sys.argv[1], sys.argv[2]
PACIFIC = {"EA653", "LL721", "WA619", "GU513"}
CS_MIN = 70


# ---------- inputs ----------
def f107_by_day(path):
    out = {}
    for line in open(path):
        p = line.split()
        if len(p) > 3 and p[0].isdigit() and len(p[0]) == 4:
            out[datetime(int(p[0]), int(p[1]), int(p[2])).date()] = float(p[3])
    return out


def station(path):
    text = open(path).read()
    m = re.search(r"GEO \(\s*([\d.]+)\s*([NS])\s+([\d.]+)\s*E", text)
    if not m:
        return None, []
    lat = float(m.group(1)) * (1 if m.group(2) == "N" else -1)
    lon = float(m.group(3)); lon = lon - 360 if lon > 180 else lon
    rows = []
    for line in text.splitlines():
        if not line[:4].isdigit():
            continue
        p = line.split()
        try:
            t = datetime.strptime(p[0][:19], "%Y-%m-%dT%H:%M:%S")
            cs, fo, muf, m3 = int(p[1]), float(p[2]), float(p[4]), float(p[6])
        except (ValueError, IndexError):
            continue
        if (cs >= CS_MIN or cs == 999) and 0.5 < fo < 20 and 1.5 < m3 < 5:
            rows.append((t, fo, muf, m3))
    return (lat, lon), rows


def grid(path):
    d = json.load(open(path))
    pts = {(f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1]): f["properties"] for f in d["features"]}
    lons = sorted({k[0] for k in pts}); lats = sorted({k[1] for k in pts})
    return datetime.strptime(d["time_tag"][:19], "%Y-%m-%dT%H:%M:%S"), pts, lons, lats


def bil(g, lat, lon, key):
    _, pts, lons, lats = g
    lon = ((lon + 180) % 360) - 180
    i = max(0, min(len(lons) - 2, bisect.bisect(lons, lon) - 1))
    j = max(0, min(len(lats) - 2, bisect.bisect(lats, lat) - 1))
    x0, x1, y0, y1 = lons[i], lons[i + 1], lats[j], lats[j + 1]
    tx = min(1, max(0, (lon - x0) / (x1 - x0))); ty = min(1, max(0, (lat - y0) / (y1 - y0)))
    v = lambda a, b: pts[(a, b)][key]
    return v(x0, y0) * (1 - tx) * (1 - ty) + v(x1, y0) * tx * (1 - ty) + v(x0, y1) * (1 - tx) * ty + v(x1, y1) * tx * ty


F107 = f107_by_day(DSI)
coords, sound = {}, {}
for p in sorted(glob.glob(f"{D}/fc_*.txt")):
    st = p.split("fc_")[1][:5]
    c, rows = station(p)
    if c and rows:
        coords[st], sound[st] = c, rows
grids = [grid(p) for p in sorted(glob.glob(f"{D}/glotec_*.geojson"))]
if not grids or not coords:
    sys.exit(f"week.py: no grids or no stations under {D}")
times = [g[0] for g in grids]
STS = sorted(coords)


def mainland_us(st):
    la, lo = coords[st]
    return 24 <= la <= 50 and -125 <= lo <= -66


def gcd(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(la1) * math.sin(la2) + math.cos(la1) * math.cos(la2) * math.cos(lo1 - lo2)
    return 6371.0 * math.acos(max(-1.0, min(1.0, c)))


DIST = {(a, b): gcd(coords[a], coords[b]) for a in STS for b in STS}

# ---------- observations and GloTEC at each grid time ----------
obs = {}   # (t, st) -> (fo, muf, m3)
glo = {}   # (t, st) -> (fo, m3)
for g in grids:
    t0 = g[0]
    for st in STS:
        rows = sound[st]
        near = [r for r in rows if abs(r[0] - t0) <= timedelta(minutes=10)]
        if near:
            r = min(near, key=lambda r: abs(r[0] - t0))
            obs[(t0, st)] = r[1:]
        N = bil(g, *coords[st], "NmF2"); hm = bil(g, *coords[st], "hmF2")
        glo[(t0, st)] = (8.98e-6 * math.sqrt(max(N, 0.0)), 1490.0 / (hm + 176.0))
if not obs:
    sys.exit("week.py: no pairs")

# ---------- climatologies ----------
COEFF_ML = PyIRI.coeff_dir if hasattr(PyIRI, "coeff_dir") else None


def f107(day, rule):
    if rule == "day":
        return F107[day]
    prev = [F107[day - timedelta(days=k)] for k in range(1, 31) if day - timedelta(days=k) in F107]
    return sum(prev) / len(prev)


CLIMS = [("CCIR raw", "ml", 0), ("URSI raw", "ml", 1), ("CCIR refit", "sh", "CCIR"), ("URSI refit", "sh", "URSI")]
clim = {}  # (name, rule) -> {(t, st): (fo, m3)}
lats = np.array([coords[s][0] for s in STS]); lons = np.array([coords[s][1] for s in STS])
by_day = defaultdict(list)
for t in times:
    by_day[t.date()].append(t)
for name, lib, which in CLIMS:
    for rule in ("day", "30d"):
        out = {}
        for day, ts in sorted(by_day.items()):
            ut = np.array([t.hour + t.minute / 60 for t in ts])
            if lib == "ml":
                F2 = ml.IRI_density_1day(day.year, day.month, day.day, ut, lons, lats, np.array([300.0]),
                                         f107(day, rule), COEFF_ML, which)[0]
            else:
                F2 = sh.IRI_density_1day(day.year, day.month, day.day, ut, lons, lats, np.array([300.0]),
                                         f107(day, rule), foF2_coeff=which, old_output=True)[0]
            fo = np.array(F2["fo"]).reshape(len(ts), len(STS)); m3 = np.array(F2["M3000"]).reshape(len(ts), len(STS))
            for i, t in enumerate(ts):
                for j, st in enumerate(STS):
                    out[(t, st)] = (float(fo[i, j]), float(m3[i, j]))
        clim[(name, rule)] = out


# ---------- B on a background, held out ----------
def gp_loo(back, L, noise):
    """{(t, st): (fo, m3)} predicted at each held-out station from the others' residuals at time t."""
    pred = {}
    for t in times:
        here = [s for s in STS if (t, s) in obs]
        for held in here:
            rest = [s for s in here if s != held]
            if len(rest) < 3:
                continue
            out = []
            for k in (0, 2):            # foF2, then M(3000)F2
                bk = 0 if k == 0 else 1
                res = np.array([obs[(t, s)][k] - back[(t, s)][bk] for s in rest])
                mu = res.mean(); y = res - mu; var = max(float(y.var()), 1e-4)
                K = np.array([[var * math.exp(-DIST[(a, b)] / L) for b in rest] for a in rest])
                K += noise * var * np.eye(len(rest))
                kv = np.array([var * math.exp(-DIST[(held, b)] / L) for b in rest])
                out.append(back[(t, held)][bk] + mu + kv @ np.linalg.solve(K, y))
            pred[(t, held)] = (out[0], out[1])
    return pred


def errors(pred, keys):
    fo = [pred[k][0] - obs[k][0] for k in keys if k in pred]
    mf = [pred[k][0] * pred[k][1] - obs[k][1] for k in keys if k in pred]
    return np.array(fo), np.array(mf)


rms = lambda e: float(np.sqrt(np.mean(np.square(e)))) if len(e) else float("nan")
bias = lambda e: float(np.mean(e)) if len(e) else float("nan")
split = times[0] + timedelta(days=3)
ALL = sorted(obs)
TUNE = [k for k in ALL if k[0] < split]
TEST = [k for k in ALL if k[0] >= split]


def tune(back):
    best = None
    for L in (500, 1000, 2000, 4000, 8000):
        for noise in (0.05, 0.2, 0.5, 1.0, 2.0, 4.0):
            p = gp_loo(back, L, noise)
            fo, mf = errors(p, TUNE)
            score = rms(fo) / 1.0 + rms(mf) / 3.0
            if best is None or score < best[0]:
                best = (score, L, noise, p)
    return best[1], best[2], best[3]


# the shipped climatology for the floor: chosen by its own error over the whole week, the most favourable
# reading of the fallback (so B on D is held to the hardest comparison)
def clim_rms(c):
    fo, mf = errors(c, ALL)
    return rms(fo) + rms(mf) / 3.0


ranked = sorted(clim, key=lambda k: clim_rms(clim[k]))
CBEST = ranked[0]
Lg, Ng, BD = tune(glo)
Lc, Nc, BC = tune(clim[CBEST])

print(f"week: {times[0]:%Y-%m-%d %H:%M} to {times[-1]:%Y-%m-%d %H:%M}, {len(times)} grids, {len(STS)} stations, "
      f"{len(ALL)} pairs (tune: first 3 days {len(TUNE)}, test: rest {len(TEST)})")
print(f"F10.7 (day): {', '.join(f'{d:%m-%d} {F107[d]:.0f}' for d in sorted(by_day))}")
print(f"stations with paired soundings: {len(STS)} of {len(glob.glob(f'{D}/fc_*.txt'))} fetched (the rest had none at CS >= {CS_MIN})")
print(f"kernel tuned: B on D L={Lg} km noise={Ng}; B on C L={Lc} km noise={Nc}; best climatology: {CBEST[0]} / F10.7 {CBEST[1]}")

print("\n1. Climatologies (all pairs): foF2 RMS / bias | MUF(3000) RMS / bias")
for k in ranked:
    fo, mf = errors(clim[k], ALL)
    print(f"   {k[0]:11s} F10.7 {k[1]:3s}  {rms(fo):.2f} / {bias(fo):+.2f} | {rms(mf):.2f} / {bias(mf):+.2f}")

# hybrid: foF2 from B on D, M(3000)F2 from B on C (GloTEC's hmF2-derived M(3000)F2 is the weak half)
HY = {k: (BD[k][0], BC[k][1]) for k in BD if k in BC}


# climatology plus the other stations' mean residual at that time, held out: an effective-index proxy (CQ-N1)
def clim_plus_mean(c):
    out = {}
    for t in times:
        here = [s for s in STS if (t, s) in obs]
        for held in here:
            rest = [s for s in here if s != held]
            if len(rest) < 3:
                continue
            dfo = sum(obs[(t, s)][0] - c[(t, s)][0] for s in rest) / len(rest)
            dm3 = sum(obs[(t, s)][2] - c[(t, s)][1] for s in rest) / len(rest)
            out[(t, held)] = (c[(t, held)][0] + dfo, c[(t, held)][1] + dm3)
    return out


CM = clim_plus_mean(clim[CBEST])
methods = [("B on D", BD), ("hybrid", HY), ("GloTEC", glo), ("B on C", BC), ("clim+mean", CM), ("clim", clim[CBEST])]
groups = [("all", lambda k: True), ("mainland US", lambda k: mainland_us(k[1])),
          ("Pacific", lambda k: k[1] in PACIFIC), ("elsewhere", lambda k: not mainland_us(k[1]) and k[1] not in PACIFIC)]


def table(title, keys):
    print(f"\n{title}: foF2 RMS / bias | MUF(3000) RMS / bias   (n)")
    for gname, sel in groups:
        ks = [k for k in keys if sel(k)]
        if not ks:
            continue
        cells = []
        for mname, m in methods:
            fo, mf = errors(m, ks)
            cells.append(f"{mname} {rms(fo):.2f}/{bias(fo):+.2f} | {rms(mf):.2f}/{bias(mf):+.2f}")
        print(f"   {gname:11s} (n={len(ks):4d})  " + "   ".join(cells))


table("2. Held out, test days (after tuning)", TEST)
table("3. Held out, whole week", ALL)

print("\n4. By distance to the nearest other reporting station, whole week (foF2 RMS | MUF RMS)")
nearest = {}
for k in ALL:
    others = [s for s in STS if s != k[1] and (k[0], s) in obs]
    nearest[k] = min(DIST[(k[1], s)] for s in others) if others else 1e9
for lo, hi in ((0, 500), (500, 1000), (1000, 2000), (2000, 20000)):
    ks = [k for k in ALL if lo <= nearest[k] < hi]
    if ks:
        cells = []
        for mname, m in methods:
            fo, mf = errors(m, ks)
            cells.append(f"{mname} {rms(fo):.2f} | {rms(mf):.2f}")
        print(f"   {lo:5d}-{hi:5d} km (n={len(ks):4d})  " + "   ".join(cells))

print("\n5. By station, whole week, held out: n, B on D foF2 RMS/bias, MUF RMS/bias, clim foF2 RMS, region")
for st in STS:
    ks = [k for k in ALL if k[1] == st]
    if not ks:
        continue
    fo, mf = errors(BD, ks); cf, cm = errors(clim[CBEST], ks)
    reg = "US" if mainland_us(st) else ("Pacific" if st in PACIFIC else "")
    print(f"   {st} ({coords[st][0]:6.1f},{coords[st][1]:7.1f}) n={len(ks):3d}  {rms(fo):.2f}/{bias(fo):+.2f}  "
          f"{rms(mf):.2f}/{bias(mf):+.2f}  clim {rms(cf):.2f}/{rms(cm):.2f}  {reg}")

# ---------- forecast ----------
C = clim[CBEST]


def forecast(h, tau, base=None):
    pred = {}
    for (t, st), (fo, m3) in (base or BD).items():
        tt = t + timedelta(hours=h)
        if (tt, st) not in C:
            continue
        w = 0.0 if tau == 0 else (1.0 if tau == math.inf else math.exp(-h / tau))
        pred[(tt, st)] = (C[(tt, st)][0] + (fo - C[(t, st)][0]) * w, C[(tt, st)][1] + (m3 - C[(t, st)][1]) * w)
    return pred


def blend(w, base=None):
    """w x (B on D a day before) + (1 - w) x climatology, at the target time: usable for any h <= 24."""
    pred = {}
    for (t, st), v in (base or BD).items():
        tt = t + timedelta(hours=24)
        if (tt, st) in C:
            pred[(tt, st)] = (w * v[0] + (1 - w) * C[(tt, st)][0], w * v[1] + (1 - w) * C[(tt, st)][1])
    return pred


def yesterday(h):
    pred = {}
    for (t, st), v in BD.items():
        tt = t + timedelta(hours=24)       # issued at tt-h, using B on D from tt-24 h
        if h <= 24:
            pred[(tt, st)] = v
    return pred


bw = None
for w in (0.25, 0.5, 0.75, 1.0):
    p = blend(w)
    fo, mf = errors(p, [k for k in TUNE if k in p])
    s = rms(fo) + rms(mf) / 3.0
    if bw is None or s < bw[0]:
        bw = (s, w)
W_BLEND = bw[1]

print("\n6. Forecast, held out (foF2 RMS | MUF RMS); tau tuned on the first three days, scored on the rest")
for h in (3, 12):
    best = None
    for tau in (3, 6, 12, 24, 48, math.inf):
        p = forecast(h, tau)
        fo, mf = errors(p, [k for k in TUNE if k in p])
        s = rms(fo) + rms(mf) / 3.0
        if best is None or s < best[0]:
            best = (s, tau)
    tau = best[1]
    cands = ((f"decay tau={tau}", forecast(h, tau)), (f"hybrid decay", forecast(h, tau, HY)),
             ("persistence", forecast(h, math.inf)),
             ("yesterday", yesterday(h)), (f"blend w={W_BLEND}", blend(W_BLEND)),
             ("hybrid blend", blend(W_BLEND, HY)), ("climatology", forecast(h, 0)))
    common = [k for k in TEST if all(k in p for _, p in cands)]   # every method scored on the same pairs
    for label, p in cands:
        ks = common
        fo, mf = errors(p, ks)
        us = [k for k in ks if mainland_us(k[1])]
        fu, mu = errors(p, us)
        print(f"   +{h:2d} h {label:16s} n={len(ks):4d}  all {rms(fo):.2f} | {rms(mf):.2f}   mainland US (n={len(us)}) "
              f"{rms(fu):.2f} | {rms(mu):.2f}")

# ---------- by day, and quiet against disturbed ----------
print("\n7. By day, held out (foF2 RMS | MUF RMS), all stations and mainland US")
for day in sorted(by_day):
    ks = [k for k in ALL if k[0].date() == day]
    us = [k for k in ks if mainland_us(k[1])]
    cells = []
    for mname, m in methods:
        fo, mf = errors(m, ks); fu, mu = errors(m, us)
        cells.append(f"{mname} {rms(fo):.2f}|{rms(mf):.2f} (US {rms(fu):.2f}|{rms(mu):.2f})")
    print(f"   {day:%m-%d} n={len(ks):3d}  " + "  ".join(cells))

if len(sys.argv) > 3:   # DISTURBED days, comma-separated YYYY-MM-DD (from NOAA's daily geomagnetic indices)
    bad = {datetime.strptime(d, "%Y-%m-%d").date() for d in sys.argv[3].split(",")}
    print(f"\n8. Forecast on the test days, quiet against disturbed ({', '.join(sorted(d.isoformat() for d in bad))})")
    for h in (3, 12):
        cands = ((f"decay tau={'6' if h == 3 else '12'}", forecast(h, 6 if h == 3 else 12)),
                 ("blend", blend(W_BLEND)), ("hybrid blend", blend(W_BLEND, HY)), ("climatology", forecast(h, 0)))
        common = [k for k in TEST if all(k in p for _, p in cands)]
        for label, p in cands:
            for name, sel in (("quiet", lambda k: k[0].date() not in bad), ("disturbed", lambda k: k[0].date() in bad)):
                ks = [k for k in common if sel(k)]; us = [k for k in ks if mainland_us(k[1])]
                fo, mf = errors(p, ks); fu, mu = errors(p, us)
                print(f"   +{h:2d} h {label:13s} {name:9s} n={len(ks):3d}  all {rms(fo):.2f} | {rms(mf):.2f}   US (n={len(us)}) {rms(fu):.2f} | {rms(mu):.2f}")

