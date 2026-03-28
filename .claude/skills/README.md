# Skills

Skills are complex, multi-step workflows that combine multiple tools and actions to accomplish sophisticated tasks.

Each skill is stored in its own subdirectory containing a `SKILL.md` file that defines the workflow.

## Available Skills

### Development Workflows
- **security-review/** - Comprehensive security audit to find vulnerabilities
- **deploy/** - Complete deployment workflow with pre-flight checks and release process

## Skills vs Commands

### Commands (`.claude/commands/`)
- Simple, single-purpose instructions
- Invoked with slash commands: `/review`, `/fix-issue`
- Quick actions that execute immediately

### Skills (`.claude/skills/`)
- Complex, multi-step workflows
- Can activate automatically based on context
- Multiple tools and decision points
- Example: `security-review` runs full security audit

## How Skills Work

Skills can activate in two ways:

1. **Explicitly referenced**: "Use the security-review skill"
2. **Automatically triggered**: Based on the `trigger` field in SKILL.md frontmatter

Skills guide Claude through complex workflows that require:
- Multiple sequential steps
- Decision points based on results
- Tool usage (Read, Edit, Bash, Grep, etc.)
- Verification and validation
- Documentation and commits
- Recovery from failures

## Skill Structure

Each skill is a subdirectory with:

```
skills/
├── security-review/
│   ├── SKILL.md              # Main workflow definition
│   └── checklist.md          # Supporting documentation (optional)
└── deploy/
    ├── SKILL.md              # Main workflow definition
    └── release-notes-template.md  # Supporting files
```

### SKILL.md Format

```markdown
---
name: skill-name
description: Brief description of what this skill does
trigger: When this skill should automatically activate
---

# Skill Name

## When This Activates
[Conditions when skill activates]

## Workflow

### 1. First Step
[What to do]

### 2. Second Step
[What to do]

### 3. Final Step
[What to do]
```

## Using Skills

Reference skills in your conversations:

```
Use the security-review skill to audit the authentication code
```

```
Run the deploy skill to prepare for production release
```

Claude will follow the skill's workflow, adapting to your specific situation.

## Creating New Skills

1. Create subdirectory: `skills/my-skill/`
2. Create `SKILL.md` with:
   - YAML frontmatter (`name`, `description`, `trigger`)
   - Workflow steps
   - Decision points
   - Verification steps
3. Add supporting files if needed (templates, checklists, etc.)

**Example:**
```bash
mkdir -p skills/my-skill
cat > skills/my-skill/SKILL.md <<'EOF'
---
name: my-skill
description: Brief description
trigger: When user mentions X or Y
---

# My Skill

## Workflow

### 1. Step One
- Do this
- Then this

### 2. Step Two
- Check condition
- If X, do A
- If Y, do B
EOF
```

## Good Skills Include

### Clear Steps
- Numbered sequential steps
- Each step has specific goal
- Prerequisites listed

### Decision Points
- What to do in different scenarios
- How to handle errors
- When to ask for input

### Tool Usage
- Which tools to use (Read, Edit, Bash, Grep)
- When to use each tool
- Expected outputs

### Verification
- How to validate success
- What to check after each step
- How to confirm completion

### Recovery
- What to do if something fails
- How to rollback
- When to stop and ask for help

### Documentation
- What to document
- Where to record information
- Commit message templates

## Project-Specific Skills

Check `SSD/.claude/skills/` for SSD-specific workflow skills:
- **test-workflow/** - Complete SSD test execution from Chrome setup to results
- **add-test/** - Workflow for adding new Playwright tests

---

*Skills encode expert workflows so they can be repeated consistently*
