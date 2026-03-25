# Secure Credential Setup for Claude Code + AWS Bedrock

## Overview

This setup provides secure credential management for Claude Code with AWS Bedrock, avoiding hardcoded credentials in settings files.

## Architecture

```
Claude Code (VSCode Extension)
    ↓ uses AWS_PROFILE=bedrock-secure
~/.aws/config [profile bedrock-secure]
    ↓ calls credential_process
~/.aws/bedrock-credential-helper.sh
    ↓ reads from
~/.aws/credentials [cb-e2etest-nonprod-dev-cli]
    ↑ updated by
~/.aws/setMfaSessionToken.sh (MFA script)
```

## Components

### 1. Credential Helper Script
**Location**: `~/.aws/bedrock-credential-helper.sh`

This script:
- Reads credentials from `~/.aws/credentials`
- Outputs them in AWS `credential_process` format
- Is called automatically by AWS SDK when credentials are needed

### 2. AWS Profile Configuration
**Location**: `~/.aws/config`

Profile: `bedrock-secure`
```ini
[profile bedrock-secure]
region = us-east-1
output = json
credential_process = /Users/rgunalan/.aws/bedrock-credential-helper.sh cb-e2etest-nonprod-dev-cli
```

### 3. Claude Code Settings
**Location**: `/Users/rgunalan/Document/Main/Newfolder/Claude_Code_Amazon_Bedrock/settings.json`

```json
{
    "claudeCode.environmentVariables": [
        {
            "name": "CLAUDE_CODE_USE_BEDROCK",
            "value": "1"
        },
        {
            "name": "AWS_REGION",
            "value": "us-east-1"
        },
        {
            "name": "AWS_PROFILE",
            "value": "bedrock-secure"
        }
    ],
    "terminal.integrated.env.osx": {
        "AWS_PROFILE": "bedrock-secure",
        "AWS_REGION": "us-east-1"
    }
}
```

**Note**: The `terminal.integrated.env.osx` setting makes VS Code's integrated terminal also use the secure profile.

## Security Benefits

1. **No hardcoded credentials** - settings.json only contains profile name
2. **Standard AWS location** - credentials stay in `~/.aws/credentials`
3. **Dynamic fetching** - credentials are fetched on-demand
4. **Works with existing MFA workflow** - no changes to your authentication process
5. **Temporary credentials** - session tokens expire after 12 hours

## Usage

### Initial Setup (Already Complete)
1. Credential helper script created and made executable
2. `bedrock-secure` profile added to `~/.aws/config`
3. `settings.json` updated to use secure profile

### Daily Workflow

#### When credentials are valid:
- Just use Claude Code normally
- Credentials are fetched automatically from `~/.aws/credentials`

#### When credentials expire (after 12 hours):
1. Run the MFA script:
   ```bash
   ~/.aws/setMfaSessionToken.sh -p cb-e2etest-nonprod-dev
   ```

2. Enter your MFA token when prompted

3. Credentials are automatically updated in `~/.aws/credentials`

4. Claude Code will pick up the new credentials automatically (no restart needed)

## VS Code Integrated Terminal

The integrated terminal in VS Code is now configured to use the secure credentials automatically.

### How it works:
- The `terminal.integrated.env.osx` setting in `settings.json` sets `AWS_PROFILE=bedrock-secure`
- Any AWS CLI commands in the VS Code terminal will use the secure profile
- No need to specify `--profile bedrock-secure` every time

### Using AWS CLI in integrated terminal:
```bash
# These commands will automatically use bedrock-secure profile
aws sts get-caller-identity
aws s3 ls
aws bedrock list-foundation-models
```

### Testing:
1. Open VS Code integrated terminal (`` Ctrl+` `` or View → Terminal)
2. Run: `aws sts get-caller-identity`
3. Should show your AWS account without needing `--profile` flag

## Verification

### Test credential helper:
```bash
~/.aws/bedrock-credential-helper.sh cb-e2etest-nonprod-dev-cli
```

Expected output: JSON with AccessKeyId, SecretAccessKey, SessionToken, Expiration

### Test AWS profile:
```bash
aws sts get-caller-identity --profile bedrock-secure
```

Expected output: Your AWS account info

### Test Claude Code:
1. Reload VSCode window: `⌘⇧P` → "Developer: Reload Window"
2. Open Claude Code panel
3. Send a test message
4. Should work without credential errors

## Troubleshooting

### Error: "Could not load credentials from any providers"

**Cause**: Credentials expired or not found

**Solution**:
```bash
# Check if credentials exist and when they expire
aws configure get expiration --profile cb-e2etest-nonprod-dev-cli

# If expired, refresh them:
~/.aws/setMfaSessionToken.sh -p cb-e2etest-nonprod-dev
```

### Error: Permission denied on credential helper

**Cause**: Script not executable

**Solution**:
```bash
chmod +x ~/.aws/bedrock-credential-helper.sh
```

### Credentials not refreshing after MFA script

**Cause**: Using wrong profile name or script configuration

**Solution**:
1. Verify the profile name matches: `cb-e2etest-nonprod-dev-cli`
2. Check credentials were updated:
   ```bash
   grep -A 3 "cb-e2etest-nonprod-dev-cli" ~/.aws/credentials
   ```

## Credential Expiration

- **Duration**: 12 hours (default in MFA script)
- **Expires**: Check with `aws configure get expiration --profile cb-e2etest-nonprod-dev-cli`
- **Current expiration**: 2026-03-20T03:56:08+00:00

## File Locations Reference

| File | Location | Purpose |
|------|----------|---------|
| Credential helper | `~/.aws/bedrock-credential-helper.sh` | Fetches credentials dynamically |
| AWS config | `~/.aws/config` | Contains `bedrock-secure` profile |
| AWS credentials | `~/.aws/credentials` | Stores temporary session credentials |
| MFA script | `~/.aws/setMfaSessionToken.sh` | Refreshes credentials with MFA |
| Claude Code settings | `<project>/settings.json` | VSCode workspace settings |

## Maintenance

### When switching AWS accounts:
1. Update the profile parameter in `~/.aws/config`:
   ```ini
   credential_process = /Users/rgunalan/.aws/bedrock-credential-helper.sh <new-profile-name>
   ```

### When changing regions:
1. Update `AWS_REGION` in `settings.json`
2. Update `region` in the `bedrock-secure` profile

## Security Notes

⚠️ **Important**:
- Never commit settings files with hardcoded credentials to version control
- Keep `~/.aws/credentials` file permissions at `600` (readable only by you)
- Temporary credentials expire - this is a security feature
- The old `settings.json.backup` file contains exposed credentials - delete it after testing

## Migration from Hardcoded Credentials

If you ever need to revert or have old backups with hardcoded credentials:

1. **Delete old backups** with exposed credentials:
   ```bash
   rm /Users/rgunalan/Document/Main/Newfolder/Claude_Code_Amazon_Bedrock/settings.json.backup
   ```

2. **Use this secure setup** going forward

3. **If you shared credentials** (e.g., in chat logs), rotate them after expiration

## Support

For issues:
1. Check troubleshooting section above
2. Verify all components are in place
3. Check AWS CLI works: `aws sts get-caller-identity --profile bedrock-secure`
4. Check credential helper output directly

---

**Setup Date**: March 19, 2026
**Last Updated**: March 19, 2026
**Created By**: Claude Code
