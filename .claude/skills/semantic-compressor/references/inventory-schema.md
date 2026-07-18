# Preservation Inventory

Create one inventory per source file before drafting a candidate. The deterministic validator binds it to the source SHA-256 and requires every listed literal to remain byte-for-byte present.

## Schema

```json
{
  "schema_version": 1,
  "status": "complete",
  "source_sha256": "64 lowercase hex characters",
  "literals": {
    "triggers": [],
    "commands": [],
    "tools": [],
    "formats": [],
    "paths": [],
    "numbers": [],
    "error_messages": [],
    "security_rules": []
  },
  "category_attestations": {
    "triggers": true,
    "commands": true,
    "tools": true,
    "formats": true,
    "paths": true,
    "numbers": true,
    "error_messages": true,
    "security_rules": true
  },
  "concepts": [
    {
      "id": "stable-kebab-case-id",
      "description": "One behavior or constraint whose meaning must remain equivalent"
    }
  ]
}
```

Do not hand-type the source hash. Generate the template with the bundled `inventory` command. It starts as `draft` with every category attestation set to `false`; fill it, reread the complete source, set each reviewed category to `true`, and change the status to `complete`. Validation rejects draft inventories, missing attestations, and inventories with no concepts.

## Extraction rules

Read the complete source and review each category explicitly:

- `triggers`: phrases or domain terms that determine when the skill/agent is selected.
- `commands`: slash commands, command variants, flags, subcommands, and callable names.
- `tools`: tool identifiers, MCP tool names, CLIs, runtimes, and required integrations.
- `formats`: file extensions, protocols, output formats, schemas, and language names.
- `paths`: paths that consumers or commands depend on. Keep exact capitalization and separators.
- `numbers`: limits, versions, timeouts, retry counts, thresholds, ports, prices, and other values whose change affects behavior.
- `error_messages`: exact errors that users, parsers, or recovery logic rely on.
- `security_rules`: exact prohibitions, permission boundaries, secret-handling rules, and safety checks.

An empty array is valid only after reviewing that category, confirming it does not apply, and setting that category's attestation to `true`.

## Concepts

Use concepts for meaning that can be rephrased. Each concept should be independently testable and narrowly scoped. Good concepts describe:

- a capability and its boundary;
- a required sequence or dependency;
- a decision and why it matters;
- a fallback or rollback condition;
- an output contract;
- a limitation or unsupported case.

Do not combine unrelated behaviors into one vague concept such as `all-features`. The semantic reviewer needs enough granularity to cite an exact source excerpt and exact candidate excerpt for every preserved behavior and identify unsupported additions.

## Frontmatter

Do not duplicate frontmatter fields in the literal inventory solely to make the static gate see them. The control script separately verifies that:

- frontmatter presence does not change;
- no top-level key is added or removed;
- `name`, tool/permission fields, hooks, model, context, arguments, version, and unknown fields remain value-equivalent;
- only `description` and `when_to_use` may be rewritten.

Still include trigger phrases from `description` or `when_to_use` under `literals.triggers` when exact wording affects activation.

## Completeness check

Before drafting, answer all of these from the source:

1. What can invoke this file, and what must not invoke it?
2. What operations, tools, formats, and environments does it support?
3. What exact values or messages affect downstream behavior?
4. What safety boundaries or permission controls must remain unchanged?
5. What output shape and failure states do consumers rely on?
6. What limitations, fallbacks, and later corrections override earlier statements?

If any answer is uncertain, reread the source rather than guessing.
