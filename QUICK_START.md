# Quick Start - Daily Connection

## 🚀 Start Your Day (2 commands)

```bash
# 1. Connect Claude Code (every 12 hours)
aws sts get-caller-identity --profile bedrock-secure

# 2. For AWS work (if needed)
aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader
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
aws sts get-caller-identity --profile bedrock-secure
```

**Script asks for MFA every time?**
```bash
# Authenticate first, then run script
aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader
python query_with_cli_creds.py 4443Y7XU 94 26
```

---

**Full guide:** [DAILY_CONNECTION_GUIDE.md](DAILY_CONNECTION_GUIDE.md)
