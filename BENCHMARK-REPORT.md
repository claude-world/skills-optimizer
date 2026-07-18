# Semantic Compressor Deterministic Benchmark

> Generated from tracked sample files. Text metrics are deterministic and are not Claude tokenizer counts.

## Summary

| Metric | Original | Compressed | Ratio | Reduction |
|---|---:|---:|---:|---:|
| Lines | 6,101 | 864 | 7.06:1 | 85.8% |
| Words | 18,058 | 5,697 | 3.17:1 | 68.5% |
| Characters | 154,177 | 48,980 | 3.15:1 | 68.2% |
| Bytes | 155,331 | 49,009 | 3.17:1 | 68.4% |

## Sample pairs

| Sample | Kind | Lines | Words | Word ratio |
|---|---|---:|---:|---:|
| `skills/api-tester` | skill | 316 → 51 | 982 → 409 | 2.40:1 |
| `skills/code-analyzer` | skill | 349 → 60 | 1260 → 486 | 2.59:1 |
| `skills/doc-processor` | skill | 153 → 48 | 787 → 318 | 2.47:1 |
| `skills/full-stack-generator` | skill | 2757 → 279 | 7244 → 1651 | 4.39:1 |
| `agents/code-reviewer` | agent | 183 → 80 | 924 → 391 | 2.36:1 |
| `agents/db-specialist` | agent | 280 → 75 | 1120 → 439 | 2.55:1 |
| `agents/devops-orchestrator` | agent | 1752 → 172 | 4530 → 1468 | 3.09:1 |
| `agents/security-auditor` | agent | 311 → 99 | 1211 → 535 | 2.26:1 |

## Interpretation

This report proves file pairing and size measurements only. Semantic preservation is a separate gate: frontmatter and literal inventories are deterministic; conceptual equivalence is an LLM judgment and must be reported with model and evidence rather than as an absolute guarantee.
