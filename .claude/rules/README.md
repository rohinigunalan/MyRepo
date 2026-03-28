# Path-Scoped Rules

This folder contains rules that apply to specific file patterns using glob matching.

## Available Rules

### Code Style
- **code-style.md** - Formatting, naming, and style conventions
  - Applies to: `**/*.py`, `**/*.js`, `**/*.ts`

### Testing Standards
- **testing.md** - Test structure, naming, fixtures, coverage
  - Applies to: `**/test_*.py`, `**/*.test.js`, `**/*.spec.ts`

### API Design
- **api-conventions.md** - REST API and internal API patterns
  - Applies to: `**/api/**/*.py`, `**/routes/**/*.py`, `**/endpoints/**/*.py`

## How Path-Scoped Rules Work

Rules in this folder use YAML frontmatter with `globs` to specify which files they apply to:

```yaml
---
name: code-style
description: Code formatting conventions
globs:
  - "**/*.py"
  - "**/*.js"
---
```

When Claude works on a file matching the glob pattern, it automatically applies the rules from that file.

## Creating New Rules

1. Create a `.md` file in this folder
2. Add YAML frontmatter with `name`, `description`, and `globs`
3. Write the rule content in markdown

**Example:**
```markdown
---
name: security-rules
description: Security best practices
globs:
  - "**/auth/**/*.py"
  - "**/api/**/*.py"
---

# Security Rules

Never hardcode credentials...
```

## Rule Priority

1. Most specific glob wins
2. Rules are cumulative (multiple rules can apply)
3. Project-specific rules (SSD) override cross-project rules (Main)

---

*Rules help maintain consistency across the codebase*
