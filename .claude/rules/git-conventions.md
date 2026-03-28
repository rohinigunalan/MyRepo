---
name: git-conventions
description: Git commit messages, branch naming, and workflow standards
globs:
  - "**/*"
---

# Git Conventions

Standards for Git commits, branches, and pull requests across all projects.

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation only changes
- **style:** Code formatting (no logic change)
- **refactor:** Code restructuring (no behavior change)
- **test:** Adding or updating tests
- **chore:** Maintenance tasks (deps, config, build)

### Subject Line

- Use imperative mood: "Add feature" not "Added feature"
- Lowercase first letter (except proper nouns)
- No period at the end
- Max 50 characters
- Describe what and why, not how

### Body (Optional)

- Wrap at 72 characters
- Explain the motivation and context
- Describe what changed and why
- Reference issues or tickets

### Footer (Optional)

- Reference issues: `Fixes #123`, `Closes #456`
- Breaking changes: `BREAKING CHANGE: description`
- Co-authored by: `Co-Authored-By: Name <email>`

## Examples

### Simple Commit
```
feat: Add user authentication

Implements login/logout functionality using JWT tokens.
Users can now sign in with email and password.

Fixes #123
```

### Bug Fix
```
fix: Prevent race condition in file upload

Added mutex lock to ensure only one upload processes at a time.
Previous implementation could corrupt files if multiple uploads
occurred simultaneously.

Closes #456
```

### Refactoring
```
refactor: Extract validation logic to separate module

Moved all input validation functions from handlers to validators/
for better reusability and testing. No behavior changes.
```

### Documentation
```
docs: Update README with deployment instructions

Added section on deploying to production environment with
step-by-step instructions and troubleshooting tips.
```

## Branch Naming

### Format
```
<type>/<short-description>
```

### Examples
```
feat/user-authentication
fix/proxy-connection-issue
docs/update-readme
test/add-integration-tests
refactor/extract-validation
chore/update-dependencies
```

### Rules
- Lowercase with hyphens
- No spaces
- Keep short but descriptive
- Match commit type when possible

## Pull Request Guidelines

### Title
- Follow commit message format
- Example: `feat: Add user authentication`

### Description Must Include

**What changed:**
- Summary of changes
- Why this change was needed

**Testing:**
- How was this tested?
- What test cases were added?
- Manual testing steps if applicable

**Screenshots/Videos:**
- For UI changes, include before/after screenshots

**Breaking Changes:**
- Call out any breaking changes
- Migration steps if needed

**Related Issues:**
- Link to issues: `Fixes #123`, `Relates to #456`

### Example PR Description
```markdown
## What Changed
Implemented user authentication using JWT tokens. Users can now sign in
with email/password and access protected routes.

## Testing
- Added unit tests for auth middleware
- Added integration tests for login/logout endpoints
- Manually tested in dev environment
- All existing tests pass

## Breaking Changes
None

## Related Issues
Fixes #123
```

## Git Workflow

### Starting New Work
```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feat/my-feature

# Work on changes...
git add <files>
git commit -m "feat: Add feature X"
```

### Before Pushing
```bash
# Run tests
pytest tests/ -v

# Check code quality
black --check src/ tests/
flake8 src/ tests/

# Review changes
git diff --cached

# Push branch
git push origin feat/my-feature
```

### Creating Pull Request
1. Push branch to remote
2. Create PR on GitHub/GitLab
3. Fill out PR template
4. Request review from team
5. Address review comments
6. Merge when approved

### After Merge
```bash
# Update main
git checkout main
git pull origin main

# Delete feature branch
git branch -d feat/my-feature
git push origin --delete feat/my-feature
```

## What NEVER to Commit

### Security
- ❌ `.env` files with secrets
- ❌ API keys, tokens, passwords
- ❌ Database credentials
- ❌ SSL certificates/private keys (`.pem`, `.key`)
- ❌ AWS credentials
- ❌ `secrets/` folders
- ❌ Any file matching `*secret*`, `*password*`, `*credentials*`

### Generated Files
- ❌ Virtual environments (`.venv`, `.venvmac`)
- ❌ Build artifacts (`dist/`, `build/`)
- ❌ Compiled files (`*.pyc`, `__pycache__/`)
- ❌ IDE settings (`.vscode/`, `.idea/`)
- ❌ OS files (`.DS_Store`, `Thumbs.db`)
- ❌ Log files (`*.log`)

### Temporary Files
- ❌ Debug print statements
- ❌ Commented-out code blocks
- ❌ TODO comments (use issue tracker)
- ❌ Large binary files (images, videos)
- ❌ Test screenshots (except examples)

## Dangerous Git Commands

### Never Do (Unless Explicitly Asked)
```bash
# ❌ Force push to main/master
git push --force origin main

# ❌ Hard reset (loses changes)
git reset --hard HEAD~1

# ❌ Skip hooks (bypasses validation)
git commit --no-verify

# ❌ Force push (overwrites history)
git push -f

# ❌ Delete branches without checking
git branch -D branch-name

# ❌ Checkout with force (loses changes)
git checkout -f
```

### Safe Alternatives
```bash
# ✅ Instead of force push - create new commit
git revert HEAD

# ✅ Instead of hard reset - keep changes
git reset --soft HEAD~1

# ✅ Instead of skipping hooks - fix the issue
# Let hooks run and address the failures

# ✅ Instead of force push - rebase and push
git pull --rebase origin main
git push origin branch-name
```

## Git Best Practices

### Commits
- ✅ Commit early and often
- ✅ Keep commits small and focused
- ✅ One logical change per commit
- ✅ Test before committing
- ✅ Write clear commit messages

### Branches
- ✅ Create branch per feature/fix
- ✅ Keep branches short-lived
- ✅ Rebase frequently from main
- ✅ Delete branches after merge
- ✅ Use descriptive branch names

### Pull Requests
- ✅ Keep PRs small (< 400 lines)
- ✅ Request review from relevant people
- ✅ Respond to review comments
- ✅ Update PR based on feedback
- ✅ Squash commits if needed

### Collaboration
- ✅ Pull before starting work
- ✅ Push at end of day
- ✅ Communicate changes to team
- ✅ Review others' code
- ✅ Be respectful in code reviews

## Troubleshooting

### Merge Conflicts
```bash
# Pull latest main
git pull origin main

# Resolve conflicts in files
# Look for <<<<<<< HEAD markers

# Test after resolving
pytest tests/ -v

# Complete merge
git add <resolved-files>
git commit
```

### Undo Last Commit (Not Pushed)
```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes and commit
git reset --hard HEAD~1
```

### Undo Last Commit (Already Pushed)
```bash
# Create revert commit
git revert HEAD
git push origin branch-name
```

### Amend Last Commit (Not Pushed)
```bash
# Change commit message
git commit --amend -m "New message"

# Add forgotten files
git add forgotten-file.py
git commit --amend --no-edit
```

---

*Follow these conventions for clean, maintainable git history*
