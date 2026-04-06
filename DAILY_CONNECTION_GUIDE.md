# Daily AWS Connection Guide

Quick reference for connecting to AWS services and Claude Code each day.

---

## 🚀 Daily Startup Routine

### Step 1: Connect Claude Code (Every 12 hours)

When Claude Code prompts for connection or after 12 hours:

```bash
aws sts get-caller-identity --profile bedrock-secure
```

**What happens:**
- Prompts for MFA code (6 digits from authenticator app)
- Caches credentials for 12 hours
- Claude Code will work automatically

**Check if still valid:**
```bash
~/.aws/check-claude-creds.sh
```

---

### Step 2: Connect to AWS for Your Work (Optional)

Only needed if you're querying DynamoDB or using AWS services:

```bash
# For DynamoDB queries
aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader

# For general dev work
aws sts get-caller-identity --profile cb-e2etest-nonprod-dev
```

**What happens:**
- Prompts for MFA code (same authenticator app)
- Caches credentials for 12 hours
- Can run queries without MFA for 12 hours

---

## 📋 Quick Reference Commands

### Check Credential Status

```bash
# Check Claude Code credentials
~/.aws/check-claude-creds.sh

# Check any profile expiration
aws configure get expiration --profile PROFILE_NAME
```

### Run DynamoDB Queries

```bash
# Query APExamResponse-OAT table
python query_with_cli_creds.py <pKey> <cbExamCode> <adminYear>

# Example:
python query_with_cli_creds.py 4443Y7XU 94 26
```

### List All Exam Codes

```bash
# Get exam codes for adminYear 26
python get_exam_codes.py <MFA_CODE> 26
```

---

## 🔑 Available AWS Profiles

| Profile | Purpose | When to Use |
|---------|---------|-------------|
| **bedrock-secure** | Claude Code connection | Every 12 hours for Claude |
| **cb-e2etest-nonprod-dev** | E2E testing dev work | Your daily dev work |
| **cb-apexamresponse-nonprod-reader** | DynamoDB read access | Query exam response data |
| **cb-cds-nonprod-dev** | CDS development | CDS work |
| **cb-consent-management-nonprod-dev** | Consent management | Consent mgmt work |

---

## ⚠️ Troubleshooting

### Issue: Claude Code Not Connecting

**Solution:**
```bash
# Re-authenticate
aws sts get-caller-identity --profile bedrock-secure
# Enter your MFA code when prompted
```

### Issue: "Enter MFA code" Every Time

**Check if using wrong profile:**
```bash
echo $AWS_PROFILE
```

**Should show:** `bedrock-secure` (or nothing)

**If wrong, fix it:**
```bash
unset AWS_PROFILE
export AWS_PROFILE=bedrock-secure
```

### Issue: Python Script Asks for MFA

**Solution:**
```bash
# Authenticate the profile first
aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader

# Then run your script (will use cache)
python query_with_cli_creds.py 4443Y7XU 94 26
```

### Issue: Credentials Expired

**Symptom:** Get "ExpiredToken" error

**Solution:**
```bash
# Clear cache and re-authenticate
rm -f ~/.aws/cli/cache/*
aws sts get-caller-identity --profile bedrock-secure
```

---

## 📂 Available Scripts

All scripts are in: `/Users/rgunalan/Document/Main/`

### DynamoDB Query Scripts

**1. `query_with_cli_creds.py`** ✅ Recommended
- Uses AWS CLI cached credentials
- No MFA prompt if cache valid
- Usage: `python query_with_cli_creds.py <pKey> <cbExamCode> <adminYear>`

**2. `query_apexam_by_key.py`**
- Requires MFA code in command
- Usage: `python query_apexam_by_key.py <MFA_CODE> <pKey> <cbExamCode> <adminYear>`

**3. `get_exam_codes.py`**
- List all exam codes with filters
- Usage: `python get_exam_codes.py <MFA_CODE> [adminYear]`

### Utility Scripts

**4. `~/.aws/check-claude-creds.sh`**
- Check if Claude Code credentials are still valid
- Shows time remaining

**5. `~/.aws/setMfaSessionToken.sh`** (Legacy - not needed anymore)
- Old method for authentication
- No longer required with new setup

---

## 🎯 Common Workflows

### Workflow 1: Start Your Day

```bash
# 1. Check if Claude Code needs authentication
~/.aws/check-claude-creds.sh

# 2. If expired, authenticate
aws sts get-caller-identity --profile bedrock-secure

# 3. Start working with Claude Code!
```

### Workflow 2: Query DynamoDB Data

```bash
# 1. Authenticate once (if not done today)
aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader

# 2. Run queries (no MFA for 12 hours)
python query_with_cli_creds.py 4443Y7XU 94 26
python query_with_cli_creds.py ANOTHER_KEY 12 26
python query_with_cli_creds.py THIRD_KEY 30 26
```

### Workflow 3: Check Exam Codes

```bash
# Get your current MFA code
# Then run:
python get_exam_codes.py 123456 26

# This shows all exam codes for adminYear 26
```

---

## 📝 Important Notes

### MFA Code
- Get from your authenticator app
- 6-digit code
- Changes every 30 seconds
- Same device for all profiles

### Session Duration
- All profiles: **12 hours**
- Set via: `duration_seconds = 43200`
- Automatically cached by AWS CLI

### Cache Location
- Credentials cached in: `~/.aws/cli/cache/`
- Automatically managed by AWS
- Cleared on expiration

### Environment Variables
- `AWS_PROFILE=bedrock-secure` - For Claude Code (set in `~/.zshrc`)
- Don't change this unless you know what you're doing!

---

## 🔄 When Credentials Expire (After 12 Hours)

### Claude Code Connection
```bash
# You'll see: "Authentication required" or similar message
# Just run:
aws sts get-caller-identity --profile bedrock-secure
# Enter MFA when prompted
```

### AWS Work Queries
```bash
# You'll see: "Enter MFA code..." prompt
# Or "ExpiredToken" error
# Just re-authenticate:
aws sts get-caller-identity --profile PROFILE_NAME
# Enter MFA when prompted
```

---

## 📞 Quick Help

### Show This Guide
```bash
cat ~/Document/Main/DAILY_CONNECTION_GUIDE.md
```

### List All Profiles
```bash
aws configure list-profiles
```

### Get Help on Scripts
```bash
python query_with_cli_creds.py --help
python get_exam_codes.py --help
```

---

## 🎓 Understanding the Setup

### What Changed (April 6, 2026)

**Before:**
- Needed to run `setMfaSessionToken.sh` script every 12 hours
- Multiple steps to connect Claude Code

**After:**
- Single command: `aws sts get-caller-identity --profile bedrock-secure`
- Uses built-in AWS CLI caching
- Same method for all profiles

**Why It's Better:**
- ✅ Simpler - one command vs script
- ✅ Consistent - same method everywhere
- ✅ Automatic - AWS handles caching
- ✅ Standard - industry best practice

---

## 📊 Exam Code Reference

Quick reference for common exam codes:

| Code | Exam Name |
|------|-----------|
| 1 | US History |
| 6 | Biology |
| 7 | Chemistry |
| 12 | **English Language** |
| 13 | English Literature |
| 15 | European History |
| 30 | Psychology |
| 94 | **Seminar** |
| 103 | Computer Science Principles |
| 117 | Precalculus |

Full list: Run `python get_exam_codes.py <MFA> 26`

---

## ✅ Checklist: Daily Startup

- [ ] Check Claude Code credentials: `~/.aws/check-claude-creds.sh`
- [ ] If expired, authenticate: `aws sts get-caller-identity --profile bedrock-secure`
- [ ] For AWS work, authenticate relevant profile(s)
- [ ] Verify credentials cached (no MFA on second command)
- [ ] Start working!

---

**Last Updated:** April 6, 2026  
**Location:** `/Users/rgunalan/Document/Main/DAILY_CONNECTION_GUIDE.md`  
**Backup Config:** `/Users/rgunalan/.aws/config.backup-20260406-174810`

---

## 🆘 Emergency: Restore Old Configuration

If something breaks and you need to go back to the old method:

```bash
# Restore old config
cp ~/.aws/config.backup-20260406-174810 ~/.aws/config

# Remove new bedrock-secure from credentials
sed -i.bak '/^\[bedrock-secure\]/,/^$/d' ~/.aws/credentials

# Use old method
~/.aws/setMfaSessionToken.sh -p cb-e2etest-nonprod-dev
```

Then contact support or review the backup files.

---

**End of Guide**
