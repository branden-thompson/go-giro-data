package ionomaps_test

// gate_test.go — plan task G0.1 (NFR-1): the gate fails on what it exists to
// catch. A gate that cannot fail is refused (watchpost REFLECT L7), so each
// failure it promises is planted in a throwaway module and seen.

import (
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

// plantModule is a throwaway module holding the gate and the given files.
func plantModule(t *testing.T, files map[string]string) string {
	t.Helper()
	root := t.TempDir()
	gate, err := os.ReadFile(filepath.Join("scripts", "gate"))
	if err != nil {
		t.Fatal(err)
	}
	all := map[string]string{
		"go.mod":       "module example.com/lib\n\ngo 1.25.13\n",
		"lib.go":       "package lib\n\n// Answer is the answer.\nfunc Answer() int { return 42 }\n",
		"lib_test.go":  "package lib\n\nimport \"testing\"\n\nfunc TestAnswer(t *testing.T) {\n\tif Answer() != 42 {\n\t\tt.Fatal(\"wrong\")\n\t}\n}\n",
		"scripts/gate": string(gate),
	}
	for name, body := range files {
		all[name] = body
	}
	for name, body := range all {
		path := filepath.Join(root, name)
		if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(path, []byte(body), 0o755); err != nil {
			t.Fatal(err)
		}
	}
	for _, args := range [][]string{{"init", "-q"}, {"add", "-A"}, {"-c", "user.name=gate", "-c", "user.email=gate@example.invalid", "commit", "-q", "-m", "planted"}} {
		if out, err := exec.Command("git", append([]string{"-C", root}, args...)...).CombinedOutput(); err != nil {
			t.Fatalf("git %v: %v\n%s", args, err, out)
		}
	}
	return root
}

// runGate runs the planted module's gate in a mode: its output and whether
// it passed.
func runGate(t *testing.T, root string, args ...string) (string, bool) {
	t.Helper()
	cmd := exec.Command(filepath.Join(root, "scripts", "gate"), args...)
	cmd.Env = append(os.Environ(), "GATE_ROOT="+root, "GOFLAGS=")
	out, err := cmd.CombinedOutput()
	return string(out), err == nil
}

// TestTheGateIsGreenOnAPassingTree: a clean module passes, so the failures
// below are the planted faults and nothing else.
func TestTheGateIsGreenOnAPassingTree(t *testing.T) {
	out, ok := runGate(t, plantModule(t, nil), "--quick")
	if !ok || !strings.Contains(out, "gate: green") {
		t.Fatalf("a clean module did not pass:\n%s", out)
	}
}

// TestTheGateFailsOnWhatItCatches: a vet error, an unformatted file, a
// failing test, and a docs lane with nothing staged each fail the gate, and
// it names the leg.
func TestTheGateFailsOnWhatItCatches(t *testing.T) {
	for _, c := range []struct {
		what  string
		files map[string]string
		args  []string
		leg   string
	}{
		{"a vet error", map[string]string{"bad.go": "package lib\n\nimport \"fmt\"\n\n// Bad prints badly.\nfunc Bad() { fmt.Printf(\"%d\", \"x\") }\n"}, []string{"--quick"}, "vet"},
		{"an unformatted file", map[string]string{"ugly.go": "package lib\n\n// Ugly is unformatted.\nfunc Ugly()  int {return 1}\n"}, []string{"--quick"}, "gofmt"},
		{"a failing test", map[string]string{"fail_test.go": "package lib\n\nimport \"testing\"\n\nfunc TestFails(t *testing.T) { t.Fatal(\"planted\") }\n"}, []string{"--quick"}, "tests"},
		{"an empty docs change", nil, []string{"--docs"}, "nothing is staged"},
		{"a failing test in a tool module", map[string]string{"tools/t/go.mod": "module example.com/lib/tools/t\n\ngo 1.25.13\n",
			"tools/t/t_test.go": "package t\n\nimport \"testing\"\n\nfunc TestFails(t *testing.T) { t.Fatal(\"planted\") }\n"}, []string{"--quick"}, "tools/t: tests"},
	} {
		out, ok := runGate(t, plantModule(t, c.files), c.args...)
		if ok || !strings.Contains(out, "gate: FAILED") || !strings.Contains(out, c.leg) {
			t.Errorf("%s: the gate %s; want it FAILED, naming %q:\n%s", c.what, map[bool]string{true: "passed", false: "failed otherwise"}[ok], c.leg, out)
		}
	}
}

// TestTheGateRefusesTwoModes: one mode a run, never two.
func TestTheGateRefusesTwoModes(t *testing.T) {
	if out, ok := runGate(t, plantModule(t, nil), "--quick", "--docs"); ok || !strings.Contains(out, "one mode at most") {
		t.Errorf("two modes were taken:\n%s", out)
	}
}
