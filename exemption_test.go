package ionomaps_test

import (
	"os"
	"regexp"
	"strings"
	"testing"
)

// rootRow is the root package's P10 density row in the ledger's mirror.
var rootRow = regexp.MustCompile("(?m)^\\| `\\.` \\| `package` \\| P10-05-INVARIANT-DENSITY \\|")

// asksGIRO is whether a source file names GIRO's host.
func asksGIRO(body []byte) bool { return strings.Contains(string(body), "lgdc.uml.edu") }

// TestTheRootExemptionEndsAtGIRO is D-56: the root package's P10 density row
// covers G1's types and G4.2's NOAA-only update. Once the root package's own
// code names GIRO's host while the row stands, the gate fails: GIRO's
// fetching and the burst belong in internal/giro and internal/throttle, each
// held to the bar, and the row is reviewed then. A planted file is caught.
func TestTheRootExemptionEndsAtGIRO(t *testing.T) {
	if !asksGIRO([]byte(`const u = "https://lgdc.uml.edu/common/DIDBGetValues"`)) || asksGIRO([]byte(`const u = "https://services.swpc.noaa.gov/"`)) {
		t.Fatal("the check does not tell GIRO's host from NOAA's")
	}
	mirror, err := os.ReadFile("06_docs/p10-ledger.md")
	if err != nil {
		t.Fatal(err)
	}
	if !rootRow.Match(mirror) {
		return // the row is gone: nothing to hold
	}
	for _, name := range repoFiles(t) {
		if strings.Contains(name, "/") || !strings.HasSuffix(name, ".go") || strings.HasSuffix(name, "_test.go") {
			continue
		}
		body, err := os.ReadFile(name)
		if err != nil {
			t.Fatal(err)
		}
		if asksGIRO(body) {
			t.Errorf("%s names GIRO's host while the root package's density row stands: GIRO's fetching goes in internal/giro and internal/throttle, and the row is reviewed (D-56)", name)
		}
	}
}
