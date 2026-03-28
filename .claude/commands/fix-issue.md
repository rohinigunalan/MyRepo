---
name: fix-issue
description: Analyze and fix a bug or issue (optionally provide issue number or description)
argument-hint: [optional: issue-number-or-description]
---

# Fix Issue Command

Systematically diagnose and fix an issue or bug.

## Issue Context

$ARGUMENTS

## Recent Changes

!`git log --oneline -10`

## Current Branch Status

!`git status`

## Diagnostic Process

Claude, please help diagnose and fix this issue:

2. **Gather information**:
   - Review error messages and stack traces
   - Check relevant log files
   - Review recent changes:
     ```bash
     git log --oneline -10
     git diff HEAD~5
     ```

3. **Locate the problem**:
   - Find the relevant code files
   - Identify the functions/methods involved
   - Check for related issues in other parts of the code

4. **Analyze root cause**:
   - What is causing the issue?
   - Is this a logic error, configuration issue, or edge case?
   - Are there any upstream dependencies involved?

5. **Develop a fix**:
   - What is the minimal change needed?
   - Will this affect other parts of the system?
   - What tests need to be added/updated?

6. **Implement the fix**:
   - Make the necessary code changes
   - Add/update tests to cover the issue
   - Verify the fix works
   - Check for any side effects

7. **Verify the fix**:
   ```bash
   pytest tests/ -v
   ```

## Output

Provide:
- 🔍 Root cause analysis
- 🛠️ The fix implemented
- ✅ Tests added/updated
- 📋 Files changed with line numbers
- ⚠️ Any potential side effects or related issues to watch for

Document the fix in commit message following the project's Git conventions.
