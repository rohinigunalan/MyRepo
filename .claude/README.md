# Main/.claude - Cross-Project Configuration

This folder contains **shared conventions and standards** that apply to **ALL projects** under `/Users/rgunalan/Document/Main/`.

Individual projects (SSD, Newfolder, etc.) have their own `.claude/` folders with project-specific instructions that **take priority** over these general conventions.

---

## 📁 Structure

```
Main/.claude/
├── README.md              ← You are here
├── CLAUDE.md              ← Cross-project conventions (ALL projects)
├── settings.json          ← Common permissions
├── .gitignore             ← Excludes personal files
│
├── rules/
│   ├── python-style.md    ← Python code style (PEP 8)
│   ├── git-conventions.md ← Git commit messages, branching
│   └── testing-general.md ← pytest standards
│
├── commands/              ← (Empty, ready for cross-project commands)
├── skills/                ← (Empty, ready for cross-project workflows)
└── agents/                ← (Empty, ready for specialized agents)
```

---

## 🎯 Purpose

### This Folder (Main/.claude/)
Contains **general** standards that apply everywhere:
- Python version (3.12+)
- Code style (PEP 8)
- Git conventions (commit messages, branching)
- Testing standards (pytest)
- Documentation standards

### Project Folders (e.g., SSD/.claude/)
Contain **specific** instructions for that project:
- Project setup steps
- Technology stack details (Playwright, etc.)
- Project-specific workflows
- Custom commands for that project

---

## 🔄 How They Work Together

When working in a sub-project (e.g., SSD), Claude reads **BOTH**:

1. **Main/.claude/** (this folder) → General conventions
2. **SSD/.claude/** → SSD-specific (takes priority if conflict)

### Example:

**Main/.claude/CLAUDE.md** says:
> "Use pytest for all Python projects"

**SSD/.claude/CLAUDE.md** says:
> "Use pytest with Playwright, connect to Chrome on port 9222"

**Result:** Claude applies both! Uses pytest (from Main) with Playwright specifics (from SSD).

---

## 📚 What's Configured

### CLAUDE.md
Cross-project conventions including:
- ✅ Python 3.12+ standard
- ✅ Virtual environment conventions
- ✅ PEP 8 code style
- ✅ pytest testing standards
- ✅ Git commit message format
- ✅ Branch naming conventions
- ✅ Documentation requirements
- ✅ Security standards
- ✅ Debugging guidelines

### settings.json
Common permissions:
- ✅ Allow: Read, basic Bash commands, git status/log/diff
- ❌ Deny: rm -rf, sudo, force push, editing .env files

### rules/python-style.md
Applied to: `**/*.py`
- PEP 8 compliance
- Import ordering
- Naming conventions
- Type hints
- Docstring format

### rules/git-conventions.md
Applied to: Git operations
- Commit message format
- Branch naming
- PR description template
- What not to commit
- Safe vs dangerous commands

### rules/testing-general.md
Applied to: `**/test_*.py`, `**/tests/**/*.py`
- pytest standards
- Test organization
- Fixture usage
- Coverage goals
- Best practices

---

## 🚀 Getting Started

### For Team Members

1. **Read Main conventions:**
   ```bash
   cat .claude/CLAUDE.md
   ```

2. **Check your project's conventions:**
   ```bash
   cd SSD
   cat .claude/CLAUDE.md
   ```

3. **Create personal notes (optional):**
   ```bash
   # In Main folder
   cp .claude/CLAUDE.local.md.example .claude/CLAUDE.local.md

   # Or in specific project
   cd SSD
   cp .claude/CLAUDE.local.md.example .claude/CLAUDE.local.md
   ```

### For Project Maintainers

**To add new cross-project conventions:**
1. Update `Main/.claude/CLAUDE.md` or create new rule in `rules/`
2. Commit and push
3. Communicate to team

**To override in specific project:**
1. Update that project's `.claude/CLAUDE.md`
2. Project-specific settings take priority

---

## 📊 Hierarchy

```
~/.claude/CLAUDE.md                          ← Personal (highest priority)
    ↓ (overrides if conflict)
/Main/SSD/.claude/CLAUDE.md                  ← Project-specific
    ↓ (overrides if conflict)
/Main/.claude/CLAUDE.md                      ← Cross-project (this folder)
```

**Priority:** Personal > Project > Cross-Project

---

## 🔧 Projects Using This

All projects under `/Users/rgunalan/Document/Main/`:
- **SSD** - Playwright automation (has own `.claude/` with specifics)
- **Newfolder** - (add description)
- *(Add more projects as they're created)*

---

## 🤝 Contributing

### Updating Cross-Project Conventions

These conventions affect **ALL projects**. To update:

1. **Discuss with team** (if team project)
2. **Create branch:**
   ```bash
   git checkout -b docs/update-conventions
   ```
3. **Update files:**
   - Edit `CLAUDE.md` for general updates
   - Add new rule in `rules/` for specific topics
4. **Create PR with description:**
   - What changed and why
   - Which projects are affected
   - Breaking changes if any
5. **Get approval and merge**
6. **Communicate changes** to team

### Adding Project-Specific Rules

If a convention only applies to ONE project:
- ✅ Add to that project's `.claude/` folder
- ❌ Don't add to `Main/.claude/` (keep it general)

---

## 📖 Learn More

- **Article:** https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder
- **Individual projects:** Check each project's `.claude/README.md`
- **Global preferences:** `~/.claude/CLAUDE.md`

---

## ❓ FAQ

**Q: Do I need `.claude/` in every project?**
A: No! This Main/.claude/ applies to all. Add project-specific `.claude/` only when you need project-specific instructions.

**Q: What if Main/.claude/ and SSD/.claude/ conflict?**
A: Project-specific (SSD) takes priority. More specific always wins.

**Q: Should I commit CLAUDE.local.md?**
A: No! It's gitignored. That's for your personal notes only.

**Q: Can I override Main/.claude/ settings for my machine?**
A: Yes! Create `Main/.claude/settings.local.json` (gitignored) or `~/.claude/CLAUDE.md` (personal).

**Q: How do I test if my rules are working?**
A: Ask Claude to do something covered by the rules and see if it follows them.

---

*Last updated: 2026-03-27*
*Applies to: All projects under `/Users/rgunalan/Document/Main/`*
