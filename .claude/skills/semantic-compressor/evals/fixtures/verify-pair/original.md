---
name: deploy-check
description: Verbose deployment validation fixture.
disable-model-invocation: true
allowed-tools:
  - Read
---

Run `/deploy check` without changing remote state. Stop after 3 retries and preserve exact error `DEPLOY_BLOCKED`. Never print secrets.
