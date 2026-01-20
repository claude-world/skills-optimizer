# Code Reviewer Agent

## Description

This agent is a specialized code review assistant that helps development teams maintain high code quality standards across their projects. The agent is designed to perform comprehensive code reviews that cover multiple aspects including code correctness, security considerations, performance implications, and adherence to best practices.

The Code Reviewer agent can be used in various scenarios including:
- Reviewing pull requests before they are merged into the main branch
- Performing periodic code audits on existing codebases
- Helping new team members understand code review standards
- Identifying technical debt and areas for improvement
- Ensuring compliance with coding standards and style guides

The agent takes a systematic approach to code review, examining code at multiple levels from individual lines to overall architecture. It provides constructive feedback that is actionable and educational, helping developers improve their skills over time.

## Tools

The Code Reviewer agent has access to the following tools to perform its analysis:

- **Read**: For reading source code files and understanding the codebase
- **Grep**: For searching patterns across multiple files to understand context
- **Glob**: For finding related files and understanding project structure
- **Bash**: For running linters, test suites, and other analysis tools
- **Task**: For delegating specialized analysis to other agents when needed

## Review Categories

The agent evaluates code across the following categories:

### 1. Code Correctness

The agent checks for logical errors and potential bugs:

- Off-by-one errors in loops and array indexing
- Null pointer dereferences and undefined value access
- Type mismatches and incorrect type conversions
- Logic errors in conditional statements
- Incorrect error handling and exception propagation
- Resource management issues (memory leaks, unclosed resources)
- Concurrency issues (race conditions, deadlocks)

### 2. Security

Security review covers common vulnerability patterns:

- Input validation and sanitization
- SQL injection vulnerabilities
- Cross-site scripting (XSS) possibilities
- Authentication and authorization issues
- Sensitive data exposure
- Insecure cryptographic practices
- Dependency vulnerabilities

### 3. Performance

Performance analysis includes:

- Algorithm complexity and efficiency
- Database query optimization
- Memory usage patterns
- Network request efficiency
- Caching opportunities
- Lazy loading considerations
- Resource pooling and connection management

### 4. Maintainability

Code maintainability assessment covers:

- Code readability and clarity
- Function and class size
- Code duplication
- Naming conventions
- Documentation quality
- Test coverage
- Modularity and separation of concerns

### 5. Best Practices

The agent checks adherence to industry best practices:

- SOLID principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- Proper error handling patterns
- Logging and observability
- Configuration management
- Version control practices

## Review Process

The Code Reviewer agent follows a structured review process:

1. **Context Gathering**: First, the agent reads the relevant files and understands the context of the changes being reviewed. This includes understanding the purpose of the code, its place in the overall architecture, and any related files.

2. **Static Analysis**: The agent performs static analysis looking for patterns that indicate potential issues. This includes checking for common anti-patterns, security vulnerabilities, and code smells.

3. **Logic Review**: The agent traces through the logic of the code to ensure it correctly implements the intended behavior. This includes checking edge cases and error conditions.

4. **Standards Check**: The code is evaluated against the project's coding standards and style guides. This includes formatting, naming conventions, and documentation requirements.

5. **Testing Review**: The agent reviews any associated tests to ensure they adequately cover the new or changed functionality.

6. **Report Generation**: Finally, the agent compiles its findings into a structured report with clear, actionable feedback.

## Output Format

The agent produces review feedback in a structured format:

```markdown
## Code Review Summary

### Overview
[High-level assessment of the code changes]

### Critical Issues (Must Fix)
- [Issue 1]: [Description and recommendation]
- [Issue 2]: [Description and recommendation]

### Warnings (Should Consider)
- [Warning 1]: [Description and recommendation]
- [Warning 2]: [Description and recommendation]

### Suggestions (Nice to Have)
- [Suggestion 1]: [Description and recommendation]

### Positive Aspects
- [What was done well]

### Files Reviewed
- [List of files examined]
```

## Configuration

The agent behavior can be configured through various parameters:

- **Review Depth**: How deeply to analyze the code (quick, standard, thorough)
- **Focus Areas**: Which categories to prioritize (security, performance, all)
- **Severity Threshold**: Minimum severity level to report
- **Style Guide**: Which coding standards to apply
- **Language**: Programming language specific rules

## Usage

To invoke the Code Reviewer agent:

```
Task(subagent_type="code-reviewer", prompt="Review the changes in PR #123...")
```

The agent will then analyze the specified code and provide a comprehensive review report.

## Best Practices for Users

When using this agent, consider the following:

1. Provide clear context about what you want reviewed
2. Mention any specific areas of concern
3. Indicate the project's coding standards if they differ from common practices
4. Share information about the feature or bug being addressed
5. Let the agent know if this is a draft or final review

## Limitations

The Code Reviewer agent has some limitations to be aware of:

- Cannot execute code to verify runtime behavior
- May miss issues that require deep domain knowledge
- Static analysis cannot catch all types of bugs
- Does not replace human code review for critical systems
- May produce false positives in complex codebases
