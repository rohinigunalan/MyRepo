# Settings Guide: settings.json vs settings.local.json

Understanding the two-level settings system for Claude Code permissions.

---

## 📊 The Two Files

### **settings.json** (Team Configuration)
- ✅ **Committed to git** - Shared with team
- ✅ **Team-wide permissions** - Everyone gets same base rules
- ✅ **Project standards** - What's safe for everyone

**Location:**
- `Main/.claude/settings.json` - Cross-project permissions
- `SSD/.claude/settings.json` - SSD-specific permissions

### **settings.local.json** (Personal Overrides)
- ❌ **NOT committed** - Gitignored, personal only
- ❌ **Your overrides** - Additional allows or denies
- ❌ **Machine-specific** - Won't affect teammates

**Location:**
- `Main/.claude/settings.local.json` - Your cross-project overrides
- `SSD/.claude/settings.local.json` - Your SSD-specific overrides

---

## 🎯 How They Work Together

**Priority (highest to lowest):**
```
settings.local.json    ← Your personal overrides (highest)
        ↓
settings.json          ← Team configuration (base)
```

**Example:**

**settings.json** (team):
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(pytest*)"
    ],
    "deny": [
      "Bash(rm -rf*)"
    ]
  }
}
```

**settings.local.json** (you):
```json
{
  "permissions": {
    "allow": [
      "Bash(docker*)",           ← You add this
      "Write(my-scratch-folder/**)"  ← You add this
    ],
    "deny": [
      "Bash(git push*)"          ← You add this extra protection
    ]
  }
}
```

**Result:** You get everything from `settings.json` PLUS your additions from `settings.local.json`

---

## 📝 When to Use Each

### Use **settings.json** For:
✅ Permissions everyone on the team needs
✅ Safe commands everyone should be able to run
✅ Project-standard workflows
✅ Common file patterns everyone edits

**Examples:**
- `"Read"` - Everyone needs to read files
- `"Bash(pytest*)"` - Everyone runs tests
- `"Write(tests/**)"` - Everyone writes tests
- `"Bash(git status*)"` - Everyone checks git status

### Use **settings.local.json** For:
✅ Commands only YOU use
✅ Extra protections for YOUR workflow
✅ Personal debugging tools
✅ Machine-specific paths

**Examples:**
- `"Bash(docker*)"` - You use Docker, teammates don't
- `"Write(/Users/yourname/scratch/**)"` - Your personal folder
- `"Bash(git push*)"` - Extra deny for safety (you prefer manual push)
- Personal environment variables

---

## 🚀 Getting Started

### 1. **Use Team Settings (Already Set Up)**
Current `settings.json` files work out of the box!

### 2. **Create Personal Overrides (Optional)**
Only if you need personal customization:

```bash
# For cross-project overrides
cd /Users/rgunalan/Document/Main
cp .claude/settings.local.json.example .claude/settings.local.json
# Edit with your personal settings

# For SSD-specific overrides
cd SSD
cp .claude/settings.local.json.example .claude/settings.local.json
# Edit with SSD-specific personal settings
```

### 3. **Edit Your Local Settings**
```json
{
  "permissions": {
    "allow": [
      "Bash(your-command*)"
    ],
    "deny": [
      "Bash(dangerous-thing*)"
    ]
  }
}
```

---

## 💡 Common Use Cases

### **Case 1: You Use Docker, Teammates Don't**
**Solution:** Add to YOUR `settings.local.json`:
```json
{
  "permissions": {
    "allow": [
      "Bash(docker*)",
      "Bash(docker-compose*)"
    ]
  }
}
```

### **Case 2: Extra Safety for Git Push**
**Solution:** Add to YOUR `settings.local.json`:
```json
{
  "permissions": {
    "deny": [
      "Bash(git push*)"
    ]
  }
}
```
Now Claude will ALWAYS ask before pushing, even if team allows it.

### **Case 3: Personal Scratch Folder**
**Solution:** Add to YOUR `settings.local.json`:
```json
{
  "permissions": {
    "allow": [
      "Write(/Users/yourname/scratch/**)",
      "Edit(/Users/yourname/scratch/**)"
    ]
  }
}
```

### **Case 4: Personal Environment Variables**
**Solution:** Add to YOUR `settings.local.json`:
```json
{
  "environment": {
    "DEBUG": "true",
    "MY_CUSTOM_VAR": "value"
  }
}
```

---

## 🔒 Permission Rules

### **Allow List**
Permissions in `allow` mean Claude can use these **without asking**:
```json
"allow": [
  "Read",                    // Read any file
  "Bash(ls*)",              // Run ls commands
  "Write(tests/**)",        // Write to tests folder
  "Bash(pytest*)"           // Run pytest
]
```

### **Deny List**
Permissions in `deny` mean Claude is **blocked** from using these:
```json
"deny": [
  "Bash(rm -rf*)",          // Never delete recursively
  "Bash(sudo*)",            // Never use sudo
  "Write(.env*)",           // Never write to .env files
  "Bash(git push --force*)" // Never force push
]
```

### **Not Listed = Ask**
If a permission is **not in allow or deny**, Claude will **ask you** before using it.

---

## 🎨 Permission Patterns

### **Wildcard Matching**
```json
"Bash(git*)"              // Matches: git status, git log, git diff
"Write(src/**/*.py)"      // Matches: any .py file in src/ subdirs
"Read"                    // Matches: reading any file
```

### **Specific Commands**
```json
"Bash(git status)"        // Only git status
"Bash(pytest tests/)"     // Only pytest with tests/ argument
```

### **File Patterns**
```json
"Write(tests/**)"         // Any file under tests/
"Edit(*.py)"              // Any .py file in current dir
"Write(**/.env*)"         // Any .env file anywhere (to deny)
```

---

## 🔍 Debugging Permissions

### **Check Current Settings**
```bash
# View team settings
cat .claude/settings.json

# View your personal settings (if exists)
cat .claude/settings.local.json
```

### **Test a Permission**
Just try the action! If Claude asks, it's not in `allow`.
If blocked, it's in `deny`.

### **Claude Asks Too Much?**
Add to `settings.local.json` allow list.

### **Claude Doesn't Ask Enough?**
Add to `settings.local.json` deny list.

---

## 📚 Schema Validation

The `$schema` field enables autocomplete in VS Code:
```json
{
  "$schema": "https://raw.githubusercontent.com/anthropics/claude-code/main/schema/settings.schema.json"
}
```

Open the file in VS Code and you'll get:
- ✅ Autocomplete for field names
- ✅ Validation errors
- ✅ Hover documentation

---

## ⚠️ Important Notes

### **Don't Commit settings.local.json**
It's gitignored! Check:
```bash
cat .claude/.gitignore
# Should see: settings.local.json
```

### **Team Settings Change**
When someone updates `settings.json`:
1. `git pull` to get updates
2. Your `settings.local.json` still works (adds to team settings)
3. No conflicts!

### **Merging Logic**
- **Allow:** Your allows + Team allows (union)
- **Deny:** Your denies + Team denies (union)
- **Environment:** Your vars override team vars (if same name)

---

## 📖 Examples

### Minimal Personal Settings
```json
{
  "$schema": "https://raw.githubusercontent.com/anthropics/claude-code/main/schema/settings.schema.json",
  "permissions": {
    "allow": [
      "Bash(docker*)"
    ]
  }
}
```

### Comprehensive Personal Settings
```json
{
  "$schema": "https://raw.githubusercontent.com/anthropics/claude-code/main/schema/settings.schema.json",
  "permissions": {
    "allow": [
      "Bash(docker*)",
      "Bash(docker-compose*)",
      "Bash(npm run dev*)",
      "Write(/Users/me/scratch/**)"
    ],
    "deny": [
      "Bash(git push*)",
      "Bash(rm*)"
    ]
  },
  "environment": {
    "DEBUG": "true",
    "PERSONAL_MODE": "verbose"
  },
  "hooks": {
    "onToolUse": {
      "Bash(pytest*)": "echo '🧪 Running tests...'"
    }
  }
}
```

---

## 🤝 Best Practices

### Team (settings.json)
- ✅ Keep it minimal (only what everyone needs)
- ✅ Document why certain permissions are allowed/denied
- ✅ Review changes in PR
- ✅ Test changes don't break workflows

### Personal (settings.local.json)
- ✅ Only add what YOU specifically need
- ✅ Don't replicate team settings (redundant)
- ✅ Document with comments why you added something
- ✅ Keep it simple

---

**Questions?**
- Check `.claude/settings.local.json.example` for template
- Ask team about team settings
- Experiment! You can always delete settings.local.json

---

*Last updated: 2026-03-27*
