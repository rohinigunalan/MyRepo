---
name: deploy
description: Pre-deployment checklist and deployment steps
argument-hint: [optional: environment (dev|qa|prod)]
---

# Deploy Command

Execute pre-deployment checks and guide through deployment process.

**Target Environment:** $ARGUMENTS

## Current Git State

!`git status -sb`

## Recent Commits

!`git log --oneline -5`

## Files Changed Since Last Tag

!`git diff --name-only $(git describe --tags --abbrev=0 2>/dev/null || echo 'HEAD~10')..HEAD`

## Pre-Deployment Checklist

Claude, please verify the following before deployment:

### 1. Code Quality
```bash
# Run tests
pytest tests/ -v --cov=src

# Check code style
black --check src/ tests/
flake8 src/ tests/
```

### 2. Current State Already Shown Above
git fetch origin
git status -sb
```

### 3. Dependencies
```bash
# Verify requirements.txt is up to date
pip freeze > requirements-check.txt
diff requirements.txt requirements-check.txt
```

### 4. Security Check
- [ ] No secrets in code
- [ ] .env files not committed
- [ ] Sensitive data properly handled
- [ ] Authentication/authorization working

### 5. Documentation
- [ ] README.md updated
- [ ] CHANGELOG.md updated (if exists)
- [ ] API documentation current
- [ ] Configuration documented

### 6. Testing
- [ ] All tests passing
- [ ] Edge cases covered
- [ ] Integration tests run
- [ ] Manual testing completed

## Deployment Steps

### For Development/QA
```bash
# 1. Commit changes
git add <files>
git commit -m "type: description"

# 2. Push to feature branch
git push origin <branch-name>

# 3. Create pull request
# Review PR checklist
```

### For Production
```bash
# 1. Ensure on main branch
git checkout main
git pull origin main

# 2. Tag release (if applicable)
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 3. Deploy
# (Project-specific deployment commands here)
```

## Post-Deployment

### 1. Verification
- [ ] Application starts successfully
- [ ] Key features working
- [ ] No errors in logs
- [ ] Performance acceptable

### 2. Monitoring
- [ ] Check error tracking (if configured)
- [ ] Monitor resource usage
- [ ] Watch for anomalies

### 3. Rollback Plan
If issues occur:
```bash
# Revert to previous version
git revert <commit-hash>
# OR
git reset --hard <previous-tag>
```

## Output

Provide:
- ✅ Checklist results
- ⚠️ Any warnings or issues found
- 📋 Deployment command summary
- 🔄 Rollback instructions (if needed)

**IMPORTANT**: Never deploy without:
1. All tests passing
2. Code review completed (for team projects)
3. Backup/rollback plan ready
