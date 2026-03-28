---
name: security-review
description: Comprehensive security audit to find vulnerabilities and security issues
---

# Security Review Skill

Comprehensive security audit workflow to identify vulnerabilities and security misconfigurations.

## When This Activates

This skill automatically activates when:
- User asks for security review or audit
- Preparing for deployment
- After significant code changes
- When security concerns are mentioned
- Before committing sensitive code

## Workflow

### 1. Secret Scanning
**Search for exposed credentials:**

```bash
# Search for hardcoded secrets
grep -r "password\s*=\s*['\"]" src/
grep -r "api[_-]?key\s*=\s*['\"]" src/
grep -r "token\s*=\s*['\"]" src/
grep -r "secret\s*=\s*['\"]" src/

# Check for .env in git
git ls-files | grep -E "\.env$|credentials|secret"

# Look for AWS/cloud credentials
grep -r "AKIA[0-9A-Z]{16}" src/
```

**Common patterns to flag:**
- `password = "hardcoded"`
- `API_KEY = "sk_live_..."`
- `SECRET_TOKEN = "abc123..."`
- Private keys (-----BEGIN RSA PRIVATE KEY-----)
- Database connection strings with passwords

### 2. Injection Vulnerabilities

#### SQL Injection
```bash
# Find SQL string concatenation
grep -r "f\"SELECT.*{" src/
grep -r "\.format.*SELECT" src/
grep -r "% .*SELECT" src/

# Flag patterns like:
# query = f"SELECT * FROM users WHERE id = {user_id}"
# cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)
```

#### Command Injection
```bash
# Find shell command execution with user input
grep -r "os\.system" src/
grep -r "subprocess\.call" src/
grep -r "eval\(" src/
grep -r "exec\(" src/

# Flag patterns like:
# os.system(f"ls {user_input}")
# subprocess.call(f"rm {filename}", shell=True)
```

#### Path Traversal
```bash
# Find file operations with user input
grep -r "open\(.*request\." src/
grep -r "\/.*user.*\/" src/

# Flag patterns like:
# open(f"/uploads/{filename}")  # No sanitization!
```

### 3. Authentication & Authorization

**Check for:**
- Weak password comparison (timing attacks)
- Missing authentication on sensitive endpoints
- Hardcoded credentials
- Insecure session management
- Missing authorization checks

```bash
# Find password comparisons
grep -r "password\s*==\s*" src/
grep -r "token\s*==\s*" src/

# Should use: secrets.compare_digest()
```

### 4. Cryptography Issues

```bash
# Find weak hashing algorithms
grep -r "md5\|MD5" src/
grep -r "sha1\|SHA1" src/

# Find hardcoded crypto keys
grep -r "AES.*=.*['\"]" src/
grep -r "KEY.*=.*b['\"]" src/
```

**Flag:**
- MD5, SHA1 for passwords (use bcrypt, Argon2)
- Hardcoded encryption keys
- ECB mode (insecure)
- Small key sizes

### 5. Insecure Deserialization

```bash
# Find pickle usage
grep -r "pickle\.loads" src/
grep -r "yaml\.load\(" src/

# Flag patterns like:
# pickle.loads(untrusted_data)  # RCE risk!
# yaml.load(user_input)  # Use safe_load
```

### 6. Dependency Vulnerabilities

```bash
# Check for outdated packages
pip list --outdated

# Check for known vulnerabilities (if safety installed)
pip install safety
safety check

# Review requirements
cat requirements.txt
```

### 7. Configuration Issues

**Check for:**
- Debug mode enabled in production
- CORS misconfiguration
- Exposed admin panels
- Default credentials
- Unnecessary services enabled

```bash
# Find debug flags
grep -r "DEBUG.*=.*True" src/
grep -r "debug.*=.*true" src/

# Check for broad CORS
grep -r "Access-Control-Allow-Origin.*\*" src/
```

### 8. Input Validation

**Verify:**
- User input is validated
- File uploads are restricted
- Size limits enforced
- Content-type validated

```bash
# Find request.form/request.json without validation
grep -r "request\.form\[" src/
grep -r "request\.json\[" src/
```

## Security Checklist

### 🔴 CRITICAL Issues
- [ ] No hardcoded credentials
- [ ] No SQL injection vulnerabilities
- [ ] No command injection risks
- [ ] No remote code execution paths
- [ ] Authentication required on sensitive endpoints

### 🟠 HIGH Issues
- [ ] No weak cryptography (MD5, SHA1)
- [ ] No insecure deserialization
- [ ] No path traversal vulnerabilities
- [ ] Proper authorization checks
- [ ] Secure session management

### 🟡 MEDIUM Issues
- [ ] Input validation present
- [ ] Output encoding for XSS prevention
- [ ] CSRF protection enabled
- [ ] Secure HTTP headers set
- [ ] Error messages don't leak info

### 🟢 LOW Issues
- [ ] Debug mode off in production
- [ ] Dependencies up to date
- [ ] Security logging in place
- [ ] Rate limiting configured
- [ ] HTTPS enforced

## Report Format

```markdown
# Security Audit Report

**Date:** [Date]
**Scope:** [Files/modules reviewed]
**Findings:** X critical, Y high, Z medium, W low

---

## 🔴 CRITICAL: [Issue Title]

**File:** `src/module.py:45`

**Issue:** [What's wrong]

**Impact:** [What attacker could do]

**Code:**
```python
# Vulnerable code
```

**Fix:**
```python
# Secure code
```

**References:**
- [OWASP link]
- [CWE link]

---

[Repeat for each issue]

## Summary

[Overall assessment]
[Priority fixes]
[Recommendations]
```

## OWASP Top 10 Coverage

1. ✅ **Broken Access Control** - Check authorization
2. ✅ **Cryptographic Failures** - Check crypto usage
3. ✅ **Injection** - SQL, command, path traversal
4. ✅ **Insecure Design** - Architecture review
5. ✅ **Security Misconfiguration** - Debug, CORS, defaults
6. ✅ **Vulnerable Components** - Dependency audit
7. ✅ **Authentication Failures** - Auth review
8. ✅ **Data Integrity Failures** - Deserialization
9. ✅ **Logging Failures** - Security logging
10. ✅ **SSRF** - Request validation

## Remediation Priorities

1. **Immediate** (Critical):
   - Exposed credentials
   - SQL injection
   - Remote code execution
   - Authentication bypass

2. **This Sprint** (High):
   - Weak cryptography
   - Path traversal
   - Authorization issues
   - Insecure deserialization

3. **Next Sprint** (Medium):
   - Input validation gaps
   - XSS vulnerabilities
   - CSRF missing
   - Configuration hardening

4. **Backlog** (Low):
   - Dependency updates
   - Logging improvements
   - Documentation updates
   - Code quality issues

## False Positive Handling

Some findings may be false positives:
- Test code with intentionally bad examples
- Comments showing anti-patterns
- Sanitized/validated input (check context)
- Framework-provided security

Always review findings in context!

---

*Security review should be performed before every deployment and after significant changes*
