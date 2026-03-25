# DSR Testing & Automation Project

Organized Python project for Data Subject Rights (DSR) testing, automation, and data management.

## 📁 Project Structure

```
Newfolder/
├── docs/                              # 📚 Documentation
│   ├── README.md                      # Original project documentation
│   ├── SETUP_NOTES.md                 # Setup instructions
│   ├── AUTOMATION_SUCCESS_SUMMARY.md  # Automation results
│   ├── PYTHON_ENV_NOTES.md            # Python environment notes
│   ├── QUICK_REFERENCE.md             # Quick reference guide
│   └── DATA_FILES_INFO.md             # Data files information
│
├── config/                            # ⚙️ Configuration Files
│   └── aws/
│       └── bedrock/                   # AWS Bedrock config for Claude Code
│           ├── settings.json          # VSCode workspace settings
│           ├── settings.json.backup   # Backup of settings
│           └── SECURE_CREDENTIAL_SETUP.md
│
├── scripts/                           # 🛠️ Utility Scripts
│   ├── aws/                          # AWS operations
│   │   ├── dynamodb/                 # DynamoDB operations
│   │   │   └── DSR_Dynamo_*.py
│   │   ├── sns/                      # SNS publishing
│   │   │   └── SNS_Publish_*.py
│   │   └── api/                      # API clients
│   │       ├── api_runner.py
│   │       ├── createperson.py
│   │       └── student_info_api_client.py
│   │
│   ├── data_generation/              # Data & Excel creation
│   │   ├── create_*.py               # Excel template creators
│   │   ├── generate_*.py             # Report generators
│   │   └── success_report_*.py       # Success report scripts
│   │
│   └── validation/                   # Validation & checks
│       ├── check_*.py                # Data validation scripts
│       ├── update_*.py               # Update scripts
│       └── fix_*.py                  # Fix scripts
│
├── tests/                             # 🧪 Test Files
│   ├── playwright/                    # Playwright tests
│   │   ├── specs/                    # Test specifications
│   │   └── tests/                    # Test implementations
│   │
│   ├── browser/                       # Browser-based tests
│   │   └── (browser test scripts)
│   │
│   └── integration/                   # Integration tests
│       ├── Parent_requesttypes_submission_MULTIPLE.py
│       ├── educator_requesttypes_submission_MULTIPLE.py
│       └── myself_requesttypes_submission_MULTIPLE.py
│
├── dsr/                               # 📁 DSR Project Files
│   ├── data/                         # Test data
│   ├── reports/                      # Generated reports
│   ├── screenshots/                  # Test screenshots
│   └── scripts/                      # DSR-specific scripts
│
├── DSR_AWS/                           # 📁 AWS Integration Scripts
│   └── (AWS DSR-related scripts)
│
├── .venvmac/                          # 🐍 Virtual Environment (Mac)
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12.7 (via Anaconda)
- Virtual environment: `.venvmac`
- Playwright 1.58.0
- AWS credentials configured

### Installation

1. **Activate virtual environment:**
   ```bash
   source .venvmac/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. **Verify Playwright installation:**
   ```bash
   playwright --version
   ```

## 🔧 AWS Configuration

AWS Bedrock credentials are configured using the secure `bedrock-secure` profile.

**Refresh credentials (every 12 hours):**
```bash
refresh-aws  # Alias for: ~/.aws/setMfaSessionToken.sh -p cb-e2etest-nonprod-dev
```

**Verify AWS access:**
```bash
aws sts get-caller-identity --profile bedrock-secure
```

See [config/aws/bedrock/SECURE_CREDENTIAL_SETUP.md](config/aws/bedrock/SECURE_CREDENTIAL_SETUP.md) for details.

## 🧪 Running Tests

### Playwright Tests
```bash
# Run all Playwright tests
pytest tests/playwright/

# Run specific test
python tests/browser/test_name.py
```

### Integration Tests
```bash
# Run DSR integration tests
python tests/integration/myself_requesttypes_submission_MULTIPLE.py
python tests/integration/Parent_requesttypes_submission_MULTIPLE.py
python tests/integration/educator_requesttypes_submission_MULTIPLE.py
```

## 📊 Data Generation

### Create Excel Templates
```bash
# Create educator template
python scripts/data_generation/create_educator_excel.py

# Create parent template
python scripts/data_generation/create_parent_excel.py

# Generate success reports
python scripts/data_generation/generate_success_report.py
```

## 🔍 Validation Scripts

```bash
# Check Excel structure
python scripts/validation/check_excel_columns.py

# Validate phone data
python scripts/validation/check_phone_data.py

# Update Excel files
python scripts/validation/update_excel_close_columns.py
```

## 🔗 AWS Operations

### DynamoDB
```bash
# Insert delete request
python scripts/aws/dynamodb/DSR_Dynamo_insert_Delete_Request.py

# Read from DynamoDB
python scripts/aws/dynamodb/DSR_dynamodb_readstore_jsonformat.py
```

### SNS Publishing
```bash
# Publish confirmation
python scripts/aws/sns/SNS_Publish_Confirmation_DSR_Delete_Request.py
```

### API Operations
```bash
# Run API tests
python scripts/aws/api/api_runner.py

# Create person
python scripts/aws/api/createperson.py
```

## 📚 Documentation

All documentation is in the [docs/](docs/) directory:

- **Setup**: [docs/SETUP_NOTES.md](docs/SETUP_NOTES.md)
- **Quick Reference**: [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)
- **Python Environment**: [docs/PYTHON_ENV_NOTES.md](docs/PYTHON_ENV_NOTES.md)
- **Data Files**: [docs/DATA_FILES_INFO.md](docs/DATA_FILES_INFO.md)
- **Automation Results**: [docs/AUTOMATION_SUCCESS_SUMMARY.md](docs/AUTOMATION_SUCCESS_SUMMARY.md)

## 🤝 Contributing

When adding new scripts:

1. **AWS scripts** → `scripts/aws/{dynamodb,sns,api}/`
2. **Data generation** → `scripts/data_generation/`
3. **Validation** → `scripts/validation/`
4. **Tests** → `tests/{playwright,browser,integration}/`
5. **Documentation** → `docs/`

## 📝 Notes

- Virtual environments (`.venv/`, `.venvmac/`) are excluded from Git
- Use `bedrock-secure` AWS profile for all AWS operations
- Playwright browser binaries stored in `~/Library/Caches/ms-playwright/`
- Test screenshots saved in `dsr/screenshots/`

## 🛠️ Tech Stack

- **Python**: 3.12.7 (Anaconda)
- **Testing**: Playwright 1.58.0, pytest
- **AWS**: boto3, DynamoDB, SNS
- **Data**: openpyxl, pandas
- **Browser Automation**: Playwright (Chromium, Firefox, WebKit)

## 📞 Support

For issues or questions:
- Check documentation in `docs/`
- Review test examples in `tests/`
- Verify AWS credentials: `aws sts get-caller-identity --profile bedrock-secure`

---

**Last Updated**: March 25, 2026
**Organized By**: Claude Code
