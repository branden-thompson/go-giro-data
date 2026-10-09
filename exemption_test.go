package ionomaps_test

import (
	"os"
	"regexp"
	"strings"
	"testing"
)

// TestTheRootExemptionEndsAtUpdate is D-53: the root package's P10 density
// exemption covers G1's types and plumbing alone. Once Library.Update is
// declared (G4), the row must be gone from the ledger's tracked mirror, so
// Update and the answers are held to the bar.
func TestTheRootExemptionEndsAtUpdate(t *testing.T) {
	mirror, err := os.ReadFile("06_docs/p10-ledger.md")
	if err != nil {
		t.Fatal(err)
	}
	rootRow := regexp.MustCompile("(?m)^\\| `\\.` \\| `package` \\| P10-05-INVARIANT-DENSITY \\|")
	if !rootRow.Match(mirror) {
		return // the row is gone: nothing to hold
	}
	update := regexp.MustCompile(`(?m)^func \(l \*Library\) Update\(`)
	for _, name := range repoFiles(t) {
		if strings.Contains(name, "/") || !strings.HasSuffix(name, ".go") || strings.HasSuffix(name, "_test.go") {
			continue
		}
		body, err := os.ReadFile(name)
		if err != nil {
			t.Fatal(err)
		}
		if update.Match(body) {
			t.Errorf("%s declares Library.Update while the root package's density exemption stands: remove the row (D-53) and hold Update to the bar", name)
		}
	}
}
