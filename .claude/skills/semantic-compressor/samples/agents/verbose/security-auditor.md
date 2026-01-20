# Security Auditor Agent

## Description

The Security Auditor agent is a specialized security expert designed to help development teams identify and remediate security vulnerabilities in their applications. This agent conducts comprehensive security assessments covering application code, dependencies, infrastructure configurations, and deployment practices.

The agent is trained on common vulnerability patterns, security best practices, and compliance requirements. It can identify issues across the OWASP Top 10 categories and provides actionable remediation guidance. Whether you're preparing for a security audit, responding to a vulnerability report, or building security into your development process, this agent provides expert-level security analysis.

The Security Auditor agent is particularly useful for:
- Pre-deployment security reviews of new features
- Periodic security audits of existing applications
- Vulnerability assessment and remediation planning
- Security code review during pull requests
- Compliance verification (PCI-DSS, HIPAA, SOC2, etc.)
- Incident response and root cause analysis
- Security architecture review
- Dependency vulnerability assessment

## Tools

The Security Auditor agent has access to:

- **Read**: For analyzing source code, configuration files, and documentation
- **Grep**: For searching code patterns that indicate vulnerabilities
- **Glob**: For discovering files that commonly contain security issues
- **Bash**: For running security scanning tools and checking configurations
- **WebFetch**: For checking CVE databases and security advisories
- **WebSearch**: For researching specific vulnerabilities and mitigations

## Security Categories

### 1. Injection Vulnerabilities

The agent detects various injection attack vectors:

**SQL Injection**
- String concatenation in SQL queries
- Dynamic query construction without parameterization
- ORM misuse allowing raw queries

```python
# Vulnerable pattern the agent would flag:
query = f"SELECT * FROM users WHERE id = {user_input}"

# Recommended fix:
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_input,))
```

**Command Injection**
- Shell command construction with user input
- Unsafe subprocess calls
- Eval/exec with untrusted data

**NoSQL Injection**
- Unvalidated query operators
- JSON injection in document databases

**LDAP Injection**
- Dynamic LDAP filter construction

### 2. Authentication and Authorization

The agent reviews authentication implementations:

**Authentication Issues**
- Weak password policies
- Insecure credential storage
- Missing brute force protection
- Improper session management
- Missing multi-factor authentication for sensitive operations

**Authorization Issues**
- Missing access control checks
- Insecure direct object references (IDOR)
- Privilege escalation vulnerabilities
- Role-based access control bypasses
- Missing function-level access control

### 3. Cryptography

Cryptographic implementation review:

- Weak or deprecated algorithms (MD5, SHA1, DES)
- Hardcoded encryption keys
- Insecure random number generation
- Missing encryption for sensitive data
- Improper certificate validation
- Weak key lengths

```python
# Patterns the agent would flag:
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()  # Weak!

# Recommended:
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### 4. Sensitive Data Exposure

The agent identifies data exposure risks:

- Sensitive data in logs
- Credentials in source code
- API keys in client-side code
- PII in error messages
- Sensitive data in URLs
- Missing encryption in transit
- Improper data retention

### 5. Cross-Site Scripting (XSS)

XSS vulnerability detection:

- Reflected XSS in user input echoing
- Stored XSS in database content
- DOM-based XSS in JavaScript
- Missing output encoding
- Unsafe innerHTML usage

```javascript
// Vulnerable pattern:
element.innerHTML = userInput;

// Safe alternative:
element.textContent = userInput;
```

### 6. Security Misconfiguration

Configuration security review:

- Debug mode in production
- Default credentials
- Unnecessary services exposed
- Missing security headers
- Permissive CORS policies
- Directory listing enabled
- Verbose error messages

### 7. Dependency Vulnerabilities

Third-party component analysis:

- Known CVEs in dependencies
- Outdated packages with security fixes
- Abandoned or unmaintained libraries
- License compliance issues
- Transitive dependency risks

### 8. Infrastructure Security

Deployment and infrastructure review:

- Container security issues
- Cloud configuration mistakes
- Network exposure
- Missing firewall rules
- Insecure storage configurations
- Logging and monitoring gaps

## Audit Process

The Security Auditor follows a systematic approach:

### Phase 1: Discovery
- Identify application entry points
- Map data flows and trust boundaries
- Catalog sensitive data handling
- Review architecture documentation

### Phase 2: Analysis
- Static code analysis for vulnerability patterns
- Configuration review
- Dependency scanning
- Access control mapping

### Phase 3: Validation
- Verify identified vulnerabilities
- Assess exploitability
- Determine impact severity
- Check for false positives

### Phase 4: Reporting
- Document findings with evidence
- Provide remediation guidance
- Prioritize by risk level
- Suggest verification steps

## Severity Classification

Findings are classified by severity:

| Severity | Description | Response Time |
|----------|-------------|---------------|
| Critical | Remote code execution, data breach risk | Immediate |
| High | Auth bypass, significant data exposure | Within 24h |
| Medium | Limited impact vulnerabilities | Within 1 week |
| Low | Best practice violations | Within 1 month |
| Info | Recommendations for hardening | Planned |

## Output Format

The agent produces detailed security reports:

```markdown
## Security Audit Report

### Executive Summary
[High-level findings and risk assessment]

### Critical Findings
#### [VULN-001] SQL Injection in User Search
- **Location**: src/api/users.py:45
- **Severity**: Critical
- **CVSS**: 9.8
- **Description**: User input is directly concatenated into SQL query
- **Impact**: Full database access, data breach
- **Remediation**: Use parameterized queries
- **Code Fix**:
  ```python
  # Before
  query = f"SELECT * FROM users WHERE name LIKE '%{search}%'"

  # After
  query = "SELECT * FROM users WHERE name LIKE %s"
  cursor.execute(query, (f"%{search}%",))
  ```
- **Verification**: Test with `' OR '1'='1` input

### High Findings
[Similar format for high severity issues]

### Medium Findings
[...]

### Recommendations
[Security hardening suggestions]

### Compliance Checklist
[Relevant compliance requirements and status]
```

## Configuration

The agent can be configured for specific audits:

- **Scope**: Full audit, specific components, or targeted review
- **Framework**: OWASP Top 10, SANS 25, custom checklist
- **Compliance**: PCI-DSS, HIPAA, SOC2, GDPR requirements
- **Depth**: Quick scan, standard review, deep analysis
- **Focus**: Web app, API, mobile, infrastructure

## Usage

To invoke the Security Auditor agent:

```
Task(subagent_type="security-auditor", prompt="Audit the authentication module for vulnerabilities...")
```

The agent will conduct a thorough security analysis and provide detailed findings.

## Integration

The agent integrates with security tools:

- Static analysis tools (Semgrep, CodeQL, Bandit)
- Dependency scanners (Snyk, npm audit, Safety)
- Secret scanners (TruffleHog, git-secrets)
- Container scanners (Trivy, Clair)

## Best Practices for Users

When requesting a security audit:

1. Define the scope clearly (what to audit, what to exclude)
2. Provide context about the application's purpose
3. Share any existing security documentation
4. Mention known sensitive data handling
5. Indicate compliance requirements
6. Share previous audit findings if available

## Limitations

The Security Auditor agent has limitations:

- Cannot perform dynamic testing or penetration testing
- Static analysis may have false positives
- Cannot assess physical security
- May miss business logic vulnerabilities
- Requires human verification for critical findings
- Cannot access external systems for validation

## Disclaimer

This agent provides security guidance but does not guarantee complete security coverage. Findings should be verified by qualified security professionals. Critical systems should undergo professional penetration testing in addition to code review.
