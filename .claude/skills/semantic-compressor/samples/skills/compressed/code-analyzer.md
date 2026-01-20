---
name: code-analyzer
description: |
  Static code analysis for code quality, potential bugs, security vulnerabilities, and best practice violations.
  Analyzes files, directories, or repositories using pattern matching, AST analysis, and data flow analysis.

  Languages: JavaScript, TypeScript (ESLint), Python (Pylint, flake8, mypy), Java (PMD, SpotBugs),
  Go (golangci-lint), Rust (Clippy), C/C++ (cppcheck), Ruby, PHP.

  Features: Multi-language rulesets, OWASP Top 10 security detection, complexity metrics (cyclomatic,
  cognitive), dependency vulnerability scanning, custom rules, IDE integration, CI/CD integration,
  historical trends.

  Use for code reviews, onboarding, security audits.
---

# Code Analyzer Skill

Static analysis for multiple languages with security scanning and quality metrics.

## Supported Languages

| Language | Syntax | Type | Security | Complexity |
|----------|--------|------|----------|------------|
| JavaScript | Full | With TypeScript | Yes | Yes |
| TypeScript | Full | Full | Yes | Yes |
| Python | Full | With type hints | Yes | Yes |
| Java | Full | Full | Yes | Yes |
| Go | Full | Full | Yes | Yes |
| Rust | Full | Full | Yes | Yes |
| C/C++ | Full | Partial | Yes | Yes |
| Ruby | Full | Partial | Yes | Yes |
| PHP | Full | Partial | Yes | Yes |

## Analysis Types

**Syntax and Style Analysis**
- Indentation, formatting
- Naming violations
- Unused variables, imports
- Dead code
- Line length
- Missing docs

**Bug Detection**
- Null pointer dereferences
- Type mismatches
- Array bounds violations
- Resource leaks (unclosed files, connections)
- Race conditions
- Unreachable code

**Security Analysis** (OWASP Top 10)
- Injection: SQL injection, command injection, XSS
- Authentication: Weak password handling, session management
- Sensitive data: Hardcoded credentials, logging sensitive data
- XXE vulnerabilities
- Access control: Missing authorization checks
- Misconfigurations: Debug mode enabled, default credentials
- Dependencies: Known vulnerable libraries

**Complexity Analysis**
- Cyclomatic Complexity
- Cognitive Complexity
- Halstead Metrics
- Lines of Code
- Depth of Inheritance

**Dependency Analysis**
- Outdated packages
- CVE vulnerabilities
- License compatibility
- Unused dependencies
- Circular dependencies

## Commands

```bash
# Analyze file
/code-analyzer analyze src/main.py

# Analyze directory
/code-analyzer analyze ./src --recursive

# Security scan
/code-analyzer security ./src

# Complexity report
/code-analyzer complexity ./src --output report.html

# Check dependencies
/code-analyzer deps ./package.json
```

## Profiles

```bash
/code-analyzer analyze ./src --profile quick      # Fast, essential only
/code-analyzer analyze ./src --profile standard   # Balanced
/code-analyzer analyze ./src --profile strict     # Comprehensive
/code-analyzer analyze ./src --profile security   # Security-focused
```

## Output Formats

```bash
# Console (default)
/code-analyzer analyze ./src

# JSON
/code-analyzer analyze ./src --format json > report.json

# HTML
/code-analyzer analyze ./src --format html --output report.html

# SARIF (GitHub)
/code-analyzer analyze ./src --format sarif > results.sarif
```

## Severity Levels

| Level | Description | Required |
|-------|-------------|----------|
| Error | Critical issues | Yes, before merge |
| Warning | Potential problems | Recommended |
| Info | Suggestions | Optional |
| Hint | Style preferences | Optional |

## Configuration

`.code-analyzer.yaml`:

```yaml
profile: standard

languages:
  python:
    enabled: true
    rules:
      - no-print-statements: warn
      - type-annotations-required: error
    ignore:
      - tests/**
      - migrations/**

  javascript:
    enabled: true
    rules:
      - no-console: warn
      - prefer-const: error
    extensions:
      - .js
      - .jsx
      - .mjs

security:
  scan_dependencies: true
  check_secrets: true
  owasp_top_10: true

complexity:
  max_cyclomatic: 10
  max_cognitive: 15
  max_line_length: 120
  max_function_lines: 50

output:
  format: html
  include_source: true
  severity_threshold: warn
```

## Integration

**Git Hooks** (`.git/hooks/pre-commit`):
```bash
#!/bin/bash
/code-analyzer analyze --staged --severity error
```

**GitHub Actions**:
```yaml
name: Code Analysis
on: [push, pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: /code-analyzer analyze ./src --format sarif --output results.sarif
      - uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

**IDE Integration**:
- VS Code: Code Analyzer extension
- IntelliJ: External tool
- Vim/Neovim: ALE or coc.nvim

## Custom Rules

```yaml
# custom-rules.yaml
rules:
  - id: no-api-keys-in-code
    pattern: |
      api_key\s*=\s*["'][a-zA-Z0-9]+["']
    message: "Do not hardcode API keys"
    severity: error
    languages: [python, javascript]

  - id: require-error-handling
    pattern: |
      fetch\([^)]+\)(?!\s*\.\s*catch)
    message: "fetch() calls must have error handling"
    severity: warning
    languages: [javascript, typescript]
```

## Performance

Optimizations: Incremental analysis, parallel processing, caching, memory-efficient streaming.

Typical speeds:
- Small (< 10K LOC): < 5 seconds
- Medium (10K-100K LOC): < 30 seconds
- Large (> 100K LOC): < 2 minutes

## Limitations

- Binary files not analyzed
- Generated code may cause false positives
- Some language features may not be fully supported
- Custom frameworks may require custom rules
- Analysis accuracy varies by language
