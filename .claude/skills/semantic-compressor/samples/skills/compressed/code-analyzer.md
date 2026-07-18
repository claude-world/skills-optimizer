---
name: code-analyzer
description: |
  Static analysis of files, directories, or repositories via pattern matching, AST, and data flow: code quality, bugs, OWASP Top 10 vulnerabilities, complexity, dependencies, custom rules, IDE/CI integration, and trends.
  Languages/tools: JavaScript/TypeScript (ESLint), Python (Pylint, flake8, mypy), Java (PMD, SpotBugs), Go (golangci-lint), Rust (Clippy), C/C++ (cppcheck), Ruby, PHP.
  TRIGGERS: static code analysis, code quality, find bugs, security vulnerability, best practice violation, code review, onboarding, security audit, codebase structure, code complexity, dependency scan
---

# Code Analyzer

## Analysis

1. Syntax/style: indentation, formatting, naming, unused variables/imports, dead code, line length, missing documentation.
2. Bugs: null dereferences, type mismatches, array bounds, unclosed files/connections, races, unreachable paths.
3. Security: SQL/command injection, XSS, weak passwords/sessions, hardcoded or logged secrets, XXE, missing authorization, debug/default-credential misconfiguration, vulnerable dependencies/CVEs.
4. Metrics: cyclomatic/cognitive/Halstead complexity, physical/logical LOC, inheritance depth.
5. Dependencies: outdated/vulnerable/unused packages, license compatibility, circular dependencies.

All listed languages receive full syntax, security, and complexity analysis. Type analysis is full for TypeScript/Java/Go/Rust, uses TypeScript for JavaScript and type hints for Python, and is partial for C/C++/Ruby/PHP.

## Commands and profiles

```text
/code-analyzer analyze src/main.py
/code-analyzer analyze ./src --recursive
/code-analyzer security ./src
/code-analyzer complexity ./src --output report.html
/code-analyzer deps ./package.json
/code-analyzer analyze ./src --profile quick
/code-analyzer analyze ./src --profile standard
/code-analyzer analyze ./src --profile strict
/code-analyzer analyze ./src --profile security
/code-analyzer analyze ./src --format json > report.json
/code-analyzer analyze ./src --format html --output report.html
/code-analyzer analyze ./src --format sarif > results.sarif
/code-analyzer analyze --staged --severity error
```

Profiles mean quick/essential, standard/balanced, strict/all-rules, and security-focused. Outputs are console (default), JSON, HTML, or GitHub-compatible SARIF.

## Configuration

`.code-analyzer.yaml` supports language enablement; Python rules `no-print-statements: warn`, `type-annotations-required: error`, ignores `tests/**`/`migrations/**`; JavaScript rules `no-console: warn`, `prefer-const: error`, extensions `.js/.jsx/.mjs`; `scan_dependencies`, `check_secrets`, `owasp_top_10`; thresholds `max_cyclomatic: 10`, `max_cognitive: 15`, `max_line_length: 120`, `max_function_lines: 50`; and output format/source/severity.

Severity: Error (critical; fix before merge), Warning (review recommended), Info or Hint (optional). Canonical console sample maps `23:5` to SQL injection/security, `45:1` to cyclomatic complexity, `67:3` to f-string style, `12:1` to an unused import, and `89:5` to a possible null dereference; totals are `2 errors, 2 warnings, 1 info`.

## Integration and custom rules

- Git hook: `.git/hooks/pre-commit` with `#!/bin/bash` and the staged command above.
- GitHub Actions: `actions/checkout@v3`, run SARIF with `--output results.sarif`, then `github/codeql-action/upload-sarif@v2` using `sarif_file: results.sarif`.
- IDEs: VS Code extension; IntelliJ external tool; Vim/Neovim with ALE or coc.nvim.
- Custom YAML rules support regex patterns, messages, severity, and languages. Preserve examples `api_key\s*=\s*["'][a-zA-Z0-9]+["']` → `"Do not hardcode API keys"`/error for Python+JavaScript, and `fetch\([^)]+\)(?!\s*\.\s*catch)` → `"fetch() calls must have error handling"`/warning for JavaScript+TypeScript.

## Performance and limits

Incremental, parallel, cached, streaming analysis targets: `<10K LOC` in `<5 seconds`; `10K-100K` in `<30 seconds`; `>100K` in `<2 minutes`.

Binary files are not analyzed; generated code can false-positive; language features/accuracy vary; custom frameworks may need rules. Start standard, fix errors before warnings, integrate early, customize exceptions, and periodically run full analysis.

References: rules `rules/index.md`, security scanning `guides/security.md`, custom rules `guides/custom-rules.md`, CI/CD `guides/ci-cd.md`.
