#!/usr/bin/env bash
# Wave 2, one budget day (D-18): 5 GloTEC grids + 5 GIRO stations (24 h each) -> three-way pairs.
# Usage: day.sh YYYY-MM-DD   (the UTC day whose 00:05..20:05Z grids are fetched; run after it ends)
set -euo pipefail
D=${1:?date}
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
UA="watchpost-discover (+https://github.com/branden-thompson/watchpost)"
DD=${D//-/}; mkdir -p "$D"
log() { echo "$(date -u +%FT%TZ) $*" | tee -a requests.log; }

for hh in 0005 0505 1005 1505 2005; do
  u="https://services.swpc.noaa.gov/products/glotec/geojson_2d_urt/glotec_icao_${DD}T${hh}00Z.geojson"
  code=$(curl -s -A "$UA" -o "$D/glotec_$hh.geojson" -w '%{http_code} %{size_download}' "$u")
  log "SWPC $u $code"
  case "$code" in 200*) ;; *) echo "stop: $code"; exit 1;; esac
  sleep 5
done

Y=${D:0:4}; M=${D:5:2}; DY=${D:8:2}
for st in EG931 MHJ45 JI91J HE13N RO041; do
  u="https://lgdc.uml.edu/fastchar/getbest?ursiCode=$st&charName=foF2,MUF%28D%29,M%28D%29,hmF2&DMUF=3000&fromDate=$Y%2F$M%2F$DY+00%3A00%3A00&toDate=$Y%2F$M%2F$DY+23%3A59%3A59"
  code=$(curl -s -A "$UA" -o "$D/fc_$st.txt" -w '%{http_code} %{size_download}' "$u")
  log "GIRO GET fastchar/getbest $st $D 24h $code"
  case "$code" in 429*) echo "stop: 429"; exit 1;; esac
  sleep 20
done
echo "fetched; run: ../pyiri-venv/bin/python pairs.py $D"
