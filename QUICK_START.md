# Quick Start - Daily Connection

## 🚀 Start Your Day (2 commands)

```bash
# 1. Connect Claude Code (every 12 hours)
refresh-aws
# OR: ~/.aws/setMfaSessionToken.sh -p cb-e2etest-nonprod-dev

# 2. For AWS work (if needed)
connect-apexam
# OR: aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader
```

**That's it!** Enter MFA when prompted. Valid for 12 hours.

---

## 📊 Query DynamoDB

```bash
# After authenticating above, run queries:
python query_with_cli_creds.py 4443Y7XU 94 26
```

---

## ✅ Check Status

```bash
# Check if credentials still valid
~/.aws/check-claude-creds.sh
```

---

## 🆘 Troubleshooting

**Claude Code not connecting?**
```bash
refresh-aws
```

**DynamoDB script asks for MFA every time?**
```bash
# Authenticate first, then run script
connect-apexam
python query_with_cli_creds.py 4443Y7XU 94 26
```

---

**Full guide:** [DAILY_CONNECTION_GUIDE.md](DAILY_CONNECTION_GUIDE.md)
