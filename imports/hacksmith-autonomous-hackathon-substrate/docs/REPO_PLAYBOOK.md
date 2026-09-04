# Repository Playbook

Public root should look like a product: README, PITCH, DEMO, optional current RECORDING-SCRIPT, license, env example, package files, source, tests, docs, archive.

README top 20 lines: what it is, live demo, video, CI, sponsor, one workflow diagram.

Green CI from a **clean checkout** is mandatory. Common failures: local-only dependencies, stale submodules/gitlinks, missing generated files, case-sensitive paths, secret-dependent tests, stale README test counts.

If a secret was committed, revoke/rotate it. Removing it from HEAD alone is insufficient.
