# Main - Cross-Project Standards

Shared conventions for all projects under `/Users/rgunalan/Document/Main/`.

Sub-projects (SSD, etc.) have their own `.claude/` folders with project-specific overrides.

---

## Commands

```bash
# Python - Virtual Environment
source .venv/bin/activate       # Activate venv (or .venvmac)
python --version                # Verify Python 3.12+

# Testing
pytest tests/ -v                # Run all tests
pytest tests/ --cov=src --cov-report=html  # With coverage
pytest tests/test_file.py::test_name -v -s # Specific test with output

# Code Quality
black src/ tests/               # Format code
black --check src/ tests/       # Check formatting
flake8 src/ tests/              # Lint code
mypy src/                       # Type checking (if configured)

# Git
git status -sb                  # Short status with branch
git log --oneline -10           # Recent commits
git diff --name-only            # Changed files
```

---

## Architecture

### Python Projects
- **Python 3.12+** for all new projects
- **pytest** for testing (NOT unittest)
- **Virtual environments** (venv) - `.venv` or `.venvmac`
- **Black** for code formatting (88 char line length)
- **PEP 8** code style

### Project Structure
```
project/
├── .claude/              # Claude configuration
├── .venv/               # Virtual environment (gitignored)
├── src/                 # Source code
├── tests/               # Tests mirror src/ structure
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Dev dependencies
└── README.md
```

---

## Conventions

### Code Style
- PEP 8 compliant (detailed rules in `rules/code-style.md`)
- Descriptive variable names in snake_case
- Type hints encouraged for public APIs
- Docstrings for public functions (Google style)

### Testing
- Test files: `test_*.py`
- Test functions: `test_descriptive_name()`
- AAA pattern: Arrange, Act, Assert
- Use fixtures for setup/teardown
- One assertion concept per test

### Git Commits
- Format: `<type>: <subject>` (details in `rules/git-conventions.md`)
- Types: feat, fix, docs, test, refactor, chore
- Example: `feat: Add user authentication`
- Commit message includes "why" not just "what"

### Dependencies
- Pin versions: `package==1.2.3`
- Use requirements.txt for production
- Use requirements-dev.txt for dev tools
- Document why specific versions are pinned

---

## Watch out for

### Python
- **Always activate virtual environment** before running code
- Never commit `.venv` to git
- Use `logging` module, not `print()` statements
- Remove debug prints before committing

### Testing
- Tests must pass before committing
- Run full test suite before pushing: `pytest tests/ -v`
- Coverage minimum: 80% overall

### Git
- ❌ Never `git push --force` to main/master
- ❌ Never commit `.env` files or secrets
- ❌ Never `git commit --no-verify` (skips hooks)
- ✅ Create feature branches: `feat/feature-name`
- ✅ Keep commits small and focused

### Security
- No hardcoded credentials or API keys
- Use environment variables for secrets
- `.env` files must be gitignored
- Check `.gitignore` before first commit

---

## Quick Reference

**Start new feature:**
```bash
git checkout -b feat/my-feature
source .venv/bin/activate
```

**Before committing:**
```bash
pytest tests/ -v                # Tests pass?
black src/ tests/               # Code formatted?
git status                      # Review changes
```

**Create PR:**
```bash
git push origin feat/my-feature
# Then create PR with description
```

---

*Detailed standards are in `.claude/rules/` and load automatically.*
*Last updated: 2026-03-27*
