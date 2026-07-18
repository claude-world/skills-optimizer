# Compression Examples

These examples illustrate safe reductions after an inventory is complete. They are patterns, not permission to omit source-specific details.

## Description: preserve activation phrases

Before:

```yaml
description: |
  This skill provides a comprehensive workflow that helps users inspect and review pull requests. It should be used whenever the user asks for a PR review, code review, change audit, security review, or merge readiness assessment.
```

After:

```yaml
description: Review pull requests for correctness, security, and merge readiness. Use for PR review, code review, change audit, security review, or merge readiness assessment.
```

The shorter version retains every inventoried trigger instead of merging them into a generic “review code.”

## Workflow: remove narration, keep gates

Before:

```markdown
The first thing that should happen is that the agent should take a look at the current repository status. This is important because it allows the agent to understand whether there are already changes in the working tree. Once that has been completed, the agent should run the tests. If the tests fail, the agent should stop and explain the failures instead of continuing to deployment. If tests pass, the agent can proceed to build the application.
```

After:

```markdown
1. Inspect repository status and preserve existing changes.
2. Run the tests. On failure, stop and report the failing evidence.
3. Build only after tests pass.
```

The result keeps ordering, the failure stop, and the build precondition.

## Commands: do not collapse variants

Before:

```markdown
- `/release check`: validate without publishing.
- `/release stage`: create a draft release.
- `/release publish`: publish the staged release.
```

Unsafe:

```markdown
- `/release <action>`: manage releases.
```

Safe:

```markdown
| Command | Effect |
|---|---|
| `/release check` | Validate; no publish |
| `/release stage` | Create draft |
| `/release publish` | Publish staged release |
```

The unsafe version loses the action names and the no-publish boundary.

## Security action: preserve the dependency

Before:

```markdown
Use JWT authentication. Hash passwords with Argon2id before storage, use a unique salt, and never log credentials. Reject startup when `JWT_SECRET` is absent.
```

After:

```markdown
JWT auth: Argon2id-hash passwords with unique salts; never log credentials; fail startup if `JWT_SECRET` is absent.
```

All security actions and the exact environment variable remain. A summary that says only “Use JWT auth” is a semantic failure.

## Corrected decision: keep the latest state

Before:

```markdown
The team initially considered React. Later, accessibility testing showed the chosen component library was unsuitable, so the final decision is Vue with the approved accessible library. Do not start new React work.
```

After:

```markdown
Decision: use Vue with the approved accessible library; do not start React work (React was rejected after accessibility testing).
```

Keeping only the first-mentioned framework would reverse the decision. Removing the reason would make the prohibition harder to evaluate later.

## Failure history: retain what prevents repetition

Before:

```markdown
Direct database migrations failed because production uses a read-only credential. The supported path is the migration service account through CI. Do not retry from a developer shell.
```

After:

```markdown
Run production migrations only through CI's migration service account; developer-shell attempts fail because credentials are read-only and must not be retried.
```

The failed path remains because it is an operational safeguard.

## Frontmatter: preserve controls exactly

Before:

```yaml
---
name: release-helper
description: A long description of the release workflow.
disable-model-invocation: true
allowed-tools:
  - Read
  - Bash(git status *)
---
```

After:

```yaml
---
name: release-helper
description: Validate and stage releases when the user explicitly invokes the release workflow.
disable-model-invocation: true
allowed-tools:
  - Read
  - Bash(git status *)
---
```

Only `description` changes. Adding or removing a permission field fails the deterministic gate.

## Output schema: prefer one canonical template

Before:

```markdown
The report should mention status. It should also include the files that changed. Make sure the backup is shown. At the end, remind the user whether the source was modified.
```

After:

````markdown
Return:

```json
{
  "status": "PASS|FAIL|ERROR",
  "changed_files": [],
  "backup": null,
  "source_modified": false
}
```
````

One explicit schema is shorter and less ambiguous than repeated prose.

## When not to compress further

Original:

```markdown
Never print secrets. Stop after 3 retries. Preserve error `AUTH_401`. Restore from `.claude/backups/<run-id>/manifest.json`.
```

This is already concise. Replacing it with “Handle auth safely and retry as needed” loses a security rule, a threshold, an exact error, and a path. Return `NOT_COMPRESSIBLE` instead.
