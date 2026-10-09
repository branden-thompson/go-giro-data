package glotec

import (
	"regexp"
	"time"
)

// maxIndexBytes bounds the directory index: about eight times the measured
// 505 KB (watchpost W0.0).
const maxIndexBytes = 4 << 20

// gridName is a grid's name in the index: its valid time, to the second.
var gridName = regexp.MustCompile(`glotec_icao_(\d{8}T\d{6}Z)\.geojson`)

// Newest is the newest grid the directory index names, asked at now: its
// name and valid time. A name past the clock, or whose time does not read,
// is passed over; false when the index names no grid.
//
// Source: NOAA SWPC GloTEC's directory index, as served (watchpost D-111,
// D-141).
func Newest(index []byte, now time.Time) (name string, valid time.Time, ok bool) {
	if len(index) > maxIndexBytes {
		return "", time.Time{}, false
	}
	latest := now.Add(clockSkew)
	for _, m := range gridName.FindAllSubmatch(index, -1) {
		t, err := time.Parse("20060102T150405Z", string(m[1]))
		usable := err == nil && !t.After(latest) && t.After(valid)
		if usable {
			name, valid = string(m[0]), t
		}
	}
	if name == "" {
		return "", time.Time{}, false
	}
	return name, valid, true
}
