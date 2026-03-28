# Custom Commands

This folder contains custom slash commands that you can invoke in Claude Code conversations.

## What Are Commands?

Commands are reusable instructions that you can trigger with `/command-name`. They help standardize common workflows and save time on repetitive tasks.

## Available Commands

### Development Workflow
- `/review` - Review code changes for quality, security, and best practices
- `/fix-issue` - Systematically diagnose and fix bugs or issues
- `/deploy` - Pre-deployment checklist and deployment guide

## How to Use

Simply type `/command-name` in your conversation with Claude Code:

```
/review
```

Some commands accept arguments:

```
/review main..HEAD
/fix-issue #123
/deploy prod
/run-login-test -v -s
```

Claude will execute shell commands embedded in the command file and follow the instructions.

## Creating New Commands

1. Create a new `.md` file in this folder
2. Add YAML frontmatter with `name`, `description`, and optional `argument-hint`
3. Embed shell commands with `` !`command` `` syntax
4. Use `$ARGUMENTS` placeholder for command arguments
5. Write instructions for Claude to follow

**Example:**
```markdown
---
name: my-command
description: Description of what this command does
argument-hint: [optional: parameter-name]
---

## Current Status

!`git status`

## With Arguments

!`git log $ARGUMENTS`

Instructions for Claude to execute...
```

### Advanced Features

**Shell Command Embedding:**
- Use `` !`command` `` to execute shell command and embed output
- Example: `` !`git diff --name-only` ``
- Output is injected before Claude processes the command

**Arguments:**
- Add `argument-hint: [param-name]` to frontmatter
- Use `$ARGUMENTS` in command or shell commands
- Example: `` !`pytest tests/$ARGUMENTS` ``

**Example with All Features:**
```markdown
---
name: check-branch
description: Check status of a specific branch
argument-hint: [branch-name]
---

## Branch Status

!`git log origin/main..$ARGUMENTS --oneline`

## Diff Summary

!`git diff origin/main...$ARGUMENTS --stat`

Claude, analyze this branch and summarize the changes.
```

## Command Structure

```
commands/
├── README.md       # This file
├── review.md       # Code review workflow
├── fix-issue.md    # Bug diagnosis and fixing
└── deploy.md       # Deployment checklist
```

## Project-Specific Commands

Check `SSD/.claude/commands/` for SSD-specific commands like:
- `/start-chrome-debug` - Start Chrome for Playwright testing
- `/check-proxy` - Verify proxy configuration
- `/run-login-test` - Execute SSD login automation

---

*These commands work across all projects under Main/*
