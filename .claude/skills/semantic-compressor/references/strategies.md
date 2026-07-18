# Safe Compression Strategies

Use these strategies only after completing the preservation inventory. They apply to Claude Code skill and agent Markdown, not source code, arbitrary documents, or conversation history.

## Priority order

1. Preserve behavior and safety boundaries.
2. Preserve operational metadata and literal contracts.
3. Keep the result easy for an agent to follow.
4. Reduce repeated or non-actionable wording.
5. Improve the ratio only while the first four remain true.

A smaller file is worse if it changes activation, permissions, supported operations, failure behavior, or user expectations.

## Frontmatter

The control script permits rewriting only `description` and `when_to_use`. Keep all other fields value-equivalent, including unknown fields.

For descriptions:

- Put the main capability first.
- State when to use the skill with concrete user intents.
- Preserve exact activation phrases recorded under `literals.triggers`.
- Remove promotional adjectives and duplicated feature prose.
- Do not merge distinct trigger words merely because they are synonyms; models may match them differently.
- Do not add a capability just to make the description sound complete.

Example:

```yaml
# Before
description: This comprehensive skill helps developers carefully review pull requests and can be used whenever someone asks for a PR review, code review, change audit, or merge readiness assessment.

# After
description: Review pull requests for correctness, security, maintainability, and merge readiness. Use for PR review, code review, change audit, or merge readiness requests.
```

## Instruction body

### Safe reductions

- Replace repeated explanations with one precise instruction.
- Convert prose sequences into numbered steps.
- Merge duplicate examples only when the remaining example covers every distinct branch.
- Replace narrative introductions with the actual precondition or action.
- Move large optional details to a referenced file when the entrypoint clearly says when to read it.
- Use a compact table for repeated mappings with identical columns.
- Keep one canonical output schema instead of describing it several times.

### Unsafe reductions

- Dropping “minor” flags, commands, tools, formats, triggers, or limitations.
- Replacing a concrete list with “etc.”, “and more,” or “such as.”
- Collapsing the newest corrected decision into an older statement.
- Removing failed attempts when they explain a blocker or prevent repeating a harmful action.
- Rewriting exact errors, security requirements, paths, or numerical thresholds.
- Turning optional behavior into a requirement, or a requirement into advice.
- Summarizing code in a way that changes executable syntax.
- Adding modern tools, platforms, or best practices that were not in the source.

## Skill-specific guidance

Retain:

- every top-level workflow state and branch;
- all invocation modes and argument grammar;
- trigger and non-trigger boundaries;
- tool names and permission implications;
- output schemas, filenames, and paths;
- retry, stop, failure, and rollback behavior;
- references and the conditions for loading them.

Descriptions are activation metadata, not a marketing summary. A concise description that drops a near-match trigger can make the skill effectively unusable even if the body is perfect.

## Agent-specific guidance

Real Claude Code agents require valid YAML frontmatter. Preserve the full operational contract before shortening the body:

- `name` and `description`;
- tool and disallowed-tool lists;
- model, effort, permission mode, and turn limits;
- hooks, MCP servers, skills, memory, isolation, and background behavior;
- all unknown or future frontmatter keys.

In the body, keep role boundaries, process, expected evidence, output format, escalation conditions, and limitations. Do not replace an existing tool with a newer or “better” one.

## Tables

Tables help when several items share a stable schema. They hurt when a cell becomes a dense paragraph or when qualifiers disappear.

Use a table for:

- command → behavior → writes?
- status → meaning → next action;
- supported format → capability → limitation;
- severity → criteria → response.

Keep prose or bullets for conditional logic, safety rules, and steps whose order matters.

## Examples

An example can be removed only if it adds no unique literal, branch, edge case, or output requirement. Before deleting an example, check it against every inventory category and concept.

When one example remains:

- prefer the one with the most representative input;
- retain exact commands and output shape;
- keep negative controls and failure examples when they define a boundary;
- do not change placeholder syntax or quote style if consumers may copy it.

## Tiny files

Some well-written files cannot safely reach 2:1. Make one careful candidate, run the gates, and return `NOT_COMPRESSIBLE` after at most three drafts if further reduction would remove meaning. Do not pad the original, minify Markdown into unreadable text, or hide content in generated files to manufacture a ratio.

## Reviewer checklist

Before sending a candidate to the independent reviewer:

- The opening frontmatter delimiter remains line 1 when the source has frontmatter.
- All inventory categories were explicitly reviewed.
- Every literal appears in both source and candidate.
- Every concept has exact, locatable source and candidate excerpts.
- No unsupported additions appear.
- No requirement strength, ordering, or failure behavior changed.
- The candidate can stand alone without the source.
- Supporting references remain reachable.
