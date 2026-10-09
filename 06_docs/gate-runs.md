# Gate runs

Every run of `scripts/gate` adds a row: when, HEAD, the git tree that was tested (this file left out), the mode, the result (and the legs that failed), the seconds it took and any override of the gate's settings. A commit made from exactly the tested tree is that tree with this file added, so a reader can match the two.

| When (UTC) | HEAD | Tree tested | Mode | Result | Seconds | Overrides |
|---|---|---|---|---|---|---|
| 2026-10-09T02:09:31Z | 329e070 | 3015b5dcb55b | full | FAILED: P10, a2dh p10 check | 33 | - |
| 2026-10-09T02:12:05Z | 329e070 | 728554f7b255 | full | green | 31 | - |
