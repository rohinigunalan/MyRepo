---
name: test-status
description: Show test suite status and recent test runs
---

# Test Status Command

Quick overview of test suite status.

## Test Collection

!`pytest --collect-only -q`

## Recent Test Results

!`ls -lt test_screenshots/ 2>/dev/null | head -10 || echo "No test screenshots found"`

## Test Coverage Status

!`pytest tests/ --cov=src --cov-report=term-missing --quiet 2>&1 | tail -20 || echo "Run tests to see coverage"`

---

Claude, summarize the test status and highlight any concerns.
