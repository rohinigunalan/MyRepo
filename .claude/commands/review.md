---
name: review
description: Review code changes for quality, security, and best practices
argument-hint: [optional: specific-file-or-branch]
---

# Code Review Command

Review the current code changes following the project's standards and best practices.

## Current Changes

!`git status -sb`

## Files Changed

!`git diff --name-only`

## Full Diff

!`git diff $ARGUMENTS`

## Review Process

Claude, please review these changes for:

2. **Review against standards**:
   - Code follows PEP 8 and project conventions (Main/.claude/CLAUDE.md)
   - Tests added/updated for changes
   - No debug statements or commented code
   - Error handling is appropriate
   - No secrets or credentials committed
   - Commit messages follow format

3. **Security check**:
   - No hardcoded credentials
   - Input validation present
   - No SQL injection risks
   - No command injection risks
   - File operations are safe

4. **Quality check**:
   - Code is readable and maintainable
   - Functions are appropriately sized
   - Variable names are descriptive
   - Comments explain "why" not "what"
   - No code duplication

5. **Testing check**:
   - Tests cover new functionality
   - Tests follow AAA pattern (Arrange, Act, Assert)
   - Edge cases are tested
   - Tests are not overly complex

## Output

Provide feedback on:
- ✅ What looks good
- ⚠️ What needs attention
- 🔴 What must be fixed before committing
- 💡 Suggestions for improvement

Be specific with file names and line numbers for any issues found.
