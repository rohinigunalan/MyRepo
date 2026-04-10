#!/bin/bash
# AWS Connection Aliases
# Add to ~/.zshrc: source ~/Document/Main/aws_aliases.sh

# Claude Code connection (must use script method for VS Code extension)
alias refresh-aws='~/.aws/setMfaSessionToken.sh -p cb-e2etest-nonprod-dev'
alias check-claude='~/.aws/check-claude-creds.sh'

# AWS work profiles
alias connect-apexam='aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader'
alias connect-e2e='aws sts get-caller-identity --profile cb-e2etest-nonprod-dev'
alias connect-cds='aws sts get-caller-identity --profile cb-cds-nonprod-dev'

# DynamoDB queries
alias query-dynamo='python ~/Document/Main/query_with_cli_creds.py'
alias list-exams='python ~/Document/Main/get_exam_codes.py'

# Quick status check
alias aws-status='echo "Claude Code:" && check-claude && echo "" && echo "AWS Cache:" && ls -lh ~/.aws/cli/cache/'

echo "✅ AWS aliases loaded!"
echo ""
echo "Available commands:"
echo "  refresh-aws       - Connect Claude Code (12hr cache) - REQUIRED for Claude"
echo "  check-claude      - Check Claude credentials status"
echo "  connect-apexam    - Connect to APExam DynamoDB (12hr cache)"
echo "  connect-e2e       - Connect to E2E testing (12hr cache)"
echo "  query-dynamo      - Query DynamoDB (usage: query-dynamo <pKey> <code> <year>)"
echo "  aws-status        - Show all credential status"
