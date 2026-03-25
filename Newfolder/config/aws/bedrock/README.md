# Claude Code Setup Guide
> AI-powered coding assistant via Amazon Bedrock — College Board AWS Infrastructure

---

## What Is Claude Code?

Claude Code is a command-line AI assistant that works directly inside your terminal and your project. You can ask it to:
- Explain what a codebase does
- Find and fix bugs
- Write unit tests
- Refactor code
- Add new features

It uses **Claude Sonnet 4.6** running securely inside AWS via Amazon Bedrock — your code never leaves the company's cloud.

---

## Prerequisites

Make sure the following are installed before starting:

| Tool | Check Command | Install |
|------|--------------|---------|
| Node.js 18+ | `node --version` | [nodejs.org](https://nodejs.org) |
| npm | `npm --version` | Comes with Node.js |
| AWS CLI | `aws --version` | [aws.amazon.com/cli](https://aws.amazon.com/cli) |
| jq | `jq --version` | `brew install jq` |

---

## One-Time Setup

### Step 1 — Verify Your AWS Credentials

```bash
aws sts get-caller-identity --profile cb-e2etest-nonprod-dev-cli
```

Expected output (enter your MFA code when prompted):
```json
{
    "UserId": "...",
    "Account": "452285021625",
    "Arn": "arn:aws:sts::452285021625:assumed-role/HeroesDevRole/..."
}
```

> If you see an error, your AWS session may have expired. Re-run the command and enter a fresh MFA code.

---

### Step 2 — Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify it installed:
```bash
claude --version
```

You should see something like: `2.1.79 (Claude Code)`

---

### Step 3 — Add the `claude-bedrock` Helper Function

This function handles MFA authentication and sets the correct environment variables automatically.

Add the following to your `~/.zshrc` (or `~/.bashrc` if you use bash):

```bash
# Claude Code on Amazon Bedrock
function claude-bedrock() {
  echo "Enter your MFA code:"
  read MFA_CODE

  CREDS=$(aws sts assume-role \
        --role-arn arn:aws:iam::452285021625:role/HeroesDevRole \
        --role-session-name claude-session \
        --serial-number arn:aws:iam::185718115448:mfa/rgunalan \
        --token-code $MFA_CODE \
        --duration-seconds 14400 \
        --profile cb-e2etest-nonprod-dev-cli)

  export AWS_ACCESS_KEY_ID=$(echo $CREDS | jq -r '.Credentials.AccessKeyId')
  export AWS_SECRET_ACCESS_KEY=$(echo $CREDS | jq -r '.Credentials.SecretAccessKey')
  export AWS_SESSION_TOKEN=$(echo $CREDS | jq -r '.Credentials.SessionToken')
  export CLAUDE_CODE_USE_BEDROCK=1
  export AWS_REGION=us-east-1
  export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'

  echo "✅ MFA session active for 12 hours. Launching Claude Code..."
  claude
}
```

Then apply the changes:
```bash
source ~/.zshrc
```

> **Note:** This has already been added to your `~/.zshrc` during initial setup. No action needed unless you set up a new machine.

---

## Daily Usage

### Launch Claude Code

Every day (or after your 12-hour session expires):

```bash
cd /path/to/your/project
claude-bedrock
```

You'll be prompted for your MFA code. After that, Claude Code launches and your session is active for **12 hours** — no need to re-authenticate until then.

---

### First Time in a New Project

Run this command once inside each new project to give Claude context about your codebase:

```
> /init
```

This creates a `CLAUDE.md` file that makes all future responses much more accurate and relevant to your project.

---

### Useful Commands Inside Claude Code

| Command | What It Does |
|---------|-------------|
| `/init` | Scan project and generate a `CLAUDE.md` summary |
| `/help` | Show all available commands |
| `Ctrl+C` | Cancel the current request |
| `exit` | Quit Claude Code |

---

### Example Prompts to Try

```
> Explain what this codebase does
> Find bugs in src/api/handler.py
> Write unit tests for the AuthService class
> Refactor this function to be more readable
> Add error handling to the database connection logic
```

You don't need to paste code — Claude reads your project files automatically.

---

## VS Code Extension (Optional)

If you prefer using Claude Code inside VS Code:

### Step 1 — Install the Extension
- Open VS Code → Extensions (`Cmd+Shift+X`)
- Search **"Claude Code"** → Install

### Step 2 — Update `settings.json`
Open settings (`Cmd+Shift+P` → "Open User Settings JSON") and add:

```json
"claudeCode.environmentVariables": [
    { "name": "CLAUDE_CODE_USE_BEDROCK", "value": "1" },
    { "name": "AWS_REGION", "value": "us-east-1" },
    { "name": "AWS_PROFILE", "value": "cb-e2etest-nonprod-dev-cli" }
]
```

### Step 3 — Restart VS Code
Fully quit (`Cmd+Q`) and reopen VS Code.

### Step 4 — Verify AWS Profile
Before opening VS Code, confirm your session is active:
```bash
aws sts get-caller-identity --profile cb-e2etest-nonprod-dev-cli
```

---

## Troubleshooting

### "On-demand throughput isn't supported"
Make sure `ANTHROPIC_MODEL` is set correctly:
```bash
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
```
The `us.` prefix is required — do **not** use `anthropic.claude-sonnet-4-6-v1:0`.

---

### "MFA required but no callback provided"
Your session has expired. Re-launch using:
```bash
claude-bedrock
```

---

### "Could not connect" or request hangs
Check your AWS session is still valid:
```bash
aws sts get-caller-identity
```
If this fails, run `claude-bedrock` again to start a new session.

---

### "Model not found" in your region
Verify the model is available:
```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query "inferenceProfileSummaries[?contains(inferenceProfileId, 'sonnet-4-6')]"
```
If empty, try `us-west-2` as the region.

---

## Quick Reference

```bash
# Verify AWS credentials
aws sts get-caller-identity --profile cb-e2etest-nonprod-dev-cli

# Launch Claude Code (every session)
cd /your/project
claude-bedrock

# Check Claude Code version
claude --version

# Check available Claude models
aws bedrock list-inference-profiles --region us-east-1 \
  --query "inferenceProfileSummaries[?contains(inferenceProfileId, 'claude')]"
```

---

## Your Setup Details

| Setting | Value |
|---------|-------|
| AWS Profile | `cb-e2etest-nonprod-dev-cli` |
| AWS Account | `452285021625` |
| Role | `HeroesDevRole` |
| MFA ARN | `arn:aws:iam::185718115448:mfa/rgunalan` |
| Region | `us-east-1` |
| Model | `us.anthropic.claude-sonnet-4-6` |
| Session Duration | 12 hours |
