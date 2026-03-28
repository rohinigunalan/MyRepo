---
name: deploy
description: Complete deployment workflow with pre-flight checks and validation
---

# Deploy Skill

Comprehensive deployment workflow with safety checks, validation, and rollback planning.

## When This Activates

This skill automatically activates when:
- User mentions deployment, release, or production
- Preparing to push to main/production branch
- Creating a release or tag
- User asks to ship or go live

## Pre-Deployment Checklist

### 1. Code Quality
**Ensure code meets standards:**

```bash
# Run test suite
pytest tests/ -v --cov=src

# Check code formatting
black --check src/ tests/

# Run linter
flake8 src/ tests/ --max-line-length=88

# Type checking (if using)
mypy src/
```

**Requirements:**
- [ ] All tests passing
- [ ] Code coverage ≥ 80%
- [ ] No linting errors
- [ ] No type errors

### 2. Security Review
**Run security checks:**

```bash
# Check for secrets
grep -r "password\s*=\s*['\"]" src/
grep -r "api[_-]?key\s*=\s*['\"]" src/

# Check dependencies
pip list --outdated
safety check  # If installed

# Verify .env not committed
git ls-files | grep -E "\.env$|credentials"
```

**Requirements:**
- [ ] No hardcoded secrets
- [ ] No known vulnerable dependencies
- [ ] Sensitive files not committed
- [ ] Security audit passed (if applicable)

### 3. Git Status
**Verify repository state:**

```bash
# Check working tree
git status

# Verify on correct branch
git branch --show-current

# Check remote sync
git fetch origin
git status -sb

# View recent commits
git log --oneline -5
```

**Requirements:**
- [ ] Clean working tree (no uncommitted changes)
- [ ] On correct branch (usually main/master)
- [ ] Up to date with remote
- [ ] All commits have meaningful messages

### 4. Documentation
**Ensure documentation is current:**

```bash
# Check README
cat README.md

# Check CHANGELOG (if exists)
cat CHANGELOG.md

# Check for API documentation
ls -la docs/
```

**Requirements:**
- [ ] README reflects current state
- [ ] CHANGELOG updated with changes
- [ ] API docs updated (if applicable)
- [ ] Configuration documented

### 5. Dependencies
**Verify dependency manifest:**

```bash
# Check requirements are up to date
pip freeze > requirements-check.txt
diff requirements.txt requirements-check.txt

# Check for unused dependencies
# (Manual review or use tool like pip-autoremove)
```

**Requirements:**
- [ ] requirements.txt is current
- [ ] No missing dependencies
- [ ] No unnecessary dependencies
- [ ] Version constraints appropriate

### 6. Configuration
**Verify environment configuration:**

```bash
# Check environment variables needed
grep -r "os\.getenv\|os\.environ" src/

# Verify .env.example exists
cat .env.example

# Check configuration files
ls -la config/
```

**Requirements:**
- [ ] All required env vars documented
- [ ] .env.example is up to date
- [ ] No hardcoded config values
- [ ] Environment-specific configs ready

### 7. Database Migrations
**Check database state (if applicable):**

```bash
# Check for pending migrations
# (Project-specific commands)

# Verify migration scripts tested
ls -la migrations/

# Check rollback plan for migrations
```

**Requirements:**
- [ ] All migrations tested
- [ ] Migrations are reversible
- [ ] Data backup plan in place
- [ ] Migration rollback tested

## Deployment Steps

### For Feature Branch → Main

```bash
# 1. Update from main
git checkout main
git pull origin main

# 2. Merge feature branch
git merge feature/branch-name --no-ff

# 3. Run tests one more time
pytest tests/ -v

# 4. Push to main
git push origin main
```

### For Production Release

```bash
# 1. Ensure on main branch
git checkout main
git pull origin main

# 2. Create release tag
# Version: MAJOR.MINOR.PATCH (e.g., 1.2.3)
git tag -a v1.2.3 -m "Release version 1.2.3

- Feature A
- Feature B
- Bug fix C

See CHANGELOG.md for full details."

# 3. Push tag
git push origin v1.2.3

# 4. Create GitHub release (if applicable)
gh release create v1.2.3 \
  --title "Release v1.2.3" \
  --notes-file release-notes.md
```

### For Deployment to Environment

```bash
# Project-specific deployment commands
# Examples:

# Heroku
git push heroku main

# Docker
docker build -t app:v1.2.3 .
docker push registry/app:v1.2.3

# SSH deploy
./deploy.sh production

# CI/CD
# Trigger via GitHub Actions / GitLab CI
```

## Post-Deployment Verification

### 1. Health Checks
**Verify application is running:**

```bash
# Check application endpoint
curl -I https://app.example.com/health

# Verify expected response
curl https://app.example.com/api/version

# Check status page
open https://status.example.com
```

**Verify:**
- [ ] Application responds
- [ ] Health check passes
- [ ] Version is correct
- [ ] No error responses

### 2. Smoke Tests
**Run critical path tests:**

```bash
# Test critical functionality
curl -X POST https://app.example.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'

# Test key features
pytest tests/smoke/ -v

# Manual verification
# - Login works
# - Key features accessible
# - Data displays correctly
```

### 3. Monitoring
**Check system health:**

```bash
# View logs
tail -f /var/log/app.log
# or
kubectl logs deployment/app -f

# Check metrics dashboard
open https://grafana.example.com

# Monitor error tracking
open https://sentry.io/project/app
```

**Monitor for:**
- [ ] No error spikes in logs
- [ ] Response times normal
- [ ] Resource usage acceptable
- [ ] No new errors in tracking

### 4. Performance
**Verify performance:**

```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s https://app.example.com

# Load test (if applicable)
ab -n 100 -c 10 https://app.example.com/

# Check database queries
# (Project-specific monitoring)
```

**Verify:**
- [ ] Response times acceptable
- [ ] No performance regression
- [ ] Database queries efficient
- [ ] Resource usage normal

## Rollback Plan

### If Issues Detected

**Immediate rollback:**

```bash
# Option 1: Revert commit
git revert HEAD
git push origin main

# Option 2: Reset to previous tag
git reset --hard v1.2.2
git push origin main --force  # CAUTION!

# Option 3: Redeploy previous version
# (Deployment-specific commands)
```

**Communication:**
1. Notify team immediately
2. Document issue in incident log
3. Create post-mortem after resolution

### Database Rollback
**If migrations need reversal:**

```bash
# Run down migrations
# (Framework-specific commands)

# Restore from backup if needed
# (Have backup restoration procedure ready)
```

## Deployment Checklist Summary

### Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Security audit passed
- [ ] Documentation updated
- [ ] Dependencies current
- [ ] Configuration verified
- [ ] Backup/rollback plan ready

### Deployment
- [ ] Tag created (if release)
- [ ] Deployed to environment
- [ ] Health checks passing
- [ ] Smoke tests completed

### Post-Deployment
- [ ] Application responding
- [ ] Monitoring showing normal metrics
- [ ] No error spikes
- [ ] Performance acceptable
- [ ] Team notified of deployment

### Rollback Ready
- [ ] Previous version identified
- [ ] Rollback procedure documented
- [ ] Backup available (if needed)
- [ ] Team knows rollback process

## Never Deploy Without

1. **Tests Passing** - All tests must pass
2. **Code Review** - At least one review (team projects)
3. **Clean Git State** - No uncommitted changes
4. **Backup Plan** - Know how to rollback
5. **Monitoring Ready** - Can detect issues

## Deployment Best Practices

### Timing
- ✅ Deploy during low-traffic hours
- ✅ Avoid deployments before weekends/holidays
- ✅ Have team available during deployment
- ❌ Don't deploy late Friday afternoon

### Communication
- ✅ Notify team before deployment
- ✅ Post deployment status updates
- ✅ Document what was deployed
- ✅ Update status page if applicable

### Safety
- ✅ Deploy to staging first
- ✅ Gradual rollout if possible
- ✅ Have rollback plan ready
- ✅ Monitor closely after deployment

### Documentation
- ✅ Update CHANGELOG.md
- ✅ Create release notes
- ✅ Document any manual steps
- ✅ Record deployment time and version

---

*Safe deployments require preparation, validation, and monitoring*
