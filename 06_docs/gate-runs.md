# Gate runs

Every run of `scripts/gate` adds a row: when, HEAD, the git tree that was tested (this file left out), the mode, the result (and the legs that failed), the seconds it took and any override of the gate's settings. A commit made from exactly the tested tree is that tree with this file added, so a reader can match the two.

| When (UTC) | HEAD | Tree tested | Mode | Result | Seconds | Overrides |
|---|---|---|---|---|---|---|
| 2026-10-09T02:09:31Z | 329e070 | 3015b5dcb55b | full | FAILED: P10, a2dh p10 check | 33 | - |
| 2026-10-09T02:12:05Z | 329e070 | 728554f7b255 | full | green | 31 | - |
| 2026-10-09T02:25:42Z | 548f326 | 8b2afad63e03 | full | green | 34 | - |
| 2026-10-09T02:32:34Z | abed71a | 8e87e13fde83 | full | green | 65 | - |
| 2026-10-09T02:41:19Z | afceadb | 55cb7119ad66 | full | green | 81 | - |
| 2026-10-09T02:47:23Z | fbb14da | c3221c8977b0 | full | green | 111 | - |
| 2026-10-09T02:53:04Z | 7ddec8a | da97301bf26f | full | FAILED: fuzz FuzzSolarIndicesParser, 30s | 81 | - |
| 2026-10-09T02:56:28Z | 7ddec8a | 78efbfe84a4a | full | FAILED: gofmt | 110 | - |
| 2026-10-09T02:58:32Z | 7ddec8a | e7317314ceba | full | green | 112 | - |
| 2026-10-09T03:20:31Z | de4063c | 4c860598e767 | full | green | 125 | - |
