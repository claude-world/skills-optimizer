---
name: code-analyzer
description: |
  This skill enables comprehensive static code analysis, providing developers with insights
  into code quality, potential bugs, security vulnerabilities, and best practice violations.
  The skill supports multiple programming languages and can analyze individual files, entire
  directories, or complete repositories.

  The analyzer uses a combination of pattern matching, abstract syntax tree analysis, and
  data flow analysis to identify issues ranging from simple style violations to complex
  security vulnerabilities. It integrates with popular linting tools and can produce reports
  in various formats.

  Supported languages include:
  - JavaScript/TypeScript (ESLint integration)
  - Python (Pylint, flake8, mypy integration)
  - Java (PMD, SpotBugs integration)
  - Go (golangci-lint integration)
  - Rust (Clippy integration)
  - C/C++ (cppcheck integration)

  Key features:
  - Multi-language support with language-specific rulesets
  - Security vulnerability detection (OWASP Top 10)
  - Code complexity metrics (cyclomatic complexity, cognitive complexity)
  - Dependency analysis and vulnerability scanning
  - Custom rule definition support
  - IDE integration for real-time feedback
  - CI/CD pipeline integration
  - Historical trend analysis

  Use this skill when helping users improve their code quality, identify potential bugs before
  they reach production, ensure security best practices, or understand the structure and
  complexity of a codebase. The skill is valuable for code reviews, onboarding new team members
  to a codebase, or preparing for security audits.
---

# Code Analyzer Skill

Advanced static code analysis for multiple languages with security scanning and quality metrics.

## Overview

The Code Analyzer skill provides comprehensive static analysis capabilities to help developers write better, more secure code. It combines multiple analysis techniques to identify issues at various levels of severity.

## Supported Languages

The skill supports the following programming languages with varying levels of analysis depth:

| Language | Syntax Analysis | Type Analysis | Security Scan | Complexity |
|----------|----------------|---------------|---------------|------------|
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

### 1. Syntax and Style Analysis

Identifies violations of coding style and conventions:

- Indentation and formatting issues
- Naming convention violations
- Unused variables and imports
- Dead code detection
- Line length violations
- Missing documentation

### 2. Bug Detection

Finds potential bugs before they cause problems:

- Null pointer dereferences
- Type mismatches
- Array bounds violations
- Resource leaks (unclosed files, connections)
- Race conditions in concurrent code
- Unreachable code paths

### 3. Security Analysis

Identifies security vulnerabilities based on OWASP Top 10:

- **Injection Flaws**: SQL injection, command injection, XSS
- **Authentication Issues**: Weak password handling, session management
- **Sensitive Data Exposure**: Hardcoded credentials, logging sensitive data
- **XXE Vulnerabilities**: Unsafe XML parsing
- **Access Control**: Missing authorization checks
- **Security Misconfigurations**: Debug mode enabled, default credentials
- **Insecure Dependencies**: Known vulnerable libraries

### 4. Complexity Analysis

Measures code complexity to identify maintainability issues:

```
Complexity Metrics:
  Cyclomatic Complexity: Measures decision points in code
  Cognitive Complexity: Measures how hard code is to understand
  Halstead Metrics: Measures computational complexity
  Lines of Code: Physical and logical line counts
  Depth of Inheritance: For OOP languages
```

### 5. Dependency Analysis

Analyzes project dependencies for issues:

- Outdated packages
- Known vulnerabilities (CVE database)
- License compatibility
- Unused dependencies
- Circular dependencies

## Usage

### Basic Commands

```bash
# Analyze a single file
/code-analyzer analyze src/main.py

# Analyze entire directory
/code-analyzer analyze ./src --recursive

# Security-focused scan
/code-analyzer security ./src

# Generate complexity report
/code-analyzer complexity ./src --output report.html

# Check dependencies
/code-analyzer deps ./package.json
```

### Analysis Profiles

Use predefined profiles for common scenarios:

```bash
# Quick check - fast, essential issues only
/code-analyzer analyze ./src --profile quick

# Standard - balanced analysis
/code-analyzer analyze ./src --profile standard

# Strict - comprehensive, all rules enabled
/code-analyzer analyze ./src --profile strict

# Security - focus on security issues
/code-analyzer analyze ./src --profile security
```

### Custom Configuration

Create a `.code-analyzer.yaml` file for custom settings:

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

## Output Formats

The skill can generate reports in various formats:

### Console Output (Default)

```
src/auth/login.py
  Line 23:5  error    SQL injection vulnerability     security/sql-injection
  Line 45:1  warning  Function too complex (CC=15)    complexity/cyclomatic
  Line 67:3  info     Consider using f-string         style/string-format

src/utils/helpers.py
  Line 12:1  warning  Unused import 'os'              imports/unused
  Line 89:5  error    Possible null dereference       bugs/null-check

Summary: 2 errors, 2 warnings, 1 info
```

### JSON Output

```bash
/code-analyzer analyze ./src --format json > report.json
```

### HTML Report

```bash
/code-analyzer analyze ./src --format html --output report.html
```

### SARIF Format (for GitHub integration)

```bash
/code-analyzer analyze ./src --format sarif > results.sarif
```

## Severity Levels

Issues are categorized by severity:

| Level | Description | Action Required |
|-------|-------------|-----------------|
| Error | Critical issues that must be fixed | Yes, before merge |
| Warning | Potential problems to review | Recommended |
| Info | Suggestions for improvement | Optional |
| Hint | Style preferences | Optional |

## Integration

### Git Hooks

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
/code-analyzer analyze --staged --severity error
```

### CI/CD Pipeline

GitHub Actions example:

```yaml
name: Code Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Analysis
        run: /code-analyzer analyze ./src --format sarif --output results.sarif
      - name: Upload Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

### IDE Integration

The skill provides integration with popular IDEs:

- **VS Code**: Install the Code Analyzer extension
- **IntelliJ**: Add as external tool
- **Vim/Neovim**: Use with ALE or coc.nvim

## Custom Rules

Define custom rules for project-specific requirements:

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

The analyzer is optimized for large codebases:

- Incremental analysis (only changed files)
- Parallel processing for multi-core systems
- Caching of analysis results
- Memory-efficient streaming for large files

Typical performance:
- Small project (< 10K LOC): < 5 seconds
- Medium project (10K-100K LOC): < 30 seconds
- Large project (> 100K LOC): < 2 minutes

## Limitations

- Binary files are not analyzed
- Generated code may produce false positives
- Some language features may not be fully supported
- Custom frameworks may require custom rules
- Analysis accuracy varies by language

## Best Practices

1. **Start with Standard Profile**: Begin with the standard profile and adjust as needed
2. **Fix High Severity First**: Prioritize errors over warnings
3. **Integrate Early**: Add analysis to your workflow early in development
4. **Customize for Your Project**: Add project-specific rules and exceptions
5. **Review Regularly**: Run full analysis periodically, not just on changed files

## See Also

- [Rule Reference](rules/index.md)
- [Security Scanning Guide](guides/security.md)
- [Custom Rules Tutorial](guides/custom-rules.md)
- [CI/CD Integration](guides/ci-cd.md)
