# Release Notes Template

Use this template when creating release notes for a new version.

## Version X.Y.Z - YYYY-MM-DD

### 🎉 New Features
- **Feature name**: Brief description of what it does and why it's useful
- **Feature name**: Brief description

### 🔧 Improvements
- **Area**: What was improved and the benefit
- **Area**: What was improved

### 🐛 Bug Fixes
- **Issue #123**: What was fixed and how it affects users
- **Issue #456**: What was fixed

### ⚠️ Breaking Changes
- **Change description**: What changed, why, and migration instructions
- **Change description**: What changed and how to update

### 📚 Documentation
- Updated README with new feature documentation
- Added API documentation for X endpoint
- Updated deployment guide

### 🔒 Security
- Fixed vulnerability in X (if applicable)
- Updated dependency Y to secure version

### ⚡ Performance
- Improved X by Y% through optimization Z
- Reduced memory usage in module A

### 🔄 Dependencies
- Updated package X from v1.0 to v2.0
- Added new dependency Y for feature Z
- Removed deprecated package W

---

## Upgrade Instructions

### Prerequisites
- Ensure you're running version X.Y.Z or higher
- Backup your data before upgrading
- Review breaking changes section above

### Steps
1. Pull latest code: `git pull origin main`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: (if applicable)
4. Restart services: (if applicable)

### Rollback
If issues occur, rollback to previous version:
1. Checkout previous tag: `git checkout vX.Y.Z-1`
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Restore backup (if database changes made)

---

## Contributors
- @username - Feature A, Bug fix B
- @username - Feature C
- @username - Documentation improvements

## Full Changelog
https://github.com/org/repo/compare/vX.Y.Z-1...vX.Y.Z

---

*Thank you to everyone who contributed to this release!*
